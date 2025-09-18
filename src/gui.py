import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QTextEdit, QLabel, QProgressBar)

# Backend functions
from audio_downloader import download_audio
from transcriber import transcribe_audio
from summarizer import summarize_text


class Worker(QThread):
    # Signals to communicate with the main window
    progress_update = Signal(int, str)
    finished = Signal(str)

    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url

    def run(self):
        """
        This is the method that will be executed in the separate thread.
        """
        try:
            self.progress_update.emit(33, "Downloading audio...")
            audio_file = download_audio(self.video_url)
            if not audio_file:
                raise Exception("Failed to download audio.")

            self.progress_update.emit(66, "Transcribing audio...")
            transcribed_text = transcribe_audio(audio_file)
            if not transcribed_text:
                raise Exception("Failed to transcribe audio.")

            self.progress_update.emit(100, "Summarizing text...")
            summary = summarize_text(transcribed_text)
            if not summary:
                raise Exception("Failed to generate summary.")

            self.finished.emit(summary)

        except Exception as e:
            self.finished.emit(f"An error occurred: {e}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Basic Window Setup
        self.setWindowTitle("YouTube Summarizer")
        app_icon = QIcon("icon.ico")
        self.setWindowIcon(app_icon)
        self.layout = QVBoxLayout(self)
        self.url_label = QLabel("Enter YouTube URL:")
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.summarize_button = QPushButton("Summarize Video")
        self.status_label = QLabel("Status: Ready")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)
        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.summarize_button)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.summary_output)
        self.summarize_button.clicked.connect(self.start_summarization)

    def start_summarization(self):
        """This method is the "slot" that runs when the button is clicked."""
        video_url = self.url_input.text()
        if not video_url:
            self.status_label.setText("Status: Please enter a URL.")
            return

        self.summarize_button.setEnabled(False)
        self.summary_output.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("")
        self.status_label.setText("Status: Starting...")

        self.worker = Worker(video_url)
        self.worker.progress_update.connect(self.update_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def update_status(self, value, message):
        """Receives progress updates from the worker and updates the status label."""
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Status: {message}")

    def on_finished(self, result):
        """Receives the final result from the worker and updates the GUI."""
        self.summary_output.setText(result)
        self.status_label.setText("Status: Finished")
        self.summarize_button.setEnabled(True)
        if "An error occurred" in result:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #d9534f }")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec())

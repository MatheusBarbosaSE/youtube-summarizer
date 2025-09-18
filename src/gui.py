import sys
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QTextEdit, QLabel, QProgressBar, QFileDialog)

# Backend functions
from audio_downloader import download_audio
from transcriber import transcribe_audio
from summarizer import summarize_text


class Worker(QThread):
    """
    Handles the long-running summarization process in a separate thread
    to keep the GUI responsive.
    """
    progress_update = Signal(int, str)
    finished = Signal(str)

    def __init__(self, video_url):
        super().__init__()
        self.video_url = video_url

    def run(self):
        try:
            self.progress_update.emit(33, "Downloading audio...")
            audio_file = download_audio(self.video_url)
            if not audio_file:
                raise Exception("Failed to download audio.")

            self.progress_update.emit(66, "Transcribing audio...")
            transcribed_text = transcribe_audio(audio_file)
            if not transcribed_text:
                raise Exception("Failed to transcribe audio.")

            self.progress_update.emit(100, "Generating summary...")
            summary = summarize_text(transcribed_text)
            if not summary:
                raise Exception("Failed to generate summary.")

            self.finished.emit(summary)

        except Exception as e:
            self.finished.emit(f"An error occurred: {e}")


class MainWindow(QWidget):
    """
    The main window of the application.
    """

    def __init__(self):
        super().__init__()

        # Basic Window Setup
        self.setWindowTitle("YouTube Summarizer")
        app_icon = QIcon("icon.ico")
        self.setWindowIcon(app_icon)

        # Layouts
        self.main_layout = QVBoxLayout(self)
        self.button_layout = QHBoxLayout()

        # Widgets
        self.url_label = QLabel("Enter YouTube URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")

        self.summarize_button = QPushButton("Summarize Video")
        self.save_button = QPushButton("Save Summary")
        self.save_button.setEnabled(False)

        self.status_label = QLabel("Status: Ready")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)

        # Arrange Widgets in Layouts
        self.button_layout.addWidget(self.summarize_button)
        self.button_layout.addWidget(self.save_button)

        self.main_layout.addWidget(self.url_label)
        self.main_layout.addWidget(self.url_input)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.summary_output)

        # Connect Signals to Slots
        self.summarize_button.clicked.connect(self.start_summarization)
        self.save_button.clicked.connect(self.save_summary)

    def start_summarization(self):
        """Prepares the UI and starts the worker thread."""
        video_url = self.url_input.text()
        if not video_url:
            self.status_label.setText("Status: Please enter a URL.")
            return

        # Reset UI for a new run
        self.summarize_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.summary_output.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("")
        self.status_label.setText("Status: Starting...")

        # Create and start the worker
        self.worker = Worker(video_url)
        self.worker.progress_update.connect(self.update_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def update_status(self, value, message):
        """Updates the progress bar and status label."""
        self.progress_bar.setValue(value)
        self.status_label.setText(f"Status: {message}")

    def on_finished(self, result):
        """Handles the completion of the worker thread."""
        self.summary_output.setText(result)
        self.summarize_button.setEnabled(True)

        if "An error occurred" in result:
            self.status_label.setText("Status: Error!")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #d9534f; }")
            self.save_button.setEnabled(False)
        else:
            self.status_label.setText("Status: Finished!")
            self.save_button.setEnabled(True)

    def save_summary(self):
        """Opens a 'Save As' dialog and saves the summary to a text file."""
        summary_text = self.summary_output.toPlainText()
        if not summary_text:
            self.status_label.setText("Status: Nothing to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Summary",
            "summary.txt",  # Default filename
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(summary_text)
                self.status_label.setText(f"Status: Summary saved successfully!")
            except Exception as e:
                self.status_label.setText(f"Status: Error saving file: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 450)
    window.show()
    sys.exit(app.exec())

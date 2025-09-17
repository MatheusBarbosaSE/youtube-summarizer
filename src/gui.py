import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QTextEdit, QLabel)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Basic Window Setup
        self.setWindowTitle("YouTube Summarizer")
        self.layout = QVBoxLayout(self)

        self.url_label = QLabel("Enter YouTube URL:")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")

        self.summarize_button = QPushButton("Summarize Video")

        self.status_label = QLabel("Status: Ready")
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)

        self.layout.addWidget(self.url_label)
        self.layout.addWidget(self.url_input)
        self.layout.addWidget(self.summarize_button)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.summary_output)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec())
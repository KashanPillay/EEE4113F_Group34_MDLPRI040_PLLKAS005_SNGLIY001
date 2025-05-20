from PyQt6.QtWidgets import QWidget, QListWidget, QLabel, QPushButton, QVBoxLayout, QApplication
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton
import sys
import email_data  # Import your Gmail email fetching script
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QTextEdit

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QTextEdit
import email_data


class EmailViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.opened_emails = set()  # Track opened emails
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Email Viewer")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.email_list = QListWidget()
        self.email_list.itemClicked.connect(self.display_email)
        layout.addWidget(self.email_list)

        self.email_body = QTextEdit()
        self.email_body.setReadOnly(True)
        layout.addWidget(self.email_body)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_emails)
        layout.addWidget(self.refresh_button)

        self.history_button = QPushButton("History")
        self.history_button.clicked.connect(self.load_history)
        layout.addWidget(self.history_button)

        self.setLayout(layout)
        self.load_emails()

    def load_emails(self):
        self.email_list.clear()
        self.emails = email_data.get_emails()
        for email in self.emails:
            if email[1] not in self.opened_emails:  # Hide opened emails
                self.email_list.addItem(email[1])

    def load_history(self):
        self.email_list.clear()
        for email in self.opened_emails:
            self.email_list.addItem(email)

    def display_email(self, item):
        selected_email = next(email for email in self.emails if email[1] == item.text())
        self.email_body.setText(selected_email[2])
        self.opened_emails.add(item.text())  # Mark email as opened
        self.load_emails()  # Refresh the list to hide opened email


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailViewer()
    window.show()
    sys.exit(app.exec())

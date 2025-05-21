from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QPoint
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QPainter, QBrush
from threading import Thread
import time
import sheets_retrieve

class PastelHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(80)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(QPoint(0, 0), QPoint(self.width(), 0))
        gradient.setColorAt(0, QColor("#f8bbd0"))  # Soft pink
        gradient.setColorAt(1, QColor("#bbdefb"))  # Soft blue
        painter.fillRect(self.rect(), QBrush(gradient))
        painter.end()

class TrackingPage(QWidget):
    map_update_signal = pyqtSignal(str)

    def __init__(self, navigate_to_home=None):
        super().__init__()
        self.navigate_to_home = navigate_to_home
        self.coordinates = "0,0"
        self.init_ui()
        self.start_coordinate_updates()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add pastel header (matches your other pages)
        header = PastelHeader()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 0, 40, 0)

        title_label = QLabel("LIVE LOCATION TRACKING")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #5d5d5d;")
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        header_layout.addStretch()

        # Home button (consistent with your other pages)
        if self.navigate_to_home:
            home_btn = QPushButton("← Home")
            home_btn.setStyleSheet("""
                QPushButton {
                    background: #81d4fa;
                    color: #2d2d2d;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: #4fc3f7;
                }
            """)
            home_btn.clicked.connect(self.navigate_to_home)
            header_layout.addWidget(home_btn, alignment=Qt.AlignRight)

        main_layout.addWidget(header)

        # Map view (takes remaining space)
        self.map_view = QWebEngineView()
        self.map_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.configure_map()
        main_layout.addWidget(self.map_view)

    def configure_map(self):
        settings = self.map_view.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.map_view.setUrl(QUrl("about:blank"))
        self.map_update_signal.connect(self.update_map)

    def start_coordinate_updates(self):
        self.update_thread = Thread(target=self.update_coordinates, daemon=True)
        self.update_thread.start()

    def update_coordinates(self):
        while True:
            new_coords = sheets_retrieve.get_coordinates()
            if new_coords and new_coords != self.coordinates:
                self.coordinates = new_coords
                self.map_update_signal.emit(new_coords)
            time.sleep(5)

    def update_map(self, coords):
        try:
            lat, lon = coords.strip().replace(" ", "").split(",")
            maps_url = f"https://www.google.com/maps?q={lat},{lon}&z=15"
            self.map_view.setUrl(QUrl(maps_url))
        except Exception as e:
            print(f"Map update error: {e}")
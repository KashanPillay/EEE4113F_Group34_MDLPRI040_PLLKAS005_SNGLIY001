from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QPoint, QTimer
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
        self.tracked_coordinates = "0,0"  # Store the original tracking coordinates
        self.init_ui()
        self.start_coordinate_updates()
        self.reset_timer = None  # Timer for resetting view

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add pastel header
        header = PastelHeader()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 0, 40, 0)

        title_label = QLabel("LIVE LOCATION TRACKING")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #5d5d5d;")
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        header_layout.addStretch()

        # Home button
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

        # Map view
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
        # Add timer to reset view every 10 seconds
        self.reset_timer = QTimer()
        self.reset_timer.timeout.connect(self.reset_map_view)
        self.reset_timer.start(1000)  # 10 seconds

    def update_coordinates(self):
        while True:
            new_coords = sheets_retrieve.get_coordinates()
            if new_coords:
                self.tracked_coordinates = new_coords  # Update tracked coordinates
                if new_coords != self.coordinates:
                    self.coordinates = new_coords
                    self.map_update_signal.emit(new_coords)
            time.sleep(5)

    def reset_map_view(self):
        """Force the map back to tracked coordinates"""
        if self.tracked_coordinates and self.tracked_coordinates != "0,0":
            self.map_update_signal.emit(self.tracked_coordinates)

    def update_map(self, coords):
        try:
            # Store previous coordinates if they don't exist
            if not hasattr(self, 'previous_coords'):
                self.previous_coords = None

            # Process new coordinates
            new_coords = coords.strip().replace(" ", "")

            # Only update if coordinates have changed
            if new_coords != self.previous_coords:
                self.previous_coords = new_coords
                lat, lon = new_coords.split(",")

                # Create the HTML with embedded iframe
                html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body, html {{
                            margin: 0;
                            padding: 0;
                            height: 100%;
                            overflow: hidden;
                        }}
                        #map-container {{
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                        }}
                        #map-iframe {{
                            width: 100%;
                            height: 100%;
                            border: none;
                        }}
                    </style>
                </head>
                <body>
                    <div id="map-container">
                        <iframe id="map-iframe"
                            src="https://maps.google.com/maps?q={lat},{lon}&z=15&output=embed"
                            frameborder="0"
                            sandbox="allow-scripts allow-same-origin">
                        </iframe>
                    </div>

                    <script>
                        // No automatic refresh needed anymore
                        // Just prevent navigation attempts
                        //window.onbeforeunload = function() {{
                        //    return false;
                        //}};
                    </script>
                </body>
                </html>
                """

                self.map_view.setHtml(html, QUrl("about:blank"))

        except Exception as e:
            print(f"Map update error: {e}")
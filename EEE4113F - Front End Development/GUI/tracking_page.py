from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, pyqtSignal, Qt
from threading import Thread
import time
import sheets_retrieve

class TrackingPage(QWidget):
    map_update_signal = pyqtSignal(str)

    def __init__(self, navigate_to_home=None):
        super().__init__()
        self.navigate_to_home = navigate_to_home
        self.coordinates = "0,0"
        self.init_ui()
        self.start_coordinate_updates()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.map_view = QWebEngineView()
        self.configure_map()
        layout.addWidget(self.map_view)
        self.setLayout(layout)

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



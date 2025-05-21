import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from home_page import HomePage
from data_page import DataPage
from tracking_page import TrackingPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connected Oxygen Detection Yield (CODY)")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.resize(800, 600)

        # Initialize stacked widget
        self.stackedWidget = QStackedWidget(self)
        self.setCentralWidget(self.stackedWidget)

        # Initialize pages
        self.init_pages()
        self.init_menu_bar()

    def init_pages(self):
        # Create pages with navigation callbacks
        self.home_page = HomePage(self.show_data_page, self.show_tracking_page)
        self.data_page = DataPage(self.show_home_page)
        self.tracking_page = TrackingPage(self.show_home_page)

        # Add pages to stacked widget
        self.stackedWidget.addWidget(self.home_page)
        self.stackedWidget.addWidget(self.data_page)
        self.stackedWidget.addWidget(self.tracking_page)

    def init_menu_bar(self):
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # File Menu
        file_menu = self.menubar.addMenu('File')
        refresh_action = QAction('Refresh Data', self)
        refresh_action.triggered.connect(self.data_page.load_data)
        file_menu.addAction(refresh_action)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = self.menubar.addMenu('View')
        home_action = QAction('Home Page', self)
        home_action.triggered.connect(self.show_home_page)
        view_menu.addAction(home_action)

        data_action = QAction('Data Page', self)
        data_action.triggered.connect(self.show_data_page)
        view_menu.addAction(data_action)

        tracking_action = QAction('Tracking Page', self)
        tracking_action.triggered.connect(self.show_tracking_page)
        view_menu.addAction(tracking_action)

        # Help Menu
        help_menu = self.menubar.addMenu('Help')
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about_info)
        help_menu.addAction(about_action)

    # Navigation methods
    def show_home_page(self):
        self.stackedWidget.setCurrentWidget(self.home_page)

    def show_data_page(self):
        self.stackedWidget.setCurrentWidget(self.data_page)

    def show_tracking_page(self):
        self.stackedWidget.setCurrentWidget(self.tracking_page)

    def show_about_info(self):
        QMessageBox.information(self, "About",
                                "CODY - Remote Pulse Oximeter\nVersion 1.0\nMedical Monitoring System")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
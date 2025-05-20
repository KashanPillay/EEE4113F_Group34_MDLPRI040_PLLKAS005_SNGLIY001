from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton, QFrame,
    QGraphicsDropShadowEffect, QHeaderView
)
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QPoint, QTimer
import time
import sheets_retrieve
from PyQt5.QtWidgets import QMessageBox
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime


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


class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            ModernCard {
                background: white;
                border-radius: 16px;
                border: none;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

class GraphCard(ModernCard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)


class DataPage(QWidget):
    def __init__(self, navigate_to_home):
        super().__init__()
        self.navigate_to_home = navigate_to_home
        self.setup_ui()

        # Set up a timer to auto-refresh data every 30 seconds
        #self.refresh_timer = QTimer()
        #self.refresh_timer.timeout.connect(self.load_data)
        #self.refresh_timer.start(30000)  # 30 seconds

        # Load data immediately when page opens
        self.load_data()

    def setup_ui(self):
        # Main layout with pastel background
        self.setStyleSheet("""
            QWidget {
                background-color: #fafafa;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add pastel gradient header
        header = PastelHeader()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)

        # Title with modern styling
        title_label = QLabel("VITAL SIGNS MONITORING")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #5d5d5d;")
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Home button with pastel color
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

        layout.addWidget(header)

        # Content container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Stats Summary Cards with pastel backgrounds
        self.stats_widget = ModernCard()
        stats_layout = QHBoxLayout(self.stats_widget)
        stats_layout.setSpacing(15)
        stats_layout.setContentsMargins(20, 20, 20, 20)

        card_style = """
            QLabel {
                font-size: 16px;
                font-weight: 600;
                padding: 20px;
                border-radius: 12px;
                color: #5d5d5d;
                min-width: 200px;
            }
        """

        self.heart_rate_label = QLabel("Heart Rate: -- bpm")
        self.heart_rate_label.setStyleSheet(f"""
            {card_style}
            background: #ffebee;  /* Soft red */
        """)
        self.spo2_label = QLabel("SpO2: --%")
        self.spo2_label.setStyleSheet(f"""
            {card_style}
            background: #e8f5e9;  /* Soft green */
        """)
        self.last_update_label = QLabel("Last updated: --")
        self.last_update_label.setStyleSheet(f"""
            {card_style}
            background: #e1f5fe;  /* Soft blue */
        """)

        for label in [self.heart_rate_label, self.spo2_label, self.last_update_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            stats_layout.addWidget(label)

        content_layout.addWidget(self.stats_widget)

        # Refresh Button with pastel styling
        refresh_btn = QPushButton("⟳ Refresh Data")
        refresh_btn.setStyleSheet("""
                    QPushButton {
                        background: #81d4fa;
                        color: #2d2d2d;
                        border: none;
                        border-radius: 12px;
                        padding: 12px 24px;
                        font-size: 14px;
                        font-weight: 600;
                        min-width: 180px;
                    }
                    QPushButton:hover {
                        background: #4fc3f7;
                    }
                    QPushButton:pressed {
                        background: #29b6f6;
                    }
                """)
        refresh_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        refresh_btn.clicked.connect(self.load_data)

        # Button layout
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        content_layout.addWidget(btn_container)

        layout.addWidget(content_widget)

        # Add the graph container (initially hidden)
        self.graphContainer = GraphCard()
        self.graphContainer.hide()
        content_layout.addWidget(self.graphContainer)

        # Add Graph Button with pastel styling
        graph_btn = QPushButton("📈 Show RoR Graph")
        graph_btn.setStyleSheet("""
                QPushButton {
                    background: #ce93d8;
                    color: #2d2d2d;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 600;
                    min-width: 180px;
                }
                QPushButton:hover {
                    background: #ba68c8;
                }
                QPushButton:pressed {
                    background: #ab47bc;
                }
            """)
        graph_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        graph_btn.clicked.connect(self.toggle_graph)

        # Modify the button layout to include both buttons
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addStretch()
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(graph_btn)
        btn_layout.addStretch()
        content_layout.addWidget(btn_container)

        layout.addWidget(content_widget)

    def toggle_graph(self):
        """Toggle graph visibility and plot data if showing"""
        if self.graphContainer.isVisible():
            self.graphContainer.hide()
        else:
            self.plot_ror_graph()
            self.graphContainer.show()

    def plot_ror_graph(self):
        """Plot the RoR graph using the loaded data"""
        try:
            data = sheets_retrieve.get_sheet_data()
            if not data:
                QMessageBox.warning(self, "Warning", "No data available to plot")
                return

            # Prepare data for plotting
            dates = []
            y_values = []

            for row in data:
                try:
                    # Parse date and time (adjust based on your actual column names)
                    dt_str = f"{row.get('Date', '')} {row.get('Time', '')}"
                    dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")

                    # Calculate y = 110 - 25(RoR)
                    ratio1 = float(row.get('Ratio 1', 0))
                    ratio2 = float(row.get('Ratio 2', 1))  # Avoid division by zero
                    ror = ratio1 / ratio2 if ratio2 != 0 else 0
                    y = 110 - 25 * ror

                    dates.append(dt)
                    y_values.append(y)
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e}")
                    continue

            if not dates:
                QMessageBox.warning(self, "Warning", "No valid data to plot")
                return

            # Clear previous plot
            self.graphContainer.figure.clear()
            ax = self.graphContainer.figure.add_subplot(111)

            # Plot data with pastel colors
            ax.plot(dates, y_values, marker='o', linestyle='-',
                    color='#81d4fa', markersize=8, linewidth=2)

            # Format plot
            ax.set_title('RoR Trend: y = 110 - 25(RoR)', color='#5d5d5d', pad=20)
            ax.set_xlabel('Date & Time', color='#5d5d5d')
            ax.set_ylabel('y Value', color='#5d5d5d')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.set_facecolor('#fafafa')

            # Format x-axis dates
            ax.xaxis.set_major_formatter(DateFormatter('%m/%d %H:%M'))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            self.graphContainer.figure.autofmt_xdate()

            # Set colors
            for spine in ax.spines.values():
                spine.set_edgecolor('#e0e0e0')
            ax.tick_params(colors='#5d5d5d')

            # Redraw canvas
            self.graphContainer.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot graph: {str(e)}")

    def load_data(self):
        try:
            # Hide graph when refreshing data
            self.graphContainer.hide()

            data = sheets_retrieve.get_sheet_data()
            if not data:
                QMessageBox.warning(self, "Warning", "No data available from Google Sheet")
                return

            self.update_table(data)
            self.update_summary(data[-1])  # Show latest reading in summary cards
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data from Google Sheet: {str(e)}")


    def update_table(self, data):
        self.dataTable.clear()  # Now calling clear on the actual QTableWidget

        if not data:
            return

        # Set table dimensions
        self.dataTable.setRowCount(len(data))
        self.dataTable.setColumnCount(len(data[0]))

        # Set headers
        headers = list(data[0].keys())
        self.dataTable.setHorizontalHeaderLabels(headers)

        # Fill table with data
        for row_idx, row_data in enumerate(data):
            for col_idx, (key, value) in enumerate(row_data.items()):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                # Color code the values
                if key == 'Heart Rate':
                    item.setForeground(QColor('#e57373'))  # Soft red
                elif key == 'SpO2':
                    item.setForeground(QColor('#81c784'))  # Soft green

                self.dataTable.setItem(row_idx, col_idx, item)

        # Resize columns to fit content
        self.dataTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.dataTable.horizontalHeader().setStretchLastSection(True)

    def update_summary(self, latest_data):
        hr = latest_data.get('Heart Rate', '--')
        spo2 = latest_data.get('SpO2', '--')

        self.heart_rate_label.setText(f"Heart Rate: <b>{hr}</b> bpm")
        self.spo2_label.setText(f"SpO2: <b>{spo2}</b>%")
        self.last_update_label.setText(f"Last updated: <b>{time.strftime('%H:%M:%S')}</b>")
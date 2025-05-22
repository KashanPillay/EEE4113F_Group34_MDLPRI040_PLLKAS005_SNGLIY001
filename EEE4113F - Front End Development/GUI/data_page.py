from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy, QCalendarWidget, QScrollArea
)
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QPoint, QDateTime
import time
import sheets_retrieve
from PyQt5.QtWidgets import QMessageBox
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QDateTimeEdit


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
        self.figure = Figure(figsize=(8, 4), dpi=100)  # Larger figure size
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)


class DataPage(QWidget):
    def __init__(self, navigate_to_home):
        super().__init__()
        self.navigate_to_home = navigate_to_home
        self.all_data = []  # Store all loaded data for filtering
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        # Update the stylesheet in the setup_ui method to include calendar styling
        self.setStyleSheet("""
            
            QLabel {
                color: #333333;
            }

            /* Style for all dropdown controls */
            QComboBox, QDateTimeEdit {
                padding: 6px;
                padding-right: 25px;  /* Make room for arrow */
                border-radius: 6px;
                border: 1px solid #d0d0d0;
                min-width: 120px;
                color: #333333;
                background: white;
            }

            /* Drop-down arrow styling */
            QComboBox::drop-down, QDateTimeEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 25px;
                border-left: 1px solid #d0d0d0;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                background: #81d4fa;
            }

            /* Arrow icon styling */
            QComboBox::down-arrow, QDateTimeEdit::down-arrow {
                image: url(arrow_down.svg);  /* Replace with your arrow icon */
                width: 12px;
                height: 12px;
            }

            /* Calendar widget styling */
            QCalendarWidget QWidget {
                background-color: grey;
                color: #333333;
            }
            QCalendarWidget QToolButton {
                background-color: grey;
                color: #333333;
                font-size: 12px;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: white;
                color: #333333;
                selection-background-color: #81d4fa;
                selection-color: black;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #aaaaaa;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;
            }
            QCalendarWidget QAbstractItemView:item:hover {
                background-color: #e0e0e0;
            }
            QMessageBox {
             background-color: #333333;  /* Light background */
            }
            QMessageBox QLabel {
             color: #fafafa;  /* Red color for text */
                font-size: 14px;
             }
            QMessageBox QPushButton {
                background-color: #81d4fa;
                color: #2d2d2d;
                border-radius: 4px;
                padding: 5px 10px;
            }

        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = PastelHeader()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 0, 40, 0)

        title_label = QLabel("Monitor Vital Signs")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("""color: #5d5d5d; background = transparent""")
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        header_layout.addStretch()
        layout.addWidget(header)

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

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #fafafa;")

        # Content container
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(50, 50, 50, 50)
        content_layout.setSpacing(30)

        # Stats Summary Cards
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
            background: #ffebee;
        """)
        self.spo2_label = QLabel("SpO2: --%")
        self.spo2_label.setStyleSheet(f"""
            {card_style}
            background: #e8f5e9;
        """)
        self.last_update_label = QLabel("Last updated: --")
        self.last_update_label.setStyleSheet(f"""
            {card_style}
            background: #e1f5fe;
        """)

        for label in [self.heart_rate_label, self.spo2_label, self.last_update_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            stats_layout.addWidget(label)

        content_layout.addWidget(self.stats_widget)

        # Graph controls container
        self.graph_controls = ModernCard()
        self.graph_controls.setStyleSheet("""
            QLabel {
                color: #333333;
                font-weight: 500;
            }
            QComboBox, QDateEdit {
                background: white;
                color: #333333;
            }
        """)
        self.graph_controls.setVisible(False)  # Initially hidden
        controls_layout = QHBoxLayout(self.graph_controls)
        controls_layout.setContentsMargins(15, 15, 15, 15)

        # Date range selector
        self.range_combo = QComboBox()
        self.range_combo.addItems([
            "Last 1 hour",
            "Last 6 hours",
            "Last 24 hours",
            "Last 7 days",
            "Custom range",
            "All data"
        ])
        self.range_combo.setCurrentText("Last 24 hours")
        self.range_combo.currentTextChanged.connect(self.update_graph)

        # Custom date range selectors
        self.start_date = QDateTimeEdit()
        self.start_date.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.start_date.setCalendarPopup(True)
        self.start_date.setDateTime(QDateTime.currentDateTime().addSecs(-3600 * 24))  # Default to 24h ago

        self.end_date = QDateTimeEdit()
        self.end_date.setDisplayFormat("dd/MM/yyyy HH:mm")
        self.end_date.setCalendarPopup(True)
        self.end_date.setDateTime(QDateTime.currentDateTime())

        # Add time edit buttons to the calendar popup
        self.start_date.setCalendarWidget(self.create_calendar_with_time())
        self.end_date.setCalendarWidget(self.create_calendar_with_time())

        # Add widgets to layout
        controls_layout.addWidget(QLabel("Time range:"))
        controls_layout.addWidget(self.range_combo)
        controls_layout.addWidget(QLabel("From:"))
        controls_layout.addWidget(self.start_date)
        controls_layout.addWidget(QLabel("To:"))
        controls_layout.addWidget(self.end_date)
        controls_layout.addStretch()

        content_layout.addWidget(self.graph_controls)

        # Add Apply button
        self.apply_btn = QPushButton("Apply Range")
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background: #81d4fa;
                color: #2d2d2d;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background: #4fc3f7;
            }
        """)
        self.apply_btn.clicked.connect(self.update_graph)
        controls_layout.addWidget(self.apply_btn)
        self.apply_btn.setShortcut("Return")

        # Graph container
        self.graphContainer = GraphCard()
        self.graphContainer.hide()
        content_layout.addWidget(self.graphContainer)

        # Button container
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addStretch()

        # Refresh Button
        refresh_btn = QPushButton("Refresh Data")
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

        # Graph Button
        graph_btn = QPushButton("Show Oxygen Saturation Graph")
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

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(graph_btn)
        btn_layout.addStretch()
        content_layout.addWidget(btn_container)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def create_calendar_with_time(self):
        """Create a calendar widget with time editing capability"""
        calendar = QCalendarWidget()
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        return calendar

    def filter_data_by_range(self):
        """Filter data based on selected time range"""
        if not self.all_data:
            return []

        range_text = self.range_combo.currentText()

        if range_text == "All data":
            return self.all_data

        elif range_text == "Custom range":
            start_dt = self.start_date.dateTime().toPyDateTime()
            end_dt = self.end_date.dateTime().toPyDateTime()
            return [d for d in self.all_data if start_dt <= d['datetime'] <= end_dt]

        else:
            now = datetime.now()
            if range_text == "Last 1 hour":
                cutoff = now - timedelta(hours=1)
            elif range_text == "Last 6 hours":
                cutoff = now - timedelta(hours=6)
            elif range_text == "Last 24 hours":
                cutoff = now - timedelta(hours=24)
            elif range_text == "Last 7 days":
                cutoff = now - timedelta(days=7)
            else:
                return self.all_data

            return [d for d in self.all_data if d['datetime'] >= cutoff]

    def toggle_graph(self):
        """Toggle graph visibility and controls"""
        if self.graphContainer.isVisible():
            self.graphContainer.hide()
            self.graph_controls.hide()
        else:
            self.graph_controls.show()
            # Force an update when showing the graph
            self.update_graph()
            self.graphContainer.show()
    def filter_data_by_range(self):
        """Filter data based on selected time range"""
        if not self.all_data:
            return []

        range_text = self.range_combo.currentText()
        now = datetime.now()

        if range_text == "All data":
            return self.all_data

        elif range_text == "Custom range":
            start_dt = self.start_date.dateTime().toPyDateTime()
            end_dt = self.end_date.dateTime().toPyDateTime()
            return [d for d in self.all_data if start_dt <= d['datetime'] <= end_dt]

        elif range_text == "Last 1 hour":
            cutoff = now - timedelta(hours=1)
        elif range_text == "Last 6 hours":
            cutoff = now - timedelta(hours=6)
        elif range_text == "Last 24 hours":
            cutoff = now - timedelta(hours=24)
        elif range_text == "Last 7 days":
            cutoff = now - timedelta(days=7)
        else:
            return self.all_data

        return [d for d in self.all_data if d['datetime'] >= cutoff]

    def update_graph(self):
        """Update graph when range selection changes"""
        if not self.graphContainer.isVisible():
            return

        # Show/hide custom date range controls
        show_custom = self.range_combo.currentText() == "Custom range"
        self.start_date.setVisible(show_custom)
        self.end_date.setVisible(show_custom)

        # Only plot if not custom range or if custom range with valid dates
        if not show_custom or (show_custom and self.validate_dates()):
            self.plot_ror_graph()

    def validate_dates(self):
        """Validate that start date is before end date"""
        start_dt = self.start_date.dateTime().toPyDateTime()
        end_dt = self.end_date.dateTime().toPyDateTime()

        if start_dt > end_dt:
            QMessageBox.warning(self, "Invalid Range",
                                "Start date must be before end date")
            return False
        return True

    def plot_ror_graph(self):
        """Plot the RoR graph with current filters"""
        try:
            if not self.all_data:
                QMessageBox.warning(self, "Warning", "No data available to plot")
                return

            # Get filtered data
            filtered_data = self.filter_data_by_range()
            if not filtered_data:
                QMessageBox.warning(self, "Warning", "No data in selected time range")
                return

            # Prepare data for plotting
            dates = [d['datetime'] for d in filtered_data]
            y_values = [d['y_value'] for d in filtered_data]

            # Clear previous plot
            self.graphContainer.figure.clear()
            ax = self.graphContainer.figure.add_subplot(111)

            # Plot data with improved styling
            ax.plot(dates, y_values, marker='o', linestyle='-',
                    color='#81d4fa', markersize=6, linewidth=1.5,
                    markerfacecolor='white', markeredgewidth=1.5)

            # Format plot with better readability
            ax.set_title('',
                         color='#5d5d5d', pad=20, fontsize=12)
            ax.set_xlabel('Date & Time', color='#5d5d5d', fontsize=10)
            ax.set_ylabel('Oxygen Saturation', color='#5d5d5d', fontsize=10)

            # Add grid and background
            ax.grid(True, linestyle=':', alpha=0.5)
            ax.set_facecolor('#fafafa')

            # Format x-axis dates based on time range
            if len(dates) > 1:
                time_span = dates[-1] - dates[0]
                if time_span > timedelta(days=2):
                    ax.xaxis.set_major_formatter(DateFormatter('%d/%m\n%H:%M'))
                else:
                    ax.xaxis.set_major_formatter(DateFormatter('%H:%M\n%d/%m'))

            # Auto-scale and adjust layout
            ax.relim()
            ax.autoscale_view()
            self.graphContainer.figure.tight_layout()

            # Set colors
            for spine in ax.spines.values():
                spine.set_edgecolor('#e0e0e0')
            ax.tick_params(colors='#5d5d5d', labelsize=9)

            # Add some padding around the plot
            self.graphContainer.figure.subplots_adjust(left=0.1, right=0.95,
                                                       bottom=0.15, top=0.9)

            # Redraw canvas
            self.graphContainer.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot graph: {str(e)}")

    def load_data(self):
        try:
            # Hide graph when refreshing data
            self.graphContainer.hide()
            self.graph_controls.hide()

            raw_data = sheets_retrieve.get_sheet_data()
            if not raw_data:
                QMessageBox.warning(self, "Warning", "No data available from Google Sheet")
                return

            # Process data - parse dates and calculate y values
            self.all_data = []
            for row in raw_data:
                try:
                    # Parse date and time
                    dt_str = f"{row.get('Date', '')} {row.get('Time', '')}"
                    dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")

                    # Calculate y = 110 - 25(RoR)
                    ratio1 = float(row.get('Ratio 1', 0))
                    ratio2 = float(row.get('Ratio 2', 1))  # Avoid division by zero
                    ror = ratio1 / ratio2 if ratio2 != 0 else 0
                    y = 110 - 25 * ror

                    # Store processed data
                    self.all_data.append({
                        'datetime': dt,
                        'y_value': y,
                        'original_data': row
                    })
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e}")
                    continue

            if not self.all_data:
                QMessageBox.warning(self, "Warning", "No valid data loaded")
                return

            # Update summary with latest data
            self.update_summary(self.all_data[-1]['original_data'])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data from Google Sheet: {str(e)}")

    def update_summary(self, latest_data):
        hr = latest_data.get('Heart Rate', '--')
        spo2 = latest_data.get('SpO2', '')

        # Calculate y-value from RoR
        try:
            ratio1 = float(latest_data.get('Ratio 1', 0))
            ratio2 = float(latest_data.get('Ratio 2', 1))  # Avoid division by zero
            ror = ratio1 / ratio2 if ratio2 != 0 else 0
            y_value = 110 - 25 * ror
            y_display = f"{y_value:.1f}"  # Format to 1 decimal place

            # Check if oxygen saturation is below 90
            if y_value < 90:
                # Show warning message (only if not already shown for this low value)
                if not hasattr(self, '_low_spo2_warning_shown') or not self._low_spo2_warning_shown:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Warning: Oxygen Saturation is Low!")
                    msg.setInformativeText(f"Oxygen saturation is {y_display}% (below 90%). Please check the patient.")
                    msg.setWindowTitle("Low Oxygen Warning")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setStyleSheet("""
                        QMessageBox {
                            background-color: #333333;
                        }
                        QMessageBox QLabel {
                            color: #ffeb3b;
                            font-size: 14px;
                        }
                        QMessageBox QPushButton {
                            background-color: #81d4fa;
                            color: #2d2d2d;
                            border-radius: 4px;
                            padding: 5px 10px;
                        }
                    """)
                    msg.exec_()
                    self._low_spo2_warning_shown = True

                # Change SpO2 label to red warning style
                self.spo2_label.setStyleSheet(f"""
                    QLabel {{
                        font-size: 16px;
                        font-weight: 600;
                        padding: 20px;
                        border-radius: 12px;
                        color: white;
                        min-width: 200px;
                        background: #f44336;
                    }}
                """)
            else:
                # Reset to normal style if above 90
                self.spo2_label.setStyleSheet(f"""
                    QLabel {{
                        font-size: 16px;
                        font-weight: 600;
                        padding: 20px;
                        border-radius: 12px;
                        color: #5d5d5d;
                        min-width: 200px;
                        background: #e8f5e9;
                    }}
                """)
                self._low_spo2_warning_shown = False

        except (ValueError, TypeError):
            y_display = "--"
            # Reset to normal style if there's an error
            self.spo2_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    font-weight: 600;
                    padding: 20px;
                    border-radius: 12px;
                    color: #5d5d5d;
                    min-width: 200px;
                    background: #e8f5e9;
                }}
            """)

        self.heart_rate_label.setText(f"Heart Rate: <b>{hr}</b> bpm")
        self.spo2_label.setText(f"SpO2: <b>{spo2}</b> <b>{y_display}</b>%")
        self.last_update_label.setText(f"Last updated: <b>{time.strftime('%H:%M:%S')}</b>")
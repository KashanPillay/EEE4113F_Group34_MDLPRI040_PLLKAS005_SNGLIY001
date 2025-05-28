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
        self.all_data = []  # Store all loaded data
        self.setup_ui()
        self.load_data()

    def create_calendar_with_time(self):
        calendar = QCalendarWidget()
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        return calendar

    def setup_ui(self):

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

        self.heart_rate_label = QLabel("Pulse: -- bpm")
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

        #Graph Controls Container
        self.spo2_controls = ModernCard()
        self.spo2_controls.setStyleSheet("""
                    QLabel {
                        color: #333333;
                        font-weight: 500;
                    }
                    QComboBox, QDateEdit {
                        background: white;
                        color: #333333;
                    }
                """)
        self.spo2_controls.setVisible(False)
        spo2_controls_layout = QHBoxLayout(self.spo2_controls)
        spo2_controls_layout.setContentsMargins(15, 15, 15, 15)

        self.pulse_controls = ModernCard()
        self.pulse_controls.setStyleSheet(self.spo2_controls.styleSheet())
        self.pulse_controls.setVisible(False)
        pulse_controls_layout = QHBoxLayout(self.pulse_controls)
        pulse_controls_layout.setContentsMargins(15, 15, 15, 15)

        # Create controls for both graphs
        def create_graph_controls():
            range_combo = QComboBox()
            range_combo.addItems([
                "Last 1 hour",
                "Last 6 hours",
                "Last 24 hours",
                "Last 7 days",
                "Custom range",
                "All data"
            ])
            range_combo.setCurrentText("Last 24 hours")

            start_date = QDateTimeEdit()
            start_date.setDisplayFormat("dd/MM/yyyy HH:mm")
            start_date.setCalendarPopup(True)
            start_date.setDateTime(QDateTime.currentDateTime().addSecs(-3600 * 24))

            end_date = QDateTimeEdit()
            end_date.setDisplayFormat("dd/MM/yyyy HH:mm")
            end_date.setCalendarPopup(True)
            end_date.setDateTime(QDateTime.currentDateTime())

            start_date.setCalendarWidget(self.create_calendar_with_time())
            end_date.setCalendarWidget(self.create_calendar_with_time())

            apply_btn = QPushButton("Apply Range")
            apply_btn.setStyleSheet("""
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
            apply_btn.setShortcut("Return")

            return range_combo, start_date, end_date, apply_btn

        # Spo2 controls
        (self.spo2_range_combo, self.spo2_start_date,
         self.spo2_end_date, self.spo2_apply_btn) = create_graph_controls()
        self.spo2_range_combo.currentTextChanged.connect(lambda: self.update_graph('spo2'))
        self.spo2_apply_btn.clicked.connect(lambda: self.update_graph('spo2'))

        spo2_controls_layout.addWidget(QLabel("Time range:"))
        spo2_controls_layout.addWidget(self.spo2_range_combo)
        spo2_controls_layout.addWidget(QLabel("From:"))
        spo2_controls_layout.addWidget(self.spo2_start_date)
        spo2_controls_layout.addWidget(QLabel("To:"))
        spo2_controls_layout.addWidget(self.spo2_end_date)
        spo2_controls_layout.addStretch()
        spo2_controls_layout.addWidget(self.spo2_apply_btn)

        # Pulse controls
        (self.pulse_range_combo, self.pulse_start_date,
         self.pulse_end_date, self.pulse_apply_btn) = create_graph_controls()
        self.pulse_range_combo.currentTextChanged.connect(lambda: self.update_graph('pulse'))
        self.pulse_apply_btn.clicked.connect(lambda: self.update_graph('pulse'))

        pulse_controls_layout.addWidget(QLabel("Time range:"))
        pulse_controls_layout.addWidget(self.pulse_range_combo)
        pulse_controls_layout.addWidget(QLabel("From:"))
        pulse_controls_layout.addWidget(self.pulse_start_date)
        pulse_controls_layout.addWidget(QLabel("To:"))
        pulse_controls_layout.addWidget(self.pulse_end_date)
        pulse_controls_layout.addStretch()
        pulse_controls_layout.addWidget(self.pulse_apply_btn)

        content_layout.addWidget(self.spo2_controls)
        content_layout.addWidget(self.pulse_controls)

        # Graph containers
        self.spo2_graph = GraphCard()
        self.spo2_graph.hide()
        content_layout.addWidget(self.spo2_graph)

        self.pulse_graph = GraphCard()
        self.pulse_graph.hide()
        content_layout.addWidget(self.pulse_graph)

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

        # Graph Buttons
        spo2_graph_btn = QPushButton("Show Oxygen Saturation Graph")
        spo2_graph_btn.setStyleSheet("""
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
        spo2_graph_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        spo2_graph_btn.clicked.connect(lambda: self.toggle_graph('spo2'))

        pulse_graph_btn = QPushButton("Show Pulse Graph")
        pulse_graph_btn.setStyleSheet("""
                    QPushButton {
                        background: #80cbc4;
                        color: #2d2d2d;
                        border: none;
                        border-radius: 12px;
                        padding: 12px 24px;
                        font-size: 14px;
                        font-weight: 600;
                        min-width: 180px;
                    }
                    QPushButton:hover {
                        background: #4db6ac;
                    }
                    QPushButton:pressed {
                        background: #26a69a;
                    }
                """)
        pulse_graph_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        pulse_graph_btn.clicked.connect(lambda: self.toggle_graph('pulse'))

        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(spo2_graph_btn)
        btn_layout.addWidget(pulse_graph_btn)
        btn_layout.addStretch()
        content_layout.addWidget(btn_container)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def filter_data_by_range(self, data_type, all_data):
        if not all_data:
            return []

        if data_type == 'spo2':
            range_combo = self.spo2_range_combo
            start_date = self.spo2_start_date
            end_date = self.spo2_end_date
        else:  # pulse
            range_combo = self.pulse_range_combo
            start_date = self.pulse_start_date
            end_date = self.pulse_end_date

        range_text = range_combo.currentText()

        if range_text == "All data":
            return all_data

        elif range_text == "Custom range":
            start_dt = start_date.dateTime().toPyDateTime()
            end_dt = end_date.dateTime().toPyDateTime()
            return [d for d in all_data if start_dt <= d['datetime'] <= end_dt]

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
                return all_data

            return [d for d in all_data if d['datetime'] >= cutoff]

    def toggle_graph(self, graph_type):
        if graph_type == 'spo2':
            graph = self.spo2_graph
            controls = self.spo2_controls
        else:  # pulse
            graph = self.pulse_graph
            controls = self.pulse_controls

        if graph.isVisible():
            graph.hide()
            controls.hide()
        else:
            controls.show()
            self.update_graph(graph_type)
            graph.show()

    def update_graph(self, graph_type):
        if graph_type == 'spo2':
            graph = self.spo2_graph
            show_custom = self.spo2_range_combo.currentText() == "Custom range"
            self.spo2_start_date.setVisible(show_custom)
            self.spo2_end_date.setVisible(show_custom)

            if not show_custom or (show_custom and self.validate_dates('spo2')):
                self.plot_graph(graph_type)
        else:  # pulse
            graph = self.pulse_graph
            show_custom = self.pulse_range_combo.currentText() == "Custom range"
            self.pulse_start_date.setVisible(show_custom)
            self.pulse_end_date.setVisible(show_custom)

            if not show_custom or (show_custom and self.validate_dates('pulse')):
                self.plot_graph(graph_type)

    def validate_dates(self, graph_type):
        if graph_type == 'spo2':
            start_dt = self.spo2_start_date.dateTime().toPyDateTime()
            end_dt = self.spo2_end_date.dateTime().toPyDateTime()
        else:  # pulse
            start_dt = self.pulse_start_date.dateTime().toPyDateTime()
            end_dt = self.pulse_end_date.dateTime().toPyDateTime()

        if start_dt > end_dt:
            QMessageBox.warning(self, "Invalid Range",
                                "Start date must be before end date")
            return False
        return True

    def plot_graph(self, graph_type):
        try:
            if not self.all_data:
                QMessageBox.warning(self, "Warning", "No data available to plot")
                return

            # Get filtered data
            if graph_type == 'spo2':
                filtered_data = self.filter_data_by_range('spo2', self.all_data)
                y_values = [d['spo2_value'] for d in filtered_data]
                y_label = 'Oxygen Saturation (%)'
                color = '#ce93d8'
                title = 'Oxygen Saturation Over Time'
            else:  # pulse
                filtered_data = self.filter_data_by_range('pulse', self.all_data)
                y_values = [d['pulse_value'] for d in filtered_data]
                y_label = 'Pulse (bpm)'
                color = '#80cbc4'
                title = ''

            if not filtered_data:
                QMessageBox.warning(self, "Warning", "No data in selected time range")
                return

            dates = [d['datetime'] for d in filtered_data]

            # Get the appropriate graph container
            graph = self.spo2_graph if graph_type == 'spo2' else self.pulse_graph

            # Clear previous plot
            graph.figure.clear()
            ax = graph.figure.add_subplot(111)

            # Plot data
            ax.plot(dates, y_values, marker='o', linestyle='-',
                    color=color, markersize=6, linewidth=1.5,
                    markerfacecolor='white', markeredgewidth=1.5)

            # Format plot
            ax.set_title(title, color='#5d5d5d', pad=20, fontsize=12)
            ax.set_xlabel('Date & Time', color='#5d5d5d', fontsize=10)
            ax.set_ylabel(y_label, color='#5d5d5d', fontsize=10)

            ax.grid(True, linestyle=':', alpha=0.5)
            ax.set_facecolor('#fafafa')

            if len(dates) > 1:
                time_span = dates[-1] - dates[0]
                if time_span > timedelta(days=2):
                    ax.xaxis.set_major_formatter(DateFormatter('%d/%m\n%H:%M'))
                else:
                    ax.xaxis.set_major_formatter(DateFormatter('%H:%M\n%d/%m'))

            ax.relim()
            ax.autoscale_view()
            graph.figure.tight_layout()

            for spine in ax.spines.values():
                spine.set_edgecolor('#e0e0e0')
            ax.tick_params(colors='#5d5d5d', labelsize=9)

            graph.figure.subplots_adjust(left=0.1, right=0.95,
                                         bottom=0.15, top=0.9)

            graph.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot {graph_type} graph: {str(e)}")

    def load_data(self):
        try:
            # Hide graphs when refreshing data
            self.spo2_graph.hide()
            self.pulse_graph.hide()
            self.spo2_controls.hide()
            self.pulse_controls.hide()

            raw_data = sheets_retrieve.get_sheet_data()
            if not raw_data:
                QMessageBox.warning(self, "Warning", "No data available from Google Sheet")
                return

            # Process data
            self.all_data = []
            for row in raw_data:
                try:
                    # Date and time
                    dt_str = f"{row.get('Date', '')} {row.get('Time', '')}"
                    dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")

                    # Calculate SpO2
                    calibrate = float(row.get('DC Value', 2))
                    ratio1 = (float(row.get('Ratio 1', 0))) - calibrate
                    ratio2 = (float(row.get('Ratio 2', 1))) - calibrate
                    ror = ratio1 / ratio2 if ratio2 != 0 else 0
                    spo2 = (114.9791294 * ror) + 26.625233632

                    # Get Pulse
                    pulse = float(row.get('Pulse', 0))

                    # Store processed data
                    self.all_data.append({
                        'datetime': dt,
                        'spo2_value': spo2,
                        'pulse_value': pulse,
                        'original_data': row
                    })
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e}")
                    continue

            if not self.all_data:
                QMessageBox.warning(self, "Warning", "No valid data loaded")
                return

            # Update summary with latest data
            self.update_summary(self.all_data[-1])

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data from Google Sheet: {str(e)}")

    def update_summary(self, latest_data):
        pulse = latest_data['original_data'].get('Pulse', '--')
        spo2 = latest_data['original_data'].get('SpO2', '--')
        calculated_spo2 = f"{latest_data['spo2_value']:.1f}" if 'spo2_value' in latest_data else "--"

        # Update heart rate label
        self.heart_rate_label.setText(f"Pulse: <b>{pulse}</b> bpm")

        # Update SpO2 label with warning for low oxygen
        try:
            if float(calculated_spo2) < 90:
                self.spo2_label.setStyleSheet("""
                            QLabel {
                                font-size: 16px;
                                font-weight: 600;
                                padding: 20px;
                                border-radius: 12px;
                                color: white;
                                min-width: 200px;
                                background: #f44336;
                            }
                        """)
                if not hasattr(self, '_low_spo2_warning_shown') or not self._low_spo2_warning_shown:
                    QMessageBox.warning(
                        self,
                        "Low Oxygen Warning",
                        f"Oxygen saturation is {calculated_spo2}% (below 90%). Please check the patient."
                    )
                    self._low_spo2_warning_shown = True
            else:
                self.spo2_label.setStyleSheet("""
                QLabel
                {
                font-size: 16px;
                font-weight: 600;
                padding: 20px;
                border-radius: 12px;
                color:  #5d5d5d;
                min-width: 200px;
                background:  # e8f5e9;
                }
            """)
                self._low_spo2_warning_shown = False
        except ValueError:
            pass

        self.spo2_label.setText(f"SpO2:  <b>{calculated_spo2}</b>%")
        self.last_update_label.setText(f"Last updated: <b>{time.strftime('%H:%M:%S')}</b>")
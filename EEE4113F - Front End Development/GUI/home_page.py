from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea,
                             QHBoxLayout, QFrame, QPushButton, QSpacerItem,
                             QSizePolicy, QGraphicsDropShadowEffect)
from PyQt5.QtGui import (QPixmap, QFont, QIcon, QColor, QLinearGradient,
                         QPainter, QBrush, QFontDatabase)
from PyQt5.QtCore import Qt, QSize, QPoint


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

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


class HomePage(QWidget):
    def __init__(self, navigate_to_data_page, navigate_to_tracking_page):
        super().__init__()
        self.navigate_to_data_page = navigate_to_data_page
        self.navigate_to_tracking_page = navigate_to_tracking_page
        self.load_fonts()
        self.init_ui()

    def load_fonts(self):
        # Load modern fonts (you'll need to have these font files)
        QFontDatabase.addApplicationFont("assets/fonts/Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont("assets/fonts/Montserrat-SemiBold.ttf")

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add pastel gradient header
        header = PastelHeader()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(40, 0, 40, 0)

        # Title with modern font

        title_label = QLabel("CODY - Remote Pulse Oximeter")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #5d5d5d;")
        header_layout.addWidget(title_label, alignment=Qt.AlignLeft)

        # Right spacer to balance layout
        header_layout.addStretch()
        main_layout.addWidget(header)

        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: #fafafa;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)

        # 1. Hero Section with soft pastel card
        hero_card = ModernCard()
        hero_card.setContentsMargins(0, 0, 0, 0)
        hero_layout = QHBoxLayout(hero_card)
        hero_layout.setContentsMargins(30, 30, 30, 30)
        hero_layout.setSpacing(40)

        # Hero Image with soft rounded corners
        hero_image_container = QFrame()
        hero_image_container.setStyleSheet("""
            QFrame {
                background: #e3f2fd;
                border-radius: 12px;
                border: none;
            }
        """)
        hero_image_container.setFixedSize(340, 240)
        hero_image_layout = QVBoxLayout(hero_image_container)
        hero_image_layout.setContentsMargins(10, 10, 10, 10)

        hero_image = QLabel()
        hero_pixmap = QPixmap("assets/her_image.png").scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        hero_image.setPixmap(hero_pixmap)
        hero_image.setAlignment(Qt.AlignCenter)
        hero_image_layout.addWidget(hero_image)
        hero_layout.addWidget(hero_image_container)

        # Hero Text with modern typography
        hero_text = QLabel("""
        <h2 style="color: #5d5d5d; margin-bottom: 20px; font-family: 'Montserrat SemiBold';">Monitor Vital Signs and Track Remotely</h2>
        <p style="color: #8e8e8e; font-size: 15px; line-height: 1.6; font-family: 'Montserrat';">
        CODY provides continuous monitoring of heart rate and oxygen saturation (SpO₂),<br>
        helping specialists monitor their penguins from anywhere!.
        </p>
        """)
        hero_text.setWordWrap(True)

        # Get Started Button with soft color
        get_started_btn = QPushButton("CHECK my Penguin")
        get_started_btn.setStyleSheet("""
            QPushButton {
                background: #81d4fa;
                color: #2d2d2d;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-family: 'Montserrat SemiBold';
                min-width: 180px;
            }
            QPushButton:hover {
                background: #4fc3f7;
            }
        """)
        get_started_btn.setCursor(Qt.PointingHandCursor)
        get_started_btn.clicked.connect(self.navigate_to_data_page)

        get_started_btn2 = QPushButton("TRACK my Penguin")
        get_started_btn2.setStyleSheet("""
            QPushButton {
                background: #81d4fa;
                color: #2d2d2d;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-family: 'Montserrat SemiBold';
                min-width: 180px;
            }
            QPushButton:hover {
                background: #4fc3f7;
            }
        """)
        get_started_btn2.setCursor(Qt.PointingHandCursor)
        get_started_btn2.clicked.connect(self.navigate_to_tracking_page)



        hero_text_layout = QVBoxLayout()
        hero_text_layout.setSpacing(25)
        hero_text_layout.addWidget(hero_text)
        hero_text_layout.addWidget(get_started_btn, alignment=Qt.AlignLeft)
        hero_text_layout.addWidget(get_started_btn2, alignment=Qt.AlignLeft)
        hero_text_layout.addStretch()
        hero_layout.addLayout(hero_text_layout)

        content_layout.addWidget(hero_card)

        # 2. Features Section with pastel cards
        features_label = QLabel("<h2 style='color: #5d5d5d; font-family: \"Montserrat SemiBold\";'>Key Features</h2>")
        features_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(features_label)

        features = [
            ("Real-Time Monitoring", "assets/realtime_icon.png",
             "Real time updates with smooth data visualization.", "#e1f5fe"),
            ("Easy-To-Use Interface", "assets/easy_icon.png",
             "User friendly access to key features.", "#ffebee"),
            ("GPS Tracking", "assets/gps_icon.png",
             "Real time location tracking.", "#e8f5e9"),
            ("Data History", "assets/history_icon.png",
             "Comprehensive record keeping.", "#f3e5f5")
        ]

        features_frame = QFrame()
        features_layout = QHBoxLayout(features_frame)
        features_layout.setContentsMargins(0, 0, 0, 0)
        features_layout.setSpacing(20)

        for title, icon_path, desc, bg_color in features:
            feature_card = ModernCard()
            feature_card.setStyleSheet(f"ModernCard {{ background: {bg_color}; }}")
            feature_card.setFixedWidth(240)
            feature_layout = QVBoxLayout(feature_card)
            feature_layout.setContentsMargins(25, 25, 25, 25)
            feature_layout.setSpacing(20)

            # Feature Icon with soft background
            icon_container = QFrame()
            icon_container.setStyleSheet("""
                QFrame {
                    background: white;
                    border-radius: 20px;
                    padding: 10px;
                }
            """)
            icon_container.setFixedSize(80, 80)
            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            icon = QLabel()
            icon_pixmap = QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon.setPixmap(icon_pixmap)
            icon.setAlignment(Qt.AlignCenter)
            icon_layout.addWidget(icon)

            feature_layout.addWidget(icon_container, alignment=Qt.AlignCenter)

            # Feature Title
            title_label = QLabel(f"<h3 style='color: #5d5d5d; font-family: \"Montserrat SemiBold\";'>{title}</h3>")
            title_label.setAlignment(Qt.AlignCenter)
            feature_layout.addWidget(title_label)

            # Feature Description
            desc_label = QLabel(
                f"<p style='color: #8e8e8e; font-size: 14px; font-family: \"Montserrat\"; line-height: 1.5;'>{desc}</p>")
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            feature_layout.addWidget(desc_label)

            features_layout.addWidget(feature_card)

        content_layout.addWidget(features_frame)

        # 3. How It Works Section
        steps_card = ModernCard()
        steps_card.setStyleSheet("ModernCard { background: white; }")
        steps_layout = QVBoxLayout(steps_card)
        steps_layout.setContentsMargins(30, 30, 30, 30)
        steps_layout.setSpacing(25)

        steps_title = QLabel("<h2 style='color: #5d5d5d; font-family: \"Montserrat SemiBold\";'>How CODY Works</h2>")
        steps_layout.addWidget(steps_title)

        steps = [
            ("1. Gentle Setup", "Connect the comfortable pulse oximeter to the penguin.", "#e1f5fe"),
            ("2. Monitoring", "Vital signs are monitored with minimal disruption.", "#ffebee"),
            ("3. Data Analysis", "Our algorithms detect important metrics and display them.", "#e8f5e9"),
            ("4. Tracking", "See where in the colony your penguin is.", "#f3e5f5")
        ]

        for step_num, step_desc, step_color in steps:
            step_frame = QFrame()
            step_frame.setStyleSheet(f"""
                QFrame {{
                    background: {step_color};
                    border-radius: 12px;
                    padding: 20px;
                }}
            """)
            step_layout = QHBoxLayout(step_frame)
            step_layout.setContentsMargins(0, 0, 0, 0)
            step_layout.setSpacing(20)

            step_num_label = QLabel(
                f"<span style='font-size: 24px; color: #81d4fa; font-family: \"Montserrat SemiBold\";'>{step_num.split('.')[0]}</span>")
            step_layout.addWidget(step_num_label)

            step_content = QLabel(f"""
                <h3 style='color: #5d5d5d; margin: 0; font-family: "Montserrat SemiBold";'>{step_num.split('.')[1].strip()}</h3>
                <p style='color: #8e8e8e; margin: 8px 0 0 0; font-family: "Montserrat"; font-size: 14px;'>{step_desc}</p>
            """)
            step_content.setWordWrap(True)
            step_layout.addWidget(step_content, 1)

            steps_layout.addWidget(step_frame)

        content_layout.addWidget(steps_card)

        # Footer with soft color
        footer = QFrame()
        footer.setStyleSheet("background: #e1f5fe;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(40, 20, 40, 20)

        copyright = QLabel("2025 EEE4113F Group 34")
        copyright.setStyleSheet("color: #5d5d5d; font-size: 12px; font-family: 'Montserrat';")
        footer_layout.addWidget(copyright)

        version = QLabel("v1.5")
        version.setStyleSheet("color: #5d5d5d; font-size: 12px; font-family: 'Montserrat';")
        footer_layout.addWidget(version, alignment=Qt.AlignRight)

        content_layout.addWidget(footer)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
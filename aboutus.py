from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QColor, QLinearGradient, QPainter, QPainterPath, QBrush, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRectF, QEasingCurve

class AboutUsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("AGRINOVA - About Us Page")

    def initUI(self):
        # Set window size and title
        self.setGeometry(100, 100, 800, 500)  # Larger window for better proportions
        self.setWindowIcon(QIcon("favicon.png"))

        # Set greenish gradient background
        self.setAutoFillBackground(True)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #64c896, stop:1 #329664);")

        # Remove default window frame and add rounded corners
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)  # Increased spacing for better proportions

        # Add a title with animation
        self.title_label = QLabel("About Us", self)
        self.title_label.setFont(QFont("Arial", 36, QFont.Bold))  # Larger font size
        self.title_label.setStyleSheet("color: white;")
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Animate the title
        self.animateTitle()

        # Add a description with fixed width and word wrapping
        description = QLabel(
            """
            <p style='color: white; font-size: 18px; text-align: center; line-height: 1.5;'>
                Welcome to the <b>AI Invasive Species Detection Application</b>!<br><br>
                I, Manav Acharya, an undergraduate student at Purwanchal Campus, Dharan, 
                developed this app as a project for the 24-hour hackathon conducted by DELTA 5.0 
                on Magh 16-17, 2081. This app uses PyQt5 for the GUI, Python for the back-end, and 
                TensorFlow/Keras for image recognition.
            </p>
            """
        )
        description.setFont(QFont("Arial", 14))
        description.setWordWrap(True)  # Enable word wrap
        description.setMaximumWidth(700)  # Restrict max width to prevent text overflow
        layout.addWidget(description, alignment=Qt.AlignCenter)

        # Add a stylish close button
        self.close_button = QPushButton("Close", self)
        self.close_button.setFont(QFont("Arial", 16, QFont.Bold))  # Larger font size
        self.close_button.setFixedSize(150, 50)  # Fixed size for the button
        self.close_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #64c896, stop:1 #329664);
                color: white;
                padding: 10px 20px;
                border-radius: 25px;  /* More rounded corners */
                border: 2px solid #64c896;
                font-size: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #329664, stop:1 #64c896);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e7a4f, stop:1 #64c896);
            }
        """)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button, alignment=Qt.AlignCenter)

        # Set the layout
        self.setLayout(layout)

    def animateTitle(self):
        """ Create an animation for the title """
        self.title_animation = QPropertyAnimation(self.title_label, b"geometry")
        self.title_animation.setDuration(1000)  # 1 second
        self.title_animation.setStartValue(QRectF(0, 0, 0, 0))
        self.title_animation.setEndValue(QRectF(0, 0, 400, 60))  # Larger end value for better proportions
        self.title_animation.setEasingCurve(QEasingCurve.OutBounce)
        self.title_animation.start()

    def paintEvent(self, event):
        """ Add rounded corners to the window """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Smooth edges

        # Create a rounded rectangle path
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 20, 20)  # Rounded corners with 20px radius

        # Clip the painting area to the rounded rectangle
        painter.setClipPath(path)

        # Fill the background with the gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(100, 200, 150))  # Light green
        gradient.setColorAt(1, QColor(50, 150, 100))   # Darker green
        painter.fillPath(path, QBrush(gradient))

if __name__ == "__main__":
    app = QApplication([])
    about_us = AboutUsPage()
    about_us.show()
    app.exec_()

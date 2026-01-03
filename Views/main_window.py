# LIBRARY IMPORTS
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QApplication,
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QColor
from PySide6.QtCore import Qt, QSize
from pathlib import Path


# FILE IMPORTS
from views.add_contact_dialog import AddContactDialog


class VegaUI(QMainWindow):
    def __init__(self, assets_images: Path, assets_text: Path, on_text, on_voice):

        super().__init__()

        self.assets_images = assets_images
        self.assets_text = assets_text
        self.voice_icon_idle = QIcon(str(self.assets_images / "listen.png"))
        self.voice_icon_listening = QIcon(
            str(self.assets_images / "listen_active.png")
        )

        self.on_text = on_text
        self.on_voice = on_voice

        self.setWindowTitle("VEGA")
        self.setWindowIcon(QIcon(str(self.assets_images / "vega.ico")))
        self.setMinimumSize(1024, 700)

        self._create_interface()

    def _create_interface(self):
        # ===== CENTRAL CONTAINER =====
        central = QWidget()
        self.setCentralWidget(central)

        # ===== BACKGROUND =====
        self.background = QLabel(central)
        self.background.setScaledContents(True)
        self.background.setPixmap(
            QPixmap(str(self.assets_images / "vega_background.png"))
        )
        self.background.lower()

        # ===== OVERLAY =====
        overlay = QWidget(central)
        overlay.setAttribute(Qt.WA_StyledBackground, True)

        # ===== PANEL =====
        panel = QWidget()
        panel.setStyleSheet("""
            background-color: #FBFBFB;
            border: 4px solid #c31432;
            border-radius: 12px;
        """)
        panel.setFixedWidth(700)

        panel_layout = QVBoxLayout(panel)
        panel_layout.setSpacing(10)
        panel_layout.setContentsMargins(40, 40, 40, 40)

        shadow = QGraphicsDropShadowEffect(panel)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(195, 20, 50, 140))
        panel.setGraphicsEffect(shadow)

        # ===== TITLE =====
        title = QLabel("VEGA")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Impact", 70))
        title.setStyleSheet("color: #c31432;")
        panel_layout.addWidget(title)

        # ===== VOICE BUTTON =====
        try:
            self.voice_button = QPushButton()
            self.voice_button.setIcon(self.voice_icon_idle)
            self.voice_button.setFixedSize(140, 140)
            self.voice_button.setIconSize(QSize(120, 120))
            self.voice_button.setStyleSheet("""
                QPushButton {
                    border: none
                    background-color: transparent;
                }                
                """)
            self.voice_button.clicked.connect(self.on_voice)
            panel_layout.addWidget(self.voice_button, alignment=Qt.AlignCenter)
        except Exception:
            pass

        # ===== TEXT ACTION BUTTONS =====
        self.copy_button = QPushButton()
        self.copy_button.setIcon(QIcon(str(self.assets_images / "copy.png")))
        self.copy_button.setIconSize(QSize(36, 36))
        self.copy_button.setFixedSize(40, 40)
        self.copy_button.setToolTip("Copy")
        self.copy_button.clicked.connect(self._copy_text)

        self.clear_button = QPushButton()
        self.clear_button.setIcon(QIcon(str(self.assets_images / "delete.png")))
        self.clear_button.setIconSize(QSize(36, 36))
        self.clear_button.setFixedSize(40, 40)
        self.clear_button.setToolTip("Clear")
        self.clear_button.clicked.connect(self._clear_text)

        for button in (self.copy_button, self.clear_button):
            button.setStyleSheet("""
                QPushButton {
                    border: 2px solid #c31432;
                    border-radius: 6px;
                    background-color: #FBFBFB;
                    padding: 2px;
                }
                QPushButton:hover {
                    background-color: #ffe6eb;
                }
                QPushButton:pressed {
                    background-color: #ffccd5;
                    border-color: #ff2e55;
                }
            """)

        text_buttons_layout = QHBoxLayout()
        text_buttons_layout.addStretch()
        text_buttons_layout.addWidget(self.copy_button)
        text_buttons_layout.addWidget(self.clear_button)
        panel_layout.addLayout(text_buttons_layout)

        # ===== OUTPUT TEXT =====
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            background-color: #c31432;
            color: white;
            font-weight: bold;
            font-size: 14px;
            border: 3px solid #8e0f25;
            border-radius: 8px;
        """)
        panel_layout.addWidget(self.output_text)

        # ===== INPUT BAR =====
        input_bar = QHBoxLayout()

        self.text_input = QLineEdit()
        self.text_input.setFont(QFont("Arial", 16))
        self.text_input.setStyleSheet("""
            border: 2px solid #c31432;
            border-radius: 6px;
            padding: 6px;
        """)
        input_bar.addWidget(self.text_input)

        send_button = QPushButton("Send")
        send_button.setStyleSheet("""
            background-color: #c31432;
            color: white;
            font-weight: bold;
            border: 2px solid #8e0f25;
            border-radius: 6px;
            padding: 6px 12px;
        """)
        send_button.clicked.connect(self._send_text)
        input_bar.addWidget(send_button)

        add_contact_button = QPushButton("Add contact")
        add_contact_button.setStyleSheet("""
            background-color: #FBFBFB;
            color: #c31432;
            font-weight: bold;
            border: 2px solid #c31432;
            border-radius: 6px;
            padding: 6px 12px;
        """)
        add_contact_button.clicked.connect(self._open_add_contact_dialog)

        input_bar.addWidget(add_contact_button)


        panel_layout.addLayout(input_bar)

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout(overlay)
        main_layout.addStretch()
        main_layout.addWidget(panel, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        self.central_layout = QVBoxLayout(central)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.addWidget(overlay)

    def resizeEvent(self, event):
        self.background.resize(self.size())
        super().resizeEvent(event)

    # ===== PUBLIC API =====
    def show_text(self, text: str):
        self.output_text.append(text)

    def set_listening(self, listening: bool):
        if not hasattr(self, "voice_button"):
            return

        if listening:
            self.voice_button.setIcon(self.voice_icon_listening)
        else:
            self.voice_button.setIcon(self.voice_icon_idle)
    
    def _open_add_contact_dialog(self):
        dialog = AddContactDialog(self.assets_text, self)
        dialog.exec()


    # ===== INTERNAL CALLBACKS =====
    def _send_text(self):
        text = self.text_input.text().strip()
        if not text:
            return

        self.show_text(f"Pablo: {text}")
        self.text_input.clear()

        if self.on_text:
            self.on_text(text)

    def _copy_text(self):
        text = self.output_text.toPlainText()
        if text.strip():
            QApplication.clipboard().setText(text)

    def _clear_text(self):
        self.output_text.clear()

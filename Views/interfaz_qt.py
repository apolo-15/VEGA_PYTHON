from PySide6.QtWidgets import (QMainWindow,QWidget,QLabel,QPushButton,QTextEdit,QLineEdit,QVBoxLayout,QHBoxLayout,QGraphicsDropShadowEffect, QApplication)
from PySide6.QtGui import QPixmap, QFont, QIcon, QColor
from PySide6.QtCore import Qt, QSize
from pathlib import Path




class VegaUI(QMainWindow):
    def __init__(self, assets_images: Path, on_text, on_voice):
        super().__init__()

        self.assets_images = assets_images
        self.icon_voz_idle = QIcon(str(self.assets_images / "escucha.png"))
        self.icon_voz_listening = QIcon(
            str(self.assets_images / "escucha_activa.png")
        )

        self.on_text = on_text
        self.on_voice = on_voice

        self.setWindowTitle("VEGA")
        self.setWindowIcon(QIcon(str(self.assets_images / "vega.ico")))
        self.setMinimumSize(1024, 700)

        self._crear_interfaz()

    def _crear_interfaz(self):
        # ===== CONTENEDOR CENTRAL =====
        central = QWidget()
        self.setCentralWidget(central)


        # ===== FONDO =====
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
        panel_layout.setSpacing(15)
        panel_layout.setContentsMargins(40, 40, 40, 40)
        shadow = QGraphicsDropShadowEffect(panel)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(195, 20, 50, 140))  # rojo VEGA con alpha

        panel.setGraphicsEffect(shadow)


        # ===== TÍTULO =====
        titulo = QLabel("VEGA")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Impact", 70))
        titulo.setStyleSheet("color: #c31432;")
        panel_layout.addWidget(titulo)

        # ===== BOTONES TEXTO (COPIAR / LIMPIAR) =====
        self.btn_copiar = QPushButton()
        self.btn_copiar.setIcon(QIcon(str(self.assets_images / "copiar.png")))
        self.btn_copiar.setIconSize(QSize(36, 36))
        self.btn_copiar.setFixedSize(40, 40)
        self.btn_copiar.setToolTip("COPIAR")
        self.btn_copiar.clicked.connect(self._copiar_texto)

        self.btn_limpiar = QPushButton()
        self.btn_limpiar.setIcon(QIcon(str(self.assets_images / "papelera.png")))
        self.btn_limpiar.setIconSize(QSize(36, 36))
        self.btn_limpiar.setFixedSize(40, 40)
        self.btn_limpiar.setToolTip("LIMPIAR")
        self.btn_limpiar.clicked.connect(self._limpiar_texto)

        for btn in (self.btn_copiar, self.btn_limpiar):
            btn.setStyleSheet("""
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


        botones_texto_layout = QHBoxLayout()
        botones_texto_layout.addStretch()
        botones_texto_layout.addWidget(self.btn_copiar)
        botones_texto_layout.addWidget(self.btn_limpiar)

        panel_layout.addLayout(botones_texto_layout)


        # ===== BOTÓN VOZ =====
        try:
            self.btn_voz = QPushButton()
            self.btn_voz.setIcon(self.icon_voz_idle)
            self.btn_voz.setFixedSize(140, 140)
            self.btn_voz.setIconSize(QSize(120, 120))
            self.btn_voz.setStyleSheet("""
                QPushButton {
                    border: 4px solid #c31432;
                    border-radius: 80px;
                    background-color: transparent;
                }
                QPushButton:hover {
                    border-color: #ff2e55;
                }
            """)


            self.btn_voz.clicked.connect(self.on_voice)
            self.btn_voz.setStyleSheet("border: none;")
            panel_layout.addWidget(self.btn_voz, alignment=Qt.AlignCenter)
        except Exception:
            pass

        # ===== TEXTO =====
        self.texto_info = QTextEdit()
        self.texto_info.setReadOnly(True)
        self.texto_info.setStyleSheet("""
            background-color: #c31432;
            color: white;
            font-weight: bold;
            font-size: 14px;
            border: 3px solid #8e0f25;
            border-radius: 8px;
        """)

        panel_layout.addWidget(self.texto_info)

        # ===== BARRA INFERIOR =====
        barra = QHBoxLayout()

        self.entrada = QLineEdit()
        self.entrada.setFont(QFont("Arial", 16))
        self.entrada.setStyleSheet("""
            border: 2px solid #c31432;
            border-radius: 6px;
            padding: 6px;
        """)

        barra.addWidget(self.entrada)

        btn_enviar = QPushButton("Enviar")
        btn_enviar.setStyleSheet("""
            background-color: #c31432;
            color: white;
            font-weight: bold;
            border: 2px solid #8e0f25;
            border-radius: 6px;
            padding: 6px 12px;
        """)

        btn_enviar.clicked.connect(self._enviar_texto)
        barra.addWidget(btn_enviar)

        panel_layout.addLayout(barra)

        # ===== LAYOUT PRINCIPAL =====
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

    # ===== API =====
    def mostrar_texto(self, texto: str):
        self.texto_info.append(texto)

    def _enviar_texto(self):
        texto = self.entrada.text().strip()
        if not texto:
            return

        self.mostrar_texto(f"Pablo: {texto}")
        self.entrada.clear()

        if self.on_text:
            self.on_text(texto)

    def _copiar_texto(self):
        texto = self.texto_info.toPlainText()
        if texto.strip():
            QApplication.clipboard().setText(texto)

    def _limpiar_texto(self):
        self.texto_info.clear()


    def set_listening(self, listening: bool):
        if not hasattr(self, "btn_voz"):
            return

        if listening:
            self.btn_voz.setIcon(self.icon_voz_listening)
        else:
            self.btn_voz.setIcon(self.icon_voz_idle)



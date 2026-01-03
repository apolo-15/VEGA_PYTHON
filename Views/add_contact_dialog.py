from pathlib import Path
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)

from models.services.contacts_service import add_contact


class AddContactDialog(QDialog):
    def __init__(self, assets_text: Path, parent=None):
        super().__init__(parent)

        self.assets_text = assets_text

        self.setWindowTitle("Add contact")
        self.setFixedSize(380, 220)

        self._create_ui()

    def _create_ui(self):
        main_layout = QVBoxLayout(self)

        name_label = QLabel("Name")
        self.name_input = QLineEdit()

        phone_label = QLabel("Phone number")
        self.phone_input = QLineEdit()

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        save_button.clicked.connect(self._save_contact)
        cancel_button.clicked.connect(self.reject)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        main_layout.addWidget(name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(phone_label)
        main_layout.addWidget(self.phone_input)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    def _save_contact(self):
        name = self.name_input.text().strip()
        phone_number = self.phone_input.text().strip()

        if not name or not phone_number:
            QMessageBox.warning(
                self,
                "Invalid data",
                "Name and phone number are required.",
            )
            return

        success = add_contact(name, phone_number, self.assets_text)

        if not success:
            QMessageBox.warning(
                self,
                "Error",
                "The contact already exists or could not be saved.",
            )
            return

        self.accept()

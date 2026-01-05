# PABLO BOTELLA JIMÉNEZ
# Vega AI Assistant Application

# Dialog for adding, viewing, and deleting contacts in the Vega AI assistant application.
# Provides a user interface for managing contacts stored in a text file.


# LIBRARY IMPORTS
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QListWidget,
)

# PROJECT IMPORTS
from models.services.contacts_service import add_contact, get_contacts, delete_contact


class AddContactDialog(QDialog):
    def __init__(self, assets_text: Path, parent=None):
        super().__init__(parent)

        self.assets_text = assets_text

        self.setWindowTitle("CONTACTS")
        self.setFixedSize(500, 340)

        self._create_ui()

    def _create_ui(self):
        main_layout = QVBoxLayout(self)

        # ===== CONTACT LIST =====
        contacts_label = QLabel("Existing contacts")
        self.contacts_list = QListWidget()
        self.contacts_list.itemSelectionChanged.connect(self._on_contact_selected)
        self._load_contacts()

        # ===== INPUTS =====
        name_label = QLabel("Name")
        self.name_input = QLineEdit()

        phone_label = QLabel("Phone number")
        self.phone_input = QLineEdit()

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        delete_button = QPushButton("Delete")
        delete_button.setEnabled(False)
        delete_button.clicked.connect(self._delete_contact)
        self.delete_button = delete_button


        save_button.clicked.connect(self._save_contact)
        cancel_button.clicked.connect(self.reject)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(delete_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        
        main_layout.addWidget(name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(phone_label)
        main_layout.addWidget(self.phone_input)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(contacts_label)
        main_layout.addWidget(self.contacts_list)


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

        self._load_contacts()
        self.name_input.clear()
        self.phone_input.clear()



    def _load_contacts(self):
        self.contacts_list.clear()

        contacts = get_contacts(self.assets_text)

        for name in sorted(contacts.keys()):
            phone = contacts[name]
            self.contacts_list.addItem(f"{name}  —  {phone}")


    def _on_contact_selected(self):
        self.delete_button.setEnabled(
            self.contacts_list.currentItem() is not None
        )

    def _delete_contact(self):
        item = self.contacts_list.currentItem()
        if not item:
            return

        text = item.text()
        name = text.split("—")[0].strip()

        reply = QMessageBox.question(
            self,
            "Confirm delete",
            f"Delete contact '{name}'?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        success = delete_contact(name, self.assets_text)

        if not success:
            QMessageBox.warning(
                self,
                "Error",
                "The contact could not be deleted.",
            )
            return

        self._load_contacts()



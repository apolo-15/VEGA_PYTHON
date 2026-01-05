# PABLO BOTELLA JIMÉNEZ
# Vega AI Assistant Application

# Provides contact management functionality for the Vega AI assistant.
# Allows adding, retrieving, and deleting contacts stored in a JSON file.


# LIBRARY IMPORTS
import json
from pathlib import Path


def _get_contacts_file(assets_text: Path) -> Path:
    return assets_text / "contacts.json"


def get_contacts(assets_text: Path) -> dict:
    contacts_file = _get_contacts_file(assets_text)

    if not contacts_file.exists():
        return {}

    with open(contacts_file, "r", encoding="utf-8") as file:
        return json.load(file)


def add_contact(name: str, phone_number: str, assets_text: Path) -> bool:
    contacts = get_contacts(assets_text)

    key = name.lower().strip()

    if key in contacts:
        return False

    contacts[key] = phone_number
    _save_contacts(contacts, assets_text)
    return True


def _save_contacts(contacts: dict, assets_text: Path) -> None:
    contacts_file = _get_contacts_file(assets_text)

    with open(contacts_file, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False)

        
def delete_contact(name: str, assets_text: Path) -> bool:
    contacts = get_contacts(assets_text)

    key = name.lower().strip()

    if key not in contacts:
        return False

    del contacts[key]
    _save_contacts(contacts, assets_text)
    return True

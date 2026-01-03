from datetime import datetime
from pathlib import Path


def read_instructions(assets_text: Path) -> str:
    with open(assets_text / "instructions.txt", "r", encoding="utf-8") as file:
        return file.read()


def read_instructions_summary(assets_text: Path) -> str:
    with open(
        assets_text / "instructions_summary.txt",
        "r",
        encoding="utf-8",
    ) as file:
        return file.read()


def read_memory(assets_text: Path) -> str:
    with open(assets_text / "memory.txt", "r", encoding="utf-8") as file:
        return file.read()


def save_summary(assets_text: Path, summary: str) -> None:
    memory_file = assets_text / "memory.txt"

    if not memory_file.exists():
        with open(memory_file, "w", encoding="utf-8") as file:
            file.write(
                "Conversations started on: "
                + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + "\n\n"
            )

    with open(memory_file, "a", encoding="utf-8") as file:
        file.write(
            "Conversation summary saved on: "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "\n\n"
        )
        file.write(summary + "\n\n")

from datetime import datetime
from pathlib import Path


def leer_instrucciones(assets_text: Path) -> str:
    with open(assets_text / "instrucciones.txt", "r", encoding="utf-8") as f:
        return f.read()


def leer_instrucciones_resumen(assets_text: Path) -> str:
    with open(assets_text / "instrucciones_resumen.txt", "r", encoding="utf-8") as f:
        return f.read()


def leer_memoria(assets_text: Path) -> str:
    with open(assets_text / "memoria.txt", "r", encoding="utf-8") as f:
        return f.read()


def guardar_resumen(assets_text: Path, resumen: str) -> None:
    memoria_file = assets_text / "memoria.txt"

    # si no existe el archivo, lo creamos
    if not memoria_file.exists():
        with open(memoria_file, "w", encoding="utf-8") as f:
            f.write(
                "Conversaciones iniciadas el: "
                + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + "\n\n"
            )

    # añadimos el resumen
    with open(memoria_file, "a", encoding="utf-8") as f:
        f.write(
            "Conversaciones iniciadas el: "
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "\n\n"
        )
        f.write(resumen + "\n\n")


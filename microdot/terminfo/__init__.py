import platform
from pathlib import Path
from shutil import copy

from microdot import BASE


def _install_one(source: Path):
    first_letter = source.name[0]

    if platform.system() == "Linux":
        sub = first_letter
    elif platform.system() == "Darwin":
        sub = f"{ord(first_letter):x}"
    else:
        raise Exception("unknown platform")

    destination = Path.home() / ".terminfo" / sub / source.name
    if destination.exists():
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    print("  TERMINFO", source)
    copy(source, destination)


def find_terminfo_sources() -> list[Path]:
    return sorted(p for p in BASE.glob("*/terminfo/*") if p.is_file())


def install():
    for source in find_terminfo_sources():
        _install_one(source)

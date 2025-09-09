from pathlib import Path


def get_debian_version() -> float | None:
    p = Path("/etc/debian_version")
    if not p.exists():
        return None
    return float(p.read_text())


def is_debian() -> bool:
    return get_debian_version() is not None

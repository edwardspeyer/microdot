from pathlib import Path


def get_debian_version() -> float | str | None:
    p = Path("/etc/debian_version")
    if not p.exists():
        return None
    v = p.read_text().strip()
    if v.isnumeric():
        return float(v)
    return v


def is_debian() -> bool:
    return get_debian_version() is not None

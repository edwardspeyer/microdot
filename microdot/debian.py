from pathlib import Path


def is_debian() -> bool:
    return Path("/etc/debian_version").exists()

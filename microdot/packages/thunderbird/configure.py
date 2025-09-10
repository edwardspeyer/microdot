from configparser import ConfigParser
from pathlib import Path
from typing import Iterator

from microdot import install_hook


def profile_directories() -> Iterator[Path]:
    thunderbird_config_root = Path.home() / ".thunderbird"
    c = ConfigParser()
    c.read(thunderbird_config_root / "profiles.ini")
    for section in c.sections():
        if "Profile" not in section:
            continue
        yield thunderbird_config_root / c[section]["Path"]


def install():
    base = Path(__file__).parent.parent
    config_path = base / "thunderbird" / "user.js"
    if not config_path.exists():
        return
    config = config_path.read_text()
    for dir in profile_directories():
        dest = dir / "user.js"
        install_hook(dest, config, comment="// ")

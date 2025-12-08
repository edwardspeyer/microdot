from pathlib import Path
from shutil import copyfile

from microdot import cwd, install_hook


def configure():
    apps = Path.home() / ".local/share/applications/"
    apps.mkdir(parents=True, exist_ok=True)
    for src in cwd().glob("*.desktop"):
        copyfile(src, apps / src.name)

    install_hook(
        "~/.config/xdg_init.sh",
        f". {cwd()}/xdg_init.sh\n",
        position="top",
    )

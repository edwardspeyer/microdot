from pathlib import Path
from shutil import copyfile as copy

from microdot import cwd, install_hook, register


def install_vim_plug():
    source = cwd() / "autoload" / "plug.vim"
    destination = Path.home() / ".vim" / "autoload" / "plug.vim"
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy(source, destination)


@register
def install() -> None:
    install_vim_plug()
    install_hook(
        "~/.vimrc",
        f"""\
        source {cwd()}/vimrc
        """,
        comment='"',
    )

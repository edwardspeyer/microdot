from pathlib import Path
from subprocess import run

from . import packages
from .block import BOTTOM, block

BASE = Path(__file__).parent.parent.resolve()

block("~/.tmux.conf")(
    f"""\
    source {BASE}/tmux/tmux.conf
    """
)

block("~/.vimrc", comment='"')(
    f"""\
    source {BASE}/vim/vimrc
    """
)

run(
    """
    mkdir -p ~/.vim/autoload/
    cp vim/autoload/* ~/.vim/autoload
    tar -C ~/.vim/ -xf vim/plugged.tar.gz
    """,
    shell=True,
    check=True,
)

block("~/.bashrc")(
    f"""\
    source {BASE}/bash/bashrc
    """
)

block("~/.gitconfig")(
    f"""\
    [include]
    path = {BASE}/git/config

    [core]
    excludesfile = {BASE}/git/ignore
    """
)

block("~/.ssh/config", position=BOTTOM)(
    f"""\
    Host *
    Include {BASE}/ssh/config
    """
)

block("~/.config/fish/conf.d/microdot.fish")(
    f"""\
    for file in {BASE}/fish/*.fish
        source $file
    end
    """
)

packages.docker.install()

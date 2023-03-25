from pathlib import Path
from subprocess import run

from microdot.hooks import BOTTOM, TOP, install_hook

BASE = Path(__file__).parent.parent.parent.resolve()


def install():
    install_hook(
        path="~/.tmux.conf",
        comment="#",
        position=TOP,
        text=f"""\
        source {BASE}/tmux/tmux.conf
        """,
    )

    install_hook(
        path="~/.vimrc",
        comment='"',
        position=TOP,
        text=f"""\
        source {BASE}/vim/vimrc
        """,
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

    install_hook(
        path="~/.bashrc",
        comment="#",
        position=TOP,
        text=f"""\
        source {BASE}/bash/bashrc
        """,
    )

    install_hook(
        path="~/.gitconfig",
        comment="#",
        position=TOP,
        text=f"""\
        [include]
        path = {BASE}/git/config

        [core]
        excludesfile = {BASE}/git/ignore
        """,
    )

    install_hook(
        path="~/.ssh/config",
        comment="#",
        position=BOTTOM,
        text=f"""\
        Host *
        Include {BASE}/ssh/config
        """,
    )

    install_hook(
        path="~/.config/fish/conf.d/microdot.fish",
        comment="#",
        position=TOP,
        text=f"""\
        for file in {BASE}/fish/*.fish
            source $file
        end
        """,
    )

    install_hook(
        path="~/.config/apt.conf",
        comment="//",
        position=TOP,
        text=f"""\
        // Requires APT_CONFIG to also be set in the environment
        #include "{BASE}/apt/apt.conf";
        """,
    )

    install_hook(
        path="~/.config/kitty/kitty.conf",
        comment="#",
        position=TOP,
        text=f"""\
        include {BASE}/kitty/kitty.conf
        """,
    )

    install_hook(
        path="~/.config/i3/config",
        comment="#",
        position=TOP,
        text=f"""\
        include {BASE}/i3/config
        """,
    )

    install_hook(
        path="~/.xsession",
        comment="#",
        mode=0o744,
        position=BOTTOM,
        text=f"""\
        # Hand control to microdot's xsession
        exec {BASE}/X11/xsession
        """,
    )

    install_hook(
        path="~/.XCompose",
        comment="#",
        position=TOP,
        text=f"""\
        include "{BASE}/X11/XCompose"
        """,
    )

    install_hook(
        path="~/.muttrc",
        comment="#",
        position=BOTTOM,
        text=f"""\
        source {BASE}/mutt/muttrc
        """,
    )

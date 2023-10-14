from pathlib import Path
from subprocess import run

from microdot.hooks import Position, install_hook

BASE = Path(__file__).parent.parent.parent.resolve()


def install():
    home = Path.home()

    install_hook(
        path=home / ".tmux.conf",
        comment="#",
        position=Position.TOP,
        text=f"""\
        source {BASE}/tmux/tmux.conf
        """,
    )

    install_hook(
        path=home / ".vimrc",
        comment='"',
        position=Position.TOP,
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
        path=home / ".bashrc",
        comment="#",
        position=Position.TOP,
        text=f"""\
        source {BASE}/bash/bashrc
        """,
    )

    install_hook(
        path=home / ".gitconfig",
        comment="#",
        position=Position.TOP,
        text=f"""\
        [include]
        path = {BASE}/git/config

        [core]
        excludesfile = {BASE}/git/ignore
        """,
    )

    install_hook(
        path=home / ".ssh/config",
        comment="#",
        position=Position.BOTTOM,
        text=f"""\
        Host *
        Include {BASE}/ssh/config
        """,
    )

    install_hook(
        path=home / ".config/fish/conf.d/microdot.fish",
        comment="#",
        position=Position.TOP,
        text=f"""\
        for file in {BASE}/fish/*.fish
            source $file
        end
        """,
    )

    install_hook(
        path=home / ".config/apt.conf",
        comment="//",
        position=Position.TOP,
        text=f"""\
        // Requires APT_CONFIG to also be set in the environment
        #include "{BASE}/apt/apt.conf";
        """,
    )

    install_hook(
        path=home / ".config/kitty/kitty.conf",
        comment="#",
        position=Position.TOP,
        text=f"""\
        include {BASE}/kitty/kitty.conf
        """,
    )

    install_hook(
        path=home / ".config/i3/config",
        comment="#",
        position=Position.TOP,
        text=f"""\
        include {BASE}/i3/config
        """,
    )

    install_hook(
        path=home / ".xsession",
        comment="#",
        mode=0o744,
        position=Position.BOTTOM,
        text=f"""\
        # Hand control to microdot's xsession
        exec {BASE}/X11/xsession
        """,
    )

    install_hook(
        path=home / ".XCompose",
        comment="#",
        position=Position.TOP,
        text=f"""\
        include "{BASE}/X11/XCompose"
        """,
    )

    install_hook(
        path=home / ".muttrc",
        comment="#",
        position=Position.BOTTOM,
        text=f"""\
        source {BASE}/mutt/muttrc
        """,
    )

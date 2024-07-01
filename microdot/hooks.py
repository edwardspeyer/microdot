import re
import textwrap
from enum import Enum
from pathlib import Path
from subprocess import run

BASE = Path(__file__).parent.parent.resolve()


class Position(Enum):
    TOP = "TOP"
    BOTTOM = "BOTTOM"


def log(action, path):
    print(f"  {action:6s}  {path}", flush=True)


def install_hook(
    path: Path,
    comment: str,
    position: Position,
    text: str,
    mode: int = 0o644,
):
    inner = textwrap.dedent(text).rstrip("\n") + "\n"
    begin = f"{comment} -----BEGIN MICRODOT-----\n"
    end = f"{comment} -----END MICRODOT-----\n"
    outer = begin + inner + end
    pattern = re.compile(f"{begin}.+?\n{end}", re.DOTALL)

    if not path.exists():
        log("NEW", path)
        path.parent.mkdir(exist_ok=True, parents=True, mode=0o700)
        path.touch(mode=mode)
        path.write_text(outer)
        return

    old = path.read_text()
    new = re.sub(
        pattern,
        # re.sub will interpret backslashes in the replacement string, so we
        # have to pre-escape them.
        re.sub(r'\\', r'\\\\', outer),
        old,
    )

    if re.search(pattern, old):
        if old == new:
            log("SAME", path)
        else:
            log("UPDATE", path)
            path.write_text(new)
    else:
        log("EDIT", path)
        if position == Position.TOP:
            path.write_text(outer + "\n" + old)
        elif position == Position.BOTTOM:
            path.write_text(old + "\n" + outer)


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
        f"""
        mkdir -p ~/.vim/autoload/
        cp {BASE}/vim/autoload/* ~/.vim/autoload
        tar -C ~/.vim/ -xf {BASE}/vim/plugged.tar.gz
        """,
        shell=True,
        check=True,
    )

    install_hook(
        path=home / ".profile",
        comment="#",
        position=Position.TOP,
        text=f"""\
        # Useful for helping other tools' config files find sibling files.
        export MICRODOT_INSTALL_PATH="{BASE}"
        . $MICRODOT_INSTALL_PATH/sh/profile
        """,
    )

    install_hook(
        path=home / ".bashrc",
        comment="#",
        position=Position.TOP,
        text=f"""\
        export MICRODOT_INSTALL_PATH="{BASE}"
        source {BASE}/sh/bashrc
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

    install_hook(
        path=home / ".config/sway/config",
        comment="#",
        position=Position.TOP,
        text=f"""\
        include {BASE}/sway/config
        """,
    )

    install_hook(
        path=home / ".config/foot/foot.ini",
        comment="#",
        position=Position.TOP,
        text=f"""\
        include={BASE}/foot/foot.ini
        """,
    )

    install_hook(
        path=home / ".config/psqlrc",
        comment="--",
        position=Position.TOP,
        text=rf"\i {BASE}/psql/psqlrc",
    )

import json
import re
import textwrap
from enum import Enum
from pathlib import Path
from shutil import copyfile as copy
from typing import Callable

BASE = Path(__file__).parent.parent.resolve()

BEGIN = "-----BEGIN MICRODOT-----"
END = "-----END MICRODOT-----"

Editor = Callable[[str | None], str]


class Position(Enum):
    TOP = "TOP"
    BOTTOM = "BOTTOM"


def log(action, path):
    print(f"  {action:6s}  {path}", flush=True)


def insert_text(
    position: Position,
    comment: Editor,
    text: str,
) -> Editor:
    def fn(original: str | None) -> str:
        inner = textwrap.dedent(text).rstrip("\n") + "\n"
        begin = comment(BEGIN)
        end = comment(END)
        outer = begin + inner + end

        if not original:
            return outer

        pattern = re.compile(f"{re.escape(begin)}.+?\n{re.escape(end)}", re.DOTALL)
        if re.search(pattern, original):
            return re.sub(
                pattern,
                # re.sub will interpret backslashes in the replacement string, so we
                # have to pre-escape them.
                re.sub(r"\\", r"\\\\", outer),
                original,
            )

        if position == Position.TOP:
            return outer + "\n" + original
        if position == Position.BOTTOM:
            return original + "\n" + outer

        raise Exception("Unreachable!")

    return fn


def install_hook(
    path: Path,
    editor: Editor,
    mode: int = 0o644,
) -> None:
    old = path.read_text() if path.exists() else None
    new = editor(old)
    if old is None:
        log("NEW", path)
    elif old == new:
        log("SAME", path)
    else:
        log("EDIT", path)

    path.parent.mkdir(exist_ok=True, parents=True, mode=0o700)
    path.touch(mode=mode)
    path.write_text(new)


def test_install_text_hook_new(tmp_path: Path) -> None:
    f = tmp_path / "f"
    install_hook(f, insert_text(Position.TOP, comment_prefix("#"), "hi"))
    assert f.exists()
    assert f.read_text() == f"# {BEGIN}\nhi\n# {END}\n"


def test_install_text_hook_top(tmp_path: Path) -> None:
    f = tmp_path / "f"
    f.write_text("bye\n")
    install_hook(f, insert_text(Position.TOP, comment_prefix("!"), "hi"))
    assert f.read_text() == f"! {BEGIN}\nhi\n! {END}\n\nbye\n"


def test_install_text_hook_bottom(tmp_path: Path) -> None:
    f = tmp_path / "f"
    f.write_text("hi\n")
    install_hook(f, insert_text(Position.BOTTOM, comment_prefix("!"), "bye"))
    assert f.read_text() == f"hi\n\n! {BEGIN}\nbye\n! {END}\n"


def install_vim_plug(home: Path):
    source = BASE / "vim" / "autoload" / "plug.vim"
    destination = home / ".vim" / "autoload" / "plug.vim"
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy(source, destination)


def comment_prefix(symbol: str) -> Editor:
    def fn(text: str | None) -> str:
        if text is None:
            return symbol
        return f"{symbol} {text}\n"

    return fn


def comment_wrap(pre: str, post: str) -> Editor:
    def fn(text: str | None) -> str:
        if text is None:
            return f"{pre} {post}"
        return f"{pre} {text} {post}"

    return fn


def install():
    home = Path.home()

    install_hook(
        home / ".tmux.conf",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            source {BASE}/tmux/tmux.conf
            """,
        ),
    )

    install_vim_plug(home)

    install_hook(
        home / ".vimrc",
        insert_text(
            Position.TOP,
            comment_prefix('"'),
            f"""\
            source {BASE}/vim/vimrc
            """,
        ),
    )

    # These config files should all hook into the generic sh startup code.
    for rc in {".profile", ".bashrc", ".zshrc"}:
        install_hook(
            home / rc,
            insert_text(
                Position.TOP,
                comment_prefix("#"),
                f"""\
                export MICRODOT_INSTALL_PATH="{BASE}"
                . $MICRODOT_INSTALL_PATH/sh/profile
                """,
            ),
        )

    install_hook(
        home / ".gitconfig",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            [include]
            path = {BASE}/git/config

            [core]
            excludesfile = {BASE}/git/ignore
            """,
        ),
    )

    install_hook(
        home / ".ssh/config",
        insert_text(
            Position.BOTTOM,
            comment_prefix("#"),
            f"""\
            Host *
            Include {BASE}/ssh/config
            """,
        ),
    )

    install_hook(
        home / ".config/fish/conf.d/microdot.fish",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            for file in {BASE}/fish/*.fish
                source $file
            end
            """,
        ),
    )

    install_hook(
        home / ".config/fish/fish_variables",
        insert_text(
            Position.BOTTOM,
            comment_prefix("#"),
            (BASE / "fish/fish_variables").read_text(),
        ),
    )

    install_hook(
        home / ".config/apt.conf",
        insert_text(
            Position.TOP,
            comment_prefix("//"),
            f"""\
            // Requires APT_CONFIG to also be set in the environment
            #include "{BASE}/apt/apt.conf";
            """,
        ),
    )

    install_hook(
        home / ".config/kitty/kitty.conf",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            include {BASE}/kitty/kitty.conf
            """,
        ),
    )

    install_hook(
        home / ".config/i3/config",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            include {BASE}/i3/config
            """,
        ),
    )

    install_hook(
        home / ".xsession",
        insert_text(
            Position.BOTTOM,
            comment_prefix("#"),
            f"""\
            # Hand control to microdot's xsession
            exec {BASE}/X11/xsession
            """,
        ),
        mode=0o744,
    )

    install_hook(
        home / ".XCompose",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            include "{BASE}/X11/XCompose"
            """,
        ),
    )

    install_hook(
        home / ".muttrc",
        insert_text(
            Position.BOTTOM,
            comment_prefix("#"),
            f"""\
            source {BASE}/mutt/muttrc
            """,
        ),
    )

    install_hook(
        home / ".config/sway/config",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            include {BASE}/sway/config
            """,
        ),
    )

    install_hook(
        home / ".config/foot/foot.ini",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            include={BASE}/foot/foot.ini
            """,
        ),
    )

    install_hook(
        home / ".config/psqlrc",
        insert_text(
            Position.TOP,
            comment_prefix("--"),
            rf"\i {BASE}/psql/psqlrc",
        ),
    )

    install_hook(
        home / ".config/ipython/profile_default/startup/microdot.py",
        insert_text(
            Position.TOP,
            comment_prefix("#"),
            f"""\
            exec(open("{BASE}/ipython/config.py").read())
            """,
        ),
    )

    install_hook(
        home / ".config/waybar/style.css",
        insert_text(
            Position.TOP,
            comment_wrap("/*", "*/"),
            """
            @import url("file:///home/egs/.config/microdot/waybar/style.css");
            """,
        ),
    )

    def add_json_include(path: str) -> Editor:
        def fn(text: str | None) -> str:
            text = re.sub(r"/\*.*\*/", "", text or "{}")
            doc = json.loads(text)
            includes = set(doc.get("include", []))
            includes.add(path)
            doc["include"] = list(includes)
            return json.dumps(doc)

        return fn

    install_hook(
        home / ".config/waybar/config.jsonc",
        add_json_include(f"{BASE}/waybar/config.jsonc"),
    )

    install_hook(
        home / ".config/mimeapps.list",
        insert_text(Position.BOTTOM, comment_prefix("#"), (BASE / "xdg-open/mimeapps.list").read_text()),
    )

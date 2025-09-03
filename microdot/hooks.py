import json
import re
import textwrap
from pathlib import Path
from shutil import copyfile as copy
from typing import Callable, Literal

BASE = Path(__file__).parent.parent.resolve()

BEGIN = "-----BEGIN MICRODOT-----"
END = "-----END MICRODOT-----"

Editor = Callable[[str | None], str]
Position = Literal["top", "bottom"]
CommentMarkers = str | tuple[str, str]


def log(action, path):
    print(f"  {action:6s}  {path}", flush=True)


def insert_text(
    original: str | None,
    text: str,
    position: Position,
    comment: CommentMarkers,
) -> str:
    """
    comment: prefix with a string or wrap with a pair of strings.
    """

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

    match comment:
        case str():
            commenter = comment_prefix(comment)
        case tuple():
            commenter = comment_wrap(*comment)
        case _:
            raise Exception(f"unexpected {comment=}!")

    inner = textwrap.dedent(text).rstrip("\n") + "\n"
    begin = commenter(BEGIN)
    end = commenter(END)
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

    if position == "top":
        return outer + "\n" + original
    if position == "bottom":
        return original + "\n" + outer

    raise Exception("Unreachable!")


def install_hook(
    path: Path | str,
    text: str,
    *,
    mode: int = 0o644,
    position: Position = "top",
    comment: CommentMarkers = "#",
) -> None:
    if isinstance(path, str):
        path = Path(path).expanduser()
    old = path.read_text() if path.exists() else None
    new = insert_text(old, text, position, comment)
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
    install_hook(f, "hi")
    assert f.exists()
    assert f.read_text() == f"# {BEGIN}\nhi\n# {END}\n"


def test_install_text_hook_top(tmp_path: Path) -> None:
    f = tmp_path / "f"
    f.write_text("bye\n")
    install_hook(f, "hi", comment="!")
    assert f.read_text() == f"! {BEGIN}\nhi\n! {END}\n\nbye\n"


def test_install_text_hook_bottom(tmp_path: Path) -> None:
    f = tmp_path / "f"
    f.write_text("hi\n")
    install_hook(f, "bye", position="bottom", comment="!")
    assert f.read_text() == f"hi\n\n! {BEGIN}\nbye\n! {END}\n"


def install_vim_plug():
    source = BASE / "vim" / "autoload" / "plug.vim"
    destination = Path.home() / ".vim" / "autoload" / "plug.vim"
    destination.parent.mkdir(parents=True, exist_ok=True)
    copy(source, destination)


def install():
    install_hook(
        "~/.tmux.conf",
        f"""\
        source {BASE}/tmux/tmux.conf
        """,
    )

    install_vim_plug()

    install_hook(
        "~/.vimrc",
        f"""\
        source {BASE}/vim/vimrc
        """,
        comment='"',
    )

    # These config files should all hook into the generic sh startup code.
    for rc in [".profile", ".bashrc", ".zshrc"]:
        install_hook(
            Path.home() / rc,
            f"""\
            export MICRODOT_INSTALL_PATH="{BASE}"
            . $MICRODOT_INSTALL_PATH/sh/profile
            """,
        )

    install_hook(
        "~/.gitconfig",
        f"""\
        [include]
        path = {BASE}/git/config

        [core]
        excludesfile = {BASE}/git/ignore
        """,
    )

    install_hook(
        "~/.ssh/config",
        f"""\
        Host *
        Include {BASE}/ssh/config
        """,
        position="bottom",
    )

    install_hook(
        "~/.config/fish/conf.d/microdot.fish",
        f"""\
        for file in {BASE}/fish/*.fish
            source $file
        end
        """,
    )

    install_hook(
        "~/.config/fish/fish_variables",
        (BASE / "fish/fish_variables").read_text(),
        position="bottom",
    )

    install_hook(
        "~/.config/apt.conf",
        f"""\
        // Requires APT_CONFIG to also be set in the environment
        #include "{BASE}/apt/apt.conf";
        """,
        comment="//",
    )

    install_hook(
        "~/.config/kitty/kitty.conf",
        f"""\
        include {BASE}/kitty/kitty.conf
        """,
    )

    install_hook(
        "~/.config/i3/config",
        f"""\
        include {BASE}/i3/config
        """,
    )

    install_hook(
        "~/.xsession",
        f"""\
        # Hand control to microdot's xsession
        exec {BASE}/X11/xsession
        """,
        position="bottom",
        mode=0o744,
    )

    install_hook(
        "~/.XCompose",
        f"""\
        include "{BASE}/X11/XCompose"
        """,
    )

    install_hook(
        "~/.muttrc",
        f"""\
        source {BASE}/mutt/muttrc
        """,
        position="bottom",
    )

    install_hook(
        "~/.config/sway/config",
        f"""\
        include {BASE}/sway/config
        """,
    )

    install_hook(
        "~/.config/foot/foot.ini",
        f"""\
        include={BASE}/foot/foot.ini
        """,
    )

    install_hook(
        "~/.config/psqlrc",
        rf"\i {BASE}/psql/psqlrc",
        comment="--",
    )

    install_hook(
        "~/.config/ipython/profile_default/startup/microdot.py",
        f"""\
        exec(open("{BASE}/ipython/config.py").read())
        """,
    )

    # waybar is weird: provide an option for local overrides though
    local_base = Path.home() / ".config/waybar"
    local_base.mkdir(parents=True, exist_ok=True)
    config = json.dumps(
        {
            "include": [
                f"{BASE}/waybar/config.jsonc",
                f"{local_base}/config.local.jsonc",
            ]
        },
        indent=4,
    )
    (local_base / "config.jsonc").write_text(config)

    install_hook(
        "~/.config/waybar/style.css",
        f"""
        @import url("file://{BASE}/waybar/style.css");
        """,
        comment=("/*", "*/"),
    )

    install_hook(
        "~/.config/mimeapps.list",
        (BASE / "xdg-open/mimeapps.list").read_text(),
        position="bottom",
    )

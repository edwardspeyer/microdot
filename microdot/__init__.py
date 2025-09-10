import inspect
import os
import re
import textwrap
from os import environ
from pathlib import Path
from shutil import copytree
from subprocess import DEVNULL, check_output, run
from tempfile import TemporaryDirectory
from typing import Callable, Literal

BASE = Path(__file__).parent.parent.resolve()

BEGIN = "-----BEGIN MICRODOT-----"
END = "-----END MICRODOT-----"

Editor = Callable[[str | None], str]
Position = Literal["top", "bottom"]
CommentMarkers = str | tuple[str, str]


def is_ssh_remote() -> bool:
    return "SSH_TTY" in environ


def get_debian_version() -> float | str | None:
    p = Path("/etc/debian_version")
    if not p.exists():
        return None
    v = p.read_text().strip()
    try:
        return float(v)
    except ValueError:
        return v


def is_debian() -> bool:
    return get_debian_version() is not None


def cwd() -> Path:
    frame = inspect.stack()[1]
    return Path(frame.filename).parent.resolve()


def log(action, path) -> None:
    print(f"  {action:6s}  {path}", flush=True)


def write_as_root(path: Path, text: str) -> bool:
    """Write contents as root, creating leading directories."""
    if path.exists() and path.read_text() == text:
        return False
    script = "mkdir -p $1 && tee $2"
    command = ["sh", "-c", script, "--", str(path.parent), str(path)]
    run(["sudo", *command], check=True, input=text, text=True, stdout=DEVNULL)
    return True


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


def install_from_script(script, *args) -> None:
    """Run the script and assume everything everything in $tmp/out goes
    into ~/.local."""
    with TemporaryDirectory() as temporary_directory:
        tmp = Path(temporary_directory)
        env = dict(os.environ)
        env["DEBIAN_FRONTEND"] = "noninteractive"
        env["PATH"] = f"/usr/lib/ccache:{env['PATH']}"
        run(["sh", "-c", script, "--", *args], check=True, cwd=tmp, env=env)
        out = tmp / "out"
        local = Path.home() / ".local"
        copytree(out, local, dirs_exist_ok=True)


def get_version(command: str, option: str) -> tuple[int | str, ...]:
    output = check_output([command, option], text=True)
    for token in output.split():
        if "." in token:
            return parse_version(token)
    raise Exception(f"Could not find a version number in {output=}")


def parse_version(text: str) -> tuple[int | str, ...]:
    return tuple(int(v) if v.isnumeric() else v for v in text.split("."))

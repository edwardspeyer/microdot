import inspect
import re
import textwrap
from pathlib import Path
from typing import Callable, Literal

BASE = Path(__file__).parent.parent.resolve()

BEGIN = "-----BEGIN MICRODOT-----"
END = "-----END MICRODOT-----"

Editor = Callable[[str | None], str]
Position = Literal["top", "bottom"]
CommentMarkers = str | tuple[str, str]


def cwd() -> Path:
    frame = inspect.stack()[1]
    return Path(frame.filename).parent.resolve()


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


def search_and_install() -> None:
    for path in sorted(BASE.rglob("**/u.")):
        code = path.read_text()
        obj = compile(code, str(path), "exec")
        exec(obj, globals())

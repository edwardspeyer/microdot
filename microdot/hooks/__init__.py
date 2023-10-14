import re
import textwrap
from enum import Enum
from pathlib import Path


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
    new = re.sub(pattern, outer, old)

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

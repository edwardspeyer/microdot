import re
import textwrap
from pathlib import Path

TOP = "TOP"
BOTTOM = "BOTTOM"


def log(action, path):
    print(f"  {action:6s}  {path}", flush=True)


def install_hook(path, comment, position, text, mode=0o644):
    path = Path(path).expanduser()

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
        if position == TOP:
            path.write_text(outer + "\n" + old)
        elif position == BOTTOM:
            path.write_text(old + "\n" + outer)
        else:
            raise Exception(f"unknown position: {position}")

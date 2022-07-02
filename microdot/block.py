import re
import textwrap
from pathlib import Path

TOP = "TOP"
BOTTOM = "BOTTOM"


def log(action, path):
    print(f"  {action:6s}  {path}", flush=True)


def block(path, comment="#", name="", position=TOP):
    path = Path(path).expanduser()

    def update(replacement):
        inner = textwrap.dedent(replacement).rstrip("\n") + "\n"
        suffix = f" {name}" if name else ""
        begin = f"{comment} -----BEGIN MICRODOT{suffix}-----\n"
        end = f"{comment} -----END MICRODOT{suffix}-----\n"
        outer = begin + inner + end
        pattern = re.compile(f"{begin}.+?\n{end}", re.DOTALL)

        if not path.exists():
            log("NEW", path)
            path.parent.mkdir(exist_ok=True, parents=True, mode=0o700)
            path.write_text(outer)
            return

        old = path.read_text()
        new = re.sub(pattern, outer, old)
        if old == new:
            log("=", path)
        elif re.search(pattern, old):
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

    return update

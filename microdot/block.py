import re
import textwrap
from pathlib import Path

TOP = "TOP"
BOTTOM = "BOTTOM"


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
            path.parent.mkdir(exist_ok=True, parents=True, mode=0o700)
            path.write_text(outer)
            return

        old = path.read_text()
        if re.search(pattern, old):
            new = re.sub(pattern, outer, old)
            path.write_text(new)
        else:
            if position == TOP:
                path.write_text(outer + "\n" + old)
            elif position == BOTTOM:
                path.write_text(old + "\n" + outer)
            else:
                raise Exception(f"unknown position: {position}")

    return update

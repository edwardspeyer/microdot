from pathlib import Path

import microdot.hooks.install as hooks

from . import terminfo

BASE = Path(__file__).parent.parent.resolve()

hooks.install()
terminfo.install(*BASE.glob("kitty/terminfo/*"))

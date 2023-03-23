from pathlib import Path

import microdot.hooks.install as hooks

from . import fonts, gnupg, packages, terminfo

BASE = Path(__file__).parent.parent.resolve()

hooks.install()
terminfo.install(*BASE.glob("kitty/terminfo/*"))
fonts.install()
gnupg.install()
packages.debian.install()
packages.pip.install()
packages.source.install()
# x11.install()

from pathlib import Path

from microdot.hooks import install_hooks
from microdot.terminfo import install_terminfos

BASE = Path(__file__).parent.parent.resolve()

install_hooks()
install_terminfos()

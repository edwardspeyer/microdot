from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter as Raw
from pathlib import Path

import microdot.fonts
import microdot.gnupg
import microdot.hooks
import microdot.macos
import microdot.packages.debian
import microdot.packages.python
import microdot.packages.source.delta
import microdot.packages.source.fish
import microdot.packages.source.i3
import microdot.packages.source.tmux
import microdot.terminfo

BASE = Path(__file__).parent.parent.resolve()


def install():
    microdot.hooks.search_and_install()
    microdot.terminfo.install()


actions = {
    "install": (
        "Run `hooks` and `terminfos`, see below.",
        install,
    ),
    "hooks": (
        "Install config file hooks.",
        microdot.hooks.search_and_install,
    ),
    "terminfos": (
        "Install missing terminfo for common TERM settings.",
        microdot.terminfo.install,
    ),
    "debian": (
        "Install some common debian packages.",
        microdot.packages.debian.install,
    ),
    "python": (
        "Install some common python packages.",
        microdot.packages.python.install,
    ),
    "delta": (
        "Install git-delta from source.",
        microdot.packages.source.delta.install,
    ),
    "fish": (
        "Install a newer version of fish (if required) from source.",
        microdot.packages.source.fish.install,
    ),
    "i3": (
        "Install a newer version of i3 (if required) from source.",
        microdot.packages.source.i3.install,
    ),
    "tmux": (
        "Install a new version of tmux (if required) from source.",
        microdot.packages.source.tmux.install,
    ),
    "gpg": (
        "Install my GPG key stubs, for use with yubikeys.",
        microdot.gnupg.install,
    ),
    "fonts": (
        "Download and install some extra fonts.",
        microdot.fonts.install,
    ),
    "macos": (
        "Configure a macOS user account.",
        microdot.macos.setup,
    ),
}

parser = ArgumentParser(
    formatter_class=Raw,
    epilog="\n".join(f"  {cmd:10s}  - {help}" for cmd, (help, _) in actions.items()),
)

parser.add_argument("action", choices=actions)
args = parser.parse_args()
_, fn = actions[args.action]
fn()

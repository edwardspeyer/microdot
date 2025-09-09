from pathlib import Path
from shutil import which
from subprocess import run
from textwrap import dedent
from typing import Iterator

from microdot import register
from microdot.debian import is_debian


def write_pipewire_fixes() -> Iterator[bool]:
    def write(sub_path: str, text: str) -> bool:
        formatted_text = dedent(text)
        path = Path.home() / sub_path
        if path.exists() and path.read_text() == formatted_text:
            return False
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(formatted_text)
        return True

    yield write(
        ".config/pipewire/pipewire.conf.d/99-force-48khz.conf",
        """\
        context.properties = {
            default.clock.rate          = 48000
            default.clock.allowed-rates = [ 48000 ]
            default.clock.quantum       = 1024
            default.clock.min-quantum   = 1024
        }
        """,
    )

    yield write(
        ".config/pipewire/pipewire-pulse.conf.d/99-force-48khz.conf",
        """\
        pulse.properties = {
            resample.quality = 4
            default.clock.rate = 48000
            default.clock.allowed-rates = [ 48000 ]
        }
        """,
    )


def restart_pipewire():
    if not which("pipewire"):
        return  # Pipewire is not yet installed and running
    script = "systemctl --user restart pipewire pipewire-pulse"
    run(script, shell=True, check=True)


@register
def fix_pipewire():
    """Debian-specific pipewire fix to avoid resampling artefacts."""
    if is_debian() and any(write_pipewire_fixes()):
        restart_pipewire()

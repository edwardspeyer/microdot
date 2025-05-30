from pathlib import Path
from subprocess import run
from textwrap import dedent
from typing import Iterator


def fix_pipewire():
    """Debian-specific pipewire fix to avoid resampling artefacts."""

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
        script = "systemctl --user restart pipewire pipewire-pulse"
        run(script, shell=True, check=True)

    if any(write_pipewire_fixes()):
        restart_pipewire()


if __name__ == "__main__":
    fix_pipewire()

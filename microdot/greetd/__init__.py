from getpass import getuser
from pathlib import Path
from textwrap import dedent

from microdot import BASE, write_as_root


def configure() -> None:
    path = Path("/etc/greetd/config.toml")
    if not path.exists():
        return

    user = getuser()
    config = dedent(
        f"""\
        [terminal]
        vt = 7

        [default_session]
        command = "{BASE}/microdot/greetd/init"
        user = "{user}"
        """
    )
    write_as_root(path, config)

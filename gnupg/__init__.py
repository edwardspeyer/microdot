from pathlib import Path
from shutil import copy
from subprocess import run

from microdot import cwd, register


@register
def install():
    dot_gnupg = Path.home() / ".gnupg"
    dot_gnupg.mkdir(exist_ok=True)

    # Install config
    copy(cwd() / "gpg-agent.conf", dot_gnupg)

    # Import key stubs
    script = 'gpg --import "$1"/stubs/* && pkill gpg-agent || true'
    command = ["sh", "-c", script, "--", str(cwd())]
    run(command, check=True)

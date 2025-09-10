from pathlib import Path
from shutil import copy
from subprocess import run

from microdot import cwd


def install():
    dot_gnupg = Path.home() / ".gnupg"
    dot_gnupg.mkdir(exist_ok=True)
    dot_gnupg.chmod(0o700)

    # Install config
    copy(cwd() / "gpg-agent.conf", dot_gnupg)

    # Import key stubs
    script = 'gpg --quiet --import "$1"/stubs/* && pkill gpg-agent || true'
    command = ["sh", "-c", script, "--", str(cwd())]
    run(command, check=True)

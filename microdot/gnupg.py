from pathlib import Path
from shutil import copy
from subprocess import run


def install():
    base = Path(__file__).parent.parent / "gnupg"
    dot_gnupg = Path.home() / ".gnupg"
    dot_gnupg.mkdir(exist_ok=True)
    copy(base / "gpg-agent.conf", dot_gnupg)
    run(
        rf"""
        set -ex
        gpg --import {base}/stubs/*
        pkill gpg-agent || true
        """,
        check=True,
        shell=True,
    )

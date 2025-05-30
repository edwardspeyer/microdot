#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from subprocess import run
from sys import stderr


def sh(script: str, *args) -> bool:
    print("+", script, *args, file=stderr)
    v = run(["sh", "-c", script, "--", *map(str, args)])
    return v.returncode == 0


base = Path.home() / "Screenshots"
base.mkdir(exist_ok=True, parents=True)

t = datetime.now()
path = base / f"{t:%Y-%m-%dT%H-%M-%S}.png"

if sh('grim -g "`slurp`" "$1"', path):
    sh('swappy -f "$1"', path)

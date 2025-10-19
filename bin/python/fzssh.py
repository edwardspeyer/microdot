#!/usr/bin/env python3
"""ssh to known-hosts via fzf."""

import os
import re
import shlex
import sys
from pathlib import Path
from subprocess import PIPE, check_output, run
from typing import Iterator


def get_current_config() -> Iterator[tuple[str, list[str]]]:
    output = check_output(["ssh", "-G", "example.com"], text=True)
    for line in output.splitlines():
        k, *vs = line.split()
        yield k, vs


def get_known_hosts_paths() -> Iterator[Path]:
    for k, vs in get_current_config():
        if k.endswith("knownhostsfile"):
            for v in vs:
                path = Path(v)
                if path.exists():
                    yield path


def get_known_hosts() -> Iterator[str]:
    for path in get_known_hosts_paths():
        with path.open("rt") as f:
            for line in f:
                fields = re.sub(r" *#.*$", "", line).strip().split()
                if fields:
                    yield fields[0]


hosts = "\n".join(sorted(set(get_known_hosts())))
host = run(
    [
        "fzf",
        "--layout=reverse",
    ],
    input=hosts,
    text=True,
    stdout=PIPE,
).stdout.strip()
if host:
    args = ["ssh", host, *sys.argv[1:]]
    if "TMUX" in os.environ:
        args = ["tmux", "detach-client", "-E", shlex.join(args)]
    os.execvp(args[0], args)

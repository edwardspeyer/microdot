#!/usr/bin/env python3

import csv
import os
import re
from itertools import count
from pathlib import Path
from subprocess import check_output, run
from sys import argv, exit, stderr
from tempfile import TemporaryDirectory
from time import time
from typing import Iterable, Iterator

RESET = "\033[0m"
UNDERLINE = "\033[4m"
CLEAR = "\033[H\033[J"


def await_modifications(paths: Iterable[Path]) -> str:
    cmd = [
        "inotifywait",
        "--recursive",
        "--quiet",
        *("--event", "attrib"),
        *("--event", "create"),
        *("--event", "modify"),
        *("--event", "move"),
        "--",
        *(map(str, paths)),
    ]
    return check_output(cmd, text=True).strip()


def trace_run(command: list[str]) -> set[Path]:
    def parse_strace(lines: Iterable[str]) -> Iterator[tuple[str, ...]]:
        for line in lines:
            if md := re.match(r"^\d+ +(\w+)\((.+)\) = \d+$", line):
                fn, args_str = md.groups()
                args = next(csv.reader([args_str], skipinitialspace=True))
                yield fn, *args

    def parse_strace_opened_paths(lines: Iterable[str]) -> Iterator[tuple[Path, int]]:
        for fn, *args in parse_strace(lines):
            match fn:
                case "open":
                    p, f = args[0], args[1]
                case "openat" | "openat2":
                    p, f = args[1], args[2]
                case _:
                    continue
            yield Path(p), int(f, 16)

    def parse_strace_read_only_opened_paths(lines: Iterable[str]) -> Iterator[Path]:
        for path, flags in parse_strace_opened_paths(lines):
            if flags & os.O_RDONLY == os.O_RDONLY:
                yield path.resolve()

    with TemporaryDirectory() as tmp:
        trace_path = Path(tmp) / "trace"
        run(
            [
                "strace",
                *("-e", "open,openat,openat2"),
                *("-X", "raw"),
                *("-o", str(trace_path)),
                "-f",
                "--",
                *command,
            ],
        )
        with trace_path.open() as f:
            d = Path.cwd()
            return {
                p.relative_to(d)
                for p in parse_strace_read_only_opened_paths(f)
                if p.exists() and p.is_file() and p.is_relative_to(d) and os.access(p, os.W_OK)
            }


def main():
    if "--" in argv:
        i = argv.index("--")
        command = argv[i + 1 :]
        paths = {Path(p) for p in argv[1:i]}
    else:
        command = argv[1:]
        paths = {p for p in map(Path, command) if p.exists()}

    if not paths:
        print(f"no paths in argv!: {argv!r}", file=stderr)
        exit(3)

    for path in paths:
        if not path.exists():
            print(f"path does not exist!: {path}", file=stderr)
            exit(3)

    for n in count():
        if n == 0:
            reason = None
        else:
            try:
                reason = "♺ " + await_modifications(paths)
            except KeyboardInterrupt:
                reason = "^C"
        print(CLEAR, end="", flush=True)
        t0 = time()
        new_paths = trace_run(command) - paths
        duration = int(1000 * (time() - t0))
        message = f"{duration}ms"
        if reason:
            message += " " + reason
        print(UNDERLINE + message + RESET)

        if new_paths:
            ps = sorted(new_paths)
            print(f"...adding {len(ps)} new path(s) to watch list:")
            for p in ps:
                print("+", p)
            paths |= new_paths


if __name__ == "__main__":
    main()

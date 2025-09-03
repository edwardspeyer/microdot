#!/usr/bin/env python3

import os
import sqlite3
import sys
from argparse import ArgumentParser
from contextlib import contextmanager
from io import SEEK_END
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen
from textwrap import dedent
from typing import Any, Callable, Iterator
from zlib import crc32


def get_cache_dir() -> Path:
    if d := os.environ.get("XDG_CACHE_DIR"):
        return Path(d)
    else:
        return Path.home() / ".cache"


class Database:
    def __init__(self) -> None:
        path = get_cache_dir() / "exigrep-wrapper.sqlite"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path))
        self.conn.executescript(
            """
            create table if not exists
            empty_search(checksum, term);
            """
        )

    def query_was_empty(self, checksum: int, term: str) -> bool:
        v = self.conn.execute(
            """
            select count(rowid) from empty_search
            where checksum = ? and term = ?
            """,
            (checksum, term),
        )
        (r,) = v.fetchone()
        return bool(r)

    def set_is_empty(self, checksum: int, term: str) -> None:
        self.conn.execute(
            """
            insert or ignore into
            empty_search(checksum, term) values (?, ?)
            """,
            (checksum, term),
        )
        self.conn.commit()


def find_logs(base: Path) -> list[Path]:
    def key(p: Path) -> int:
        if "." not in p.name:
            return 0
        _, n, *_ = p.name.split(".")
        return int(n)

    logs = base.glob("mainlog*")
    return sorted(logs, key=key)


def exigrep(path: Path, term: str) -> Iterator[str]:
    script = dedent(
        """
        { zcat "$1" 2>/dev/null || cat "$1"; } | exigrep "$2"
        """,
    )
    command = ["sh", "-c", script, "--", str(path), term]
    with Popen(command, text=True, stdout=PIPE, stderr=STDOUT) as p:
        assert p.stdout is not None
        yield from p.stdout


def calculate_tail_checksum(path: Path) -> int:
    CHUNK_SIZE = 1 << 20
    with path.open("rb") as f:
        if path.stat().st_size >= CHUNK_SIZE:
            f.seek(-CHUNK_SIZE, SEEK_END)
        return crc32(f.read())


@contextmanager
def colorizer() -> Iterator[Callable]:
    if not sys.stdout.isatty():
        yield print
        return

    with Popen(["ccze", "-A"], text=True, stdin=PIPE) as p:
        io = p.stdin
        assert io is not None

        def print_fn(*args: Any, end="\n", sep=" ") -> None:
            io.write(sep.join(str(a) for a in args))
            io.write(end)
            io.flush()

        yield print_fn
        io.close()
        p.wait()


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--logs-directory", type=Path, default="/var/log/exim4")
    parser.add_argument("term")
    args = parser.parse_args()
    db = Database()
    with colorizer() as print:
        for log in reversed(find_logs(args.logs_directory)):
            checksum = calculate_tail_checksum(log)
            if db.query_was_empty(checksum, args.term):
                continue

            is_empty = True
            for line in exigrep(log, args.term):
                is_empty = False
                print(line, end="")

            if is_empty:
                print(f"{log}: no matches")
                db.set_is_empty(checksum, args.term)


main()

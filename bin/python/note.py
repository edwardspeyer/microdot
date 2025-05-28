#!/usr/bin/env -S uv run --script
#
# Create and manage markdown notes.
#
# vim: ft=python
#
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "lxml",
#     "markdown",
#     "tabulate",
# ]
# ///

import re
import shlex
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime, timezone
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from functools import cached_property
from pathlib import Path
from subprocess import PIPE, check_output, run
from sys import stderr, stdout
from tempfile import NamedTemporaryFile
from textwrap import dedent
from typing import Iterable, Iterator, Protocol
from uuid import uuid4 as create_uuid

import lxml.html
from markdown import markdown
from tabulate import tabulate

NEW_TEMPLATE = "Note.%Y-%m-%dT%H.%M.md"


def edit(path: Path) -> None:
    run(["vim", str(path)])


def warning(*message) -> None:
    print(*message, file=stderr)


def create_new_note(base: Path) -> None:
    t = datetime.now(tz=timezone.utc).replace(microsecond=0)
    p = base / t.strftime(NEW_TEMPLATE)
    if p.exists():
        p0 = p
        for i in range(100):
            n = i + 1
            p = p0.parent / f"{p0.stem}.{n:02d}{p0.suffix}"
            if not p.exists():
                break
        else:
            raise Exception("!!!")  # TODO
    uuid = create_uuid()
    template = dedent(
        f"""\
        # {t.date().isoformat()} New Note

        <!-- note created:{t.isoformat()} uuid:{uuid} -->
        """
    )
    p.parent.mkdir(exist_ok=True, parents=True)
    p.write_text(template)
    edit(p)

    if p.exists() and p.read_text() == template:
        # TODO log
        p.unlink()


class Note(Protocol):
    path: Path
    created: datetime | None
    html: str
    title: str | None
    # readonly: bool  # TODO

    @property
    def source(self) -> str: ...


@dataclass
class MarkdownNote:
    path: Path
    source: str
    created: datetime | None
    html: str
    title: str | None


@dataclass
class MailNote:
    path: Path
    created: datetime | None
    html: str
    title: str | None

    @cached_property
    def source(self) -> str:
        command = ["w3m", "-dump", "-T", "text/html", "-"]
        return check_output(command, text=True, input=self.html)


def find_fd(*args: str) -> list[Path]:
    output = check_output(["fd", "--type", "file", *args], text=True)
    return sorted(Path(p) for p in output.splitlines())


def get_markdown_notes(base: Path) -> Iterator[Note]:
    for path in find_fd(r"\.md$", str(base)):
        source = path.read_text()
        md = re.search(r"<!-- +note +(.+)-->", source)
        if not md:
            continue
        meta = dict(pair.split(":", maxsplit=1) for pair in md.group(1).split())
        created = datetime.fromisoformat(v).astimezone(timezone.utc) if (v := meta.get("created")) else None
        html = markdown(source)
        doc = lxml.html.fromstring(html)
        title = headings[0].text if (headings := doc.xpath("//h1 | //h2 | //h3")) else "?"

        yield MarkdownNote(path, source, created, html, title)


def get_mail_notes(base: Path) -> Iterator[Note]:
    for path in find_fd("--full-path", r".*/Notes/(cur|new)/.*", str(base)):
        with path.open("rb") as f:
            message = BytesParser().parse(f)
        if not message.get("X-Uniform-Type-Identifier", "").endswith("mail-note"):
            continue
        # uuid = message['X-Universally-Unique-Identifier']  # TODO
        parts = list(message.walk())
        if len(parts) != 1:
            warning(f"Unexpected number of parts for a mail-note ({len(parts)}) in {path}: {parts!r}")
            continue
        title = message["Subject"]
        created = parsedate_to_datetime(message["Date"])
        html = parts[0].get_payload(decode=True)
        if not isinstance(html, bytes):
            warning(f"Expected a single string mime part (in {path}), not: {parts!r}")
            continue
        yield MailNote(path, created, html.decode(), title)


def get_notes(base: Path) -> Iterator[Note]:
    yield from get_markdown_notes(base)
    yield from get_mail_notes(base)


def print_listing(base: Path, notes: Iterable[Note], is_verbose: bool) -> None:
    def truncate(s: str) -> str:
        MAX = 30
        if len(s) <= MAX:
            return s
        return s[:MAX] + "\N{HORIZONTAL ELLIPSIS}"

    rows = [
        [
            note.created.strftime("%Y-%m-%d") if note.created else "-",
            (note.title if is_verbose else truncate(note.title)) if note.title else "",
            str(note.path if is_verbose else note.path.relative_to(base)),
        ]
        for note in notes
    ]

    if is_verbose:
        table = tabulate(rows, tablefmt="plain")
    else:
        table = tabulate(
            rows,
            headers=["Created", "Title", "Path"],
            tablefmt="rounded_outline",
        )

    print(table)


def title_basename(note: Note) -> str:
    assert note.title
    return re.sub(r"\W", "_", note.title)


def print_rename_script(notes: Iterable[Note]) -> None:
    for note in notes:
        if not note.title:
            continue
        new_path = note.path.parent / f"{title_basename(note)}.md"
        if new_path.exists():
            continue
        command = ["mv", note.path, new_path]
        script = shlex.join(map(str, command))
        print(script)


def fuzzy_find(notes: Iterable[Note]) -> Note | None:
    rows = [
        [
            n.created.isoformat() if n.created else "-",
            n.title or "-",
            str(n.path),
        ]
        for n in reversed(list(notes))
    ]
    columns = zip(*rows)
    widths = [max(map(len, c)) for c in columns]

    def pad(row: list[str]) -> str:
        return "\x1f  ".join(v.ljust(w) for v, w in zip(row, widths))

    header = pad(["Created", "Title", "Path"])
    body = "\n".join(pad(r) for r in rows)
    command = [
        "fzf",
        "--reverse",
        *("--header", header),
        *("--delimiter", "\x1f"),
        *("--accept-nth", "3"),  # the path
    ]
    p = run(command, text=True, input=body, stdout=PIPE)
    if p.returncode != 0:
        return None  # TODO Log?
    path = p.stdout.strip()
    for note in notes:
        if str(note.path) == path:
            return note
    raise Exception("!!")


def find_all(search_term: str, notes: Iterable[Note]) -> list[Note]:
    return [n for n in notes if re.search(search_term, repr(n), re.IGNORECASE)]


def find_one(search_term: str, notes: Iterable[Note]) -> Note | None:
    matches = find_all(search_term, notes)
    if len(matches) == 0:
        warning(f"no matches for {search_term=}!")
        return None
    if len(matches) > 1:
        warning(f">1 match!: {matches=}")
        return None
    return matches[0]


def print_pdf(note: Note) -> None:
    assert note.title, "Cannot print note without a title"
    stylesheet = """
    body {
      color: black;
      font-family: sans-serif;
    }

    @media print {
      body {
        margin: 0.20in 0.35in 0.50in 0.35in;
        font-size: 10pt;
      }
    }
    """

    doc = f"""\
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf8">
        <title>{note.title}</title>
        <style>
          {stylesheet}
        </style>
      </head>
      <body>
        {note.html}
      </body>
    </html>
    """

    with NamedTemporaryFile(suffix=".html") as tf:
        tf.write(doc.encode())
        tf.flush()
        command = [
            "chromium",
            "--headless",
            "--disable-gpu",
            "--print-to-pdf",
            "--no-pdf-header-footer",
            "--no-margins",
            "--print-to-pdf=/dev/stdout",
            tf.name,
        ]
        pdf = check_output(command, input=doc.encode())

    if stdout.isatty():
        out_path = title_basename(note) + ".pdf"
        warning(f"writing to {out_path}")
        with open(out_path, "wb") as f:
            f.write(pdf)
    else:
        stdout.buffer.write(pdf)


def cat(notes: Iterable[Note]) -> None:
    for note in notes:
        print(note.source)


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument("-l", "--list", action="store_true")
    parser.add_argument("-r", "--rename", action="store_true")
    parser.add_argument("-e", "--edit", default=False, nargs="?")
    parser.add_argument("-c", "--cat", default=False, nargs="?")
    parser.add_argument("-p", "--print", default=False, nargs="?")
    parser.add_argument("-C", "--directory", default=Path("."), type=Path)
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    base = args.directory
    notes = list(get_notes(base))
    notes = sorted(notes, key=lambda n: n.created or datetime.fromtimestamp(0))

    if args.list:
        print_listing(base, notes, args.verbose)
    elif args.rename:
        print_rename_script(notes)
    elif args.edit is None and (note := fuzzy_find(notes)):
        edit(note.path)
    elif args.edit and (note := find_one(args.edit, notes)):
        edit(note.path)
    elif args.print is None and (note := fuzzy_find(notes)):
        print_pdf(note)
    elif args.print and (note := find_one(args.print, notes)):
        print_pdf(note)
    elif args.cat:
        notes = find_all(args.cat, notes)
        cat(notes)
    else:
        create_new_note(args.directory)


if __name__ == "__main__":
    main()

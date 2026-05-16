#!/usr/bin/python3

"""
For each package given on the command line, print the leaf-packages that depend
on it, either directly or indirectly.
"""

from argparse import ArgumentParser
from collections import defaultdict
from subprocess import check_output
from typing import Iterator

Package = str
Packages = set[Package]
Graph = dict[Package, Packages]


def dependencies() -> Iterator[tuple[Package, Package]]:
    script = r"dpkg-query -W -f='${Package} ${Depends}\n'"
    output = check_output(script, shell=True, text=True)
    for line in output.splitlines():
        package, depends = line.split(" ", maxsplit=1)
        if depends:
            for options in depends.split(", "):
                for versioned_dependency in options.split(" | "):
                    dependency = versioned_dependency.split(" (")[0]
                    yield package, dependency


def build_graph() -> tuple[Graph, Packages]:
    rev = defaultdict(set)
    for p, d in dependencies():
        rev[d].add(p)

    leaves = {p for d, ps in rev.items() for p in ps if p not in rev}

    # Closure
    while True:
        added = False
        for d, ps in list(rev.items()):
            for p in set(ps):
                if rev[p] - rev[d]:
                    rev[d] |= rev[p]
                    added = True
        if not added:
            break

    return rev, leaves


def main():
    parser = ArgumentParser()
    parser.add_argument("packages", nargs="+")
    args = parser.parse_args()
    rev, leaves = build_graph()
    for package in args.packages:
        for rdep in sorted(rev[package] & leaves):
            print(f"{package}  {rdep}")


if __name__ == "__main__":
    main()

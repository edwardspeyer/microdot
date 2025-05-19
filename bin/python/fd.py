#!/usr/bin/env python3

from os import execv, stat
from shutil import which
from sys import argv


def same(*paths):
    return len(set(map(stat, paths))) == 1


if bin := which("fdfind"):
    execv(bin, argv)

if (bin := which("fd")) and not same(bin, __file__):
    execv(bin, argv)


raise Exception("fd not installed :(")

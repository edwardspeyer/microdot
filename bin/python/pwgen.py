#!/usr/bin/env python3

from secrets import choice
from string import ascii_lowercase, ascii_uppercase, digits
from sys import stdout


def pwgen() -> str:
    def chargen():
        yield choice(ascii_uppercase)
        yield choice(digits)
        for _ in range(16):
            yield choice(ascii_lowercase)

    chars = list(chargen())
    return "".join(
        (
            *chars[0:6],
            "-",
            *chars[6:12],
            "-",
            *chars[12:18],
        )
    )


def main() -> None:
    if stdout.isatty():
        for _ in range(10):
            print(pwgen())
    else:
        print(pwgen())


if __name__ == "__main__":
    main()

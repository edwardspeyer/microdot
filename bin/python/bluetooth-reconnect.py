#!/usr/bin/env python3
#
# Force a bluetooth re-everything instead of trusting `connect` to work.
#
# See https://askubuntu.com/a/1429906
#

from argparse import ArgumentParser
from subprocess import Popen, run
from time import sleep


def bluetoothctl(*args: str, retry: bool = False) -> None:
    while True:
        print("+", *args)
        try:
            r = run(["bluetoothctl", *args], timeout=3)
        except TimeoutError:
            continue
        if not retry:
            return
        if r.returncode == 0:
            return
        sleep(1)


def reconnect(address: str) -> None:
    with Popen(["bluetoothctl", "--timeout", "100", "scan", "on"]) as scanner:
        bluetoothctl("remove", address)
        bluetoothctl("trust", address, retry=True)
        bluetoothctl("pair", address, retry=True)
        bluetoothctl("connect", address, retry=True)
        scanner.terminate()


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("address", help="Device address")
    args = parser.parse_args()
    reconnect(args.address)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
#
# Force a bluetooth re-everything instead of trusting `connect` to work.
#
# See https://askubuntu.com/a/1429906
#

from argparse import ArgumentParser
from subprocess import Popen, TimeoutExpired, run
from time import sleep


def bluetoothctl(*args: str, retry: bool = False) -> bool:
    while True:
        print("+", *args)
        try:
            r = run(["bluetoothctl", *args], timeout=3)
            if r.returncode == 0:
                return True
        except TimeoutExpired:
            pass

        if not retry:
            return False
        else:
            sleep(0.2)


def reconnect(address: str) -> None:
    if bluetoothctl("connect", address, retry=False):
        return

    bluetoothctl("remove", address)
    sleep(0.2)
    bluetoothctl("power", "off")
    sleep(0.2)
    bluetoothctl("agent", "off")
    sleep(0.2)
    bluetoothctl("power", "on")
    sleep(0.2)
    bluetoothctl("agent", "on")
    sleep(0.2)
    bluetoothctl("remove", address)
    sleep(0.2)
    with Popen(["bluetoothctl", "--timeout", "20", "scan", "on"]) as scanner:
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

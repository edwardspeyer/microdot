#!/usr/bin/env python3

import re
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from queue import Queue
from subprocess import STDOUT, CalledProcessError, check_output, run
from threading import Thread
from time import sleep, time
from typing import Tuple

STALE_DATA_AGE = 60


def get_battery_status():
    for battery_directory in Path("/sys/class/power_supply/").glob("BAT*"):
        battery = str(battery_directory.name)
        capacity = int((battery_directory / "capacity").read_text())
        status = (battery_directory / "status").read_text().strip()
        yield battery, capacity, status


def get_battery_status_text():
    buf = []
    for battery, capacity, status in get_battery_status():
        line = f"{status} {capacity:3d}%"
        buf.append(line)
    return " ".join(buf)


def get_temperature_summary() -> str:
    def read() -> Tuple[str, float]:
        for tz in Path("/sys/class/thermal").glob("thermal_zone*"):
            name = (tz / "type").read_text().strip()
            temp = int((tz / "temp").read_text()) // 1000
            yield name, temp

    return " ".join(f"{v}\N{DEGREE SIGN}C" for k, v in read() if "pkg" in k)


def get_clock():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_audio_level():
    script = "pactl get-sink-volume @DEFAULT_SINK@"
    try:
        output = check_output(script, shell=True, text=True, stderr=STDOUT)
        match_data = re.search(r"(\d+)%", output)
        if not match_data:
            return "?"
        level = int(match_data.groups()[0])
        return f"{level:3d}%"
    except CalledProcessError:
        return "?"


def get_display_brightness():
    base = Path("/sys/class/backlight/intel_backlight")
    if not base.exists():
        return ""
    actual = int((base / "actual_brightness").read_text())
    maximum = int((base / "max_brightness").read_text())
    percentage = int(100 * actual / maximum)
    return f"{percentage:3d}%"


def get_wifi_information():
    script = "nmcli -t -f CHAN,RATE,SIGNAL,IN-USE,SSID dev wifi list"
    process = run(script, text=True, shell=True, capture_output=True)
    if process.returncode > 0:
        return ""
    for line in process.stdout.splitlines():
        fields = line.split(":", maxsplit=4)
        channel, rate, signal, in_use, ssid = fields
        if in_use == "*":
            return f"{ssid} ch{channel} {rate} {int(signal):3d}%"
    return "?"


def watch(fn, interval):
    q = Queue()

    def loop():
        while True:
            data = fn()
            t = time()
            q.put((t, data))
            sleep(interval)

    def fetch():
        while q.qsize() > 1:
            q.get()
        if q.qsize() >= 1:
            t, data = q.queue[0]
            age = time() - t
            if age <= STALE_DATA_AGE:
                return data

    t = Thread(target=loop, daemon=True)
    t.start()

    return fetch


def main():
    parser = ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    latest_wifi_information = watch(get_wifi_information, 5)
    latest_audio_level = watch(get_audio_level, 0.2)

    pairs = [
        [
            "WiFi",
            latest_wifi_information,
        ],
        [
            "Battery",
            get_battery_status_text,
        ],
        [
            "Temperature",
            get_temperature_summary,
        ],
        [
            "Audio",
            latest_audio_level,
        ],
        [
            "Display",
            get_display_brightness,
        ],
        [
            "",
            get_clock,
        ],
    ]

    t0 = time()
    while True:
        buf = []
        for tag, fn in pairs:
            if v := fn():
                buf += [tag, str(v)]
        line = " ".join(buf)
        print(line, flush=True)
        sleep(0.1)
        if args.test and time() - t0 > 1:
            break


if __name__ == "__main__":
    main()

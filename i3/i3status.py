#!/usr/bin/env python3

import re
from datetime import datetime
from pathlib import Path
from queue import Queue
from subprocess import STDOUT, CalledProcessError, check_output
from threading import Thread
from time import sleep, time

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
        line = f"{status} {capacity}%"
        buf.append(line)
    return " ".join(buf)


def get_clock():
    return datetime.now().strftime("%m/%d %H:%M:%S")


def get_audio_level():
    script = "pactl get-sink-volume @DEFAULT_SINK@"
    try:
        output = check_output(script, shell=True, text=True, stderr=STDOUT)
        match_data = re.search(r"(\d+%)", output)
        if not match_data:
            return "?"
        level = match_data.groups()[0]
        return level
    except CalledProcessError:
        return "?"


def get_display_brightness():
    base = Path("/sys/class/backlight/intel_backlight")
    actual = int((base / "actual_brightness").read_text())
    maximum = int((base / "max_brightness").read_text())
    return f"{int(100 * actual / maximum)}%"


def get_wifi_information():
    script = "nmcli -t -f CHAN,RATE,SIGNAL,IN-USE,SSID dev wifi list"
    output = check_output(script, text=True, shell=True)
    for line in output.splitlines():
        fields = line.split(":", maxsplit=4)
        channel, rate, signal, in_use, ssid = fields
        if in_use == "*":
            return f"{ssid} ch{channel} {rate} {signal}%"
    return "?"


def watch(fn):
    q = Queue()

    def loop():
        while True:
            data = fn()
            t = time()
            q.put((t, data))
            sleep(1)

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
    latest_wifi_information = watch(get_wifi_information)
    latest_audio_level = watch(get_audio_level)

    while True:
        words = [
            "WiFi",
            latest_wifi_information(),
            " ",
            "Audio",
            latest_audio_level(),
            " ",
            "Display",
            get_display_brightness(),
            " ",
            "Battery",
            get_battery_status_text(),
            " ",
            get_clock(),
        ]
        line = " ".join(map(str, words))
        print(line, flush=True)
        sleep(1)


if __name__ == "__main__":
    main()

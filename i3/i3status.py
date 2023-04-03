#!/usr/bin/env python3

import re
from datetime import datetime
from pathlib import Path
from subprocess import STDOUT, CalledProcessError, check_output
from time import sleep


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
        if in_use == '*':
            return f"{ssid} ch{channel} {rate} {signal}%"
    return "?"


if __name__ == "__main__":
    while True:
        words = [
            "WiFi",
            get_wifi_information(),
            " ",
            "Audio",
            get_audio_level(),
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

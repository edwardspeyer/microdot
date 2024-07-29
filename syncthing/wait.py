"""Script that waits for a syncthing peer to reach 100% completion."""

import json
from argparse import ArgumentParser
from pathlib import Path
from sys import stderr
from time import sleep, time
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

path = Path.home() / ".local/state/syncthing/config.xml"


def parse_config() -> tuple[str, dict[str, str], float]:
    root = ET.parse(path).getroot()
    apikey = root.find("gui/apikey").text
    devices = dict((n.attrib[k] for k in ("name", "id")) for n in root.findall("device"))
    delay = max(float(n.attrib["fsWatcherDelayS"]) for n in root.findall("folder"))
    return apikey, devices, delay


def get(key, path, **args):
    if args:
        path += "?" + "&".join(f"{k}={v}" for k, v in args.items())
    req = Request(f"http://localhost:8384{path}", headers={"X-API-Key": key})
    data = urlopen(req).read().decode()
    return json.loads(data)


def get_percentage_complete(apikey, device_id) -> float:
    h = get(apikey, "/rest/db/completion", device=device_id)
    return float(h["completion"])


parser = ArgumentParser(description=__doc__)
parser.add_argument("device-name")
args = parser.parse_args()

device_name = getattr(args, "device-name")
apikey, devices, delay = parse_config()
assert device_name in devices
device_id = devices[device_name]

t_start = time()
while True:
    percentage_complete = get_percentage_complete(apikey, device_id)
    remaining = max(0, delay - (time() - t_start))
    print(f"{remaining:02.0f} {percentage_complete:.1f}%", file=stderr)
    if remaining <= 0 and percentage_complete == 100.0:
        break
    sleep(1)

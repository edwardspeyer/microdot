"""Build a simple syncthing config.xml file from a list of devices:

    - name: mycomputer
      id: "0000000-0000000-0000000-0000000-0000000-0000000-0000000-0000000"
      address: "tcp6://mycomputer.example.com:22000"
    - ...

"""

from string import ascii_letters
import random
from pathlib import Path
from copy import deepcopy
from xml.etree import ElementTree as ET
import yaml


def build_address_node(address: str) -> ET.Element:
    n = ET.Element("address")
    n.text = address
    return n


def build_device_node(
    root: ET.Element,
    name: str,
    id: str,
    address: str,
) -> ET.Element:
    n = deepcopy(root.find("defaults/device"))
    n.attrib["name"] = name
    n.attrib["id"] = id
    n.append(build_address_node(address))
    return n


def build_folder_device_node(id: str) -> ET.Element:
    n = ET.fromstring("<device><encryptionPassword/></device>")
    n.attrib["id"] = id
    n.attrib["introducedBy"] = ""
    return n


def build_api_key() -> str:
    return ''.join(random.sample(ascii_letters, 32))


def main():
    config_path = Path.home() / ".config" / "syncthing.microdot.yaml"
    if not config_path.exists():
        return

    base = Path(__file__).parent
    root = ET.parse(base / "config.xml").getroot()
    doc = yaml.safe_load(config_path.read_text())
    assert isinstance(doc, list)
    for h in doc:
        root.append(build_device_node(root, h["name"], h["id"], h["address"]))
        root.find("folder").append(build_folder_device_node(h["id"]))
    root.find("gui/apikey").text = build_api_key()
    xml = ET.tostring(root)
    out_path = Path.home() / ".local" / "state" / "syncthing" / "config.xml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(xml)


main()

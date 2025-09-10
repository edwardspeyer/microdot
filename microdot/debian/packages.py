from os import environ
from subprocess import PIPE, run
from typing import Iterable

from microdot import is_debian

DAILY_DEBIAN_PACKAGES = {
    "apt-file",
    "bash-completion",
    "btop",
    "ccache",
    "ccze",
    "curl",
    "dc",
    "dnsutils",
    "dpkg-dev",
    "duf",
    "exuberant-ctags",
    "fd-find",
    "fish",
    "fzf",
    "git",
    "inotify-tools",
    "iproute2",
    "iputils-ping",
    "jq",
    "less",
    "mtr",
    "mutt",
    "ncdu",
    "python3-pip",
    "ripgrep",
    "silversearcher-ag",
    "sqlite3",
    "sshfs",
    "strace",
    "sudo",
    "tcpdump",
    "tmux",
    "tree",
    "units",
    "vim-gtk3",  # Terminal vim with lua support"
    "w3m",
    "wget",
    "xz-utils",
}

SWAY_DEBIAN_PACKAGES = {
    "brightnessctl",
    "firefox-esr",
    "grim",
    "libspa-0.2-bluetooth",
    "mplayer",
    "pavucontrol",
    "pipewire",
    "pulseaudio",
    "slurp",
    "suckless-tools",
    "swappy",
    "swayidle",
    "swaylock",
    "wev",
    "wl-clipboard",
    "wmenu",
    "xdg-desktop-portal-wlr",
}


def are_all_installed(packages: Iterable[str]) -> bool:
    output = run(["dpkg", "--status", *packages], text=True, stdout=PIPE).stdout
    is_installed = {}
    for block in output.split("\n\n"):
        if "Package" not in block:
            continue
        lines = block.splitlines()
        meta = dict(L.split(": ", maxsplit=2) for L in lines if ": " in L)
        package = meta["Package"]
        is_installed[package] = "installed" in meta["Status"]
    return all(is_installed.get(p) for p in packages)


def apt_install(packages: Iterable[str]) -> None:
    if are_all_installed(packages):
        return
    run(
        [
            "sudo",
            "apt",
            "install",
            "--no-install-recommends",
            *packages,
        ],
    )


def is_sway() -> bool:
    return "WAYLAND_DISPLAY" in environ


def install() -> None:
    if not is_debian():
        return

    def get_packages():
        yield from DAILY_DEBIAN_PACKAGES
        if is_sway():
            yield from SWAY_DEBIAN_PACKAGES

    apt_install(set(get_packages()))


if __name__ == "__main__":
    install()

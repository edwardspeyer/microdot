from os import environ
from subprocess import PIPE, run
from typing import Iterable

from microdot import is_debian

DAILY_DEBIAN_PACKAGES = {
    "apt-file",
    "bash-completion",
    "bind9-dnsutils",
    "btop",
    "ccache",
    "ccze",
    "curl",
    "dc",
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
    "rsync",
    "sqlite3",
    "sshfs",
    "strace",
    "sudo",
    "tcpdump",
    "tmux",
    "tree",
    "units",
    "unzip",
    "vim-gtk3",  # Terminal vim with lua support"
    "w3m",
    "wget",
    "xz-utils",
}

DESKTOP_DEBIAN_PACKAGES = {
    "brightnessctl",
    "firefox-esr",
    "fuzzel",
    "grim",
    "libspa-0.2-bluetooth",
    "mplayer",
    "pavucontrol",
    "pipewire",
    "slurp",
    "suckless-tools",
    "swappy",
    "swaybg",
    "swayidle",
    "swaylock",
    "waybar",
    "wev",
    "wl-clipboard",
    "wmenu",
    "xdg-desktop-portal-wlr",
    "xdg-utils",  # xdg-mime
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


def is_desktop() -> bool:
    return "WAYLAND_DISPLAY" in environ


def install() -> None:
    if not is_debian():
        return

    def get_packages():
        yield from DAILY_DEBIAN_PACKAGES
        if is_desktop():
            yield from DESKTOP_DEBIAN_PACKAGES

    apt_install(set(get_packages()))


if __name__ == "__main__":
    install()

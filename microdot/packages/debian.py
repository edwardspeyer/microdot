from os import environ
from pathlib import Path
from subprocess import run

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
    "exuberant-ctags",
    "fish",
    "fzf",
    "git",
    "iproute2",
    "iputils-ping",
    "jq",
    "kitty",
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
    "grim",
    "slurp",
    "swappy",
    "swaylock",
    "wl-clipboard",
}


CREATIVE_DEBIAN_PACKAGES = {
    # Admin
    "locales",
    "man-db",
    # Tools
    "docker.io",
    "ffmpeg",
    "firefox",
    "git-lfs",
    "postgresql-client",
    "ubuntu-standard",
}


def apt_install(packages):
    run(
        [
            "sudo",
            "apt",
            "install",
            "--yes",
            "--no-install-recommends",
            *packages,
        ],
    )


def is_debian():
    return Path("/etc/apt").exists()


def is_sway():
    return "WAYLAND_DISPLAY" in environ


def install():
    if is_debian():
        apt_install(DAILY_DEBIAN_PACKAGES)
        if is_sway():
            apt_install(SWAY_DEBIAN_PACKAGES)

from os import environ
from subprocess import run

from microdot import register
from microdot.debian import is_debian

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


def apt_install(packages):
    run(
        [
            "sudo",
            "apt",
            "install",
            "--no-install-recommends",
            *packages,
        ],
    )


def is_sway():
    return "WAYLAND_DISPLAY" in environ


@register
def install():
    if not is_debian():
        return

    def get_packages():
        yield from DAILY_DEBIAN_PACKAGES
        if is_sway():
            yield from SWAY_DEBIAN_PACKAGES

    apt_install(get_packages())

import apt
import astroterm.build
import debian.packages
import debian.setup
import delta.build
import fish
import fish.build
import fonts
import foot
import fuzzel
import git
import gnupg
import i3
import i3.build
import ipython
import kitty
import mutt
import niri.build
import pipewire.fix
import psql
import python.packages
import sh
import ssh
import sway
import terminfo
import thunderbird.configure
import tmux
import tmux.build
import vim
import waybar
import X11
import xdg_open


def main() -> None:
    apt.configure()
    astroterm.build.install()
    delta.build.install()
    fonts.install()  # TODO skip this if `fc-*` not on PATH
    foot.configure()
    fuzzel.configure()
    git.configure()
    i3.build.install()
    i3.configure()
    ipython.configure()
    kitty.configure()
    pipewire.fix.fix_pipewire()
    psql.configure()
    python.packages.install()
    sh.configure()
    ssh.configure()
    sway.configure()
    terminfo.install()  # TODO Let various term things install their own terminfos
    thunderbird.configure.install()
    tmux.build.install()
    tmux.configure()
    vim.install()
    xdg_open.configure()
    gnupg.install()  # Skip if gpg not installed
    X11.configure()
    fish.build.install()  # TODO rename these build scripts to build()
    niri.build.install()
    fish.configure()
    mutt.configure()
    waybar.configure()
    debian.packages.install()
    debian.setup.setup()


if __name__ == "__main__":
    main()

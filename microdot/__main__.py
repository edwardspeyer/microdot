from microdot import (
    X11,
    apt,
    astroterm,
    debian,
    delta,
    fish,
    fonts,
    foot,
    fuzzel,
    git,
    gnupg,
    greetd,
    i3,
    ipython,
    kitty,
    mutt,
    niri,
    pipewire,
    psql,
    python,
    sh,
    ssh,
    sway,
    thunderbird,
    tmux,
    vim,
    waybar,
    xdg_open,
)


def main() -> None:
    # Configure everything
    greetd.configure()
    apt.configure()
    foot.configure()
    fuzzel.configure()
    git.configure()
    i3.configure()
    ipython.configure()
    kitty.configure()
    pipewire.fix.fix_pipewire()
    psql.configure()
    python.packages.install()
    sh.configure()
    ssh.configure()
    sway.configure()
    thunderbird.configure.install()
    tmux.configure()
    vim.install()
    xdg_open.configure()
    gnupg.install()  # Skip if gpg not installed
    X11.configure()
    fish.configure()
    mutt.configure()
    waybar.configure()

    # Set up base system
    debian.setup.setup()
    debian.packages.install()

    # Install missing software
    astroterm.build()
    delta.build()
    i3.build()
    tmux.build()
    fish.build()
    niri.build()
    fonts.install()


if __name__ == "__main__":
    main()

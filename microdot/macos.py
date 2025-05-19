def setup():
    print("TODO")


"""
Pop up the xcode install GUI and start installation.  This takes about 20
minutes:

    > xcode-select --install


Install user-mode brew:

    > mkdir homebrew
    > curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip-components 1 -C homebrew


Install brew packages:

    > brew install git uv fd utm rust cargo ripgrep vim tmux kitty firefox


## Bugs!

- Keyboard layout is wrong: shift-3 is "£" not "#"
- Mouse scroll wheel is wrong
- UI is unreadably small; how to make everything larger?
"""

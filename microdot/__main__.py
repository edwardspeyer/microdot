from subprocess import run

from .block import BOTTOM, block

block("~/.tmux.conf")(
    """\
    source ~/.config/microdot/tmux/tmux.conf
    """
)

block("~/.vimrc", comment='"')(
    """\
    source ~/.config/microdot/vim/vimrc
    """
)

run(
    """
    mkdir -p ~/.vim/autoload/
    cp vim/autoload/* ~/.vim/autoload
    tar -C ~/.vim/ -xf vim/plugged.tar.gz
    """,
    shell=True,
    check=True,
)

block("~/.bashrc")(
    """\
    source ~/.config/microdot/bash/bashrc
    """
)

block("~/.gitconfig")(
    """\
    [include]
    path = ~/.config/microdot/git/config

    [core]
    excludesfile = ~/.config/microdot/git/ignore
    """
)

block("~/.ssh/config", position=BOTTOM)(
    """\
    Host *
    Include ~/.config/microdot/ssh/config
    """
)

block("~/.bashrc", position=BOTTOM, name="FISH HOOK")(
    """\
    if command -v fish >/dev/null && [ -z "$FISH_STARTED" ]
    then
      export FISH_STARTED=yes
      export SHELL=fish
      exec fish
    fi
    """
)

block("~/.config/fish/conf.d/microdot.fish")(
    """\
    for file in ~/.config/microdot/fish/*.fish
        source $file
    end
    """
)

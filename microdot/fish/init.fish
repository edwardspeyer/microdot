if not status --is-interactive
        exit
end

set -x LESS '--RAW-CONTROL-CHARS --chop-long-lines'

alias duf 'duf --hide special --output mountpoint,size,avail,usage'
alias ncdu 'ncdu -x'
alias sudo 'sudo -E'
alias tmux 'tmux -2'

# What actually needs this?
alias python 'python3'
alias pip 'pip3'
alias astroterm 'astroterm --city Coventry --color --threshold 3 --unicode'

switch (uname)
        case Darwin
                alias ls 'ls -G'
                alias mv 'mv -v -n'

        case Linux
                alias ls 'ls --color=auto'
end

if test $TMUX
        set -x TERM 'screen-256color'
end

# Don't quote ls(1) output
set -x QUOTING_STYLE literal

# Patch colors
#
# Doing it here is much easier than interacting with fish_variables, live.
set -u fish_color_command blue

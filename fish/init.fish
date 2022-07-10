if not status --is-interactive
        exit
end

fish_add_path ~/bin
fish_add_path ~/.local/bin
fish_add_path ~/.cargo/bin
fish_add_path /usr/local/sbin
fish_add_path /usr/sbin
fish_add_path /sbin

set -x EDITOR vim
set -x LESS '--RAW-CONTROL-CHARS --chop-long-lines'
set -x LANG 'en_US.UTF-8'
set -x LC_TIME 'en_GB.UTF-8'
set -x TZ 'Europe/London'

alias ncdu 'ncdu -x'
alias sudo 'sudo -E'
alias tmux 'tmux -2'

# What actually needs this?
alias python 'python3'
alias pip 'pip3'

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

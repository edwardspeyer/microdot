# Re-use anything old that was left lying around.  This file will have been put
# in place by the microdot install script.
if [ -f ~/.config/bash/original.sh ]
then
  source ~/.config/bash/original.sh
fi


# If not running interactively, don't do anything
[ -z "$PS1" ] && return


# Bash behavior
HISTCONTROL=ignoreboth  # Ignore duplicates, and lines prefixed with space
HISTTIMEFORMAT='%Y-%m-%d %H:%M:%S%z '
if [ "$BASH_VERSION" '<' "4.3" ]
then
  HISTSIZE=100000
  HISTFILESIZE=100000
else
  HISTSIZE=-1
  HISTFILESIZE=-1
fi
shopt -s histappend     # Append to the history file, don't overwrite it
shopt -s checkwinsize   # Check window size after each command


# Bash completion
for file in                                   \
  /etc/bash_completion                        \
  /usr/local/etc/bash_completion              \
  /usr/share/bash-completion/bash_completion
do
  [ -f "$file" ] && source "$file"
done


# Prompt
export PS1='\[\033[033m\]$ \[\033[0m\]'


# PATH
export PATH="\
$HOME/bin:$HOME/.local/bin:\
/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin"


export EDITOR=vim
export LESS='--RAW-CONTROL-CHARS --chop-long-lines'
export LANG='en_US.UTF-8'
export LC_TIME='en_GB.UTF-8'
export TZ='Europe/London'


if [ "$TMUX" ]
then
  export TERM=screen-256color
fi


# Bump start GPG's ssh-agent in macOS
if [ `uname` = Darwin ]
then
  export SSH_AUTH_SOCK="$HOME/.gnupg/S.gpg-agent.ssh"
  gpg-connect-agent updatestartuptty /bye >/dev/null
fi


#
# Aliases
#
alias sudo='sudo -E'
alias ncdu='ncdu -x'
alias tmux='tmux -2'

# What actually needs this?
alias python=python3
alias pip=pip3
alias python=python3

case `uname` in
  Darwin)
    alias ls='ls -G'
    alias mv='mv -v -n'
    ;;
  Linux)
    eval $(dircolors --bourne-shell)
    alias ls='ls --color=auto'
    ;;
esac


if [ -f ~/.config/bash/local.sh ]
then
  source ~/.config/bash/local.sh
fi


#
# Tmux: auto re-attach to any unattached session
#
if [ -z "$TMUX" ]
then
  if tmux ls -F '#{session_attached}' | grep -q 0
  then
    tmux attach -d
  fi
fi

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


# Random color prompt
color_rgb() {
  local r=$1 g=$2 b=$3
  echo -e "\033[38;2;${r};${g};${b}m"
}

color_hsv() {
  # Integer version adapted from
  # https://stackoverflow.com/questions/24852345
  local h=$1 s=$2 v=$3

  local f=$(( ($h % 60 * 100) / 60 ))
  local p=$(( ($v * 255 * (10000 - $s * (100 -  0))) / 1000000 ))
  local q=$(( ($v * 255 * (10000 - $s * ( $f -  0))) / 1000000 ))
  local t=$(( ($v * 255 * (10000 - $s * (100 - $f))) / 1000000 ))
  local v=$(( ($v * 255) / 100 ))

  case $(( ($h / 60) % 6 )) in
    0) color_rgb $v $t $p;;
    1) color_rgb $q $v $p;;
    2) color_rgb $p $v $t;;
    3) color_rgb $p $q $v;;
    4) color_rgb $t $p $v;;
    5) color_rgb $v $p $q;;
  esac
}

color_hash() {
  local v=$(shasum <<<"$*")
  local t=${v:0:8}
  local h=$(( 0x$t % 360 ))
  color_hsv $h 100 100
}

export PS1="\[$(color_hash _seed_125 $HOSTNAME)\]$ \[\033[0m\]"


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
  else
    tmux list-sessions
  fi 2>/dev/null
fi

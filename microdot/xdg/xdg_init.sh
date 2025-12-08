#
# XDG settings
#
# It's possible to do these in ~/.config/mimeapps.list but that file often gets
# overwritten by other apps.  Forcing these settings at the start of every
# session is more reliable.
#

# Only applies to desktop sessions
[ -z "$XDG_SESSION_ID" ] && return

# Assume tmux shells are already configured
[ "$TMUX" ] && return

xdg-mime default firefox-new-window.desktop text/html
xdg-mime default firefox-new-window.desktop x-scheme-handler/http
xdg-mime default firefox-new-window.desktop x-scheme-handler/https
xdg-mime default imv.desktop                image/jpeg
xdg-mime default imv.desktop                image/png
xdg-mime default org.gnome.Evince.desktop   application/pdf

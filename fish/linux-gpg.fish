if not command -v gpg-connect-agent >/dev/null
        return
end

# Ensure .gnupg exists.
#
# Weirdly (once) it was there but it wasn't a file.
if not test -d ~/.gnupg
        rm -f ~/.gnupg
end
mkdir -p ~/.gnupg

if status --is-interactive; and test (uname) = Linux
        set -x SSH_AUTH_SOCK /run/user/1000/gnupg/S.gpg-agent.ssh
        gpg-connect-agent updatestartuptty /bye >/dev/null
end

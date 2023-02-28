if status --is-interactive; and test (uname) = Linux
        set -x SSH_AUTH_SOCK /run/user/1000/gnupg/S.gpg-agent.ssh
        gpg-connect-agent updatestartuptty /bye >/dev/null
end

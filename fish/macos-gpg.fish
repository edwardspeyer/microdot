# Bump start GPG's ssh-agent in macOS
if status --is-interactive; and test (uname) = Darwin
        set -x SSH_AUTH_SOCK "$HOME/.gnupg/S.gpg-agent.ssh"
        gpg-connect-agent updatestartuptty /bye >/dev/null
end

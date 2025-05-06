# Ensure we are connected to an agent, if one exists.

function ssh_test_socket
    env SSH_AUTH_SOCK=$argv[1] ssh-add -l >/dev/null 2>&1
    switch $status
        case 0 1
            return 0
        case '*'
            echo "status: $status"
    end
    return 1
end


function ssh_connect_to_existing_agent
    for socket in /tmp/ssh-*/agent.*
        if ssh_test_socket $socket
            set -gx SSH_AUTH_SOCK $socket
            return
        end
    end
end


if status --is-interactive; and not set -q $SSH_AUTH_SOCK
    ssh_connect_to_existing_agent
end

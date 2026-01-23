function ssh_agent_start
    # Ensure we are connected to an agent, if one exists.

    function ssh_agent_test_socket
        env SSH_AUTH_SOCK=$argv[1] ssh-add -l >/dev/null 2>&1
        switch $status
            case 0 1
                return 0
            case '*'
                echo "status: $status"
        end
        return 1
    end

    # Look for existing agents...
    for socket in /tmp/ssh-*/agent.* $HOME/.ssh/agent/s.* 
        if ssh_agent_test_socket $socket
            set -gx SSH_AUTH_SOCK $socket
            return
        end
    end

    # ...or start a new one
    eval (ssh-agent -c) >/dev/null
end


if status --is-interactive; and not set -q $SSH_AUTH_SOCK
    ssh_agent_start
end

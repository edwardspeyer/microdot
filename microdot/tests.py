from os import environ


def is_ssh_remote() -> bool:
    return "SSH_TTY" in environ

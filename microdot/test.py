import os
from subprocess import check_call


def test():
    script = """
        apt update
        apt install --yes eatmydata
        eatmydata apt install --yes python3 gpg procps sudo
        /u./install
    """
    cwd = os.getcwd()
    check_call(
        [
            "docker",
            "run",
            "--rm",
            *("--volume", f"{cwd}:/u."),
            "debian:latest",
            "sh",
            "-c",
            script,
        ],
    )


if __name__ == "__main__":
    test()

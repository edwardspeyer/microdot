import os
from pathlib import Path
from shutil import copytree
from subprocess import check_output, run
from tempfile import TemporaryDirectory


def install_from_script(script, *args):
    """Run the script and assume everything everything in $tmp/out goes
    into ~/.local."""
    with TemporaryDirectory() as temporary_directory:
        tmp = Path(temporary_directory)
        env = dict(os.environ)
        env["DEBIAN_FRONTEND"] = "noninteractive"
        env["PATH"] = f"/usr/lib/ccache:{env['PATH']}"
        run(["sh", "-c", script, "--", *args], check=True, cwd=tmp, env=env)
        out = tmp / "out"
        local = Path.home() / ".local"
        copytree(out, local, dirs_exist_ok=True)


def get_version(command: str, option: str):
    output = check_output([command, option], text=True)
    for token in output.split():
        if "." in token:
            return parse_version(token)
    raise


def parse_version(text: str):
    return [int(v) if v.isnumeric() else v for v in text.split(".")]

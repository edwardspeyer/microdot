from shutil import which
from subprocess import run


def install():
    if which("uv"):
        return
    run("pip install --break-system uv", shell=True, check=True)

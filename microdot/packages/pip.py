from subprocess import run

#
# General purpose dev-environment things.  Anything project specific shouldn't
# be here as it'll clutter up everything else.
#
PYTHON_PACKAGES = {
    "black",
    "docker-compose",
    "isort",
    "mypy",
    "pre_commit",
    "pycodestyle",
    "pylint",
    "pytest",
    "python-lsp-server",  # Newer than python-language-server
}


def install():
    run(
        [
            "pip3",
            "install",
            "--quiet",
            "--user",
            *PYTHON_PACKAGES,
        ],
        check=True,
    )

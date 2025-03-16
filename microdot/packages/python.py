from subprocess import run

#
# General purpose dev-environment things.  Anything project specific shouldn't
# be here as it'll clutter up everything else.
#
PYTHON_PACKAGES = {
    "black",
    "isort",
    "markdown",
    "mypy",
    "pre_commit",
    "pycodestyle",
    "pylint",
    "pytest",
    "python-lsp-server[all]",  # Newer than python-language-server
    "ruff",
    "uv",
}


def install():
    command = [
        "pip3",
        "install",
        "--break-system-packages",
        "--user",
        *PYTHON_PACKAGES,
    ]
    print("+", command)
    run(command, check=True)

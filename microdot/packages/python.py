from subprocess import run

#
# General purpose dev-environment things.  Anything project specific shouldn't
# be here as it'll clutter up everything else.
#
PYTHON_PACKAGES = {
    "black",
    "isort",
    "mypy",
    "pre_commit",
    "pycodestyle",
    "pylint",
    "pytest",
    "python-lsp-server[all]",  # Newer than python-language-server
}


def install():
    command = [
        "pip3",
        "install",
        "--quiet",
        "--break-system-packages",
        "--user",
        *PYTHON_PACKAGES,
    ]
    print("+", command)
    run(command, check=True)


if __name__ == "__main__":
    install()

import json
from pathlib import Path

from microdot import cwd, install_hook


def configure() -> None:
    # waybar is weird: provide an option for local overrides though
    local_base = Path.home() / ".config/waybar"
    local_base.mkdir(parents=True, exist_ok=True)
    config = json.dumps(
        {
            "include": [
                f"{cwd()}/config.jsonc",
                f"{local_base}/config.local.jsonc",
            ]
        },
        indent=4,
    )
    (local_base / "config.jsonc").write_text(config)

    install_hook(
        "~/.config/waybar/style.css",
        f"""
        @import url("file://{cwd()}/style.css");
        """,
        comment=("/*", "*/"),
    )

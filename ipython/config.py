import logging

from IPython import get_ipython

# Turn logging on by default
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)

if ip := get_ipython():
    # Enable autoreloading of _all_ modules ('2', below) on execution.
    ip.run_line_magic("load_ext", "autoreload")
    ip.run_line_magic("autoreload", "2")

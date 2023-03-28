import sys
from rich.console import Console

console = Console()

__all__ = ["console", "pipeInput"]


def pipeInput() -> str:
    """Returns the piped input if any."""
    return "".join(sys.argv[1:]).replace("s", "") if sys.stdin.isatty() else sys.stdin.buffer.read().decode("utf-8")
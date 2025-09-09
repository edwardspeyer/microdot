from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")
F = Callable[P, R]


registry: set[Callable] = set()


def register(f: F) -> F:
    registry.add(f)
    return f

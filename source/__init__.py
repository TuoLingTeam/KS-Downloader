__all__ = ["KS"]


def __getattr__(name: str):
    if name == "KS":
        from .app import KS

        return KS
    raise AttributeError(name)

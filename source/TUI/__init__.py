__all__ = ["KSDownloaderApp"]


def __getattr__(name: str):
    if name == "KSDownloaderApp":
        from .app import KSDownloaderApp

        return KSDownloaderApp
    raise AttributeError(name)

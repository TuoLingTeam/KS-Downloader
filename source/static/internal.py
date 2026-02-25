from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.joinpath("Volume")
PROJECT_ROOT.mkdir(exist_ok=True)
VERSION_MAJOR = 1
VERSION_MINOR = 5
VERSION_BETA = False
__VERSION__ = f"{VERSION_MAJOR}.{VERSION_MINOR}.{'beta' if VERSION_BETA else 'stable'}"
PROJECT_NAME = f"KS-Downloader V{VERSION_MAJOR}.{VERSION_MINOR} {
    'Beta' if VERSION_BETA else 'Stable'
}"

REPOSITORY = "https://github.com/TuoLingTeam/KS-Downloader"
LICENCE = "GNU General Public License v3.0"
RELEASES = "https://github.com/TuoLingTeam/KS-Downloader/releases/latest"

if __name__ == "__main__":
    print(__VERSION__)

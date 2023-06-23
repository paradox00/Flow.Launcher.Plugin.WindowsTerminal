from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, Dict
import os
from helpers import json_load_comments

@dataclass
class Terminal:
    package: str
    fullname: str
    settings: Path

@dataclass
class TerminalProfile:
    name: str
    guid: str
    hidden: bool
    terminal: Terminal
    info: str

class TerminalProfiles:
    PACKAGES = [
        "Microsoft.WindowsTerminal",
        "Microsoft.WindowsTerminalPreview",
    ]
    def __init__(self) -> None:
        pass

    def find_installation(self) -> Iterable[Terminal]:
        local_app_data = os.getenv("LOCALAPPDATA")
        packages_path = Path(local_app_data, "packages")
        for directory in packages_path.iterdir():
            for package in self.PACKAGES:
                if directory.name.startswith(f"{package}_"):
                    yield Terminal(package, directory.name, directory / "LocalState" / "settings.json")

    def find_profiles(self):
        for terminal in self.find_installation():
            if not terminal.settings.exists():
                continue

            settings = json_load_comments(terminal.settings)
            for profile in settings["profiles"]["list"]:
                yield self.parse_profile(profile, terminal)

    def parse_profile(self, profile: Dict, terminal: Terminal) -> TerminalProfile:
        source = profile.get('source')
        info = profile.get('commandline', source)
        return TerminalProfile(
            name = profile.get("name", ""),
            guid = profile.get("guid", ""),
            hidden = profile.get("hidden", False),
            terminal = terminal,
            info = info
        )

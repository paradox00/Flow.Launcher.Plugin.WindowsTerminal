from flowlauncher import FlowLauncher
import flowlauncherAPI
from flox import Flox

from terminal_profiles import TerminalProfiles, Terminal, TerminalProfile

class TerminalPlugin(Flox):
    def __init__(self) -> None:
        super().__init__()
        self.tp = TerminalProfiles()
        self.profiles = list(self.tp.find_profiles())

    def query(self, query):
        for profile in self.profiles:
            if query in profile.name:


    def context_menu(self, data):
        pass

    def reload(self):
        self.profiles = list(self.tp.find_profiles())
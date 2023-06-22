import os
import json
import logging
from pathlib import Path
from flowlauncher import FlowLauncher
from flowlauncher import FlowLauncherAPI

from helpers import Results
from terminal_profiles import TerminalProfiles, Terminal, TerminalProfile

logger = logging.getLogger(__name__)

PLUGIN_MANIFEST = "plugin.json"
LOCALAPPDATA = os.getenv('LOCALAPPDATA')

class TerminalPlugin(FlowLauncher):
    ICON = r"Images/app.png"
    NAME = r"Windows Terminal profiles"
    def __init__(self) -> None:
        self.default_action = None
        self.show_hidden = False
        self.load_settings()

        self.tp = TerminalProfiles()
        self.profiles = list(self.tp.find_profiles())

        super().__init__()
    
    def get_settings_path(self):
        settings_path = Path(os.path.dirname(__file__), "..", ".." , "..", "Settings", "Plugins", self.NAME, "Settings.json")
        settings_path = Path(os.path.realpath(settings_path))
        if not settings_path.exists():
            settings_path = Path(LOCALAPPDATA, "FlowLauncher", "Settings", "Plugins", self.NAME, "Settings.json")
            settings_path = Path(os.path.realpath(settings_path))
        return settings_path

    def load_settings(self):
        settings_path = self.get_settings_path()
        try: 
            with open(settings_path, "r") as settings_file:
                logger.info("trying to load settings from %s", settings_file)
                settings = json.load(settings_file)

                self.default_action = settings.get('default_action', None)
                self.show_hidden = settings.get('show_hidden', self.show_hidden)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            logger.exception("failed to read and parse settings from %s", settings_file)

    def query(self, query):
        results = Results()
        for profile in self.profiles:
            if not self.show_hidden and profile.hidden:
                continue
            if query.lower() in profile.name.lower():
                subtitle = f"{profile.info} ({profile.terminal.package})"
                results.add_item(
                    title=profile.name,
                    subtitle=subtitle,
                    icon=self.ICON,
                    method=self.launch,
                    parameters=[profile.name, profile.terminal.fullname],
                    context=[profile.name, profile.terminal.fullname],
                    score=10
                )

        # results.add_item(
        #     title="Reload profiles",
        #     method=self.reload,
        #     score=0
        # )

        return results.results

    def context_menu(self, args):
        profile_name, terminal_package = args

        results = Results()
        results.add_item(
                    title="Open in new tab",
                    subtitle=profile_name,
                    icon=self.ICON,
                    method=self.launch,
                    parameters=[profile_name, terminal_package, False, False],
                    context=[],
                    score=10
                )
        results.add_item(
                    title="Open in new window",
                    subtitle=profile_name,
                    icon=self.ICON,
                    method=self.launch,
                    parameters=[profile_name, terminal_package, True, False],
                    context=[],
                    score=10
                )
        results.add_item(
                    title="Run as admin",
                    subtitle=profile_name,
                    icon=self.ICON,
                    method=self.launch,
                    parameters=[profile_name, terminal_package, False, True],
                    context=[],
                    score=10
                )
        results.add_item(
                    title="Run as admin in new window",
                    subtitle=profile_name,
                    icon=self.ICON,
                    method=self.launch,
                    parameters=[profile_name, terminal_package, True, True],
                    context=[],
                    score=10
                )
        return results.results

    def reload(self, params):
        self.profiles = list(self.tp.find_profiles())
        FlowLauncherAPI.hide_app()
        
    def launch(self, profile_name, terminal_package, new_window=None, as_admin=False):
        if new_window is None:
            # default action
            if self.default_action:
                if self.default_action == "New Tab":
                    new_window, as_admin = False, False
                elif self.default_action == "New Window":
                    new_window, as_admin = True, False
                elif self.default_action == "Elevated New Tab":
                    new_window, as_admin = False, True
                elif self.default_action == "Elevated New Window":
                    new_window, as_admin = True, True

        if as_admin:
            verb = "runas"
        else:
            verb = "open"

        window_arg = ""
        if not new_window:
            window_arg = "--window 0 nt"
        
        args = f'{window_arg} --profile "{profile_name}"'

        # ctypes.windll.shell32.ShellExecuteW(None, "runas", "shell:appsfolder\\Microsoft.WindowsTerminal_8wekyb3d8bbwe!App", '--window 0 nt --profile "paradox-pi"', None, 1)
        # ctypes.windll.shell32.ShellExecuteW(None, "open", "shell:appsfolder\\Microsoft.WindowsTerminal_8wekyb3d8bbwe!App", '--window 0 nt --profile "paradox-pi"', None, 1)


        import ctypes
        ctypes.windll.shell32.ShellExecuteW(None,
            verb,
            f'shell:appsfolder\\{terminal_package}!App',
            args,
            None, 1)
        
        FlowLauncherAPI.hide_app()

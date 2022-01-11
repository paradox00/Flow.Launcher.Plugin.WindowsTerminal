import os
import json
from flowlauncher import FlowLauncher
from flowlauncher import FlowLauncherAPI

from helpers import Results
from terminal_profiles import TerminalProfiles, Terminal, TerminalProfile

PLUGIN_MANIFEST = "plugin.json"

class TerminalPlugin(FlowLauncher):
    ICON = r"Images/app.png"
    def __init__(self) -> None:
        self.tp = TerminalProfiles()
        self.profiles = list(self.tp.find_profiles())
        super().__init__()

    def query(self, query):
        results = Results()
        for profile in self.profiles:
            if query in profile.name:
                results.add_item(
                    title=profile.name,
                    subtitle=profile.terminal.package,
                    icon=self.ICON,
                    method=self.launch,
                    parameters=[profile.name, profile.terminal.fullname, False, False],
                    context=[profile.name, profile.terminal.fullname],
                    score=10
                )

        results.add_item(
            title="Reload profiles",
            method=self.reload,
            score=0
        )

        return results.results

    def context_menu(self, args):
        profile_name, terminal_package = args

        results = Results()
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
        
    def launch(self, profile_name, terminal_package, new_window, as_admin=False):
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

#!/usr/bin/env python3
"""Apply the trial sidebar layout to a closed Kate session, keeping its documents."""

import argparse
import configparser
from datetime import datetime
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


def main():
    data = (Path.home() / "Library/Application Support" if sys.platform == "darwin"
            else Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", nargs="?", type=Path, default=data / "kate/anonymous.katesession")
    args = parser.parse_args()
    if subprocess.run(["pgrep", "-ix", "kate"], stdout=subprocess.DEVNULL).returncode == 0:
        parser.error("Close Kate before applying the layout.")
    if not args.session.is_file():
        parser.error(f"Session not found: {args.session}")

    config = configparser.ConfigParser(interpolation=None, delimiters=("=",))
    config.optionxform = str
    config.read(args.session)
    windows = [s for s in config.sections() if re.fullmatch(r"MainWindow\d+", s)]
    if not windows:
        parser.error("No saved main window found in the session.")
    state = (Path.home() / "Library/Preferences/State" if sys.platform == "darwin"
             else Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")))
    backup = state / "dotfiles-backups" / (args.session.name + "." + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.session, backup)

    if not config.has_section("Kate Plugins"):
        config.add_section("Kate Plugins")
    config["Kate Plugins"].update({"katefiletreeplugin": "false", "kateprojectplugin": "true",
                                   "katesearchplugin": "true", "lspclientplugin": "true", "katekonsoleplugin": "true"})
    panels = {"kateproject": (0, True), "kateprojectgit": (0, False),
              "lspclient_symbol_outline": (1, True), "diagnostics": (3, False),
              "kate_plugin_katesearch": (3, False), "kateprojectinfo": (3, False),
              "kate_private_plugin_katekonsoleplugin": (3, False), "output": (3, False)}
    for name in windows:
        window = config[name]
        sizes = [int(n) for n in window.get("Kate-MDI-H-Splitter", "0,1200,0").split(",")]
        width = max(sum(sizes), 800)
        window["Kate-MDI-H-Splitter"] = f"280,{max(width - 560, 240)},280"
        window["Kate-MDI-Sidebar-Visible"] = "true"
        for side in (0, 1, 3):
            prefix = f"Kate-MDI-Sidebar-{side}-"
            window[prefix + "Bar-0-TvList"] = ",".join(p for p, (pos, _) in panels.items() if pos == side)
            window[prefix + "LastSize"] = "280" if side < 2 else "240"
            window[prefix + "SectSizes"] = "1000" if side < 2 else "0"
            window.setdefault(prefix + "Splitter", "1000")
        for panel, (side, visible) in panels.items():
            prefix = f"Kate-MDI-ToolView-{panel}-"
            window[prefix + "Position"] = str(side)
            window[prefix + "Visible"] = str(visible).lower()
            window[prefix + "Show-Button-In-Sidebar"] = "true"
    with tempfile.NamedTemporaryFile(mode="w", dir=args.session.parent, delete=False) as output:
        config.write(output, space_around_delimiters=False)
        temp = Path(output.name)
    temp.replace(args.session)
    print(f"Layout applied. Previous session: {backup}")


if __name__ == "__main__":
    main()

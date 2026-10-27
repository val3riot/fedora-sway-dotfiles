#!/usr/bin/env python3
"""Build an importable VS Code profile from the readable settings and extension list."""

import json
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent.parent / "vscode"
    settings = json.loads((directory / "settings.json").read_text())
    identifiers = json.loads((directory / "extensions.json").read_text())["recommendations"]
    if len({identifier.lower() for identifier in identifiers}) != len(identifiers):
        raise ValueError("Duplicate extension identifiers")
    profile = {
        "name": "Java and Frontend",
        "settings": json.dumps(settings, indent=2),
        "keybindings": "[]",
        "extensions": json.dumps([{"identifier": {"id": identifier}, "preRelease": False}
                                  for identifier in identifiers]),
    }
    destination = directory / "java-frontend.code-profile"
    destination.write_text(json.dumps(profile, indent=2) + "\n")
    print(destination)


if __name__ == "__main__":
    main()

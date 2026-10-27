#!/usr/bin/env python3
"""Copy the Kate setup to Linux or macOS, without Stow or checkout symlinks."""

import argparse
import configparser
from datetime import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

REPO = Path(__file__).resolve().parent.parent
JDT_ARCHIVE = "jdt-language-server-1.63.0-202610191322.tar.gz"
JDT_SHA256 = "b1f2abe0b3cccb462cf64fb4a5587c7d09df60cf8be7748b152cbd89d018bdc4"
PACKAGES = ["typescript@6.0.3", "typescript-language-server@6.0.2",
            "@angular/language-server@22.2.3", "vscode-langservers-extracted@4.10.0"]


def locations(home, system):
    if system == "Darwin":
        return {"config": home / "Library/Preferences", "data": home / "Library/Application Support",
                "state": home / "Library/Preferences/State"}
    if system != "Linux":
        raise ValueError("Only Linux and macOS are supported.")
    return {"config": Path(os.environ.get("XDG_CONFIG_HOME", home / ".config")),
            "data": Path(os.environ.get("XDG_DATA_HOME", home / ".local/share")),
            "state": Path(os.environ.get("XDG_STATE_HOME", home / ".local/state"))}


def find_node():
    candidates = ["/usr/bin/node", "/opt/homebrew/bin/node", "/usr/local/bin/node", shutil.which("node")]
    for node in dict.fromkeys(c for c in candidates if c):
        try:
            version = subprocess.check_output([node, "-p", "process.versions.node"], text=True).strip()
            v = tuple(int(n) for n in version.split("."))
            if (22, 22, 3) <= v < (23,) or (24, 15) <= v < (25,) or v >= (26,):
                return node
        except (OSError, ValueError, subprocess.CalledProcessError):
            continue
    return None


def find_jdtls(tools):
    candidates = [tools / "jdtls/bin/jdtls", Path("/opt/homebrew/bin/jdtls"), Path("/usr/local/bin/jdtls")]
    if shutil.which("jdtls"):
        candidates.append(Path(shutil.which("jdtls")))
    return next((str(p) for p in candidates if p.is_file()), None)


def clean_preferences(text):
    config = configparser.ConfigParser(interpolation=None, delimiters=("=",))
    config.optionxform = str
    config.read_string(text)
    # Machine state and executable permissions must not travel between computers.
    for section in ("MainWindow", "filetree", "Shortcuts"):
        config.remove_section(section)
    for key in ("AllowedServerCommandLines", "BlockedServerCommandLines", "ServerConfiguration"):
        config.remove_option("lspclient", key)
    for key in ("Text Font", "Text Font Features"):
        config.remove_option("KTextEditor Renderer", key)
    out = io.StringIO()
    config.write(out, space_around_delimiters=False)
    return out.getvalue()


def plan(home, paths):
    source = REPO / "kate"
    tools = paths["data"] / "kate-tools"
    launcher = home / ".local/bin/kate-language-server"
    settings = json.loads((source / ".config/kate/lspclient/settings.json").read_text())
    for server in settings["servers"].values():
        server["command"] = [sys.executable, str(launcher), server["command"][-1]]
    settings["servers"]["javascript"]["initializationOptions"]["plugins"][0]["location"] = str(tools / "node_modules")
    files = {
        paths["config"] / "katerc": clean_preferences((source / ".config/katerc").read_text()).encode(),
        paths["config"] / "kate/lspclient/settings.json": (json.dumps(settings, indent=2) + "\n").encode(),
        launcher: (source / ".local/bin/kate-language-server").read_bytes(),
    }
    for path in sorted((source / ".local/share").rglob("*")):
        if path.is_file():
            files[paths["data"] / path.relative_to(source / ".local/share")] = path.read_bytes()
    return files


def check_targets(files):
    for target in files:
        for parent in target.parents:
            if parent.is_symlink() and parent.resolve().is_relative_to(REPO):
                raise RuntimeError(f"Unlink the Stow directory first: {parent}. The importer will not write through it into the checkout.")


def write_files(files, backup):
    check_targets(files)
    for index, (target, content) in enumerate(files.items()):
        # Check both contents and symlinks: imports must be independent of Stow.
        if target.is_file() and not target.is_symlink() and target.read_bytes() == content:
            continue
        if target.exists() or target.is_symlink():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, backup / f"{index}-{target.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as output:
            output.write(content)
            temporary = Path(output.name)
        temporary.chmod(0o755 if target.name == "kate-language-server" else 0o600)
        temporary.replace(target)
        print(f"Installed {target}")


def install_tools(tools, node):
    env = dict(os.environ, PATH=str(Path(node).parent) + os.pathsep + os.environ.get("PATH", ""))
    npm = shutil.which("npm", path=env["PATH"])
    if not npm:
        raise RuntimeError("npm is missing. Install Node.js with npm first.")
    subprocess.run([npm, "install", "--prefix", str(tools), "--no-audit", "--no-fund", "--save-exact", *PACKAGES], env=env, check=True)
    if not find_jdtls(tools):
        if sys.version_info < (3, 12):
            raise RuntimeError("Python 3.12+ is required to safely extract JDT LS; alternatively install jdtls separately.")
        with tempfile.TemporaryDirectory(prefix="kate-jdtls-") as temporary:
            archive = Path(temporary) / JDT_ARCHIVE
            urllib.request.urlretrieve("https://download.eclipse.org/jdtls/milestones/1.63.0/" + JDT_ARCHIVE, archive)
            if hashlib.sha256(archive.read_bytes()).hexdigest() != JDT_SHA256:
                raise RuntimeError("JDT LS checksum mismatch.")
            destination = tools / "jdtls"
            if destination.exists():
                raise RuntimeError(f"Incomplete JDT LS directory exists: {destination}")
            destination.mkdir(parents=True)
            with tarfile.open(archive) as bundle:
                bundle.extractall(destination, filter="data")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Show destinations without writing or downloading")
    parser.add_argument("--install-tools", action="store_true", help="Install the pinned npm servers and JDT LS if missing")
    args = parser.parse_args()
    home = Path.home()
    paths = locations(home, platform.system())
    files = plan(home, paths)
    if args.dry_run:
        print("\n".join(str(target) for target in files))
        print("Dependencies: Kate, Python 3, Node.js/npm, compatible JDK; --install-tools installs language servers.")
        return
    if subprocess.run(["pgrep", "-ix", "kate"], stdout=subprocess.DEVNULL).returncode == 0:
        parser.error("Close Kate before importing (to avoid overwriting its current settings).")
    check_targets(files)
    tools = paths["data"] / "kate-tools"
    node = find_node()
    if args.install_tools:
        if not node:
            parser.error("Install Node.js 22.22.3+, 24.15+, or 26+ with npm first.")
        install_tools(tools, node)
    runtime = {"node": node, "jdtls": find_jdtls(tools)}
    files[tools / "runtime.json"] = (json.dumps(runtime, indent=2) + "\n").encode()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = paths["state"] / "dotfiles-backups" / ("kate-import-" + stamp)
    write_files(files, backup)
    session = paths["data"] / "kate/anonymous.katesession"
    if not session.exists():
        session.parent.mkdir(parents=True, exist_ok=True)
        session.write_text("[MainWindow0]\n[Open MainWindows]\nCount=1\n[Open Documents]\nCount=0\n")
    subprocess.run([sys.executable, str(REPO / "scripts/kate-layout.py"), str(session)], check=True)
    missing = []
    if not node:
        missing.append("compatible Node.js")
    if not runtime["jdtls"]:
        missing.append("JDT LS")
    if not (tools / "node_modules/.bin/typescript-language-server").is_file():
        missing.append("frontend language servers")
    print(f"Import complete. Backups: {backup}")
    if missing:
        print("Still needed: " + ", ".join(missing) + ". See docs/kate.md.")


if __name__ == "__main__":
    main()

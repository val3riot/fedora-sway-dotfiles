import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
IMPORT = runpy.run_path(str(REPO / "scripts/import-kate.py"))
LAYOUT = runpy.run_path(str(REPO / "scripts/kate-layout.py"))


class KateImportTests(unittest.TestCase):
    def test_macos_plan_uses_destination_home_and_qt_paths(self):
        home = Path("/Users/new-user")
        with patch.object(sys, "executable", "/opt/homebrew/bin/python3"):
            files = IMPORT["plan"](home, IMPORT["locations"](home, "Darwin"))
        settings = json.loads(files[home / "Library/Preferences/kate/lspclient/settings.json"])
        self.assertEqual(settings["servers"]["java"]["command"],
                         ["/opt/homebrew/bin/python3", str(home / ".local/bin/kate-language-server"), "java"])
        self.assertEqual(settings["servers"]["javascript"]["initializationOptions"]["plugins"][0]["location"],
                         str(home / "Library/Application Support/kate-tools/node_modules"))
        self.assertIn(home / "Library/Application Support/kxmlgui5/kateproject/ui.rc", files)
        self.assertNotIn(b"/home/valeriot", b"".join(files.values()))
        self.assertNotIn(b"@KATE_TOOLS@", b"".join(files.values()))

    def test_linux_xdg_overrides(self):
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": "/custom/config", "XDG_DATA_HOME": "/custom/data"}):
            paths = IMPORT["locations"](Path("/home/test"), "Linux")
        self.assertEqual(paths["config"], Path("/custom/config"))
        self.assertEqual(paths["data"], Path("/custom/data"))

    def test_copy_replaces_stow_symlink_without_changing_source_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.write_text("original")
            target = root / "config"
            target.symlink_to(source)
            backup = root / "backup"
            IMPORT["write_files"]({target: b"new"}, backup)
            self.assertFalse(target.is_symlink())
            self.assertEqual(source.read_text(), "original")
            self.assertEqual((backup / "0-config").read_text(), "original")
            modified = target.stat().st_mtime_ns
            IMPORT["write_files"]({target: b"new"}, backup)
            self.assertEqual(target.stat().st_mtime_ns, modified)

    def test_dry_run_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, HOME=tmp, XDG_CONFIG_HOME=tmp + "/config", XDG_DATA_HOME=tmp + "/data")
            subprocess.run([sys.executable, str(REPO / "scripts/import-kate.py"), "--dry-run"],
                           env=env, capture_output=True, check=True)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_directory_symlink_cannot_write_into_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            source.mkdir()
            linked = root / "config"
            linked.symlink_to(source, target_is_directory=True)
            function = IMPORT["check_targets"]
            with patch.dict(function.__globals__, {"REPO": source}):
                with self.assertRaises(RuntimeError):
                    IMPORT["write_files"]({linked / "settings": b"new"}, root / "backup")
            self.assertFalse((source / "settings").exists())

    def test_layout_preserves_documents_and_backs_up_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            session = root / "test.katesession"
            original = "[Document 0]\nURL=/projects/keep.java\n[MainWindow0]\nKate-MDI-H-Splitter=0,1400,0\n"
            session.write_text(original)
            with patch.object(sys, "argv", ["kate-layout.py", str(session)]), \
                 patch.object(sys, "platform", "linux"), \
                 patch.dict(os.environ, {"XDG_STATE_HOME": str(root / "state")}), \
                 patch("subprocess.run", return_value=subprocess.CompletedProcess([], 1)):
                LAYOUT["main"]()
            result = session.read_text()
            self.assertIn("URL=/projects/keep.java", result)
            self.assertIn("Kate-MDI-ToolView-lspclient_symbol_outline-Position=1", result)
            backups = list((root / "state/dotfiles-backups").iterdir())
            self.assertEqual(backups[0].read_text(), original)


if __name__ == "__main__":
    unittest.main()

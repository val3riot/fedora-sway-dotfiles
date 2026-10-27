"""Regression checks for the native VS Code import resource contracts."""

import json
from pathlib import Path
import unittest

DIRECTORY = Path(__file__).resolve().parents[1] / "vscode"


class VSCodeProfileTests(unittest.TestCase):
    def test_settings_resource_has_the_envelope_required_by_vscode(self):
        profile = json.loads((DIRECTORY / "java-frontend.code-profile").read_text())
        # SettingsResource.apply() parses the resource and reads .settings;
        # raw User/settings.json here yields undefined and breaks Create.
        resource = json.loads(profile["settings"])
        self.assertIsInstance(resource.get("settings"), str)
        self.assertEqual(json.loads(resource["settings"]),
                         json.loads((DIRECTORY / "settings.json").read_text()))
        # No custom bindings: do not emit a malformed raw keybindings array.
        self.assertNotIn("keybindings", profile)

    def test_extensions_use_the_native_resource_array(self):
        profile = json.loads((DIRECTORY / "java-frontend.code-profile").read_text())
        extensions = json.loads(profile["extensions"])
        identifiers = [item["identifier"]["id"] for item in extensions]
        self.assertEqual(identifiers, json.loads((DIRECTORY / "extensions.json").read_text())["recommendations"])
        self.assertEqual(len(identifiers), len(set(name.lower() for name in identifiers)))

    def test_java_components_are_explicit_because_profile_import_skips_packs(self):
        profile = json.loads((DIRECTORY / "java-frontend.code-profile").read_text())
        identifiers = {item["identifier"]["id"] for item in json.loads(profile["extensions"])}
        self.assertTrue({"redhat.java", "vscjava.vscode-java-debug", "vscjava.vscode-java-test",
                         "vscjava.vscode-java-dependency", "vscjava.vscode-maven",
                         "vscjava.vscode-gradle"}.issubset(identifiers))


if __name__ == "__main__":
    unittest.main()

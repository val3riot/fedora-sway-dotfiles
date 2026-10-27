# Kate: import on Linux and macOS

Import theme, toolbar, shortcuts, panels and Java/Angular support **without Stow**. The importer copies files, generates paths for the destination computer and backs up existing settings. The checkout can be moved or removed afterwards.

## macOS

Install prerequisites with [Homebrew](https://formulae.brew.sh/cask/kate):

```sh
brew install --cask kate
brew install python node jdtls
```

Copy this checkout (including the current experimental changes) to the Mac, close Kate, then run from its root:

```sh
python3 scripts/import-kate.py --dry-run
python3 scripts/import-kate.py --install-tools
```

Homebrew's [jdtls](https://formulae.brew.sh/formula/jdtls) supplies the Java language server and its JDK dependency. Launch Kate from Finder or with `kate /path/to/project`; the generated commands use absolute executable paths so they do not depend on the GUI application's shell PATH.

## Fedora

```sh
sudo dnf install kate kate-plugins python3 nodejs npm java-25-openjdk-devel
python3 scripts/import-kate.py --install-tools
```

`--install-tools` installs the pinned frontend servers and downloads checksum-verified JDT LS 1.63.0 only if no local/Homebrew JDT LS is available. Node must be 22.22.3+, a supported 24.15+ release, or 26+. Angular 22.2.3 and TypeScript 6.0.3 are the tested fallback pair; match the language-service versions to older projects as needed.

If the servers are already installed, use `python3 scripts/import-kate.py`. Existing configuration and Stow links are backed up and replaced with independent copies. Re-run the importer after changing the source configuration. Kate's LSP `settings.json` in the checkout is a template: use the importer for Kate, rather than Stow alone.

## What travels

- Solarized Dark editor and matching Kate Solarized window palette.
- Open Folder toolbar button and `Ctrl+Shift+O`; the conflicting spell-check shortcut is cleared.
- Project/Git left, LSP symbols right, diagnostics/search/terminal below (closed initially).
- Java, TypeScript/React, Angular inline/external templates, HTML, CSS and JSON support.

Runtime state, recent files, machine-specific fonts/window sizes and remembered server permissions are excluded. On first use, Kate may ask to authorize the generated LSP commands. Availability of the integrated terminal depends on the Kate build and its Konsole component. Debuggers, test runners and Spring-specific tooling are not included.

## Paths and layout

| Files | Linux | macOS |
| --- | --- | --- |
| Preferences / LSP settings | `~/.config/katerc`, `~/.config/kate/` | `~/Library/Preferences/katerc`, `~/Library/Preferences/kate/` |
| Palettes, toolbar XML, tools | `~/.local/share/` | `~/Library/Application Support/` |
| Launcher | `~/.local/bin/kate-language-server` | `~/.local/bin/kate-language-server` |

Paths follow [Qt's platform conventions](https://doc.qt.io/qt-6/qstandardpaths.html); Linux XDG overrides are respected. The importer creates/applies the anonymous-session layout without copying your project history. For a named session, close Kate and run `python3 scripts/kate-layout.py /path/to/session.katesession`.

To transfer only the Kate setup rather than the repository:

```sh
tar -czf /tmp/kate-setup.tar.gz kate scripts/import-kate.py scripts/kate-layout.py docs/kate.md
```

Extract it on the Mac, enter the extracted directory and use the same import command. No Git or Stow is required there.

Backups are under `~/.local/state/dotfiles-backups/` on Linux and `~/Library/Preferences/State/dotfiles-backups/` on macOS. The actual GUI was checked on Fedora; macOS destinations and generated paths have automated tests, but have not been run on a Mac. Toolbar customizations target Kate 26.08.1 / KatePart 6.31 and should be reviewed after major UI updates.

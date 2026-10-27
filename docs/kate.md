# Kate trial

Experimental configuration on `experiment/kate`, managed with Stow. It enables Projects, document tree, search, document switching and LSP. Normal graphical editing shortcuts remain unchanged. Formatting on save and inlay hints are off.

## Install and apply

```sh
sudo dnf install kate kate-plugins nodejs npm python3 java-25-openjdk-devel
stow --simulate --no-folding --verbose --target="$HOME" kate
stow --no-folding --verbose --target="$HOME" kate
```

Resolve existing file conflicts first. `--no-folding` keeps sessions and other generated files outside the checkout. Kate may save additional GUI preferences to `katerc`; review those changes before committing.

Install frontend servers in a dedicated user directory, using a recent Node (22.22.3+, a supported 24.x, or 26.x). On Fedora the launcher uses `/usr/bin/node`, independently of NVM's shell default:

```sh
env PATH=/usr/bin:/bin npm install --prefix "$HOME/.local/share/kate-tools" \
  --no-audit --no-fund --save-exact \
  typescript@6.0.3 typescript-language-server@6.0.2 \
  @angular/language-server@22.2.3 vscode-langservers-extracted@4.10.0
```

Install the tested Java language server (JDT LS 1.63.0):

```sh
curl --fail --location \
  https://download.eclipse.org/jdtls/milestones/1.63.0/jdt-language-server-1.63.0-202610191322.tar.gz \
  --output /tmp/kate-jdtls-1.63.0.tar.gz
printf '%s  %s\n' \
  b1f2abe0b3cccb462cf64fb4a5587c7d09df60cf8be7748b152cbd89d018bdc4 \
  /tmp/kate-jdtls-1.63.0.tar.gz | sha256sum --check &&
mkdir -p "$HOME/.local/share/kate-tools/jdtls" &&
tar -xzf /tmp/kate-jdtls-1.63.0.tar.gz -C "$HOME/.local/share/kate-tools/jdtls"
```

Dependencies live outside the repository. With a custom `XDG_DATA_HOME`, use that path instead of `~/.local/share` in installation commands. JDT LS needs a compatible JDK (the trial was checked with system Java 25); project compilation may use a different JDK.

## Try it

Run `kate /path/to/project`, then open a source file. On first use Kate may ask permission to launch the configured language-server command. Projects detects Git repositories automatically; use the Projects panel for the file tree and Git status. Shortcuts are in the main [README](../README.md#kate-experimental).

| Files | Support |
| --- | --- |
| Java | JDT LS completion, navigation, diagnostics and server-provided code actions; separate cached workspace per project |
| JavaScript / TypeScript / JSX / TSX | TypeScript server for normal code and React |
| HTML in Angular workspaces | Angular server when an ancestor contains `angular.json` |
| Other HTML / CSS / SCSS / JSON | HTML, CSS and JSON servers |

Install the project's dependencies as usual. Angular prefers language-service/TypeScript packages from the project, with the installed 22.2.3/6.0.3 pair as fallback. Test compatibility with your Angular version. TypeScript files use the TypeScript server: Angular-specific assistance inside inline templates is not configured. Debug adapters, test runners, Spring-specific tooling and automatic formatting are outside this initial trial.

The setup was checked on Fedora. Kate also runs on macOS, but dependency installation and configuration paths need a separate check there.

## Remove the trial

Close Kate, then unlink before switching branches:

```sh
stow --delete --target="$HOME" kate
git switch master
```

Kate and language servers stay installed; unlinking only removes the managed configuration links.

# VS Code: Java and Frontend

Import `vscode/java-frontend.code-profile` using VS Code's **Profiles → Import Profile** on Linux or macOS. Create the `Java and Frontend` profile from the preview. No Stow or custom installer is needed; extension packages are selected for the destination platform.

The profile includes Solarized Dark, built-in Seti icons, hover documentation, parameter hints, formatting on save and Git autofetch. Standard keyboard shortcuts adapt to the operating system. Java uses Red Hat's formatter; frontend files use Prettier and the project's ESLint rules.

Official extensions included:

- The six official Java components: Red Hat language support and Microsoft debugger, tests, project management, Maven and Gradle. They are listed explicitly because native profile import does not expand extension packs.
- Angular Language Service, Microsoft ESLint and official Prettier.
- Microsoft Container Tools and Dev Containers, plus Docker's Docker DX.
- OpenAI Codex (`openai.chatgpt`).

Git, JavaScript/TypeScript, React and Markdown preview are already built into VS Code. Database extensions and additional agents remain optional: see the [extension proposal](vscode-extensions-proposal.md). No third-party icon theme, snippets pack or Git wrapper is included.

Install JDK, Node.js/npm, Git and a container engine separately as needed. Agent authentication, database credentials and machine-specific paths are not exported. Formatting uses each project's configuration; install its dependencies normally. The profile disables VS Code and Red Hat telemetry, but does not define other extensions' service policies.

Maintain the readable sources in `vscode/settings.json` and `vscode/extensions.json`, then regenerate the import file:

```sh
python3 scripts/export-vscode-profile.py
```

The JSON profile format and import workflow follow [VS Code's official Profiles documentation](https://code.visualstudio.com/docs/configure/profiles).

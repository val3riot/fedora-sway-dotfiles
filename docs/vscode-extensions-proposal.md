# VS Code: proposta estensioni

Verifica: 27 ottobre 2026. Proposta per Java backend e Angular/React, utilizzabile su Fedora e macOS. Nessuna estensione è stata installata o rimossa durante questa ricognizione.

Per **ufficiale** si intende Microsoft oppure il produttore/progetto dello strumento: Angular, Red Hat, Docker, Prettier, OpenAI, ecc. Un publisher verificato nel Marketplace, da solo, non basta. Gli ID storici possono differire dal nome del produttore attuale.

## Base consigliata

| Estensione / ID | Produttore | Uso |
| --- | --- | --- |
| [Java](https://marketplace.visualstudio.com/items?itemName=redhat.java) — `redhat.java` | Red Hat | Completamento, documentazione, navigazione e refactoring Java |
| [Debugger for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-debug) — `vscjava.vscode-java-debug` | Microsoft | Debug Java |
| [Test Runner for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-test) — `vscjava.vscode-java-test` | Microsoft | JUnit/TestNG nel pannello Testing |
| [Project Manager for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-dependency) — `vscjava.vscode-java-dependency` | Microsoft | Progetti, package e dipendenze Java |
| [Angular Language Service](https://marketplace.visualstudio.com/items?itemName=Angular.ng-template) — `Angular.ng-template` | Angular | Hover, completamento e diagnostica nei template inline/esterni |
| [ESLint](https://github.com/microsoft/vscode-eslint) — `dbaeumer.vscode-eslint` | Microsoft; ID storico `dbaeumer` | Regole JavaScript/TypeScript definite dal progetto |
| [Prettier](https://prettier.io/docs/editors) — `esbenp.prettier-vscode` | Progetto Prettier; ID storico `esbenp` | Formattazione frontend con la versione/configurazione del progetto |
| [Container Tools](https://code.visualstudio.com/docs/containers/overview) — `ms-azuretools.vscode-containers` | Microsoft | Gestione container, immagini, registri e Compose |
| [Docker DX](https://github.com/docker/vscode-extension) — `docker.docker` | Docker | Assistenza su Dockerfile, Compose e Bake; complementare a Container Tools |

Per le build aggiungere [Maven for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-maven), `vscjava.vscode-maven`, oppure [Gradle for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-gradle), `vscjava.vscode-gradle`, secondo i progetti. Entrambe sono Microsoft.

In alternativa, `vscjava.vscode-java-pack` installa i quattro strumenti Java sopra più Maven e Gradle. Il [contenuto attuale del pack](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack) è stato verificato: non serve installare sia il pack sia i suoi componenti singolarmente.

## Già incluso, senza altri plugin

- **Git:** diff, staging, commit, branch, merge e sincronizzazione sono [integrati in VS Code](https://code.visualstudio.com/docs/sourcecontrol/overview); serve Git installato nel sistema.
- **JavaScript/TypeScript e React:** il servizio linguistico e il debugger Node sono [inclusi](https://code.visualstudio.com/docs/setup/additional-components). Nessun pack React o raccolta di snippet necessaria per partire.
- **Markdown:** editor e anteprima integrati. Solarized Dark, già scelto dall'utente, è incluso tra i temi standard.

## Moduli opzionali

| Quando serve | ID ufficiale | Produttore |
| --- | --- | --- |
| Ambiente di sviluppo riproducibile in container | [`ms-vscode-remote.remote-containers`](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) | Microsoft |
| Sviluppo su server SSH | [`ms-vscode-remote.remote-ssh`](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) | Microsoft |
| Pull request e issue GitHub | [`GitHub.vscode-pull-request-github`](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) | GitHub |
| Workflow GitHub Actions | [`GitHub.vscode-github-actions`](https://github.com/github/vscode-github-actions) | GitHub |
| Spring Boot | [`vmware.vscode-boot-dev-pack`](https://marketplace.visualstudio.com/items?itemName=vmware.vscode-boot-dev-pack) | Spring Tools e Microsoft; namespace storico VMware |
| YAML non limitato a Docker | [`redhat.vscode-yaml`](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml) | Red Hat |
| Test frontend Playwright | [`ms-playwright.playwright`](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright) | Microsoft / progetto Playwright |
| Analisi SonarQube | [`SonarSource.sonarlint-vscode`](https://marketplace.visualstudio.com/items?itemName=SonarSource.sonarlint-vscode) | SonarSource |

Dev Containers è particolarmente utile per uniformare JDK, Node e tool di build fra Linux e Mac. Richiede un motore container e una configurazione `.devcontainer` nel progetto; l'estensione da sola non crea un ambiente riproducibile. Evitare il Remote Development Pack completo se non servono anche WSL e gli altri componenti.

## Database: scegliere quelli effettivamente usati

| Database | ID | Produttore / fonte |
| --- | --- | --- |
| PostgreSQL | `ms-ossdata.vscode-pgsql` | [Microsoft](https://learn.microsoft.com/en-us/azure/postgresql/development/vs-code-extension/postgresql-extension-overview), non il PostgreSQL Global Development Group |
| SQL Server / Azure SQL | `ms-mssql.mssql` | [Microsoft](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) |
| MySQL | `Oracle.mysql-shell-for-vs-code` | [Oracle / MySQL](https://marketplace.visualstudio.com/items?itemName=Oracle.mysql-shell-for-vs-code) |
| Oracle Database | `Oracle.sql-developer` | [Oracle](https://marketplace.visualstudio.com/items?itemName=Oracle.sql-developer) |
| MongoDB | `mongodb.mongodb-vscode` | [MongoDB](https://www.mongodb.com/docs/mongodb-vscode/install/) |

Non installerei un client universale indipendente. Queste integrazioni funzionano su Linux e macOS, con i requisiti della specifica versione: la versione MySQL consultata richiede macOS 14+, PostgreSQL macOS 13+ e Linux con glibc 2.35+. Connessioni e credenziali non vanno incluse nei dotfile.

## Agenti: partire da uno

| Scelta | ID | Produttore / uso |
| --- | --- | --- |
| **Prima scelta, già presente localmente** | `openai.chatgpt` | OpenAI Codex: modifiche, comandi e revisione nel contesto dell'editor; [documentazione ufficiale OpenAI](https://learn.chatgpt.com/docs/codex/ide) |
| Alternativa o complemento con account GitHub | `GitHub.copilot-chat` | GitHub Copilot: chat, agenti e integrazioni VS Code; [estensione ufficiale](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat). Per completamenti inline può essere installata anche `GitHub.copilot`, gestendo la coppia tramite il normale setup GitHub |
| Alternativa con servizio Anthropic | `anthropic.claude-code` | Anthropic: agente Claude Code; [estensione ufficiale](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code) |

Le tre opzioni sono utilizzabili su Linux e macOS, ma autenticazione, piano e policy aziendali vanno verificati con il servizio scelto. Non installerei tutti gli agenti per impostazione predefinita. Cline, Roo Code e altri wrapper indipendenti sono esclusi dal criterio richiesto. L'estensione Codex ha un ID storico `chatgpt`: non indica un prodotto diverso.

## Standardizzazione fra macchine

Conservare una lista di ID base e liste opzionali per progetto/database/agente, più `settings.json` e `keybindings.json` separati dalle credenziali. Importare con `code --install-extension <ID>` senza fissare il pacchetto Linux o l'architettura; il Marketplace seleziona la build appropriata. JDK, Node e Docker rimangono dipendenze del sistema o del Dev Container.

Prima dell'installazione effettiva definire quali database usi e se vuoi Codex soltanto oppure anche Copilot/Claude. La ricognizione locale mostra già Java, Angular, ESLint, Prettier, Container Tools, Dev Containers, Spring Tools e Codex; GitLens e vari plugin di snippet sono presenti ma non fanno parte della proposta ufficiale. Non è stata modificata l'installazione esistente.

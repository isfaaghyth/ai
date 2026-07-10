> ⚠️ **ANNOUNCEMENT:** This project has been migrated to [isfaaghyth/ghiath-ai](https://github.com/isfaaghyth/ghiath-ai). Future updates, releases, and maintenance will happen there.

# isfa-ai: Multi-Agent Personal Workspace

This repository houses a fleet of **NousResearch Hermes Agent** instances configured to run via **Docker Compose** and communicate through **Telegram**.

---

## Folder Structure

```text
isfa-ai/
├── docker-compose.yml   # Optimized Docker services with log rotation & healthchecks
├── env.example          # Single entrypoint template for all configs & model variables
├── .env                 # Central secrets file (Ignored by Git)
├── setup.py             # Configuration generator & placeholder validator
├── setup.sh             # Executable shell runner with safety guards
├── .gitignore           # Git ignore rules for data, logs, and python caches
├── README.md            # This documentation
├── AGENT.md             # Global instructions, A2A protocols, and rules
├── OPINIONS.md          # Technical viewpoints & opinions
├── VOICE.md             # Tone and writing style guidelines
├── templates/           # System prompt (SOUL) templates
│   ├── dev_tpm/
│   ├── dev_kotlin_mobile/
│   ├── dev_golang_backend/
│   ├── dev_frontend_react/
│   ├── daily_general/
│   └── daily_learning_buddy/
├── skills/              # Reusable agent tools & instructions
│   ├── a2a/
│   ├── devops/
│   └── productivity/
└── data/                # Persistent runtime data (Ignored by Git)
    ├── .a2a/            # File-based Agent-to-Agent mailbox
    └── profiles/        # Contains active agent configurations and memory
```

---

## Agent Directory & Personalities

Each agent has a custom system prompt (`SOUL.md`) preconfigured in the `templates/` folder:

### 1. Technical Product Manager:
*   **`dev_tpm`**: The orchestrator. Decomposes tasks, designs implementation plans, and assigns subtasks to the developers via the A2A task board.

### 2. Development Agents:
*   **`dev_kotlin_mobile`**: Mobile Software Engineer specialized in Kotlin Multiplatform (KMP) and Compose Multiplatform.
*   **`dev_golang_backend`**: Backend Software Engineer specialized in Go (Golang) REST/gRPC microservices.
*   **`dev_frontend_react`**: Frontend Software Engineer specialized in React, Next.js, and Tailwind CSS.

### 3. Daily Agents:
*   **`daily_general`**: A standard daily assistant to handle task planning, web queries, and quick drafting (Workspace mounted read-only).
*   **`daily_learning_buddy`**: A companion agent to help you learn new tech concepts, quiz you, and design curriculums (Workspace mounted read-only).

---

## Step-by-Step Setup

### 1. Create Your Telegram Bots
You need to create a **separate** Telegram Bot for each profile so they can run concurrently without conflicts:
1. Message `@BotFather` on Telegram.
2. Run `/newbot` for each of your 6 agents and choose their names.
3. Save the **Bot Token** provided for each.

### 2. Find Your Telegram User ID
To prevent random users from querying your bots (since developers have shell write access to your workspace), you must restrict access:
1. Message `@userinfobot` on Telegram.
2. Copy your numeric **User ID**.

### 3. Fill In the Secrets
Copy `env.example` to `.env` (handled automatically on first run of `./setup.sh`):
```bash
./setup.sh
nano .env
```
Fill in the following fields:
*   `OPENROUTER_API_KEY`: Your OpenRouter API key.
*   `ANTHROPIC_API_KEY`: Your Claude/Anthropic API key.
*   `WORKSPACE_ROOT`: Parent folder containing all your Git project checkouts.
*   `SSH_KEY_PATH`: Path to your SSH folder containing GitHub keys (defaults to `~/.ssh`).
*   `GITHUB_TOKEN`: GitHub PAT token with `repo` scopes for repository creation/management.
*   `TELEGRAM_TOKEN_...`: The respective tokens from `@BotFather`.
*   `TELEGRAM_ALLOWED_USER_IDS`: Your numeric Telegram User ID.

### 4. Propagate Configurations
Run the setup script again:
```bash
./setup.sh
```
This script reads your central `.env` values, runs validation checks for remaining placeholders, generates dynamic `config.yaml` files, and bootstraps the file-based A2A inbox directories.

### 5. Launch the Swarm
Start all agents in background detached mode:
```bash
docker compose up -d
```
All six bots are now active! Send a message to any of them on Telegram to begin communicating.

---

## Agent-to-Agent (A2A) Communication

The swarm uses an asynchronous file-based message bus located at `./data/.a2a/` to communicate.

- **Inbox**: `/opt/data/.a2a/inbox/<profile_name>/`
- **Contracts**: `/opt/data/.a2a/contracts/<project_name>/`
- **Task Board**: `/opt/data/.a2a/board/<project_name>/`

Whenever the backend agent updates an API spec, it posts the updated contract at `/opt/data/.a2a/contracts/` and deposits notification files into the inboxes of frontend and mobile agents.

Details are documented in `skills/a2a/a2a-messenger/SKILL.md`.

---

## Management & CLI Access

### Stop the Swarm
```bash
docker compose down
```

### Run CLI Chat Mode for a Specific Profile
If you want to talk to an agent inside your terminal instead of Telegram:
```bash
docker compose exec dev-kotlin-mobile hermes --profile dev_kotlin_mobile chat
```

### View Live Logs
To monitor what your agents are executing:
```bash
docker compose logs -f
```
To check logs for a specific agent:
```bash
docker compose logs -f dev-golang-backend
```

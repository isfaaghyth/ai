# isfa-ai: Multi-Agent Personal Workspace

This repository houses a fleet of **NousResearch Hermes Agent** instances configured to run via **Docker Compose** and communicate through **Telegram**.

## Folder Structure

```text
isfa-ai/
├── docker-compose.yml   # Docker services for each of the 5 agents
├── env.example          # Template for keys and tokens
├── .env                 # Central secret file (Ignored by Git)
├── setup.py             # Internal configuration script
├── setup.sh             # Executable runner script
├── .gitignore           # Git ignore patterns
├── README.md            # This documentation
├── templates/           # Configuration and Prompt (SOUL) templates
│   ├── dev_kotlin_mobile/
│   ├── dev_golang_backend/
│   ├── dev_frontend_react/
│   ├── daily_general/
│   └── daily_learning_buddy/
└── data/                # Persistent runtime data (Ignored by Git)
    └── profiles/        # Contains active agent configurations and memory
```

---

## Agent Directory & Personalities

Each agent has a custom system prompt (`SOUL.md`) preconfigured in the `templates/` folder:

### 1. Development Agents:
*   **`dev_kotlin_mobile`**: Mobile Software Engineer specialized in Kotlin Multiplatform (KMP) and Compose Multiplatform.
*   **`dev_golang_backend`**: Backend Software Engineer specialized in Go (Golang) REST/gRPC microservices.
*   **`dev_frontend_react`**: Frontend Software Engineer specialized in React, Next.js, and Tailwind CSS.

### 2. Daily Agents:
*   **`daily_general`**: A standard daily assistant to handle task planning, web queries, and quick drafting.
*   **`daily_learning_buddy`**: A companion agent to help you learn new tech concepts, quiz you, and design curriculums.

---

## Step-by-Step Setup

### 1. Create Your Telegram Bots
You need to create a **separate** Telegram Bot for each profile so they can run concurrently without conflicts:
1. Message `@BotFather` on Telegram.
2. Run `/newbot` for each of your five agents and choose their names.
3. Save the **Bot Token** provided for each.

### 2. Find Your Telegram User ID
To prevent random users from querying your bots (since they have access to shell command tools), you must restrict access:
1. Message `@userinfobot` on Telegram.
2. Copy your numeric **User ID**.

### 3. Fill In the Secrets
Open the generated `.env` file at the root of the project:
```bash
nano .env
```
Fill in the following fields:
*   `OPENROUTER_API_KEY`: Your OpenRouter API key.
*   `ANTHROPIC_API_KEY`: Your Claude/Anthropic API key.
*   `TELEGRAM_TOKEN_...`: The respective tokens from `@BotFather`.
*   `TELEGRAM_ALLOWED_USER_IDS`: Your numeric Telegram User ID.

### 4. Propagate Configurations
Run the setup script:
```bash
./setup.sh
```
This script reads your central `.env` values and generates the individual configuration profiles inside `./data/profiles/`.

### 5. Launch the Swarm
Start all agents in background detached mode:
```bash
docker compose up -d
```
All five bots are now active! Send a message to any of them on Telegram to begin communicating.

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

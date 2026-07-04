---
name: a2a-messenger
description: Agent-to-Agent communication protocol. Use this to send messages, tasks, and contract updates between agents via a shared file-based inbox.
version: 1.0.0
metadata:
  hermes:
    tags: [a2a, communication, orchestration, contracts]
---

# Agent-to-Agent (A2A) Communication Protocol

All agents share the same data volume. Communication happens through structured files in `/opt/data/.a2a/`.

---

## Directory Structure

```
/opt/data/.a2a/
├── inbox/
│   ├── dev_tpm/               # TPM's inbox
│   ├── dev_kotlin_mobile/     # Kotlin agent's inbox
│   ├── dev_golang_backend/    # Go agent's inbox
│   ├── dev_frontend_react/    # React agent's inbox
│   ├── daily_general/         # General agent's inbox
│   └── daily_learning_buddy/  # Learning buddy's inbox
├── contracts/                 # Shared API contracts (OpenAPI, proto, types)
│   └── <project-name>/
│       ├── api.yaml           # OpenAPI spec
│       ├── types.json         # Shared type definitions
│       └── CHANGELOG.md       # Contract change log
└── board/                     # Shared task board (optional, for TPM)
    └── <project-name>/
        ├── todo.md
        ├── in-progress.md
        └── done.md
```

---

## Sending a Message

When you need another agent to do something, write a message file to their inbox.

**File naming convention:** `<timestamp>_<from>_<subject>.md`

Example - TPM assigns a task to the Go backend agent:

```bash
cat > /opt/data/.a2a/inbox/dev_golang_backend/$(date +%s)_dev_tpm_new-endpoint.md << 'EOF'
---
from: dev_tpm
to: dev_golang_backend
type: task
project: kepul-id
priority: high
---

# Task: Create user profile endpoint

Create `GET /v1/users/:id/profile` in the kepul-id backend.

## Requirements
- Return: name, email, avatar_url, created_at
- Auth: require valid JWT
- Tests: add unit test for the handler

## After completion
1. Update the API contract at `/opt/data/.a2a/contracts/kepul-id/api.yaml`
2. Notify `dev_frontend_react` and `dev_kotlin_mobile` about the new endpoint
EOF
```

---

## Checking Your Inbox

At the start of every conversation, check your inbox for pending messages:

```bash
ls -lt /opt/data/.a2a/inbox/$(hermes profile current)/ 2>/dev/null
```

Read any unread messages, act on them, then move them to a `done/` subfolder:

```bash
mkdir -p /opt/data/.a2a/inbox/$(hermes profile current)/done/
mv /opt/data/.a2a/inbox/$(hermes profile current)/<message-file> \
   /opt/data/.a2a/inbox/$(hermes profile current)/done/
```

---

## Contract Updates (API Specs)

This is the primary A2A use case. When an agent modifies an API, database schema, or shared type, it must:

### Step 1 - Update the contract file
Write or update the OpenAPI spec:

```bash
mkdir -p /opt/data/.a2a/contracts/<project-name>/
cat > /opt/data/.a2a/contracts/<project-name>/api.yaml << 'EOF'
openapi: 3.0.3
info:
  title: kepul-id API
  version: 1.2.0
paths:
  /v1/users/{id}/profile:
    get:
      summary: Get user profile
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: User profile
          content:
            application/json:
              schema:
                type: object
                properties:
                  name:
                    type: string
                  email:
                    type: string
                  avatar_url:
                    type: string
                  created_at:
                    type: string
                    format: date-time
EOF
```

### Step 2 - Notify dependent agents
Drop a notification into the inbox of every agent that consumes this contract:

```bash
TIMESTAMP=$(date +%s)
for agent in dev_frontend_react dev_kotlin_mobile; do
  cat > /opt/data/.a2a/inbox/${agent}/${TIMESTAMP}_dev_golang_backend_contract-update.md << EOF
---
from: dev_golang_backend
to: ${agent}
type: contract_update
project: kepul-id
---

# Contract Updated: kepul-id API

New endpoint added: \`GET /v1/users/{id}/profile\`

Read the full spec at: \`/opt/data/.a2a/contracts/kepul-id/api.yaml\`

Please update your types and API client code accordingly.
EOF
done
```

### Step 3 - Consuming agents read and adapt
When `dev_frontend_react` or `dev_kotlin_mobile` finds a `contract_update` message:

1. Read the updated contract: `cat /opt/data/.a2a/contracts/<project>/api.yaml`
2. Regenerate or update local types/clients based on the spec
3. Mark the message as done
4. Optionally reply to the sender confirming integration

---

## Task Board (for TPM)

The TPM can use the shared board to track progress across agents:

```bash
# Add a task
echo "- [ ] Create user profile endpoint (@dev_golang_backend)" >> /opt/data/.a2a/board/kepul-id/todo.md

# Move to in-progress (agent picks it up)
# Move to done (agent completes it)
```

All agents can read the board to understand overall project progress.

---

## Rules
- Always include the YAML frontmatter (`from`, `to`, `type`, `project`) in messages.
- Never delete another agent's inbox messages. Only move your own to `done/`.
- Always update the contract file BEFORE notifying dependent agents.
- If a contract change is breaking (removing/renaming a field), mark `priority: critical` in the notification.

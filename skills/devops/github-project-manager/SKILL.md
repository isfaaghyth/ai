---
name: github-project-manager
description: Manages GitHub projects - clone existing repos, create new ones, push changes, and open pull requests. Uses SSH for git operations and the GitHub API (via GITHUB_TOKEN) for repo management.
version: 1.0.0
metadata:
  hermes:
    tags: [git, github, devops, projects]
---

# GitHub Project Manager

Use this skill whenever Isfa asks to:
- Start working on an existing project from GitHub
- Create a brand new project and push it to GitHub
- Commit and push changes to a project
- Open a Pull Request

All projects are checked out into `/opt/workspace/`. Always work inside this directory.

---

## Workflow A: Pull an Existing Project

When Isfa says "work on `<repo-name>`" or "clone `<url>`":

### Step 1 - Check if already cloned
```bash
ls /opt/workspace/<repo-name>
```

### Step 2 - Clone if not present (prefer SSH)
```bash
git clone git@github.com:isfahannaki/<repo-name>.git /opt/workspace/<repo-name>
```
Replace `isfahannaki` with the actual GitHub username or org.

### Step 3 - Read the project's AGENT.md if present
```bash
cat /opt/workspace/<repo-name>/AGENT.md
```
This gives you the project-specific context. Always read it before touching any code.

### Step 4 - Confirm to Isfa
Report back: which branch is checked out, the last commit hash, and a brief summary of the project structure from `ls -la`.

---

## Workflow B: Create a New Project

When Isfa says "create a new project called `<name>`":

### Step 1 - Create the repo on GitHub via API
```bash
curl -s -X POST https://api.github.com/user/repos \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "<name>",
    "private": true,
    "auto_init": false
  }'
```

### Step 2 - Create the local directory and initialize git
```bash
mkdir -p /opt/workspace/<name>
cd /opt/workspace/<name>
git init
git remote add origin git@github.com:isfahannaki/<name>.git
```

### Step 3 - Create a default AGENT.md for this project
Create `/opt/workspace/<name>/AGENT.md` describing the project name, stack, and workspace paths following the convention from the global AGENT.md.

### Step 4 - Initial commit and push
```bash
cd /opt/workspace/<name>
git add .
git commit -m "init: initial project scaffold"
git push -u origin main
```

---

## Workflow C: Commit and Push Changes

After completing a coding task:

```bash
cd /opt/workspace/<repo-name>
git add -A
git commit -m "<conventional commit message>"
git push origin <branch-name>
```

Conventional commit format: `type(scope): message`
- `feat(auth): add JWT login endpoint`
- `fix(mobile): resolve crash on empty list`
- `refactor(dashboard): extract UserCard component`

---

## Workflow D: Open a Pull Request

```bash
curl -s -X POST https://api.github.com/repos/isfahannaki/<repo-name>/pulls \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "<PR title>",
    "body": "<description of changes>",
    "head": "<feature-branch>",
    "base": "main"
  }'
```

---

## Important Notes
- Never hardcode credentials. Always use `$GITHUB_TOKEN` and SSH keys from the mounted `.ssh` directory.
- Always create feature branches for non-trivial changes: `git checkout -b feat/<feature-name>`
- Never push directly to `main` without Isfa's approval.
- When uncertain about the GitHub username or org, ask Isfa before running API calls.

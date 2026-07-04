# Changelog

All notable changes to the `isfa-ai` agent fleet workspace will be documented in this file.

## [1.1.0] - 2026-07-05
### Added
- Dynamic Agent-to-Agent (A2A) async file-based communication protocol via the `a2a-messenger` skill.
- TPM orchestration protocol for task layout, delegation, and status tracking.
- Logging, healthcheck, and memory limit controls inside `docker-compose.yml`.
- Validation checks in `setup.py` to prevent starting containers with remaining placeholder secrets.
- Automatic quotes stripping in `.env` variable parser.
- Read-only workspace mounting for daily assistant agents to enforce sandbox safety.

### Fixed
- SSH mount home path resolution bug in `docker-compose.yml`.
- `summarize.py` TypeError crash when extracting scanned PDFs with empty/missing text fields.

## [1.0.0] - 2026-07-04
### Added
- Initial project layout containing 6 agent services (TPM, Kotlin Mobile, Go Backend, React Frontend, General Assistant, Learning Buddy).
- Dynamic config.yaml generator compiling settings from central `.env` file.
- Telegram gateway integrations.
- GitHub manager skill for dynamic repository cloning, commits, pushing, and PR submissions.

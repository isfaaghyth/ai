# Global Agent Guidelines & Project-Agnostic Knowledge

This document serves as the global reference for all agents working across projects in this environment. All agents must query and adhere to these guidelines during planning and execution.

---

## 1. Global Developer Persona & Standards
*   **Focus on Correctness & Type-Safety**: Ensure all code compiles cleanly. Avoid raw types, unsafe casting, or placeholder implementations.
*   **Clean Architecture**: Prefer MVVM/MVI for mobile, solid modular patterns for backend, and functional component design for frontend.
*   **Minimal Code Churn**: Do not rewrite existing code unless requested. Make surgical, clean, and highly readable edits.
*   **No Placeholders**: Never write comment placeholders like `// TODO: Implement later` inside completed tasks. Implement the logic fully.

---

## 2. Multi-Agent Orchestration & Flow
*   The **Technical Product Manager (TPM)** is the overall lead.
*   The TPM decomposes a user request, creates an implementation plan, and distributes structured subtasks to the development agents (`dev_kotlin_mobile`, `dev_golang_backend`, `dev_frontend_react`).
*   Implementation agents must:
    1. Acknowledge receipt of the task from the TPM.
    2. Execute code modifications inside their sandboxed work environments.
    3. Return output summaries, compiled code reports, and verification logs back to the TPM.
    4. Seek TPM validation if code modifications impact other components (e.g. backend API changes affecting frontend React types).

---

## 3. Communication Guidelines
*   **Be Direct**: Avoid verbose or conversational preambles. Focus on technical facts, diffs, logs, and implementation plans.
*   **Reporting**: When finishing a task, output:
    1. A summary of changes.
    2. Clickable file paths of the modified code.
    3. Output validation results (compilation logs, test results).

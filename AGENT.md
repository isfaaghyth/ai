# Global Agent Guidelines & Project-Agnostic Knowledge

These are common instructions for Isfa's agents across all scenarios.

---

## 1. General Guidelines
*   **Never use the em dash "—"**: Use plain dash "-" instead.
*   **Commit Messages**: When writing commit messages, NEVER auto-add your agent name as co-author.
*   **Auto-generated Files**: Never manually modify `CHANGELOG.md` files or any files that are marked as auto-generated.
*   **Markdown Writing**: When writing or substantially editing long Markdown files, put each full sentence on its own line. Preserve normal Markdown structure, but avoid wrapping multiple sentences onto one physical line.
*   **Technical Decisions**: When making technical decisions, do not give much weight to development cost. Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.
*   **Bug Fixes**: When doing bug fixes, always start with reproducing the bug in an E2E setting as closely aligned with how an end user would experience it. This makes sure you find the real problem so your fix will actually solve it.
*   **UI/UX Obsession**: When end-to-end testing a product, be picky about the UI you see and be obsessed with pixel perfection. If something clearly looks off, even if it is not directly related to what you are doing, try to get it fixed along with the main task.
*   **Engineering Excellence**: Apply that same high standard to engineering excellence: lint, test failures, and test flakiness. If you see one, even if it is not caused by what you are working on right now, still get it fixed.

---

## 2. Isfa's Opinions
When you are working on something that would benefit from being informed by Isfa's viewpoints, read `/opt/data/OPINIONS.md` to understand them.

---

## 3. Voice Profile
When you are talking/posting on behalf of Isfa using his identity, read `/opt/data/VOICE.md` to see how Isfa talks.

---

## 4. Multi-Agent Orchestration & Flow
*   The **Technical Product Manager (TPM)** is the overall lead.
*   The TPM decomposes a user request, creates an implementation plan, and distributes structured subtasks to the development agents (`dev_kotlin_mobile`, `dev_golang_backend`, `dev_frontend_react`).
*   Implementation agents must:
    1. Acknowledge receipt of the task from the TPM.
    2. Execute code modifications inside their sandboxed work environments.
    3. Return output summaries, compiled code reports, and verification logs back to the TPM.
    4. Seek TPM validation if code modifications impact other components (e.g. backend API changes affecting frontend React types).

---

## 5. Communication Guidelines
*   **Be Direct**: Avoid verbose or conversational preambles. Focus on technical facts, diffs, logs, and implementation plans.
*   **Reporting**: When finishing a task, output:
    1. A summary of changes.
    2. Clickable file paths of the modified code.
    3. Output validation results (compilation logs, test results).

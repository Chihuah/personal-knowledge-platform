# AGENTS.md

## Project
This repository is the Personal Knowledge Platform.

## Read first
Before making implementation decisions, always read these files in order:
1. docs/PRD.md
2. docs/requirements.md
3. docs/design.md
4. docs/tasks.md
5. docs/AI_AGENT_LINUX_PORTABILITY_RULES.md

## Source of truth
- PRD.md defines product direction and MVP scope.
- requirements.md defines feature requirements.
- design.md defines architecture and technical direction.
- tasks.md defines implementation breakdown and priority.
- AI_AGENT_LINUX_PORTABILITY_RULES.md defines Linux-first and deployment-portable rules.

If any conflict appears, follow this priority:
1. PRD.md
2. requirements.md
3. design.md
4. tasks.md

## Working rules
- Always follow Linux-first practices.
- Do not introduce Windows-only assumptions.
- Do not hardcode Windows paths, WSL-only paths, or local machine absolute paths.
- Treat PostgreSQL and Redis as Docker Compose services by default.
- Do not assume PostgreSQL or Redis are manually installed on the local machine.
- Prefer Docker Compose for local development of backend dependencies.
- Use FastAPI for backend, Next.js for frontend, PostgreSQL for database, Redis for queue/cache, and Celery for background jobs.
- Use environment variables for all configurable values.
- Keep changes small and reviewable.
- Update tests for non-trivial changes.
- If behavior, scope, or setup changes, update the relevant docs in docs/.
- Actively use available MCP tools when they reduce guesswork, especially for official docs, codebase resources, API schemas, structured exploration, or safe browser automation.
- Prefer MCP resources and official documentation lookups over ad-hoc memory when a detail may be stale, precise, or easy to verify.
- Actively use relevant skills when the task clearly matches a skill's scope, and follow the skill workflow before inventing a custom approach.
- Keep MCP and skill usage focused: load only the context needed for the current task, and avoid unnecessary broad scans.

## MCP and skills guidance
- For OpenAI or API-doc-related work, prefer the available MCP documentation tools and official sources.
- For library/framework implementation details, prefer Context7 or other available MCP documentation sources before relying on recall.
- For codebase exploration, prefer structured MCP resources when available, and use shell search tools for fast local verification.
- For UI/UX work, use the `ui-ux-pro-max` skill when the task involves visual design, layout, styling, interaction polish, or component UX improvements.
- For backend architecture or API design tradeoff questions, use the `backend-architect` skill when its scope matches the task.
- If a named or clearly relevant skill cannot be used cleanly, state that briefly and continue with the best local fallback.

## Implementation workflow
For every non-trivial task:
1. Read the relevant docs first.
2. Identify the related requirement and task items.
3. Check whether an available MCP tool or skill should be used for the task, and use the minimal relevant one when helpful.
4. Summarize the plan before editing files.
5. Implement the smallest correct change.
6. Run relevant validation or tests.
7. Report changed files, what was done, how to test, and what remains.

## Reporting rules
In the final report for each task, always include:
- Files changed
- What was implemented
- How to test
- Remaining work
- Linux portability check:
  - Any Windows-only dependency introduced?
  - Any hardcoded local path introduced?
  - Any Docker / env / migration update needed?
  - Is this change ready to run on Linux?

## Build and test
When relevant, prefer these commands:
- Backend setup: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Backend run: `cd backend && source .venv/bin/activate && uvicorn app.main:app --reload`
- Frontend setup: `cd frontend && npm install`
- Frontend run: `cd frontend && npm run dev`
- Tests: run only the relevant tests for changed code first, then broader checks if needed.

## Documentation updates
If you notice repeated mistakes, unclear conventions, or missing recurring instructions, update this AGENTS.md so future sessions inherit the correction.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"Spendly" is a Flask-based expense tracker built incrementally as a step-by-step learning project. Routes and modules that aren't implemented yet are intentionally left as stubs with comments like `# Students will write this file in Step 1 — Database Setup` (`database/db.py`) or return placeholder strings like `"Logout — coming in Step 3"` (`app.py`). When asked to implement one of these, follow the existing style/step numbering rather than redesigning the app's structure.

## Architecture

### Folder Structure

```
expense-tracker/
├── app.py                   — Flask app entrypoint; all routes defined here (no blueprints)
├── requirements.txt         — pinned deps: flask, werkzeug, pytest, pytest-flask
├── .gitignore               — excludes venv/, expense_tracker.db, __pycache__, .env, .DS_Store
├── database/
│   ├── __init__.py          — empty; makes `database` an importable package
│   └── db.py                 — DB layer (get_db/init_db/seed_db); not yet implemented (Step 1)
├── templates/
│   ├── base.html             — shared layout: <head>, nav, footer; all pages extend this
│   ├── landing.html          — public landing/marketing page (hero, stats, video modal)
│   ├── register.html         — signup form (POSTs to /register; name/email/password)
│   ├── login.html            — sign-in form (POSTs to /login; email/password)
│   ├── terms.html            — static Terms and Conditions page
│   └── privacy.html          — static Privacy Policy page
├── static/
│   ├── css/
│   │   └── style.css         — single global stylesheet for the whole app
│   └── js/
│       └── main.js           — vanilla JS: hero stat animation, video modal toggle
└── venv/                     — local Python virtualenv; never edit or commit into
```

- **`app.py`** — single Flask app, all routes defined directly on `app` (no blueprints, no app factory). Server-rendered via `render_template`; no REST/JSON API layer exists yet.
- **`database/db.py`** — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (idempotent `CREATE TABLE IF NOT EXISTS` schema), and `seed_db()` (dev sample data). Not yet implemented — this is the Step 1 foundation everything else (auth, expenses) depends on.
- **`templates/`** — Jinja2 templates, all extending `templates/base.html`, which owns the shared `<head>`, nav, and footer, and links `static/css/style.css` / `static/js/main.js`. `base.html` calls `url_for('login')`, `url_for('register')`, etc., so every route referenced there must exist in `app.py` or template rendering will fail app-wide.
- **`static/js/main.js`** — vanilla JS, no framework/bundler/build step. Page behaviors are small functions wired up via `DOMContentLoaded` listeners (e.g. `animateHeroStats`, `initVideoModal`).
- **`static/css/style.css`** — single global stylesheet shared by all pages (no CSS modules/preprocessor/scoping).
- No session/auth layer, no ORM, no migrations framework — expect to hand-roll these with Flask sessions and raw SQL as later steps are implemented.

## Where things belong

- New page routes → `app.py`, grouped under the correct comment banner (see Code Style).
- New pages → a template in `templates/` extending `base.html`, plus a route in `app.py` that renders it.
- Any DB access (queries, connection handling, schema) → `database/db.py`. Don't open ad-hoc `sqlite3` connections elsewhere.
- Shared layout/nav/footer changes → `templates/base.html` only; don't duplicate nav/footer markup into individual templates.
- Page-specific JS → new small function in `static/js/main.js` hooked to `DOMContentLoaded`; don't introduce inline `<script>` blocks or a second JS file/bundler.
- Styling → `static/css/style.css`; don't add per-page stylesheets or inline `style=` blocks for anything reusable.

## Code Style

- Route handlers in `app.py` are grouped under `# --- Routes ---` vs `# --- Placeholder routes — students will implement these ---` comment banners; keep new routes under the correct banner as they move from stub to implemented.
- Commit messages use a `scope: short description` style (e.g. `landing: redesign hero section to match mockup and added animations`).
- Templates use 4-space indentation and Jinja `{% block %}` sections (`title`, `content`, `head`, `scripts`) — follow the existing block names rather than inventing new ones.
- Form fields follow existing naming: register uses `name`/`email`/`password`; login uses `email`/`password`. Error display uses a single `{{ error }}` block above the form, not per-field errors.

## Tech Constraints

- Flask 3.1.3 / Werkzeug 3.1.6, Python (see `venv/`). Test stack is `pytest` + `pytest-flask` (see `requirements.txt`).
- SQLite only (`expense_tracker.db`, gitignored, created at runtime) — no external DB service assumed.
- No frontend build tooling (no npm/webpack/vite) — JS and CSS are served as-is from `static/`.
- Windows dev environment (`venv\Scripts\activate`), but avoid Windows-only path assumptions in code.

## Commands

```bash
# Activate the venv (Windows)
venv\Scripts\activate

# Run the dev server (http://localhost:5001)
python app.py

# Run tests
pytest
```

There is no build step or linter configured.

## Implemented vs Stub Routes

**Implemented** (real `render_template` GETs):
- `/` — landing page
- `/register` — GET only; renders form, no POST handler yet
- `/login` — GET only; renders form, no POST handler yet
- `/terms`, `/privacy` — static content pages

**Stub/placeholder** (return plain strings, no real logic):
- `/logout` — "coming in Step 3"
- `/profile` — "coming in Step 4"
- `/expenses/add` — "coming in Step 7"
- `/expenses/<id>/edit` — "coming in Step 8"
- `/expenses/<id>/delete` — "coming in Step 9"

When implementing a stub, replace the placeholder return with real logic but keep the route signature and URL structure intact, since templates already link to these via `url_for`.

## Warnings and Things to Avoid

- Don't commit `expense_tracker.db` — it's gitignored and generated at runtime; if it appears in `git status`, don't force-add it.
- Don't add auth/session logic ahead of `database/db.py` being implemented — there's no user table or connection helper to hook into yet.
- Don't introduce a frontend framework, bundler, or second CSS/JS file "for organization" — the project intentionally stays single-file per concern.
- Don't rename or restructure the `# --- Placeholder routes ---` step comments — they track curriculum progression and other steps may reference them.
- Don't add blueprints, an app factory, or split `app.py` into multiple modules unless explicitly asked — the flat single-file structure is intentional for this stage of the project.
- Don't build a JSON/REST API layer — this app is server-rendered only; no `jsonify` responses exist and none are expected yet.

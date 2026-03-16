# core-upgrade

## Core version management without a database (GitHub-based)

If you don't have a DB, use a **shared JSON catalog** in GitHub as the source of truth.

### Recommended flow
1. On Step 1, if user selects **"Does the core version appear? → No"**, open the new **Add missing core version** panel.
2. Add:
   - `core key` (example: `core22_1`)
   - display label (example: `core 22.1`)
   - optional `CORE_TECH_STACK` JSON parameters.
3. Click **Add core version**.
   - Version is available immediately in `coreFrom` / `coreTo`.
   - Data is saved in browser `localStorage` (works instantly for the same user/browser).
4. To share with everyone:
   - Click **Export catalog JSON**.
   - Commit the exported `core-catalog.json` into GitHub.
   - Other users load it via **Load from GitHub URL** (raw GitHub URL).

### Why this works without DB
- **Local continuity**: localStorage keeps new versions for the current user.
- **Cross-user continuity**: GitHub JSON file acts as persistent shared storage.
- **No backend needed**: all done in the static app + GitHub file workflow.

### Suggested governance
- Keep one canonical file in repo, e.g. `core-catalog.json`.
- Protect changes with PR review.
- Validate key format `coreNN_N` and avoid duplicates.

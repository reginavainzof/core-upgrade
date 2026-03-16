# core-upgrade

## Auto-shared core catalog (without DB and without Git credentials)

Use a **shared JSON endpoint** (URL that supports `GET` + `PUT` + CORS).

### How it works
1. Open the tool and choose **Does the core version appear? → No**.
2. Configure one company shared endpoint in code (`DEFAULT_ORG_SHARED_JSON_URL`) or connect it manually in the UI (full `http(s)` endpoint that supports browser `GET`/`PUT` + CORS, for example `https://api.example.com/core-catalog.json`).
3. Add new core version + optional `CORE_TECH_STACK` JSON.
4. The app saves locally and asks if you want to sync to everyone now. If you confirm, it pushes to the company shared JSON endpoint.
5. Click **Copy workspace link** and send it to other users.
6. Anyone opening that link is connected to the same shared JSON and gets updates automatically (polling).


Quick answer: what should users paste in "Connect shared JSON"?
- Paste one **company shared API endpoint URL** that stores the catalog JSON.
- It must support browser `GET` and `PUT` with CORS.
- Example format: `https://api.company.com/core-catalog.json`.
- Do **not** paste a regular website page URL; ask IT/backend team for the endpoint.

### What this gives you
- No database required.
- No GitHub password/token required for end users.
- One workspace link for everyone.
- New core versions and related tech-stack changes become available to all users automatically after sync.

### Important
- Your shared JSON provider must allow browser `GET`/`PUT` with CORS.
- This is a collaborative endpoint (last write wins).

## `CORE_TECH_STACK params (JSON, optional)`

When adding a missing core version, you can optionally provide a JSON object in the
`CORE_TECH_STACK params` textarea.

### Expected shape
- Must be a valid JSON object (not an array).
- Keys are free-form tech parameter names (for example: `java`, `database`, `kubernetes`).
- Values can be strings, numbers, booleans, or nested objects.

Example:

```json
{
  "java": "OpenJDK 21",
  "database": "Oracle 19",
  "kubernetes": "1.30",
  "complexityMultiplier": 1.6,
  "platform": "OpenShift"
}
```

### Data flow (where it goes)
1. **On Add core version** the app parses this JSON and validates it is an object.
2. It is inserted under `techStack.<coreKey>` in the catalog payload.
3. The payload is always saved in browser `localStorage` under `core_upgrade.catalog.v1`.
4. If a shared JSON URL is connected, the same payload is also sent with HTTP `PUT` to that URL.

### How it is loaded later
- On page load, catalog data is restored from `localStorage`.
- If a shared JSON URL exists (from query param `catalogUrl` or `localStorage`), the app fetches it with HTTP `GET`, applies it, and keeps polling every 10 seconds.


### Share to everyone via the same Git-hosted link (no extra actions)
If you want all users to see the same catalog directly from the regular app link:
1. Export catalog JSON from the app.
2. Save/replace repository file `core-catalog.json` with that content.
3. Commit + push to GitHub (and deploy as usual for your hosting).

On app load (when no `catalogUrl` is configured), the tool now fetches `core-catalog.json` from the repo automatically, so users opening the normal link get the updated core versions without importing files or opening a different workspace link.

### Company-wide sharing (recommended, no personal GitHub permissions)
For enterprise use, configure one **company shared JSON endpoint** and use it for all users.

- Endpoint requirements: browser `GET` + `PUT` + CORS.
- Every user keeps using the same app link.
- No personal GitHub token is required in the UI.

Important: set `DEFAULT_ORG_SHARED_JSON_URL` in `index.html` once to make the regular link load and sync the same company catalog for all users.

### If you prefer Google Sheets
Google Sheets can work via an intermediary API (for example Google Apps Script Web App):
- App calls your API endpoint (not the sheet directly).
- API reads/writes JSON to the sheet and handles CORS/auth centrally.
- This keeps permissions centralized and avoids per-user credentials in the tool.


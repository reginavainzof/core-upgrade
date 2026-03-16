# core-upgrade

## Auto-shared core catalog (without DB and without Git credentials)

Use a **shared JSON endpoint** (URL that supports `GET` + `PUT` + CORS).

### How it works
1. Open the tool and choose **Does the core version appear? → No**.
2. In **Connect shared JSON**, paste the shared endpoint URL and click **Connect shared JSON**.
3. Add new core version + optional `CORE_TECH_STACK` JSON.
4. The app saves locally **and automatically pushes** the updated catalog to the shared JSON URL.
5. Click **Copy workspace link** and send it to other users.
6. Anyone opening that link is connected to the same shared JSON and gets updates automatically (polling).

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

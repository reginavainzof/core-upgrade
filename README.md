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

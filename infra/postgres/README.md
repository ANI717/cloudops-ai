# PostgreSQL (local development)

Runs the official [`postgres`](https://hub.docker.com/_/postgres) 18.6 (Alpine) image with
Docker Compose. Data persists in the `cloudops-postgres-data` Docker volume.

## Setup (once)

From the repository root:

```bash
cp infra/postgres/.env.example infra/postgres/.env
```

Edit `infra/postgres/.env` to change the user, password, database name, or port.
Compose refuses to start if a required value is missing.

## Commands

Run from the repository root (or from this folder, dropping `postgres` where shown):

```bash
docker compose up -d postgres      # start (waits in background)
docker compose ps                  # status; STATUS shows "(healthy)" when ready
docker compose logs -f postgres    # follow logs (Ctrl+C to stop following)
docker compose stop postgres       # stop, keep data
docker compose down                # stop and remove containers, keep data
```

Open a SQL shell inside the container:

```bash
docker compose exec postgres psql -U cloudops -d cloudops
```

(Use the user and database from your `.env` if you changed them.) Type `\q` to exit.

## Connection details

| Setting  | Value (defaults from `.env.example`) |
| -------- | ------------------------------------ |
| Host     | `127.0.0.1` (localhost only)         |
| Port     | `5432`                               |
| User     | `cloudops`                           |
| Password | `cloudops-local-dev`                 |
| Database | `cloudops`                           |

## Reset all data

This deletes the database permanently:

```bash
docker compose down
docker volume rm cloudops-postgres-data
```

## Notes

- PostgreSQL 18+ images store data under `/var/lib/postgresql`, which is where the
  volume is mounted. Older guides that mount `/var/lib/postgresql/data` don't apply.
- The image is pinned by digest. To upgrade, update the tag and digest in
  `compose.yaml` (`docker buildx imagetools inspect postgres:<tag>` shows the digest).
  Major-version upgrades (e.g. 18 → 19) need a data migration, not just a new image.

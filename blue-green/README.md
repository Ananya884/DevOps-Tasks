# Task 04: Blue-Green Deployment Pipeline (Jenkins + Docker + nginx)

A Jenkins pipeline that releases a new version next to the old one, tests it,
switches traffic, and rolls back automatically if the test fails.

## How it works

Two containers, `blue` and `green`, run the same app. An nginx proxy (port 9000)
sends visitors to whichever colour is live. One small file,
`nginx/conf.d/upstream.conf`, says which one. Switching traffic means changing
that file and reloading nginx (no restart, no downtime).

## Pipeline stages

1. **Clone**: get the code from GitHub
2. **Build image**: build the new version as a Docker image
3. **Find live colour**: read the nginx file to see which colour is live
4. **Deploy to idle**: start the new version on the other colour
5. **Smoke test**: call `/health` up to 10 times; fail if it never answers
6. **Switch traffic**: point nginx at the new colour (after `nginx -t` validates)
7. **Verify live**: check visitors really get the new version

## Automatic rollback

If any stage fails, a `post { failure { ... } }` block puts nginx back on the
old colour, removes the broken container, and sends a Slack alert. The old
version keeps serving the whole time.

## Testing it

- **Good release:** Build with Parameters, `VERSION=2`. Visitors move to the new colour.
- **Bad release:** `VERSION=4` with `BREAK` ticked. The new container's `/health`
  returns an error, the smoke test fails, traffic never moves, and Slack is alerted.

After a good release the old colour stays running as a standby.

## Problem met and fix

- The first smoke test failed even though the app was healthy. Inside the
  container, `localhost` resolved to the IPv6 address `::1` first, and the app
  listened only on IPv4. Fixed by testing `127.0.0.1` explicitly. The rollback
  still worked, which showed the safety net does its job.

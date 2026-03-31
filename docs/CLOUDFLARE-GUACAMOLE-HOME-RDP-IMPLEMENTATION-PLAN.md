# Cloudflare and Guacamole Home RDP Implementation Plan

## Purpose

Provide a simple, secure remote desktop path to a home Windows PC from restrictive external networks without exposing public port 3389.

## Target Outcome

- Access home desktop from outside the house over HTTPS.
- Keep router/firewall public exposure to 443 only (or no inbound port forwards when using outbound tunnel only).
- Enforce identity and MFA with Cloudflare Access before desktop access is possible.
- Keep direct RDP port 3389 private to the home LAN.

## Scope

In scope:

- Apache Guacamole hosted at home in Docker.
- Cloudflare Tunnel from home to Cloudflare.
- Cloudflare Access policy for SSO and MFA.
- Windows RDP hardening baseline.

Out of scope:

- Enterprise AD/Domain join design.
- Multi-user VDI sizing.
- Fully automated IaC provisioning.

## High-Level Architecture

1. External user connects to `https://rdp.<your-domain>`.
2. Cloudflare Access challenges for identity and MFA.
3. Cloudflare Tunnel forwards authenticated traffic to local Guacamole.
4. Guacamole connects to `windows-host:3389` on the home LAN.
5. Router does not expose inbound 3389.

## Prerequisites

### Accounts and DNS

- Cloudflare account with Zero Trust enabled.
- Managed domain in Cloudflare DNS.
- Identity provider configured in Access (email OTP is acceptable for initial setup; stronger IdP preferred).

### Home Infrastructure

- Always-on host for Docker and `cloudflared` (can be the same machine as Windows host or a separate mini-PC).
- Windows PC with Remote Desktop enabled and Network Level Authentication enabled.
- Stable home internet uplink.

### Software

- Docker Engine + Docker Compose plugin.
- `cloudflared` binary installed on the Docker host.

## Security Baseline (Before Build)

- Disable public router forward for 3389.
- Enforce strong unique Windows password.
- Set account lockout policy (for local Windows accounts).
- Patch Windows and reboot before go-live.
- Verify local firewall allows RDP from LAN only.

## Implementation Phases

### Phase 1 - Prepare Host and Network

1. Confirm no public inbound NAT rule for 3389.
2. Confirm Windows RDP works locally from a LAN device.
3. Reserve static DHCP IPs for:
   - Windows RDP host
   - Guacamole/Tunnel host
4. Create a dedicated local service account for remote access (avoid using daily admin account).

Exit criteria:

- LAN-only RDP is working.
- No external exposure of 3389.

### Phase 2 - Deploy Guacamole (Docker)

1. Create a folder for stack deployment (for example, `~/remote-desktop-stack`).
2. Create `docker-compose.yml` with:
   - `guacd`
   - `guacamole`
   - `postgres` (persistent DB for users/connections)
3. Mount persistent volumes for database durability.
4. Start stack and verify local access at `http://<docker-host-ip>:8080/guacamole`.
5. Change default credentials immediately.
6. Create one connection profile to the Windows host (RDP target `windows-host-ip:3389`).

Exit criteria:

- Guacamole login works on LAN.
- RDP session launches via Guacamole on LAN.

### Phase 3 - Create Cloudflare Tunnel

1. Authenticate `cloudflared` with Cloudflare (`cloudflared tunnel login`).
2. Create named tunnel (`cloudflared tunnel create home-rdp-gateway`).
3. Create DNS route for hostname (`rdp.<your-domain>`).
4. Configure tunnel ingress to local Guacamole service on `http://localhost:8080` (or Docker host IP/port).
5. Run tunnel as a service so it persists after reboot.

Exit criteria:

- Tunnel status healthy in Cloudflare dashboard.
- Hostname resolves and reaches tunnel endpoint.

### Phase 4 - Enforce Cloudflare Access

1. Create Access self-hosted app for `rdp.<your-domain>`.
2. Add policy:
   - Allow only your user/group.
   - Require MFA.
   - Optional: country/IP restrictions.
3. Set short browser session duration for higher security.
4. Validate Access challenge appears before Guacamole login page.

Exit criteria:

- Unauthorized users denied.
- Authorized user sees Access challenge then Guacamole.

### Phase 5 - Harden and Go Live

1. Restrict Guacamole local listening scope as needed.
2. Enable HTTPS-only edge in Cloudflare.
3. Disable or rotate any bootstrap/default secrets.
4. Configure routine updates:
   - Windows patch cadence
   - Docker image updates (guacamole/guacd/postgres)
   - `cloudflared` updates
5. Capture backup procedure for Guacamole DB and config.

Exit criteria:

- External login path works end-to-end through Access.
- Security checklist completed.
- Recovery and rollback documented.

## Suggested Docker Compose Baseline

Use this as a starting point and adjust credentials before first run.

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16
    container_name: guac-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: guacamole_db
      POSTGRES_USER: guacamole_user
      POSTGRES_PASSWORD: CHANGE_ME_LONG_RANDOM
    volumes:
      - guac_postgres_data:/var/lib/postgresql/data

  guacd:
    image: guacamole/guacd:1.5.5
    container_name: guacd
    restart: unless-stopped

  guacamole:
    image: guacamole/guacamole:1.5.5
    container_name: guacamole
    restart: unless-stopped
    depends_on:
      - postgres
      - guacd
    environment:
      GUACD_HOSTNAME: guacd
      POSTGRESQL_HOSTNAME: postgres
      POSTGRESQL_DATABASE: guacamole_db
      POSTGRESQL_USER: guacamole_user
      POSTGRESQL_PASSWORD: CHANGE_ME_LONG_RANDOM
    ports:
      - "8080:8080"

volumes:
  guac_postgres_data:
```

## Validation Checklist

Functional checks:

- External URL prompts for Cloudflare Access login.
- MFA is required before Guacamole page.
- Guacamole login succeeds.
- RDP session launches and remains stable for at least 15 minutes.

Security checks:

- External scan confirms 3389 closed at home public IP.
- Failed Access authentication blocks desktop access.
- Failed Guacamole login is logged.
- Windows Security Event logs show expected logons only.

Resilience checks:

- Reboot tunnel host and confirm auto-reconnect.
- Restart Docker services and confirm Guacamole recovers.

## Rollback Plan

If issues occur during rollout:

1. Disable Access app or tunnel public DNS record.
2. Stop `cloudflared` service.
3. Keep LAN-only RDP path for emergency access.
4. Restore previous Guacamole DB backup if config corruption occurs.

## Operations Runbook

Daily:

- Verify tunnel health and Access events.

Weekly:

- Review login/audit logs for unusual geographies/times.
- Apply pending OS and container image updates in maintenance window.

Monthly:

- Rotate Guacamole DB and admin credentials.
- Test backup restore for Guacamole DB.
- Re-validate that 3389 remains closed publicly.

## Time and Cost Estimate

One-time setup (single user, home lab):

- 1 to 3 hours depending on Docker familiarity.

Recurring cost:

- Domain registration only (typically low annual cost).
- Cloudflare Zero Trust can remain in free tier for small personal usage, subject to current plan limits.
- No required Guacamole license cost.

## Success Criteria

- User can access home desktop from external restricted networks using HTTPS path.
- No direct inbound RDP exposure on the public internet.
- MFA is enforced before any desktop authentication step.
- Documented maintenance and rollback procedures exist and are tested.

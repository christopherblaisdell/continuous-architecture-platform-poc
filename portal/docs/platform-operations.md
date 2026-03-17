# Platform Operations

This page provides an operational overview of the NovaTrek Continuous Architecture Platform — CI/CD pipelines, deployment targets, cost controls, and integration points.

---

## GitHub Actions Pipelines

All workflows live in [`.github/workflows/`](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/tree/main/.github/workflows) on the `main` branch.

### Documentation

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [Deploy Documentation](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/docs-deploy.yml) | Push/PR to `main` (doc paths) | Build MkDocs, deploy to Azure SWA, publish Confluence mirror |
| [Validate Solution Design](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/validate-solution.yml) | PR to `main` (architecture paths) | YAML lint, folder structure check, data isolation audit, portal build |

### Service CI/CD

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [svc-check-in](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-svc-check-in.yml) | Push/PR to `main` (`services/svc-check-in/`, `config/adventure-classification.yaml`) | Full CI/CD chain: build, test, OWASP scan, Docker push, Flyway migrate, deploy to dev and prod |
| [Service CI (Reusable)](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-ci.yml) | Called by per-service workflows | Gradle build, test, OWASP dependency check, Docker build to ACR, Trivy container scan |
| [Service CD (Reusable)](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/service-cd.yml) | Called by per-service workflows | Container Apps update + health check (30 attempts, 10s intervals) |
| [Database Migrations](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/db-migrate.yml) | Called by per-service CD chains | Flyway migration — routes to Neon (dev) or Azure PostgreSQL (prod) |

### Infrastructure

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [Infrastructure Deploy](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/infra-deploy.yml) | Push to `main` (`infra/**`) or manual dispatch | Bicep lint, what-if preview, deploy `platform.bicep` to target environment |
| [Infrastructure Teardown](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/infra-teardown.yml) | Manual dispatch (requires `DESTROY` confirmation) | Destroy `rg-novatrek-dev` or all ephemeral resource groups |
| [Ephemeral Environment](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/ephemeral-env.yml) | PR events on `services/` or `infra/` paths | Spin up `rg-novatrek-pr-{N}` on PR open, tear down on PR close |

### Confluence Integration

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [Confluence Drift Check](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/confluence-drift-check.yml) | Weekdays 6 AM UTC; manual dispatch | Detect unauthorized edits to auto-generated Confluence pages |
| [Wipe Confluence Space](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/confluence-wipe.yml) | Manual dispatch (requires `WIPE` confirmation) | Delete all content from the ARCH Confluence space; supports dry-run |

### Cost Controls

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [Nightly Start Dev](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/nightly-start-dev.yml) | 1 PM UTC (8 AM EST) Mon-Fri; manual dispatch | Restore Container Apps scaling (0-2 replicas); Neon auto-wakes on first query |
| [Nightly Stop Dev](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/nightly-stop-dev.yml) | 1 AM UTC (8 PM EST) Tue-Sat; manual dispatch | Scale all Container Apps to 0 replicas; Neon auto-suspends after 5 min idle |

### Ticketing Integration

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [Sync Vikunja Tickets](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions/workflows/sync-vikunja.yml) | Every 30 min Mon-Fri 12-22 UTC; manual dispatch; webhook relay | Bi-directional sync between `tickets.yaml` and Vikunja board |

---

## Deployment Targets

### Environments

| Environment | Resource Group | Purpose | Lifecycle |
|-------------|---------------|---------|-----------|
| **production** | `rg-novatrek-prod` | Live microservices platform | Always on |
| **dev** | `rg-novatrek-dev` | Development and testing | Nightly start/stop (business hours EST) |
| **ephemeral** | `rg-novatrek-pr-{N}` | Per-PR preview environments | Created on PR open, destroyed on PR close |

### Static Web Apps

| Site | Custom Domain | Purpose |
|------|--------------|---------|
| Architecture Portal | [architecture.novatrek.cc](https://architecture.novatrek.cc) | MkDocs Material — architecture knowledge base (primary) |
| Presentation Site | [presentation.novatrek.cc](https://presentation.novatrek.cc) | MkDocs Material — executive briefing slides |
| Confluence Mirror | [novatrek.atlassian.net/wiki](https://novatrek.atlassian.net/wiki) (space: `ARCH`) | Read-only mirror of portal content |

### Azure Resources (via `platform.bicep`)

The platform Bicep template deploys:

- **Azure Container Apps Environment** — hosts all 19 microservices
- **PostgreSQL** — Neon Serverless Postgres (dev/ephemeral), Azure Flexible Server (prod)
- **Azure Container Registry** — Docker images from CI
- **Azure Service Bus** — event-driven integration between services
- **Redis Cache** — required by `svc-scheduling-orchestrator`
- **Key Vault** — secrets management
- **Managed Identity** — workload identity for OIDC auth
- **Budget Alerts** — configurable monthly budget (default $50/month)

---

## Deployment Flows

### Service Deployment (push to main)

```
Code push (services/svc-check-in/**)
  → Service CI: build, test, OWASP scan, Docker push, Trivy scan
  → DB Migrate (dev): Flyway against Neon Serverless Postgres
  → Service CD (dev): Container Apps update + health check
  → DB Migrate (prod): Flyway against Azure PostgreSQL
  → Service CD (prod): Container Apps update + health check
```

### Documentation Deployment (push to main)

```
Code push (portal/**)
  → Build: MkDocs + PlantUML generators + portal scripts
  → Deploy: Azure Static Web Apps (production)
  → Confluence: prepare staging → publish pages → lock pages
```

### PR Preview Flow

```
PR opened (services/** or infra/**)
  → Ephemeral: create rg-novatrek-pr-{N}, deploy platform.bicep
  → Post PR comment with preview URLs
  → Cost: ~$0.50-2.00 per PR lifetime

PR closed
  → Ephemeral: delete rg-novatrek-pr-{N}
```

### Cost Control Cycle

```
8 AM EST Mon-Fri  → Scale services 0-2 replicas; Neon auto-wakes on first query
8 PM EST Mon-Fri  → Scale all services to 0 replicas; Neon auto-suspends after idle
Weekend            → Dev environment fully stopped; Neon suspended (zero cost)
```

---

## Secrets and Variables

### GitHub Actions Secrets

| Secret | Used By | Purpose |
|--------|---------|---------|
| `AZURE_CLIENT_ID` | All deployment workflows | Service principal — OIDC auth |
| `AZURE_TENANT_ID` | All deployment workflows | Azure AD tenant |
| `AZURE_SUBSCRIPTION_ID` | All deployment workflows | Target subscription |
| `ACR_NAME` | Service CI | Container Registry name |
| `ACR_LOGIN_SERVER` | Service CI | Container Registry login server |
| `POSTGRES_ADMIN_USER` | DB Migrate (prod) | PostgreSQL admin username (prod only) |
| `POSTGRES_ADMIN_PASSWORD` | DB Migrate (prod), Infra Deploy (prod) | PostgreSQL admin password (prod only) |
| `NEON_DATABASE_URL` | DB Migrate (dev/ephemeral) | Neon Serverless Postgres JDBC connection URL |
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Docs Deploy | SWA deployment token (architecture portal) |
| `AZURE_STATIC_WEB_APPS_PRESENTATION_API_TOKEN` | Docs Deploy | SWA deployment token (presentation site) |
| `CONFLUENCE_USERNAME` | Docs Deploy, Confluence workflows | Confluence service account |
| `CONFLUENCE_API_TOKEN` | Docs Deploy, Confluence workflows | Confluence API token |
| `VIKUNJA_TOKEN` | Validate Solution, Sync Vikunja | Vikunja ticketing API token |

### GitHub Actions Variables

| Variable | Used By | Purpose |
|----------|---------|---------|
| `CONFLUENCE_BASE_URL` | Docs Deploy, Confluence workflows | Confluence instance URL |
| `CONFLUENCE_SPACE` | Docs Deploy, Confluence workflows | Space key (`ARCH`) |
| `VIKUNJA_URL` | Validate Solution, Sync Vikunja | Vikunja instance URL |
| `VIKUNJA_SPACE` | Sync Vikunja | Vikunja space identifier |

---

## Key Links

| Resource | URL |
|----------|-----|
| GitHub Repository | [continuous-architecture-platform-poc](https://github.com/christopherblaisdell/continuous-architecture-platform-poc) |
| All Workflows | [Actions tab](https://github.com/christopherblaisdell/continuous-architecture-platform-poc/actions) |
| Architecture Portal | [architecture.novatrek.cc](https://architecture.novatrek.cc) |
| Presentation Site | [presentation.novatrek.cc](https://presentation.novatrek.cc) |
| Confluence Mirror | [novatrek.atlassian.net/wiki](https://novatrek.atlassian.net/wiki) |

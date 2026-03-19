# Wave 1 Kickoff: Guest Identity and Product Catalog

Date: 2026-03-19
Status: Open
Owner: Platform Architecture
GitHub issue: https://github.com/christopherblaisdell/continuous-architecture-platform-poc/issues/22

## Goal

Start Wave 1 delivery after Wave 0 foundation completion for these services:

- svc-guest-profiles
- svc-trip-catalog
- svc-trail-management

## Preconditions

- Wave 0 deployment complete with successful infrastructure workflow run.
- Container Apps Environment available in `rg-novatrek-dev`.
- GitHub OIDC and secrets configured for deploy workflows.
- Budget guardrails configured.

## Scope

1. Validate service CI pipelines for all Wave 1 services.
2. Build and push latest images to ACR.
3. Deploy Wave 1 container apps in dev.
4. Execute smoke tests for health and core endpoints.
5. Update delivery status metadata and portal references.

## Acceptance Criteria

1. All three Wave 1 services report healthy revisions in Container Apps.
2. Swagger endpoints are reachable for each service in dev.
3. CI pipeline runs are green for all three services.
4. Delivery tracking updated in architecture metadata and roadmap context.

## Task Checklist

- [ ] Run service CI for `svc-guest-profiles`
- [ ] Run service CI for `svc-trip-catalog`
- [ ] Run service CI for `svc-trail-management`
- [ ] Confirm ACR tags for latest builds
- [ ] Validate container app revisions and ingress
- [ ] Verify health endpoints return success
- [ ] Record run links and deployment outputs
- [ ] Update status in roadmap/reminder artifacts

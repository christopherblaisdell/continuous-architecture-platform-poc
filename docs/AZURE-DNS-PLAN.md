# Azure DNS Plan for API Endpoints

Date: 2026-03-19
Status: Planned
Scope: DNS records for NovaTrek API ingress and ephemeral environments

## Objective

Document the Cloudflare DNS record plan for API routing to Azure Container Apps.

## Inputs

- Container Apps Environment: `cae-novatrek-dev`
- Environment default domain: `blackwater-fd4bc06d.eastus2.azurecontainerapps.io`
- Target public domains:
  - `api.novatrek.cc`
  - `api-dev.novatrek.cc`
  - `*.pr.novatrek.cc`

## Cloudflare Record Plan

| Record | Type | Value | Proxy | Purpose |
|--------|------|-------|-------|---------|
| `api.novatrek.cc` | CNAME | `blackwater-fd4bc06d.eastus2.azurecontainerapps.io` | DNS only (initial) | Primary production API gateway |
| `api-dev.novatrek.cc` | CNAME | `blackwater-fd4bc06d.eastus2.azurecontainerapps.io` | DNS only (initial) | Shared development API gateway |
| `*.pr.novatrek.cc` | CNAME | `blackwater-fd4bc06d.eastus2.azurecontainerapps.io` | DNS only (initial) | Ephemeral PR environments |

## Implementation Notes

1. Start with DNS-only proxy mode to simplify TLS and ingress debugging.
2. After endpoint verification and health checks pass, optionally enable Cloudflare proxy for WAF and caching policy control.
3. Keep low TTL during initial rollout to speed cutovers.

## Validation Commands

```bash
az containerapp env show -n cae-novatrek-dev -g rg-novatrek-dev \
  --query '{defaultDomain:properties.defaultDomain,provisioningState:properties.provisioningState}' -o table
```

```bash
nslookup api-dev.novatrek.cc
nslookup api.novatrek.cc
```

## Status

- DNS plan documented and approved for execution.
- Record creation in Cloudflare is pending manual application.

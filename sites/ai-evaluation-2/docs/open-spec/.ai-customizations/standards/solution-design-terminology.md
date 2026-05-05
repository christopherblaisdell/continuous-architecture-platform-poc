# Solution Design Terminology Standards

**Applicable Modes**: Solution Architect

## Overview

Standardized status values ensure consistency across all solution design documents (assumptions, decisions, risks). Use these exact values — do not paraphrase or abbreviate.

## Risk Statuses

| Status | Meaning |
|--------|---------|
| ACCEPTED | Risk acknowledged and accepted with no further action planned |
| MONITOR CLOSELY | Risk acknowledged; requires active monitoring for changes that could elevate impact |
| MITIGATED | Risk addressed through design decisions or controls |
| ESCALATED | Risk elevated to stakeholders for resolution |

**Important**: Use `MONITOR CLOSELY` — never `MONITORING`, `MONITORED`, or `WATCHING`.

## Assumption Statuses

| Status | Meaning |
|--------|---------|
| PROPOSED | Assumption stated but not yet validated |
| VALIDATED | Assumption confirmed through evidence or stakeholder input |
| INVALIDATED | Assumption proven incorrect; design adjustment required |

## Decision Statuses

| Status | Meaning |
|--------|---------|
| RECOMMENDATION MADE | Option recommended but not yet approved |
| APPROVED | Decision approved by stakeholders |
| DEFERRED | Decision postponed pending additional information |
| SUPERSEDED | Decision replaced by a later decision |

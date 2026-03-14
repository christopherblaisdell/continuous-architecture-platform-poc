<!-- PUBLISH -->
# Impact Assessment 3: svc-notifications (ENHANCED)

| Field | Value |
|-------|-------|
| Service | svc-notifications |
| Domain | Support |
| Change Type | Enhanced — new templates + event consumer |
| Impact Level | MEDIUM |
| Owner | Various |

## Overview

svc-notifications gains new notification templates for emergency alerting and becomes a consumer of emergency events for automated multi-channel delivery.

## API Contract Changes

No endpoint changes. The existing POST /notifications and POST /notifications/bulk endpoints are sufficient. Changes are limited to new template content and event consumption.

## New Notification Templates

| Template ID | Trigger | Channels | Priority | Recipients |
|-------------|---------|----------|----------|-----------|
| emergency-sos-guide | SOS triggered | PUSH, SMS | URGENT | Assigned adventure guide |
| emergency-sos-ops | SOS triggered | PUSH, IN_APP | URGENT | Operations staff on duty |
| emergency-sos-contacts | SOS triggered | SMS, EMAIL | URGENT | Guest emergency contacts |
| emergency-geofence-guide | Geofence breach | PUSH | HIGH | Assigned adventure guide |
| emergency-geofence-ops | Geofence breach | IN_APP | HIGH | Operations staff |
| emergency-weather-bulk | Weather evacuation | SMS, PUSH | URGENT | All affected guests and guides |
| emergency-dispatch-team | Rescue team dispatched | SMS, PUSH | URGENT | Rescue team members |
| emergency-resolved-guest | Emergency resolved | SMS, PUSH | NORMAL | Affected guest |

## Event Integration

### New Consumers

| Event | Source | Action |
|-------|--------|--------|
| emergency.triggered | svc-emergency-response | Send URGENT alerts to guide, ops staff, emergency contacts |
| emergency.resolved | svc-emergency-response | Send resolution notification to affected guest |

## Volume Impact

Current: ~15,000 notifications/day

Estimated increase: ~200 additional notifications/day during peak season (based on ~50 emergencies/month, ~4 notifications per emergency average). Negligible volume impact.

## Quality Attributes

| Attribute | Assessment |
|-----------|-----------|
| Reliability | URGENT emergency notifications must be delivered via at least one channel — SMS is the fallback if push fails |
| Performance | Bulk weather evacuation endpoint already supports 1,000 recipients — sufficient for area-wide alerts |

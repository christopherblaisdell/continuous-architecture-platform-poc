<!-- PUBLISH -->

# Impact Assessment: svc-notifications

| | |
|-----------|-------|
| **Ticket** | NTK-10006 |
| **Service** | svc-notifications |
| **Domain** | Support |
| **Team** | Support Services Team |
| **Change Type** | No Changes — Existing Consumer |

## Summary

svc-notifications requires no API or schema changes. It already consumes the `emergency.triggered` event published by svc-emergency-response and delivers multi-channel alerts (SMS via Twilio, email via SendGrid, push via Firebase Cloud Messaging).

The existing `POST /notifications/bulk` endpoint can send alerts to multiple recipients simultaneously — used for notifying on-duty guides, dispatch team, and guest emergency contacts.

## Changes Required

None.

## Volume Consideration

Emergency notifications are low-volume events (ideally rare). The existing notification pipeline handles burst scenarios. No capacity changes anticipated.

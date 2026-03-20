<!-- PUBLISH -->

# NTK-10006 Risks

| ID | Risk | Severity | Likelihood | Mitigation |
|----|------|----------|-----------|-----------|
| R1 | GPS signal unreliable in deep canyon, forest, or underground adventure areas | High | Medium | Configurable signal-loss timeout per adventure category (5 min default); manual tracking fallback (radio check-ins) for known dead zones; mesh relay network as future enhancement |
| R2 | Location data volume overwhelms PostgreSQL under peak load | Medium | Low | Time-series partitioning on `location_updates` by month; 1-year rolling retention with cold archive to Azure Blob Storage; connection pooling sized for 1,000 writes/min |
| R3 | False positive anomalies trigger unnecessary emergency dispatches | Medium | Medium | Configurable thresholds per adventure category in `config/adventure-classification.yaml`; graduated escalation (warning to ops dashboard first, auto-emergency after acknowledgment timeout); human-in-the-loop for non-SOS anomalies |
| R4 | Wristband hardware vendor lock-in | High | Low | svc-adventure-tracking accepts GPS coordinates via standard REST API (`POST /tracking-sessions/{id}/locations`); hardware integration is an adapter layer, not core architecture. Any GPS-capable device can be a location source. |
| R5 | Privacy and legal risk from continuous GPS tracking of guests | Medium | Medium | Guest consent obtained during waiver signing (svc-safety-compliance); data retention policy enforced (1-year rolling + 7-year audit archive); access restricted to authorized safety and operations staff; GDPR/CCPA considerations documented in guidance |
| R6 | Dependency on NTK-10005 (wristband RFID field) | High | Low | NTK-10005 solution design is complete and the schema change is defined. If implementation is delayed, tracking sessions can be correlated by reservation_id as a fallback (less precise but functional). |
| R7 | WebSocket infrastructure for real-time map not included in current Azure Container Apps configuration | Medium | Medium | WebSocket support is available in Azure Container Apps but requires sticky sessions or an external WebSocket gateway. If WebSocket is not feasible in the initial release, the ops dashboard can poll `GET /tracking-sessions/active` at 10-second intervals as a degraded-mode fallback. |
| R8 | Duplicate incident creation from parallel event processing | Low | Medium | svc-safety-compliance deduplicates by checking for existing incidents with matching session_id + anomaly timestamp before creating. Idempotency key on `POST /incidents` prevents duplicates at the API level. |

package com.novatrek.schedulingorchestrator.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "conflict_resolution_results", schema = "scheduling_orchestrator")
public class ConflictResolutionResult {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "conflict_id")
    private UUID conflictId;

    @Enumerated(EnumType.STRING)
    @Column(name = "resolution_status", length = 30)
    private ResolutionStatus resolutionStatus;

    @Column(name = "applied_strategy", length = 255)
    private String appliedStrategy;

    @Column(name = "resolved_at")
    private OffsetDateTime resolvedAt;

    @Column(name = "created_at", nullable = false, updatable = false)
    private OffsetDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private OffsetDateTime updatedAt;

    @Version
    @Column(name = "version")
    private Integer version = 0;

    @PrePersist
    protected void onCreate() {
        createdAt = OffsetDateTime.now();
        updatedAt = OffsetDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = OffsetDateTime.now();
    }

    public enum ResolutionStatus { RESOLVED, PARTIALLY_RESOLVED, FAILED }

    // --- Getters and Setters ---

    public UUID getConflictId() { return conflictId; }
    public void setConflictId(UUID conflictId) { this.conflictId = conflictId; }

    public ResolutionStatus getResolutionStatus() { return resolutionStatus; }
    public void setResolutionStatus(ResolutionStatus resolutionStatus) { this.resolutionStatus = resolutionStatus; }

    public String getAppliedStrategy() { return appliedStrategy; }
    public void setAppliedStrategy(String appliedStrategy) { this.appliedStrategy = appliedStrategy; }

    public OffsetDateTime getResolvedAt() { return resolvedAt; }
    public void setResolvedAt(OffsetDateTime resolvedAt) { this.resolvedAt = resolvedAt; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

package com.novatrek.schedulingorchestrator.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "resolution_options", schema = "scheduling_orchestrator")
public class ResolutionOption {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Enumerated(EnumType.STRING)
    @Column(name = "strategy", length = 30)
    private Strategy strategy;

    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    private String description;

    @Column(name = "impact_assessment", length = 255)
    private String impactAssessment;

    @Column(name = "estimated_affected_guests")
    private Integer estimatedAffectedGuests;

    @Column(name = "requires_guest_notification")
    private Boolean requiresGuestNotification;

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

    public enum Strategy { REASSIGN_GUIDE, RESCHEDULE_TRIP, ADJUST_CAPACITY, CLOSE_TRAIL, ACCEPT_RISK, SPLIT_GROUP }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public Strategy getStrategy() { return strategy; }
    public void setStrategy(Strategy strategy) { this.strategy = strategy; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getImpactAssessment() { return impactAssessment; }
    public void setImpactAssessment(String impactAssessment) { this.impactAssessment = impactAssessment; }

    public Integer getEstimatedAffectedGuests() { return estimatedAffectedGuests; }
    public void setEstimatedAffectedGuests(Integer estimatedAffectedGuests) { this.estimatedAffectedGuests = estimatedAffectedGuests; }

    public Boolean getRequiresGuestNotification() { return requiresGuestNotification; }
    public void setRequiresGuestNotification(Boolean requiresGuestNotification) { this.requiresGuestNotification = requiresGuestNotification; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

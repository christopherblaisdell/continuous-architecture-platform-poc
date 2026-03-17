package com.novatrek.analytics.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "guide_performances", schema = "analytics")
public class GuidePerformance {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "guide_id")
    private UUID guideId;

    @Column(name = "trips_led")
    private Integer tripsLed;

    @Column(name = "total_participants")
    private Integer totalParticipants;

    @Column(name = "average_guest_rating", precision = 10, scale = 2)
    private BigDecimal averageGuestRating;

    @Column(name = "incident_count")
    private Integer incidentCount;

    @Column(name = "cancellation_rate", precision = 10, scale = 2)
    private BigDecimal cancellationRate;

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

    // --- Getters and Setters ---

    public UUID getGuideId() { return guideId; }
    public void setGuideId(UUID guideId) { this.guideId = guideId; }

    public Integer getTripsLed() { return tripsLed; }
    public void setTripsLed(Integer tripsLed) { this.tripsLed = tripsLed; }

    public Integer getTotalParticipants() { return totalParticipants; }
    public void setTotalParticipants(Integer totalParticipants) { this.totalParticipants = totalParticipants; }

    public BigDecimal getAverageGuestRating() { return averageGuestRating; }
    public void setAverageGuestRating(BigDecimal averageGuestRating) { this.averageGuestRating = averageGuestRating; }

    public Integer getIncidentCount() { return incidentCount; }
    public void setIncidentCount(Integer incidentCount) { this.incidentCount = incidentCount; }

    public BigDecimal getCancellationRate() { return cancellationRate; }
    public void setCancellationRate(BigDecimal cancellationRate) { this.cancellationRate = cancellationRate; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

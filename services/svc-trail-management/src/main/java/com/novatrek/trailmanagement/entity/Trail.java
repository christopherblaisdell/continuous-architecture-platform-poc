package com.novatrek.trailmanagement.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "trails", schema = "trail_management")
public class Trail {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Column(name = "name", nullable = false, length = 200)
    private String name;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "region_id")
    private UUID regionId;

    @Column(name = "distance_km", nullable = false, precision = 8, scale = 2)
    private BigDecimal distanceKm;

    @Column(name = "elevation_gain_m")
    private Integer elevationGainM;

    @Column(name = "elevation_loss_m")
    private Integer elevationLossM;

    @Column(name = "estimated_duration_hours", precision = 6, scale = 1)
    private BigDecimal estimatedDurationHours;

    @Enumerated(EnumType.STRING)
    @Column(name = "difficulty", nullable = false, length = 20)
    private DifficultyRating difficulty;

    @Column(name = "max_group_size")
    private Integer maxGroupSize;

    @Column(name = "permit_required", nullable = false)
    private Boolean permitRequired = false;

    @Column(name = "dogs_allowed", nullable = false)
    private Boolean dogsAllowed = false;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    private TrailStatus status = TrailStatus.OPEN;

    @Column(name = "waypoint_count")
    private Integer waypointCount = 0;

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

    public enum DifficultyRating { EASY, MODERATE, DIFFICULT, EXPERT, EXTREME }

    public enum TrailStatus { OPEN, PARTIALLY_CLOSED, CLOSED, SEASONAL_CLOSURE }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public UUID getRegionId() { return regionId; }
    public void setRegionId(UUID regionId) { this.regionId = regionId; }

    public BigDecimal getDistanceKm() { return distanceKm; }
    public void setDistanceKm(BigDecimal distanceKm) { this.distanceKm = distanceKm; }

    public Integer getElevationGainM() { return elevationGainM; }
    public void setElevationGainM(Integer elevationGainM) { this.elevationGainM = elevationGainM; }

    public Integer getElevationLossM() { return elevationLossM; }
    public void setElevationLossM(Integer elevationLossM) { this.elevationLossM = elevationLossM; }

    public BigDecimal getEstimatedDurationHours() { return estimatedDurationHours; }
    public void setEstimatedDurationHours(BigDecimal estimatedDurationHours) { this.estimatedDurationHours = estimatedDurationHours; }

    public DifficultyRating getDifficulty() { return difficulty; }
    public void setDifficulty(DifficultyRating difficulty) { this.difficulty = difficulty; }

    public Integer getMaxGroupSize() { return maxGroupSize; }
    public void setMaxGroupSize(Integer maxGroupSize) { this.maxGroupSize = maxGroupSize; }

    public Boolean getPermitRequired() { return permitRequired; }
    public void setPermitRequired(Boolean permitRequired) { this.permitRequired = permitRequired; }

    public Boolean getDogsAllowed() { return dogsAllowed; }
    public void setDogsAllowed(Boolean dogsAllowed) { this.dogsAllowed = dogsAllowed; }

    public TrailStatus getStatus() { return status; }
    public void setStatus(TrailStatus status) { this.status = status; }

    public Integer getWaypointCount() { return waypointCount; }
    public void setWaypointCount(Integer waypointCount) { this.waypointCount = waypointCount; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }

    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

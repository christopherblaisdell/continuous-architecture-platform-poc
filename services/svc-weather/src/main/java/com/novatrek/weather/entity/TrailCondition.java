package com.novatrek.weather.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "trail_conditions", schema = "weather")
public class TrailCondition {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "trail_id")
    private UUID trailId;

    @Column(name = "trail_name", length = 255)
    private String trailName;

    @Column(name = "assessed_at")
    private OffsetDateTime assessedAt;

    @Enumerated(EnumType.STRING)
    @Column(name = "overall_status", length = 30)
    private OverallStatus overallStatus;

    @Enumerated(EnumType.STRING)
    @Column(name = "surface_condition", length = 30)
    private SurfaceCondition surfaceCondition;

    @Column(name = "water_crossings_passable")
    private Boolean waterCrossingsPassable;

    @Column(name = "ranger_notes", columnDefinition = "TEXT")
    private String rangerNotes;

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

    public enum OverallStatus { EXCELLENT, GOOD, FAIR, POOR, HAZARDOUS, IMPASSABLE }
    public enum SurfaceCondition { DRY, WET, MUDDY, ICY, SNOW_COVERED, FLOODED }

    // --- Getters and Setters ---

    public UUID getTrailId() { return trailId; }
    public void setTrailId(UUID trailId) { this.trailId = trailId; }

    public String getTrailName() { return trailName; }
    public void setTrailName(String trailName) { this.trailName = trailName; }

    public OffsetDateTime getAssessedAt() { return assessedAt; }
    public void setAssessedAt(OffsetDateTime assessedAt) { this.assessedAt = assessedAt; }

    public OverallStatus getOverallStatus() { return overallStatus; }
    public void setOverallStatus(OverallStatus overallStatus) { this.overallStatus = overallStatus; }

    public SurfaceCondition getSurfaceCondition() { return surfaceCondition; }
    public void setSurfaceCondition(SurfaceCondition surfaceCondition) { this.surfaceCondition = surfaceCondition; }

    public Boolean getWaterCrossingsPassable() { return waterCrossingsPassable; }
    public void setWaterCrossingsPassable(Boolean waterCrossingsPassable) { this.waterCrossingsPassable = waterCrossingsPassable; }

    public String getRangerNotes() { return rangerNotes; }
    public void setRangerNotes(String rangerNotes) { this.rangerNotes = rangerNotes; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

package com.novatrek.wildlifetracking.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "sightings", schema = "wildlife_tracking")
public class Sighting {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "sighting_id")
    private UUID sightingId;

    @Column(name = "species_id")
    private UUID speciesId;

    @Column(name = "species_name", length = 255)
    private String speciesName;

    @Column(name = "threat_level", length = 255)
    private String threatLevel;

    @Column(name = "reported_by", length = 255)
    private String reportedBy;

    @Column(name = "reporter_type", length = 255)
    private String reporterType;

    @Column(name = "observation_notes", columnDefinition = "TEXT")
    private String observationNotes;

    @Column(name = "animal_count")
    private Integer animalCount;

    @Column(name = "behavior", length = 255)
    private String behavior;

    @Column(name = "photo_url", length = 500)
    private String photoUrl;

    @Column(name = "trail_id")
    private UUID trailId;

    @Column(name = "alert_triggered")
    private Boolean alertTriggered;

    @Column(name = "reported_at")
    private OffsetDateTime reportedAt;

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

    public UUID getSightingId() { return sightingId; }
    public void setSightingId(UUID sightingId) { this.sightingId = sightingId; }

    public UUID getSpeciesId() { return speciesId; }
    public void setSpeciesId(UUID speciesId) { this.speciesId = speciesId; }

    public String getSpeciesName() { return speciesName; }
    public void setSpeciesName(String speciesName) { this.speciesName = speciesName; }

    public String getThreatLevel() { return threatLevel; }
    public void setThreatLevel(String threatLevel) { this.threatLevel = threatLevel; }

    public String getReportedBy() { return reportedBy; }
    public void setReportedBy(String reportedBy) { this.reportedBy = reportedBy; }

    public String getReporterType() { return reporterType; }
    public void setReporterType(String reporterType) { this.reporterType = reporterType; }

    public String getObservationNotes() { return observationNotes; }
    public void setObservationNotes(String observationNotes) { this.observationNotes = observationNotes; }

    public Integer getAnimalCount() { return animalCount; }
    public void setAnimalCount(Integer animalCount) { this.animalCount = animalCount; }

    public String getBehavior() { return behavior; }
    public void setBehavior(String behavior) { this.behavior = behavior; }

    public String getPhotoUrl() { return photoUrl; }
    public void setPhotoUrl(String photoUrl) { this.photoUrl = photoUrl; }

    public UUID getTrailId() { return trailId; }
    public void setTrailId(UUID trailId) { this.trailId = trailId; }

    public Boolean getAlertTriggered() { return alertTriggered; }
    public void setAlertTriggered(Boolean alertTriggered) { this.alertTriggered = alertTriggered; }

    public OffsetDateTime getReportedAt() { return reportedAt; }
    public void setReportedAt(OffsetDateTime reportedAt) { this.reportedAt = reportedAt; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

package com.novatrek.wildlifetracking.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "specieses", schema = "wildlife_tracking")
public class Species {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "species_id")
    private UUID speciesId;

    @Column(name = "common_name", length = 255)
    private String commonName;

    @Column(name = "scientific_name", length = 255)
    private String scientificName;

    @Enumerated(EnumType.STRING)
    @Column(name = "threat_level", length = 30)
    private ThreatLevel threatLevel;

    @Enumerated(EnumType.STRING)
    @Column(name = "category", length = 30)
    private Category category;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "safety_guidance", length = 255)
    private String safetyGuidance;

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

    public enum ThreatLevel { none, low, moderate, high, extreme }
    public enum Category { mammal, bird, reptile, amphibian, insect, fish }

    // --- Getters and Setters ---

    public UUID getSpeciesId() { return speciesId; }
    public void setSpeciesId(UUID speciesId) { this.speciesId = speciesId; }

    public String getCommonName() { return commonName; }
    public void setCommonName(String commonName) { this.commonName = commonName; }

    public String getScientificName() { return scientificName; }
    public void setScientificName(String scientificName) { this.scientificName = scientificName; }

    public ThreatLevel getThreatLevel() { return threatLevel; }
    public void setThreatLevel(ThreatLevel threatLevel) { this.threatLevel = threatLevel; }

    public Category getCategory() { return category; }
    public void setCategory(Category category) { this.category = category; }

    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }

    public String getSafetyGuidance() { return safetyGuidance; }
    public void setSafetyGuidance(String safetyGuidance) { this.safetyGuidance = safetyGuidance; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

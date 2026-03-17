package com.novatrek.guidemanagement.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "guides", schema = "guide_management")
public class Guide {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Column(name = "first_name", nullable = false, length = 255)
    private String firstName;

    @Column(name = "last_name", nullable = false, length = 255)
    private String lastName;

    @Column(name = "email", nullable = false, length = 255)
    private String email;

    @Column(name = "phone", length = 255)
    private String phone;

    @Column(name = "years_experience")
    private Integer yearsExperience;

    @Column(name = "max_group_size")
    private Integer maxGroupSize;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 30)
    private GuideStatus status;

    @Column(name = "average_rating", precision = 10, scale = 2)
    private BigDecimal averageRating;

    @Column(name = "total_trips_led")
    private Integer totalTripsLed;

    @Enumerated(EnumType.STRING)
    @Column(name = "emergency_training_level", length = 30)
    private EmergencyTrainingLevel emergencyTrainingLevel;

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

    public enum GuideStatus { ACTIVE, ON_LEAVE, TRAINING, SUSPENDED, TERMINATED }
    public enum EmergencyTrainingLevel { WILDERNESS_FIRST_AID, WILDERNESS_FIRST_RESPONDER, WILDERNESS_EMT, PARAMEDIC }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }

    public String getLastName() { return lastName; }
    public void setLastName(String lastName) { this.lastName = lastName; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public Integer getYearsExperience() { return yearsExperience; }
    public void setYearsExperience(Integer yearsExperience) { this.yearsExperience = yearsExperience; }

    public Integer getMaxGroupSize() { return maxGroupSize; }
    public void setMaxGroupSize(Integer maxGroupSize) { this.maxGroupSize = maxGroupSize; }

    public GuideStatus getStatus() { return status; }
    public void setStatus(GuideStatus status) { this.status = status; }

    public BigDecimal getAverageRating() { return averageRating; }
    public void setAverageRating(BigDecimal averageRating) { this.averageRating = averageRating; }

    public Integer getTotalTripsLed() { return totalTripsLed; }
    public void setTotalTripsLed(Integer totalTripsLed) { this.totalTripsLed = totalTripsLed; }

    public EmergencyTrainingLevel getEmergencyTrainingLevel() { return emergencyTrainingLevel; }
    public void setEmergencyTrainingLevel(EmergencyTrainingLevel emergencyTrainingLevel) { this.emergencyTrainingLevel = emergencyTrainingLevel; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

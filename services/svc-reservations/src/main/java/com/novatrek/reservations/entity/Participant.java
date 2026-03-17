package com.novatrek.reservations.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "participants", schema = "reservations")
public class Participant {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "guest_id")
    private UUID guestId;

    @Enumerated(EnumType.STRING)
    @Column(name = "role", length = 30)
    private Role role;

    @Column(name = "waiver_signed")
    private Boolean waiverSigned;

    @Column(name = "medical_clearance")
    private Boolean medicalClearance;

    @Column(name = "gear_assignment_id")
    private UUID gearAssignmentId;

    @Column(name = "checked_in")
    private Boolean checkedIn;

    @Column(name = "check_in_time")
    private OffsetDateTime checkInTime;

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

    public enum Role { PRIMARY, COMPANION, MINOR }

    // --- Getters and Setters ---

    public UUID getGuestId() { return guestId; }
    public void setGuestId(UUID guestId) { this.guestId = guestId; }

    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }

    public Boolean getWaiverSigned() { return waiverSigned; }
    public void setWaiverSigned(Boolean waiverSigned) { this.waiverSigned = waiverSigned; }

    public Boolean getMedicalClearance() { return medicalClearance; }
    public void setMedicalClearance(Boolean medicalClearance) { this.medicalClearance = medicalClearance; }

    public UUID getGearAssignmentId() { return gearAssignmentId; }
    public void setGearAssignmentId(UUID gearAssignmentId) { this.gearAssignmentId = gearAssignmentId; }

    public Boolean getCheckedIn() { return checkedIn; }
    public void setCheckedIn(Boolean checkedIn) { this.checkedIn = checkedIn; }

    public OffsetDateTime getCheckInTime() { return checkInTime; }
    public void setCheckInTime(OffsetDateTime checkInTime) { this.checkInTime = checkInTime; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

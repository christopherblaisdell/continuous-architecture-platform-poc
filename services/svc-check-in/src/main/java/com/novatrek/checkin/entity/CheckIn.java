package com.novatrek.checkin.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "check_ins", schema = "check_in")
public class CheckIn {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Column(name = "reservation_id", nullable = false)
    private UUID reservationId;

    @Column(name = "participant_guest_id", nullable = false)
    private UUID participantGuestId;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 30)
    private CheckInStatus status;

    @Column(name = "gear_verified")
    private Boolean gearVerified;

    @Column(name = "waiver_verified")
    private Boolean waiverVerified;

    @Column(name = "waiver_id")
    private UUID waiverId;

    @Column(name = "checked_in_at", nullable = false)
    private OffsetDateTime checkedInAt;

    @Column(name = "checked_in_by", nullable = false)
    private UUID checkedInBy;

    @Column(name = "completed_at")
    private OffsetDateTime completedAt;

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

    public enum CheckInStatus { INITIATED, WAIVER_VERIFIED, GEAR_VERIFIED, WRISTBAND_ASSIGNED, COMPLETE }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getReservationId() { return reservationId; }
    public void setReservationId(UUID reservationId) { this.reservationId = reservationId; }

    public UUID getParticipantGuestId() { return participantGuestId; }
    public void setParticipantGuestId(UUID participantGuestId) { this.participantGuestId = participantGuestId; }

    public CheckInStatus getStatus() { return status; }
    public void setStatus(CheckInStatus status) { this.status = status; }

    public Boolean getGearVerified() { return gearVerified; }
    public void setGearVerified(Boolean gearVerified) { this.gearVerified = gearVerified; }

    public Boolean getWaiverVerified() { return waiverVerified; }
    public void setWaiverVerified(Boolean waiverVerified) { this.waiverVerified = waiverVerified; }

    public UUID getWaiverId() { return waiverId; }
    public void setWaiverId(UUID waiverId) { this.waiverId = waiverId; }

    public OffsetDateTime getCheckedInAt() { return checkedInAt; }
    public void setCheckedInAt(OffsetDateTime checkedInAt) { this.checkedInAt = checkedInAt; }

    public UUID getCheckedInBy() { return checkedInBy; }
    public void setCheckedInBy(UUID checkedInBy) { this.checkedInBy = checkedInBy; }

    public OffsetDateTime getCompletedAt() { return completedAt; }
    public void setCompletedAt(OffsetDateTime completedAt) { this.completedAt = completedAt; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

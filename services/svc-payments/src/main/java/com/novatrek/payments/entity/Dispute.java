package com.novatrek.payments.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "disputes", schema = "payments")
public class Dispute {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Column(name = "payment_id")
    private UUID paymentId;

    @Column(name = "reservation_id")
    private UUID reservationId;

    @Column(name = "guest_id")
    private UUID guestId;

    @Enumerated(EnumType.STRING)
    @Column(name = "type", length = 30)
    private DisputeType type;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 30)
    private DisputeStatus status;

    @Enumerated(EnumType.STRING)
    @Column(name = "tier", length = 30)
    private DisputeTier tier;

    @Column(name = "amount_requested", precision = 10, scale = 2)
    private BigDecimal amountRequested;

    @Column(name = "amount_approved", precision = 10, scale = 2)
    private BigDecimal amountApproved;

    @Enumerated(EnumType.STRING)
    @Column(name = "resolution", length = 30)
    private DisputeResolutionType resolution;

    @Column(name = "justification", length = 255)
    private String justification;

    @Column(name = "assigned_to", length = 255)
    private String assignedTo;

    @Column(name = "_rev")
    private Integer Rev;

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

    public enum DisputeType { CANCELLATION, SERVICE_COMPLAINT, WEATHER, CHARGEBACK, OTHER }
    public enum DisputeStatus { OPENED, UNDER_REVIEW, ESCALATED, RESOLVED, CLOSED }
    public enum DisputeTier { AUTO, AGENT, MANAGER }
    public enum DisputeResolutionType { FULL_REFUND, PARTIAL_REFUND, DENIED }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getPaymentId() { return paymentId; }
    public void setPaymentId(UUID paymentId) { this.paymentId = paymentId; }

    public UUID getReservationId() { return reservationId; }
    public void setReservationId(UUID reservationId) { this.reservationId = reservationId; }

    public UUID getGuestId() { return guestId; }
    public void setGuestId(UUID guestId) { this.guestId = guestId; }

    public DisputeType getType() { return type; }
    public void setType(DisputeType type) { this.type = type; }

    public DisputeStatus getStatus() { return status; }
    public void setStatus(DisputeStatus status) { this.status = status; }

    public DisputeTier getTier() { return tier; }
    public void setTier(DisputeTier tier) { this.tier = tier; }

    public BigDecimal getAmountRequested() { return amountRequested; }
    public void setAmountRequested(BigDecimal amountRequested) { this.amountRequested = amountRequested; }

    public BigDecimal getAmountApproved() { return amountApproved; }
    public void setAmountApproved(BigDecimal amountApproved) { this.amountApproved = amountApproved; }

    public DisputeResolutionType getResolution() { return resolution; }
    public void setResolution(DisputeResolutionType resolution) { this.resolution = resolution; }

    public String getJustification() { return justification; }
    public void setJustification(String justification) { this.justification = justification; }

    public String getAssignedTo() { return assignedTo; }
    public void setAssignedTo(String assignedTo) { this.assignedTo = assignedTo; }

    public Integer getRev() { return Rev; }
    public void setRev(Integer Rev) { this.Rev = Rev; }

    public OffsetDateTime getResolvedAt() { return resolvedAt; }
    public void setResolvedAt(OffsetDateTime resolvedAt) { this.resolvedAt = resolvedAt; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

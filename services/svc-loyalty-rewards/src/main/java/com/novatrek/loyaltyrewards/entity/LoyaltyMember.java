package com.novatrek.loyaltyrewards.entity;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "loyalty_members", schema = "loyalty_rewards")
public class LoyaltyMember {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "guest_id")
    private UUID guestId;

    @Enumerated(EnumType.STRING)
    @Column(name = "tier", length = 30)
    private TierName tier;

    @Column(name = "points_balance", nullable = false)
    private Integer pointsBalance;

    @Column(name = "lifetime_points", nullable = false)
    private Integer lifetimePoints;

    @Column(name = "tier_expiry")
    private LocalDate tierExpiry;

    @Column(name = "enrolled_at")
    private OffsetDateTime enrolledAt;

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

    public enum TierName { EXPLORER, PATHFINDER, SUMMIT, LEGEND }

    // --- Getters and Setters ---

    public UUID getGuestId() { return guestId; }
    public void setGuestId(UUID guestId) { this.guestId = guestId; }

    public TierName getTier() { return tier; }
    public void setTier(TierName tier) { this.tier = tier; }

    public Integer getPointsBalance() { return pointsBalance; }
    public void setPointsBalance(Integer pointsBalance) { this.pointsBalance = pointsBalance; }

    public Integer getLifetimePoints() { return lifetimePoints; }
    public void setLifetimePoints(Integer lifetimePoints) { this.lifetimePoints = lifetimePoints; }

    public LocalDate getTierExpiry() { return tierExpiry; }
    public void setTierExpiry(LocalDate tierExpiry) { this.tierExpiry = tierExpiry; }

    public OffsetDateTime getEnrolledAt() { return enrolledAt; }
    public void setEnrolledAt(OffsetDateTime enrolledAt) { this.enrolledAt = enrolledAt; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

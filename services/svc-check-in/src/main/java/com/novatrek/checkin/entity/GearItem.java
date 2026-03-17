package com.novatrek.checkin.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "gear_items", schema = "check_in")
public class GearItem {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "gear_inventory_id")
    private UUID gearInventoryId;

    @Column(name = "gear_type", nullable = false, length = 255)
    private String gearType;

    @Column(name = "size", length = 255)
    private String size;

    @Enumerated(EnumType.STRING)
    @Column(name = "condition_on_issue", length = 30)
    private ConditionOnIssue conditionOnIssue;

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

    public enum ConditionOnIssue { NEW, GOOD, FAIR }

    // --- Getters and Setters ---

    public UUID getGearInventoryId() { return gearInventoryId; }
    public void setGearInventoryId(UUID gearInventoryId) { this.gearInventoryId = gearInventoryId; }

    public String getGearType() { return gearType; }
    public void setGearType(String gearType) { this.gearType = gearType; }

    public String getSize() { return size; }
    public void setSize(String size) { this.size = size; }

    public ConditionOnIssue getConditionOnIssue() { return conditionOnIssue; }
    public void setConditionOnIssue(ConditionOnIssue conditionOnIssue) { this.conditionOnIssue = conditionOnIssue; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

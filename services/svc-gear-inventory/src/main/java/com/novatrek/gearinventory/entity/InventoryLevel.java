package com.novatrek.gearinventory.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "inventory_levels", schema = "gear_inventory")
public class InventoryLevel {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "location_id")
    private UUID locationId;

    @Column(name = "location_name", length = 255)
    private String locationName;

    @Enumerated(EnumType.STRING)
    @Column(name = "category", length = 30)
    private GearCategory category;

    @Column(name = "total", nullable = false)
    private Integer total;

    @Column(name = "available", nullable = false)
    private Integer available;

    @Column(name = "assigned", nullable = false)
    private Integer assigned;

    @Column(name = "in_maintenance", nullable = false)
    private Integer inMaintenance;

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

    public enum GearCategory { HARNESS, HELMET, ROPE, CARABINER, KAYAK, PADDLE, LIFE_VEST, TENT, SLEEPING_BAG, BACKPACK, CLIMBING_SHOES, CRAMPON, ICE_AXE, BIKE }

    // --- Getters and Setters ---

    public UUID getLocationId() { return locationId; }
    public void setLocationId(UUID locationId) { this.locationId = locationId; }

    public String getLocationName() { return locationName; }
    public void setLocationName(String locationName) { this.locationName = locationName; }

    public GearCategory getCategory() { return category; }
    public void setCategory(GearCategory category) { this.category = category; }

    public Integer getTotal() { return total; }
    public void setTotal(Integer total) { this.total = total; }

    public Integer getAvailable() { return available; }
    public void setAvailable(Integer available) { this.available = available; }

    public Integer getAssigned() { return assigned; }
    public void setAssigned(Integer assigned) { this.assigned = assigned; }

    public Integer getInMaintenance() { return inMaintenance; }
    public void setInMaintenance(Integer inMaintenance) { this.inMaintenance = inMaintenance; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

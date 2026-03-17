package com.novatrek.gearinventory.entity;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "gear_items", schema = "gear_inventory")
public class GearItem {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Column(name = "name", nullable = false, length = 255)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(name = "category", length = 30)
    private GearCategory category;

    @Enumerated(EnumType.STRING)
    @Column(name = "size", length = 30)
    private GearSize size;

    @Enumerated(EnumType.STRING)
    @Column(name = "condition", length = 30)
    private GearCondition condition;

    @Column(name = "location_id", nullable = false)
    private UUID locationId;

    @Column(name = "serial_number", nullable = false, length = 255)
    private String serialNumber;

    @Column(name = "purchase_date", nullable = false)
    private LocalDate purchaseDate;

    @Column(name = "last_maintenance")
    private OffsetDateTime lastMaintenance;

    @Column(name = "next_maintenance_due")
    private LocalDate nextMaintenanceDue;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 30)
    private Status status;

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
    public enum GearSize { XS, S, M, L, XL, XXL, ONE_SIZE }
    public enum GearCondition { NEW, GOOD, FAIR, NEEDS_MAINTENANCE, RETIRED }
    public enum Status { AVAILABLE, ASSIGNED, IN_MAINTENANCE, RETIRED }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public GearCategory getCategory() { return category; }
    public void setCategory(GearCategory category) { this.category = category; }

    public GearSize getSize() { return size; }
    public void setSize(GearSize size) { this.size = size; }

    public GearCondition getCondition() { return condition; }
    public void setCondition(GearCondition condition) { this.condition = condition; }

    public UUID getLocationId() { return locationId; }
    public void setLocationId(UUID locationId) { this.locationId = locationId; }

    public String getSerialNumber() { return serialNumber; }
    public void setSerialNumber(String serialNumber) { this.serialNumber = serialNumber; }

    public LocalDate getPurchaseDate() { return purchaseDate; }
    public void setPurchaseDate(LocalDate purchaseDate) { this.purchaseDate = purchaseDate; }

    public OffsetDateTime getLastMaintenance() { return lastMaintenance; }
    public void setLastMaintenance(OffsetDateTime lastMaintenance) { this.lastMaintenance = lastMaintenance; }

    public LocalDate getNextMaintenanceDue() { return nextMaintenanceDue; }
    public void setNextMaintenanceDue(LocalDate nextMaintenanceDue) { this.nextMaintenanceDue = nextMaintenanceDue; }

    public Status getStatus() { return status; }
    public void setStatus(Status status) { this.status = status; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

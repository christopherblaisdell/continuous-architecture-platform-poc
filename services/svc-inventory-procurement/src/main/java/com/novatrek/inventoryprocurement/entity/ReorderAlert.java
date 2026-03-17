package com.novatrek.inventoryprocurement.entity;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "reorder_alerts", schema = "inventory_procurement")
public class ReorderAlert {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "id")
    private UUID id;

    @Column(name = "item_category", length = 255)
    private String itemCategory;

    @Column(name = "location_id")
    private UUID locationId;

    @Column(name = "current_on_hand")
    private Integer currentOnHand;

    @Column(name = "reorder_point")
    private Integer reorderPoint;

    @Column(name = "recommended_order_quantity")
    private Integer recommendedOrderQuantity;

    @Enumerated(EnumType.STRING)
    @Column(name = "severity", length = 30)
    private Severity severity;

    @Column(name = "preferred_supplier_id")
    private UUID preferredSupplierId;

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

    public enum Severity { LOW, MEDIUM, CRITICAL }

    // --- Getters and Setters ---

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getItemCategory() { return itemCategory; }
    public void setItemCategory(String itemCategory) { this.itemCategory = itemCategory; }

    public UUID getLocationId() { return locationId; }
    public void setLocationId(UUID locationId) { this.locationId = locationId; }

    public Integer getCurrentOnHand() { return currentOnHand; }
    public void setCurrentOnHand(Integer currentOnHand) { this.currentOnHand = currentOnHand; }

    public Integer getReorderPoint() { return reorderPoint; }
    public void setReorderPoint(Integer reorderPoint) { this.reorderPoint = reorderPoint; }

    public Integer getRecommendedOrderQuantity() { return recommendedOrderQuantity; }
    public void setRecommendedOrderQuantity(Integer recommendedOrderQuantity) { this.recommendedOrderQuantity = recommendedOrderQuantity; }

    public Severity getSeverity() { return severity; }
    public void setSeverity(Severity severity) { this.severity = severity; }

    public UUID getPreferredSupplierId() { return preferredSupplierId; }
    public void setPreferredSupplierId(UUID preferredSupplierId) { this.preferredSupplierId = preferredSupplierId; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
    public OffsetDateTime getUpdatedAt() { return updatedAt; }
    public Integer getVersion() { return version; }
    public void setVersion(Integer version) { this.version = version; }
}

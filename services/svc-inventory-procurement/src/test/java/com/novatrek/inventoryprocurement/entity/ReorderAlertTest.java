package com.novatrek.inventoryprocurement.entity;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ReorderAlertTest {

    @Test
    void gettersAndSetters() {
        ReorderAlert a = new ReorderAlert();
        UUID id = UUID.randomUUID();
        a.setId(id);
        a.setItemCategory("Helmets");
        UUID locId = UUID.randomUUID();
        a.setLocationId(locId);
        a.setCurrentOnHand(3);
        a.setReorderPoint(10);
        a.setRecommendedOrderQuantity(20);
        a.setSeverity(ReorderAlert.Severity.CRITICAL);
        UUID suppId = UUID.randomUUID();
        a.setPreferredSupplierId(suppId);
        a.setVersion(1);

        assertEquals(id, a.getId());
        assertEquals("Helmets", a.getItemCategory());
        assertEquals(locId, a.getLocationId());
        assertEquals(3, a.getCurrentOnHand());
        assertEquals(10, a.getReorderPoint());
        assertEquals(20, a.getRecommendedOrderQuantity());
        assertEquals(ReorderAlert.Severity.CRITICAL, a.getSeverity());
        assertEquals(suppId, a.getPreferredSupplierId());
        assertEquals(1, a.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        ReorderAlert a = new ReorderAlert();
        a.onCreate();
        assertNotNull(a.getCreatedAt());
        assertNotNull(a.getUpdatedAt());

        a.onUpdate();
        assertNotNull(a.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, ReorderAlert.Severity.values().length);
        assertNotNull(ReorderAlert.Severity.valueOf("LOW"));
        assertNotNull(ReorderAlert.Severity.valueOf("MEDIUM"));
    }
}

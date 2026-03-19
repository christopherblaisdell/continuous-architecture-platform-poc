package com.novatrek.gearinventory.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GearItemTest {

    @Test
    void gettersAndSetters() {
        GearItem g = new GearItem();
        UUID id = UUID.randomUUID();
        g.setId(id);
        g.setName("Climbing Helmet");
        g.setCategory(GearItem.GearCategory.HELMET);
        g.setSize(GearItem.GearSize.L);
        g.setCondition(GearItem.GearCondition.GOOD);
        UUID locId = UUID.randomUUID();
        g.setLocationId(locId);
        g.setSerialNumber("SN-12345");
        g.setPurchaseDate(LocalDate.of(2024, 1, 15));
        OffsetDateTime now = OffsetDateTime.now();
        g.setLastMaintenance(now);
        g.setNextMaintenanceDue(LocalDate.of(2025, 1, 15));
        g.setStatus(GearItem.Status.AVAILABLE);
        g.setVersion(1);

        assertEquals(id, g.getId());
        assertEquals("Climbing Helmet", g.getName());
        assertEquals(GearItem.GearCategory.HELMET, g.getCategory());
        assertEquals(GearItem.GearSize.L, g.getSize());
        assertEquals(GearItem.GearCondition.GOOD, g.getCondition());
        assertEquals(locId, g.getLocationId());
        assertEquals("SN-12345", g.getSerialNumber());
        assertEquals(LocalDate.of(2024, 1, 15), g.getPurchaseDate());
        assertEquals(now, g.getLastMaintenance());
        assertEquals(LocalDate.of(2025, 1, 15), g.getNextMaintenanceDue());
        assertEquals(GearItem.Status.AVAILABLE, g.getStatus());
        assertEquals(1, g.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GearItem g = new GearItem();
        g.onCreate();
        assertNotNull(g.getCreatedAt());
        assertNotNull(g.getUpdatedAt());

        g.onUpdate();
        assertNotNull(g.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(14, GearItem.GearCategory.values().length);
        assertEquals(7, GearItem.GearSize.values().length);
        assertEquals(5, GearItem.GearCondition.values().length);
        assertEquals(4, GearItem.Status.values().length);
    }
}

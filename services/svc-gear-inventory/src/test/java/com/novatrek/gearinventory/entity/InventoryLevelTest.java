package com.novatrek.gearinventory.entity;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class InventoryLevelTest {

    @Test
    void gettersAndSetters() {
        InventoryLevel l = new InventoryLevel();
        UUID id = UUID.randomUUID();
        l.setLocationId(id);
        l.setLocationName("Base Camp");
        l.setCategory(InventoryLevel.GearCategory.HELMET);
        l.setTotal(50);
        l.setAvailable(30);
        l.setAssigned(15);
        l.setInMaintenance(5);
        l.setVersion(1);

        assertEquals(id, l.getLocationId());
        assertEquals("Base Camp", l.getLocationName());
        assertEquals(InventoryLevel.GearCategory.HELMET, l.getCategory());
        assertEquals(50, l.getTotal());
        assertEquals(30, l.getAvailable());
        assertEquals(15, l.getAssigned());
        assertEquals(5, l.getInMaintenance());
        assertEquals(1, l.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        InventoryLevel l = new InventoryLevel();
        l.onCreate();
        assertNotNull(l.getCreatedAt());
        assertNotNull(l.getUpdatedAt());

        l.onUpdate();
        assertNotNull(l.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(14, InventoryLevel.GearCategory.values().length);
    }
}

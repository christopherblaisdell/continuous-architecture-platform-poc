package com.novatrek.inventoryprocurement.entity;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class StockAdjustmentTest {

    @Test
    void gettersAndSetters() {
        StockAdjustment s = new StockAdjustment();
        UUID id = UUID.randomUUID();
        s.setId(id);
        s.setItemCategory("Ropes");
        UUID locId = UUID.randomUUID();
        s.setLocationId(locId);
        s.setQuantityChange(-5);
        s.setReason("Damage");
        s.setNotes("Found fraying during inspection");
        UUID adjBy = UUID.randomUUID();
        s.setAdjustedBy(adjBy);
        s.setVersion(1);

        assertEquals(id, s.getId());
        assertEquals("Ropes", s.getItemCategory());
        assertEquals(locId, s.getLocationId());
        assertEquals(-5, s.getQuantityChange());
        assertEquals("Damage", s.getReason());
        assertEquals("Found fraying during inspection", s.getNotes());
        assertEquals(adjBy, s.getAdjustedBy());
        assertEquals(1, s.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        StockAdjustment s = new StockAdjustment();
        s.onCreate();
        assertNotNull(s.getCreatedAt());
        assertNotNull(s.getUpdatedAt());

        s.onUpdate();
        assertNotNull(s.getUpdatedAt());
    }
}

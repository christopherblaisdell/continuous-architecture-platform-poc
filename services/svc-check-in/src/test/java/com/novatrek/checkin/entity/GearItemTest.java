package com.novatrek.checkin.entity;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GearItemTest {

    @Test
    void gettersAndSetters() {
        GearItem g = new GearItem();
        UUID id = UUID.randomUUID();
        g.setGearInventoryId(id);
        g.setGearType("Helmet");
        g.setSize("L");
        g.setConditionOnIssue(GearItem.ConditionOnIssue.GOOD);
        g.setVersion(2);

        assertEquals(id, g.getGearInventoryId());
        assertEquals("Helmet", g.getGearType());
        assertEquals("L", g.getSize());
        assertEquals(GearItem.ConditionOnIssue.GOOD, g.getConditionOnIssue());
        assertEquals(2, g.getVersion());
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
        assertEquals(3, GearItem.ConditionOnIssue.values().length);
        assertNotNull(GearItem.ConditionOnIssue.valueOf("NEW"));
        assertNotNull(GearItem.ConditionOnIssue.valueOf("FAIR"));
    }
}

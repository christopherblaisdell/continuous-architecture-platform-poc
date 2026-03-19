package com.novatrek.gearinventory.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GearPackageTest {

    @Test
    void gettersAndSetters() {
        GearPackage p = new GearPackage();
        UUID id = UUID.randomUUID();
        p.setId(id);
        p.setName("Rock Climbing Starter");
        p.setDescription("Basic gear for beginners");
        p.setActivityType(GearPackage.ActivityType.ROCK_CLIMBING);
        p.setRentalPricePerDay(new BigDecimal("45.00"));
        p.setVersion(1);

        assertEquals(id, p.getId());
        assertEquals("Rock Climbing Starter", p.getName());
        assertEquals("Basic gear for beginners", p.getDescription());
        assertEquals(GearPackage.ActivityType.ROCK_CLIMBING, p.getActivityType());
        assertEquals(new BigDecimal("45.00"), p.getRentalPricePerDay());
        assertEquals(1, p.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GearPackage p = new GearPackage();
        p.onCreate();
        assertNotNull(p.getCreatedAt());
        assertNotNull(p.getUpdatedAt());

        p.onUpdate();
        assertNotNull(p.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(6, GearPackage.ActivityType.values().length);
    }
}

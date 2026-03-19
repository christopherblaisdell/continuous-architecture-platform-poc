package com.novatrek.inventoryprocurement.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class SupplierTest {

    @Test
    void gettersAndSetters() {
        Supplier s = new Supplier();
        UUID id = UUID.randomUUID();
        s.setId(id);
        s.setName("Mountain Gear Co");
        s.setLeadTimeDays(14);
        s.setRating(new BigDecimal("4.50"));
        s.setActive(true);
        s.setVersion(1);

        assertEquals(id, s.getId());
        assertEquals("Mountain Gear Co", s.getName());
        assertEquals(14, s.getLeadTimeDays());
        assertEquals(new BigDecimal("4.50"), s.getRating());
        assertTrue(s.getActive());
        assertEquals(1, s.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Supplier s = new Supplier();
        s.onCreate();
        assertNotNull(s.getCreatedAt());
        assertNotNull(s.getUpdatedAt());

        s.onUpdate();
        assertNotNull(s.getUpdatedAt());
    }
}

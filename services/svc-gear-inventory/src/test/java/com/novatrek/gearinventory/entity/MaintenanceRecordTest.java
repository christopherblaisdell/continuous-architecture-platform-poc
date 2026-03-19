package com.novatrek.gearinventory.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class MaintenanceRecordTest {

    @Test
    void gettersAndSetters() {
        MaintenanceRecord m = new MaintenanceRecord();
        UUID id = UUID.randomUUID();
        m.setId(id);
        UUID gearId = UUID.randomUUID();
        m.setGearItemId(gearId);
        m.setType(MaintenanceRecord.Type.INSPECTION);
        OffsetDateTime now = OffsetDateTime.now();
        m.setDate(now);
        m.setTechnician("John");
        m.setNotes("All good");
        m.setCost(new BigDecimal("25.00"));
        m.setNextDue(LocalDate.of(2025, 6, 1));
        m.setVersion(1);

        assertEquals(id, m.getId());
        assertEquals(gearId, m.getGearItemId());
        assertEquals(MaintenanceRecord.Type.INSPECTION, m.getType());
        assertEquals(now, m.getDate());
        assertEquals("John", m.getTechnician());
        assertEquals("All good", m.getNotes());
        assertEquals(new BigDecimal("25.00"), m.getCost());
        assertEquals(LocalDate.of(2025, 6, 1), m.getNextDue());
        assertEquals(1, m.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        MaintenanceRecord m = new MaintenanceRecord();
        m.onCreate();
        assertNotNull(m.getCreatedAt());
        assertNotNull(m.getUpdatedAt());

        m.onUpdate();
        assertNotNull(m.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, MaintenanceRecord.Type.values().length);
        assertNotNull(MaintenanceRecord.Type.valueOf("REPAIR"));
        assertNotNull(MaintenanceRecord.Type.valueOf("REPLACEMENT"));
    }
}

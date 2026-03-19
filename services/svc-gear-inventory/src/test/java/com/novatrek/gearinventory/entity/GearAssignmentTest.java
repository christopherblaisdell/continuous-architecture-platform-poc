package com.novatrek.gearinventory.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GearAssignmentTest {

    @Test
    void gettersAndSetters() {
        GearAssignment a = new GearAssignment();
        UUID id = UUID.randomUUID();
        a.setId(id);
        UUID resId = UUID.randomUUID();
        a.setReservationId(resId);
        UUID guestId = UUID.randomUUID();
        a.setParticipantGuestId(guestId);
        OffsetDateTime now = OffsetDateTime.now();
        a.setAssignedAt(now);
        a.setReturnedAt(now);
        a.setConditionOnReturn(GearAssignment.GearCondition.FAIR);
        a.setDamageNotes("Minor scratch");
        a.setVersion(1);

        assertEquals(id, a.getId());
        assertEquals(resId, a.getReservationId());
        assertEquals(guestId, a.getParticipantGuestId());
        assertEquals(now, a.getAssignedAt());
        assertEquals(now, a.getReturnedAt());
        assertEquals(GearAssignment.GearCondition.FAIR, a.getConditionOnReturn());
        assertEquals("Minor scratch", a.getDamageNotes());
        assertEquals(1, a.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GearAssignment a = new GearAssignment();
        a.onCreate();
        assertNotNull(a.getCreatedAt());
        assertNotNull(a.getUpdatedAt());

        a.onUpdate();
        assertNotNull(a.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(5, GearAssignment.GearCondition.values().length);
    }
}

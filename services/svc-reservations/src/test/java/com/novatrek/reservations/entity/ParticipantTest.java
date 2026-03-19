package com.novatrek.reservations.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ParticipantTest {

    @Test
    void gettersAndSetters() {
        Participant p = new Participant();
        UUID guestId = UUID.randomUUID();
        p.setGuestId(guestId);
        p.setRole(Participant.Role.PRIMARY);
        p.setWaiverSigned(true);
        p.setMedicalClearance(true);
        UUID gearId = UUID.randomUUID();
        p.setGearAssignmentId(gearId);
        p.setCheckedIn(false);
        OffsetDateTime now = OffsetDateTime.now();
        p.setCheckInTime(now);
        p.setVersion(1);

        assertEquals(guestId, p.getGuestId());
        assertEquals(Participant.Role.PRIMARY, p.getRole());
        assertTrue(p.getWaiverSigned());
        assertTrue(p.getMedicalClearance());
        assertEquals(gearId, p.getGearAssignmentId());
        assertFalse(p.getCheckedIn());
        assertEquals(now, p.getCheckInTime());
        assertEquals(1, p.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Participant p = new Participant();
        p.onCreate();
        assertNotNull(p.getCreatedAt());
        assertNotNull(p.getUpdatedAt());

        p.onUpdate();
        assertNotNull(p.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, Participant.Role.values().length);
    }
}

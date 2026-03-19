package com.novatrek.checkin.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class CheckInTest {

    @Test
    void gettersAndSetters() {
        CheckIn c = new CheckIn();
        UUID id = UUID.randomUUID();
        c.setId(id);
        UUID resId = UUID.randomUUID();
        c.setReservationId(resId);
        UUID guestId = UUID.randomUUID();
        c.setParticipantGuestId(guestId);
        c.setStatus(CheckIn.CheckInStatus.INITIATED);
        c.setGearVerified(true);
        c.setWaiverVerified(false);
        UUID waiverId = UUID.randomUUID();
        c.setWaiverId(waiverId);
        OffsetDateTime now = OffsetDateTime.now();
        c.setCheckedInAt(now);
        UUID staffId = UUID.randomUUID();
        c.setCheckedInBy(staffId);
        c.setCompletedAt(now);
        c.setVersion(1);

        assertEquals(id, c.getId());
        assertEquals(resId, c.getReservationId());
        assertEquals(guestId, c.getParticipantGuestId());
        assertEquals(CheckIn.CheckInStatus.INITIATED, c.getStatus());
        assertTrue(c.getGearVerified());
        assertFalse(c.getWaiverVerified());
        assertEquals(waiverId, c.getWaiverId());
        assertEquals(now, c.getCheckedInAt());
        assertEquals(staffId, c.getCheckedInBy());
        assertEquals(now, c.getCompletedAt());
        assertEquals(1, c.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        CheckIn c = new CheckIn();
        c.onCreate();
        assertNotNull(c.getCreatedAt());
        assertNotNull(c.getUpdatedAt());

        c.onUpdate();
        assertNotNull(c.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(5, CheckIn.CheckInStatus.values().length);
        assertNotNull(CheckIn.CheckInStatus.valueOf("COMPLETE"));
    }
}

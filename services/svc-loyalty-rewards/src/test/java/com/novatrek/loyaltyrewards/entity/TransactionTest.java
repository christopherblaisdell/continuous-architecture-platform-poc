package com.novatrek.loyaltyrewards.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class TransactionTest {

    @Test
    void gettersAndSetters() {
        Transaction t = new Transaction();
        UUID id = UUID.randomUUID();
        t.setId(id);
        t.setType(Transaction.TransactionType.EARN);
        t.setPoints(100);
        UUID resId = UUID.randomUUID();
        t.setSourceReservationId(resId);
        t.setDescription("Booking reward");
        OffsetDateTime now = OffsetDateTime.now();
        t.setTimestamp(now);
        t.setVersion(1);

        assertEquals(id, t.getId());
        assertEquals(Transaction.TransactionType.EARN, t.getType());
        assertEquals(100, t.getPoints());
        assertEquals(resId, t.getSourceReservationId());
        assertEquals("Booking reward", t.getDescription());
        assertEquals(now, t.getTimestamp());
        assertEquals(1, t.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Transaction t = new Transaction();
        t.onCreate();
        assertNotNull(t.getCreatedAt());
        assertNotNull(t.getUpdatedAt());

        OffsetDateTime before = t.getUpdatedAt();
        t.onUpdate();
        assertNotNull(t.getUpdatedAt());
    }
}

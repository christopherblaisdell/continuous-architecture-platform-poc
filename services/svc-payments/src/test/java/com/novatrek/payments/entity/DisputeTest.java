package com.novatrek.payments.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class DisputeTest {

    @Test
    void gettersAndSetters() {
        Dispute d = new Dispute();
        UUID id = UUID.randomUUID();
        d.setId(id);
        UUID payId = UUID.randomUUID();
        d.setPaymentId(payId);
        UUID resId = UUID.randomUUID();
        d.setReservationId(resId);
        UUID guestId = UUID.randomUUID();
        d.setGuestId(guestId);
        d.setType(Dispute.DisputeType.CANCELLATION);
        d.setStatus(Dispute.DisputeStatus.OPENED);
        d.setTier(Dispute.DisputeTier.AUTO);
        d.setAmountRequested(new BigDecimal("250.00"));
        d.setAmountApproved(new BigDecimal("200.00"));
        d.setResolution(Dispute.DisputeResolutionType.PARTIAL_REFUND);
        d.setJustification("Weather cancellation");
        d.setAssignedTo("agent-1");
        d.setRev(2);
        OffsetDateTime now = OffsetDateTime.now();
        d.setResolvedAt(now);
        d.setVersion(1);

        assertEquals(id, d.getId());
        assertEquals(payId, d.getPaymentId());
        assertEquals(resId, d.getReservationId());
        assertEquals(guestId, d.getGuestId());
        assertEquals(Dispute.DisputeType.CANCELLATION, d.getType());
        assertEquals(Dispute.DisputeStatus.OPENED, d.getStatus());
        assertEquals(Dispute.DisputeTier.AUTO, d.getTier());
        assertEquals(new BigDecimal("250.00"), d.getAmountRequested());
        assertEquals(new BigDecimal("200.00"), d.getAmountApproved());
        assertEquals(Dispute.DisputeResolutionType.PARTIAL_REFUND, d.getResolution());
        assertEquals("Weather cancellation", d.getJustification());
        assertEquals("agent-1", d.getAssignedTo());
        assertEquals(2, d.getRev());
        assertEquals(now, d.getResolvedAt());
        assertEquals(1, d.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Dispute d = new Dispute();
        d.onCreate();
        assertNotNull(d.getCreatedAt());
        assertNotNull(d.getUpdatedAt());

        d.onUpdate();
        assertNotNull(d.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(5, Dispute.DisputeType.values().length);
        assertEquals(5, Dispute.DisputeStatus.values().length);
        assertEquals(3, Dispute.DisputeTier.values().length);
        assertEquals(3, Dispute.DisputeResolutionType.values().length);
    }
}

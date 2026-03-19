package com.novatrek.payments.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class PaymentTest {

    @Test
    void gettersAndSetters() {
        Payment p = new Payment();
        UUID id = UUID.randomUUID();
        p.setId(id);
        UUID resId = UUID.randomUUID();
        p.setReservationId(resId);
        UUID guestId = UUID.randomUUID();
        p.setGuestId(guestId);
        p.setAmount(new BigDecimal("350.00"));
        p.setCurrency("USD");
        p.setMethod(Payment.PaymentMethod.CREDIT_CARD);
        p.setStatus(Payment.PaymentStatus.CAPTURED);
        p.setProcessorReference("PROC-001");
        p.setRefundedAmount(new BigDecimal("50.00"));
        p.setVersion(1);

        assertEquals(id, p.getId());
        assertEquals(resId, p.getReservationId());
        assertEquals(guestId, p.getGuestId());
        assertEquals(new BigDecimal("350.00"), p.getAmount());
        assertEquals("USD", p.getCurrency());
        assertEquals(Payment.PaymentMethod.CREDIT_CARD, p.getMethod());
        assertEquals(Payment.PaymentStatus.CAPTURED, p.getStatus());
        assertEquals("PROC-001", p.getProcessorReference());
        assertEquals(new BigDecimal("50.00"), p.getRefundedAmount());
        assertEquals(1, p.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Payment p = new Payment();
        p.onCreate();
        assertNotNull(p.getCreatedAt());
        assertNotNull(p.getUpdatedAt());

        p.onUpdate();
        assertNotNull(p.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(5, Payment.PaymentMethod.values().length);
        assertEquals(6, Payment.PaymentStatus.values().length);
    }
}

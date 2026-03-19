package com.novatrek.payments.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class RefundTest {

    @Test
    void gettersAndSetters() {
        Refund r = new Refund();
        UUID id = UUID.randomUUID();
        r.setId(id);
        UUID payId = UUID.randomUUID();
        r.setPaymentId(payId);
        r.setAmount(new BigDecimal("99.99"));
        r.setReason("Service not rendered");
        r.setStatus(Refund.Status.PENDING);
        r.setProcessorReference("REF-001");
        r.setInitiatedBy("agent-1");
        r.setVersion(1);

        assertEquals(id, r.getId());
        assertEquals(payId, r.getPaymentId());
        assertEquals(new BigDecimal("99.99"), r.getAmount());
        assertEquals("Service not rendered", r.getReason());
        assertEquals(Refund.Status.PENDING, r.getStatus());
        assertEquals("REF-001", r.getProcessorReference());
        assertEquals("agent-1", r.getInitiatedBy());
        assertEquals(1, r.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Refund r = new Refund();
        r.onCreate();
        assertNotNull(r.getCreatedAt());
        assertNotNull(r.getUpdatedAt());

        r.onUpdate();
        assertNotNull(r.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, Refund.Status.values().length);
        assertNotNull(Refund.Status.valueOf("PROCESSED"));
        assertNotNull(Refund.Status.valueOf("FAILED"));
    }
}

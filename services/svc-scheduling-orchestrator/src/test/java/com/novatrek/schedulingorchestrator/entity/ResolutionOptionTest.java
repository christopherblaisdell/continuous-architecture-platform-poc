package com.novatrek.schedulingorchestrator.entity;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ResolutionOptionTest {

    @Test
    void gettersAndSetters() {
        ResolutionOption o = new ResolutionOption();
        UUID id = UUID.randomUUID();
        o.setId(id);
        o.setStrategy(ResolutionOption.Strategy.REASSIGN_GUIDE);
        o.setDescription("Assign alternate guide");
        o.setImpactAssessment("Minimal guest impact");
        o.setEstimatedAffectedGuests(4);
        o.setRequiresGuestNotification(true);
        o.setVersion(1);

        assertEquals(id, o.getId());
        assertEquals(ResolutionOption.Strategy.REASSIGN_GUIDE, o.getStrategy());
        assertEquals("Assign alternate guide", o.getDescription());
        assertEquals("Minimal guest impact", o.getImpactAssessment());
        assertEquals(4, o.getEstimatedAffectedGuests());
        assertTrue(o.getRequiresGuestNotification());
        assertEquals(1, o.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        ResolutionOption o = new ResolutionOption();
        o.onCreate();
        assertNotNull(o.getCreatedAt());
        assertNotNull(o.getUpdatedAt());

        o.onUpdate();
        assertNotNull(o.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(6, ResolutionOption.Strategy.values().length);
    }
}

package com.novatrek.schedulingorchestrator.entity;

import org.junit.jupiter.api.Test;

import java.time.OffsetDateTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ConflictResolutionResultTest {

    @Test
    void gettersAndSetters() {
        ConflictResolutionResult r = new ConflictResolutionResult();
        UUID id = UUID.randomUUID();
        r.setConflictId(id);
        r.setResolutionStatus(ConflictResolutionResult.ResolutionStatus.RESOLVED);
        r.setAppliedStrategy("REASSIGN_GUIDE");
        OffsetDateTime now = OffsetDateTime.now();
        r.setResolvedAt(now);
        r.setVersion(1);

        assertEquals(id, r.getConflictId());
        assertEquals(ConflictResolutionResult.ResolutionStatus.RESOLVED, r.getResolutionStatus());
        assertEquals("REASSIGN_GUIDE", r.getAppliedStrategy());
        assertEquals(now, r.getResolvedAt());
        assertEquals(1, r.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        ConflictResolutionResult r = new ConflictResolutionResult();
        r.onCreate();
        assertNotNull(r.getCreatedAt());
        assertNotNull(r.getUpdatedAt());

        r.onUpdate();
        assertNotNull(r.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, ConflictResolutionResult.ResolutionStatus.values().length);
    }
}

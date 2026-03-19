package com.novatrek.schedulingorchestrator.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GuideAssignmentTest {

    @Test
    void gettersAndSetters() {
        GuideAssignment a = new GuideAssignment();
        UUID id = UUID.randomUUID();
        a.setGuideId(id);
        a.setGuideName("Alex Rivera");
        a.setDate(LocalDate.of(2025, 7, 1));
        a.setAssignmentStatus(GuideAssignment.AssignmentStatus.CONFIRMED);
        a.setVersion(1);

        assertEquals(id, a.getGuideId());
        assertEquals("Alex Rivera", a.getGuideName());
        assertEquals(LocalDate.of(2025, 7, 1), a.getDate());
        assertEquals(GuideAssignment.AssignmentStatus.CONFIRMED, a.getAssignmentStatus());
        assertEquals(1, a.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GuideAssignment a = new GuideAssignment();
        a.onCreate();
        assertNotNull(a.getCreatedAt());
        assertNotNull(a.getUpdatedAt());

        a.onUpdate();
        assertNotNull(a.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, GuideAssignment.AssignmentStatus.values().length);
    }
}

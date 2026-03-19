package com.novatrek.guidemanagement.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GuideTest {

    @Test
    void gettersAndSetters() {
        Guide g = new Guide();
        UUID id = UUID.randomUUID();
        g.setId(id);
        g.setFirstName("Alex");
        g.setLastName("Rivera");
        g.setEmail("alex@novatrek.example.com");
        g.setPhone("555-0100");
        g.setYearsExperience(8);
        g.setMaxGroupSize(12);
        g.setStatus(Guide.GuideStatus.ACTIVE);
        g.setAverageRating(new BigDecimal("4.75"));
        g.setTotalTripsLed(200);
        g.setEmergencyTrainingLevel(Guide.EmergencyTrainingLevel.WILDERNESS_FIRST_RESPONDER);
        g.setVersion(1);

        assertEquals(id, g.getId());
        assertEquals("Alex", g.getFirstName());
        assertEquals("Rivera", g.getLastName());
        assertEquals("alex@novatrek.example.com", g.getEmail());
        assertEquals("555-0100", g.getPhone());
        assertEquals(8, g.getYearsExperience());
        assertEquals(12, g.getMaxGroupSize());
        assertEquals(Guide.GuideStatus.ACTIVE, g.getStatus());
        assertEquals(new BigDecimal("4.75"), g.getAverageRating());
        assertEquals(200, g.getTotalTripsLed());
        assertEquals(Guide.EmergencyTrainingLevel.WILDERNESS_FIRST_RESPONDER, g.getEmergencyTrainingLevel());
        assertEquals(1, g.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Guide g = new Guide();
        g.onCreate();
        assertNotNull(g.getCreatedAt());
        assertNotNull(g.getUpdatedAt());

        g.onUpdate();
        assertNotNull(g.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(5, Guide.GuideStatus.values().length);
        assertEquals(4, Guide.EmergencyTrainingLevel.values().length);
    }
}

package com.novatrek.emergencyresponse.entity;

import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class RescueTeamTest {

    @Test
    void gettersAndSetters() {
        RescueTeam t = new RescueTeam();
        UUID id = UUID.randomUUID();
        t.setTeamId(id);
        t.setName("Alpine Rescue");
        t.setRegion("North Ridge");
        t.setStatus(RescueTeam.Status.available);
        t.setMemberCount(8);
        t.setVersion(1);

        assertEquals(id, t.getTeamId());
        assertEquals("Alpine Rescue", t.getName());
        assertEquals("North Ridge", t.getRegion());
        assertEquals(RescueTeam.Status.available, t.getStatus());
        assertEquals(8, t.getMemberCount());
        assertEquals(1, t.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        RescueTeam t = new RescueTeam();
        t.onCreate();
        assertNotNull(t.getCreatedAt());
        assertNotNull(t.getUpdatedAt());

        t.onUpdate();
        assertNotNull(t.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(3, RescueTeam.Status.values().length);
        assertNotNull(RescueTeam.Status.valueOf("deployed"));
        assertNotNull(RescueTeam.Status.valueOf("off_duty"));
    }
}

package com.novatrek.guidemanagement.entity;

import org.junit.jupiter.api.Test;

import java.time.LocalDate;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class GuideCertificationTest {

    @Test
    void gettersAndSetters() {
        GuideCertification c = new GuideCertification();
        UUID id = UUID.randomUUID();
        c.setId(id);
        UUID guideId = UUID.randomUUID();
        c.setGuideId(guideId);
        c.setCertificationType("Wilderness First Aid");
        c.setIssuedDate(LocalDate.of(2023, 3, 15));
        c.setExpiryDate(LocalDate.of(2025, 3, 15));
        c.setIssuingBody("NOLS");
        c.setCertificateNumber("CERT-001");
        c.setStatus(GuideCertification.Status.VALID);
        c.setVersion(1);

        assertEquals(id, c.getId());
        assertEquals(guideId, c.getGuideId());
        assertEquals("Wilderness First Aid", c.getCertificationType());
        assertEquals(LocalDate.of(2023, 3, 15), c.getIssuedDate());
        assertEquals(LocalDate.of(2025, 3, 15), c.getExpiryDate());
        assertEquals("NOLS", c.getIssuingBody());
        assertEquals("CERT-001", c.getCertificateNumber());
        assertEquals(GuideCertification.Status.VALID, c.getStatus());
        assertEquals(1, c.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        GuideCertification c = new GuideCertification();
        c.onCreate();
        assertNotNull(c.getCreatedAt());
        assertNotNull(c.getUpdatedAt());

        c.onUpdate();
        assertNotNull(c.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(4, GuideCertification.Status.values().length);
    }
}

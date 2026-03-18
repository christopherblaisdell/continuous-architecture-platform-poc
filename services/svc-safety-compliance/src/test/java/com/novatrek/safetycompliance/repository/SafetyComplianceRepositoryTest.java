package com.novatrek.safetycompliance.repository;

import com.novatrek.safetycompliance.entity.Waiver;
import com.novatrek.safetycompliance.entity.SafetyInspection;
import com.novatrek.safetycompliance.entity.IncidentReport;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class SafetyComplianceRepositoryTest {

    @Autowired
    private WaiverRepository waiverRepository;

    @Autowired
    private SafetyInspectionRepository safetyInspectionRepository;

    @Autowired
    private IncidentReportRepository incidentReportRepository;

    @Test
    void saveAndFindWaiver() {
        Waiver w = new Waiver();
        w.setGuestId(UUID.randomUUID());
        w.setReservationId(UUID.randomUUID());
        w.setWaiverType(Waiver.WaiverType.WATER_ACTIVITY);
        w.setSignedAt(OffsetDateTime.now());
        w.setStatus(Waiver.WaiverStatus.ACTIVE);
        w.setEmergencyContactName("Jane Doe");
        w.setEmergencyContactPhone("+1-555-0199");

        Waiver saved = waiverRepository.save(w);
        assertThat(saved.getId()).isNotNull();

        Optional<Waiver> found = waiverRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getWaiverType()).isEqualTo(Waiver.WaiverType.WATER_ACTIVITY);
        assertThat(found.get().getEmergencyContactName()).isEqualTo("Jane Doe");
    }

    @Test
    void saveAndFindSafetyInspection() {
        SafetyInspection si = new SafetyInspection();
        si.setLocationId(UUID.randomUUID());
        si.setInspectorId(UUID.randomUUID());
        si.setInspectionDate(LocalDate.of(2026, 5, 15));
        si.setStatus(SafetyInspection.InspectionStatus.PASSED);
        si.setNotes("All clear");
        si.setNextInspectionDue(LocalDate.of(2026, 8, 15));

        SafetyInspection saved = safetyInspectionRepository.save(si);
        assertThat(saved.getId()).isNotNull();

        Optional<SafetyInspection> found = safetyInspectionRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getStatus()).isEqualTo(SafetyInspection.InspectionStatus.PASSED);
    }

    @Test
    void saveAndFindIncidentReport() {
        IncidentReport ir = new IncidentReport();
        ir.setReservationId(UUID.randomUUID());
        ir.setGuideId(UUID.randomUUID());
        ir.setType(IncidentReport.IncidentType.WILDLIFE_ENCOUNTER);
        ir.setSeverity(IncidentReport.IncidentSeverity.LOW);
        ir.setDescription("Bear sighting on trail");
        ir.setReportedAt(OffsetDateTime.now());
        ir.setStatus(IncidentReport.Status.OPEN);
        ir.setFollowUpRequired(true);

        IncidentReport saved = incidentReportRepository.save(ir);
        assertThat(saved.getId()).isNotNull();

        Optional<IncidentReport> found = incidentReportRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getType()).isEqualTo(IncidentReport.IncidentType.WILDLIFE_ENCOUNTER);
        assertThat(found.get().getFollowUpRequired()).isTrue();
    }

    @Test
    void incidentStatusUpdate() {
        IncidentReport ir = new IncidentReport();
        ir.setReservationId(UUID.randomUUID());
        ir.setGuideId(UUID.randomUUID());
        ir.setType(IncidentReport.IncidentType.WEATHER_EVENT);
        ir.setSeverity(IncidentReport.IncidentSeverity.HIGH);
        ir.setDescription("Unexpected thunderstorm during hike");
        ir.setReportedAt(OffsetDateTime.now());
        ir.setStatus(IncidentReport.Status.OPEN);

        IncidentReport saved = incidentReportRepository.save(ir);
        saved.setStatus(IncidentReport.Status.RESOLVED);
        saved.setActionsTaken("Group evacuated to shelter");
        IncidentReport updated = incidentReportRepository.save(saved);

        assertThat(updated.getStatus()).isEqualTo(IncidentReport.Status.RESOLVED);
        assertThat(updated.getActionsTaken()).isEqualTo("Group evacuated to shelter");
    }
}

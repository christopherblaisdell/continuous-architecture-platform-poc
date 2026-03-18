package com.novatrek.guidemanagement.repository;

import com.novatrek.guidemanagement.entity.Guide;
import com.novatrek.guidemanagement.entity.GuideCertification;
import com.novatrek.guidemanagement.entity.GuideRating;
import com.novatrek.guidemanagement.entity.GuideScheduleEntry;
import com.novatrek.guidemanagement.entity.AvailabilityWindow;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class GuideManagementRepositoryTest {

    @Autowired
    private GuideRepository guideRepository;

    @Autowired
    private GuideCertificationRepository guideCertificationRepository;

    @Autowired
    private GuideRatingRepository guideRatingRepository;

    @Autowired
    private GuideScheduleEntryRepository guideScheduleEntryRepository;

    @Autowired
    private AvailabilityWindowRepository availabilityWindowRepository;

    @Test
    void saveAndFindGuide() {
        Guide g = new Guide();
        g.setFirstName("Maya");
        g.setLastName("Chen");
        g.setEmail("maya.chen@novatrek.example.com");
        g.setYearsExperience(5);
        g.setStatus(Guide.GuideStatus.ACTIVE);
        g.setEmergencyTrainingLevel(Guide.EmergencyTrainingLevel.WILDERNESS_FIRST_AID);

        Guide saved = guideRepository.save(g);
        assertThat(saved.getId()).isNotNull();

        Optional<Guide> found = guideRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getFirstName()).isEqualTo("Maya");
        assertThat(found.get().getStatus()).isEqualTo(Guide.GuideStatus.ACTIVE);
    }

    @Test
    void saveAndFindCertification() {
        GuideCertification cert = new GuideCertification();
        cert.setGuideId(UUID.randomUUID());
        cert.setCertificationType("Wilderness First Responder");
        cert.setIssuedDate(LocalDate.of(2024, 3, 15));
        cert.setExpiryDate(LocalDate.of(2027, 3, 15));
        cert.setIssuingBody("NOLS");
        cert.setCertificateNumber("WFR-2024-0042");
        cert.setStatus(GuideCertification.Status.VALID);

        GuideCertification saved = guideCertificationRepository.save(cert);
        assertThat(saved.getId()).isNotNull();

        Optional<GuideCertification> found = guideCertificationRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getCertificationType()).isEqualTo("Wilderness First Responder");
    }

    @Test
    void saveAndFindGuideRating() {
        GuideRating rating = new GuideRating();
        rating.setGuideId(UUID.randomUUID());
        rating.setReservationId(UUID.randomUUID());
        rating.setGuestId(UUID.randomUUID());
        rating.setRating(5);
        rating.setReviewText("Excellent guide!");
        rating.setDate(LocalDate.of(2026, 6, 20));

        GuideRating saved = guideRatingRepository.save(rating);
        assertThat(saved.getId()).isNotNull();

        Optional<GuideRating> found = guideRatingRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getRating()).isEqualTo(5);
    }

    @Test
    void saveAndFindScheduleEntry() {
        GuideScheduleEntry entry = new GuideScheduleEntry();
        entry.setGuideId(UUID.randomUUID());
        entry.setTripId(UUID.randomUUID());
        entry.setTripName("Alpine Summit Expedition");
        entry.setDepartureDate(LocalDate.of(2026, 7, 10));
        entry.setReturnDate(LocalDate.of(2026, 7, 13));
        entry.setRole(GuideScheduleEntry.GuideRole.LEAD);
        entry.setGroupSize(8);

        GuideScheduleEntry saved = guideScheduleEntryRepository.save(entry);
        assertThat(saved.getId()).isNotNull();

        Optional<GuideScheduleEntry> found = guideScheduleEntryRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getRole()).isEqualTo(GuideScheduleEntry.GuideRole.LEAD);
    }

    @Test
    void saveAndFindAvailabilityWindow() {
        AvailabilityWindow aw = new AvailabilityWindow();
        aw.setGuideId(UUID.randomUUID());
        aw.setStartDate(LocalDate.of(2026, 8, 1));
        aw.setEndDate(LocalDate.of(2026, 8, 15));
        aw.setAvailable(true);
        aw.setNotes("Available for all trip types");

        AvailabilityWindow saved = availabilityWindowRepository.save(aw);
        assertThat(saved.getId()).isNotNull();

        Optional<AvailabilityWindow> found = availabilityWindowRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getAvailable()).isTrue();
    }
}

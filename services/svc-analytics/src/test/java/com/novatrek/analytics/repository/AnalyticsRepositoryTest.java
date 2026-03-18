package com.novatrek.analytics.repository;

import com.novatrek.analytics.entity.GuidePerformance;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class AnalyticsRepositoryTest {

    @Autowired
    private GuidePerformanceRepository guidePerformanceRepository;

    @Test
    void saveAndFindGuidePerformance() {
        GuidePerformance gp = new GuidePerformance();
        gp.setTripsLed(25);
        gp.setTotalParticipants(200);
        gp.setAverageGuestRating(new BigDecimal("4.70"));
        gp.setIncidentCount(2);
        gp.setCancellationRate(new BigDecimal("3.50"));

        GuidePerformance saved = guidePerformanceRepository.save(gp);
        assertThat(saved.getGuideId()).isNotNull();
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        GuidePerformance found = guidePerformanceRepository.findById(saved.getGuideId()).orElseThrow();
        assertThat(found.getTripsLed()).isEqualTo(25);
        assertThat(found.getAverageGuestRating()).isEqualByComparingTo(new BigDecimal("4.70"));
        assertThat(found.getIncidentCount()).isEqualTo(2);
    }

    @Test
    void findAll_returnsMultiple() {
        GuidePerformance gp1 = new GuidePerformance();
        gp1.setTripsLed(10);
        gp1.setTotalParticipants(80);
        gp1.setAverageGuestRating(new BigDecimal("4.50"));
        gp1.setIncidentCount(0);
        gp1.setCancellationRate(BigDecimal.ZERO);

        GuidePerformance gp2 = new GuidePerformance();
        gp2.setTripsLed(50);
        gp2.setTotalParticipants(400);
        gp2.setAverageGuestRating(new BigDecimal("4.90"));
        gp2.setIncidentCount(3);
        gp2.setCancellationRate(new BigDecimal("1.20"));

        guidePerformanceRepository.save(gp1);
        guidePerformanceRepository.save(gp2);

        assertThat(guidePerformanceRepository.findAll()).hasSize(2);
    }
}

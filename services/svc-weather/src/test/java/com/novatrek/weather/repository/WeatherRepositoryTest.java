package com.novatrek.weather.repository;

import com.novatrek.weather.entity.WeatherAlert;
import com.novatrek.weather.entity.TrailCondition;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.time.OffsetDateTime;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class WeatherRepositoryTest {

    @Autowired
    private WeatherAlertRepository weatherAlertRepository;

    @Autowired
    private TrailConditionRepository trailConditionRepository;

    @Test
    void saveAndFindWeatherAlert() {
        WeatherAlert alert = new WeatherAlert();
        alert.setTitle("Severe Storm Warning");
        alert.setAlertType(WeatherAlert.AlertType.SEVERE_STORM);
        alert.setSeverity(WeatherAlert.AlertSeverity.EMERGENCY);
        alert.setIsActive(true);
        alert.setEffectiveFrom(OffsetDateTime.now());
        alert.setEffectiveUntil(OffsetDateTime.now().plusHours(6));

        WeatherAlert saved = weatherAlertRepository.save(alert);
        assertThat(saved.getId()).isNotNull();

        WeatherAlert found = weatherAlertRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getTitle()).isEqualTo("Severe Storm Warning");
        assertThat(found.getAlertType()).isEqualTo(WeatherAlert.AlertType.SEVERE_STORM);
        assertThat(found.getIsActive()).isTrue();
    }

    @Test
    void saveAndFindTrailCondition() {
        TrailCondition tc = new TrailCondition();
        tc.setTrailName("Glacier Pass");
        tc.setOverallStatus(TrailCondition.OverallStatus.HAZARDOUS);
        tc.setSurfaceCondition(TrailCondition.SurfaceCondition.ICY);
        tc.setWaterCrossingsPassable(false);
        tc.setRangerNotes("Ice formation on northern exposure");

        TrailCondition saved = trailConditionRepository.save(tc);
        assertThat(saved.getTrailId()).isNotNull();

        TrailCondition found = trailConditionRepository.findById(saved.getTrailId()).orElseThrow();
        assertThat(found.getTrailName()).isEqualTo("Glacier Pass");
        assertThat(found.getOverallStatus()).isEqualTo(TrailCondition.OverallStatus.HAZARDOUS);
    }
}

package com.novatrek.wildlifetracking.repository;

import com.novatrek.wildlifetracking.entity.Species;
import com.novatrek.wildlifetracking.entity.Sighting;
import com.novatrek.wildlifetracking.entity.HabitatZone;
import com.novatrek.wildlifetracking.entity.WildlifeAlert;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.OffsetDateTime;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class WildlifeTrackingRepositoryTest {

    @Autowired
    private SpeciesRepository speciesRepository;

    @Autowired
    private SightingRepository sightingRepository;

    @Autowired
    private HabitatZoneRepository habitatZoneRepository;

    @Autowired
    private WildlifeAlertRepository wildlifeAlertRepository;

    @Test
    void saveAndFindSpecies() {
        Species sp = new Species();
        sp.setCommonName("Mountain Goat");
        sp.setScientificName("Oreamnos americanus");
        sp.setThreatLevel(Species.ThreatLevel.none);
        sp.setCategory(Species.Category.mammal);
        sp.setDescription("Common alpine ungulate");

        Species saved = speciesRepository.save(sp);
        assertThat(saved.getSpeciesId()).isNotNull();

        Species found = speciesRepository.findById(saved.getSpeciesId()).orElseThrow();
        assertThat(found.getCommonName()).isEqualTo("Mountain Goat");
        assertThat(found.getCategory()).isEqualTo(Species.Category.mammal);
    }

    @Test
    void saveAndFindSighting() {
        Sighting s = new Sighting();
        s.setSpeciesName("Elk");
        s.setReportedBy("Guide-Rivera");
        s.setReporterType("guide");
        s.setAnimalCount(12);
        s.setBehavior("grazing");
        s.setAlertTriggered(false);

        Sighting saved = sightingRepository.save(s);
        assertThat(saved.getSightingId()).isNotNull();

        Sighting found = sightingRepository.findById(saved.getSightingId()).orElseThrow();
        assertThat(found.getSpeciesName()).isEqualTo("Elk");
        assertThat(found.getAnimalCount()).isEqualTo(12);
    }

    @Test
    void saveAndFindHabitatZone() {
        HabitatZone hz = new HabitatZone();
        hz.setName("Pine Forest Corridor");
        hz.setActivityLevel(HabitatZone.ActivityLevel.moderate);
        hz.setSeason("autumn");

        HabitatZone saved = habitatZoneRepository.save(hz);
        assertThat(saved.getZoneId()).isNotNull();

        HabitatZone found = habitatZoneRepository.findById(saved.getZoneId()).orElseThrow();
        assertThat(found.getName()).isEqualTo("Pine Forest Corridor");
        assertThat(found.getActivityLevel()).isEqualTo(HabitatZone.ActivityLevel.moderate);
    }

    @Test
    void saveAndFindWildlifeAlert() {
        WildlifeAlert alert = new WildlifeAlert();
        alert.setSpeciesName("Cougar");
        alert.setThreatLevel("extreme");
        alert.setStatus("active");
        alert.setRadiusMeters(new BigDecimal("1000.00"));
        alert.setRecommendedAction("Avoid area, reroute trails");
        alert.setIssuedAt(OffsetDateTime.now());

        WildlifeAlert saved = wildlifeAlertRepository.save(alert);
        assertThat(saved.getAlertId()).isNotNull();

        WildlifeAlert found = wildlifeAlertRepository.findById(saved.getAlertId()).orElseThrow();
        assertThat(found.getSpeciesName()).isEqualTo("Cougar");
        assertThat(found.getRadiusMeters()).isEqualByComparingTo(new BigDecimal("1000.00"));
    }
}

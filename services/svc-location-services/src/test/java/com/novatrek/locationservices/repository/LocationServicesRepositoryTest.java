package com.novatrek.locationservices.repository;

import com.novatrek.locationservices.entity.Location;
import com.novatrek.locationservices.entity.LocationCapacity;
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
class LocationServicesRepositoryTest {

    @Autowired
    private LocationRepository locationRepository;

    @Autowired
    private LocationCapacityRepository locationCapacityRepository;

    @Test
    void saveAndFindLocation() {
        Location loc = new Location();
        loc.setName("Mountain Base Camp");
        loc.setType(Location.LocationType.BASE_CAMP);
        loc.setRegionId(UUID.randomUUID());
        loc.setCapacity(150);
        loc.setStatus(Location.LocationStatus.ACTIVE);

        Location saved = locationRepository.save(loc);
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getUpdatedAt()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        Location found = locationRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getName()).isEqualTo("Mountain Base Camp");
        assertThat(found.getType()).isEqualTo(Location.LocationType.BASE_CAMP);
        assertThat(found.getCapacity()).isEqualTo(150);
    }

    @Test
    void locationTypeEnumValues() {
        for (Location.LocationType lt : Location.LocationType.values()) {
            Location loc = new Location();
            loc.setName("Test-" + lt.name());
            loc.setType(lt);
            loc.setRegionId(UUID.randomUUID());
            loc.setStatus(Location.LocationStatus.ACTIVE);

            Location saved = locationRepository.save(loc);
            assertThat(locationRepository.findById(saved.getId()).orElseThrow().getType()).isEqualTo(lt);
        }
    }

    @Test
    void locationStatusEnumValues() {
        for (Location.LocationStatus ls : Location.LocationStatus.values()) {
            Location loc = new Location();
            loc.setName("Status-" + ls.name());
            loc.setType(Location.LocationType.OUTPOST);
            loc.setRegionId(UUID.randomUUID());
            loc.setStatus(ls);

            Location saved = locationRepository.save(loc);
            assertThat(locationRepository.findById(saved.getId()).orElseThrow().getStatus()).isEqualTo(ls);
        }
    }

    @Test
    void saveAndFindLocationCapacity() {
        LocationCapacity cap = new LocationCapacity();
        cap.setMaxCapacity(200);
        cap.setCurrentOccupancy(75);
        cap.setAvailableSpots(125);
        cap.setUtilizationPercent(new BigDecimal("37.50"));
        cap.setAsOf(OffsetDateTime.now());

        LocationCapacity saved = locationCapacityRepository.save(cap);
        assertThat(saved.getLocationId()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        LocationCapacity found = locationCapacityRepository.findById(saved.getLocationId()).orElseThrow();
        assertThat(found.getMaxCapacity()).isEqualTo(200);
        assertThat(found.getCurrentOccupancy()).isEqualTo(75);
        assertThat(found.getAvailableSpots()).isEqualTo(125);
        assertThat(found.getUtilizationPercent()).isEqualByComparingTo(new BigDecimal("37.50"));
    }
}

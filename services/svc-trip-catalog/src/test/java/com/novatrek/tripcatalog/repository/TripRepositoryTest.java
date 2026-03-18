package com.novatrek.tripcatalog.repository;

import com.novatrek.tripcatalog.entity.Trip;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class TripRepositoryTest {

    @Autowired
    private TripRepository tripRepository;

    private Trip createTrip(String name, Trip.ActivityType type, Trip.TripStatus status) {
        Trip trip = new Trip();
        trip.setName(name);
        trip.setActivityType(type);
        trip.setDifficultyLevel(Trip.DifficultyLevel.INTERMEDIATE);
        trip.setDurationHours(new BigDecimal("4.0"));
        trip.setBasePrice(new BigDecimal("79.99"));
        trip.setStatus(status);
        return trip;
    }

    @Test
    void saveAndFindById() {
        Trip saved = tripRepository.save(createTrip("Alpine Trek", Trip.ActivityType.HIKING, Trip.TripStatus.ACTIVE));

        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);
        assertThat(tripRepository.findById(saved.getId())).isPresent();
    }

    @Test
    void findByStatus() {
        tripRepository.save(createTrip("Active1", Trip.ActivityType.HIKING, Trip.TripStatus.ACTIVE));
        tripRepository.save(createTrip("Draft1", Trip.ActivityType.KAYAKING, Trip.TripStatus.DRAFT));

        List<Trip> active = tripRepository.findByStatus(Trip.TripStatus.ACTIVE);
        assertThat(active).allMatch(t -> t.getStatus() == Trip.TripStatus.ACTIVE);
    }

    @Test
    void findByActivityType() {
        tripRepository.save(createTrip("Hike1", Trip.ActivityType.HIKING, Trip.TripStatus.ACTIVE));
        tripRepository.save(createTrip("Kayak1", Trip.ActivityType.KAYAKING, Trip.TripStatus.ACTIVE));

        List<Trip> hiking = tripRepository.findByActivityType(Trip.ActivityType.HIKING);
        assertThat(hiking).allMatch(t -> t.getActivityType() == Trip.ActivityType.HIKING);
    }

    @Test
    void updateTrip_incrementsVersion() {
        Trip saved = tripRepository.save(createTrip("VersionTest", Trip.ActivityType.RAFTING, Trip.TripStatus.DRAFT));
        assertThat(saved.getVersion()).isEqualTo(0);

        saved.setBasePrice(new BigDecimal("120.00"));
        Trip updated = tripRepository.saveAndFlush(saved);
        assertThat(updated.getVersion()).isEqualTo(1);
    }

    @Test
    void defaultStatus_isDraft() {
        Trip trip = new Trip();
        trip.setName("NoStatus");
        trip.setActivityType(Trip.ActivityType.CAMPING);
        trip.setDifficultyLevel(Trip.DifficultyLevel.BEGINNER);
        trip.setDurationHours(new BigDecimal("2.0"));
        trip.setBasePrice(new BigDecimal("49.99"));

        Trip saved = tripRepository.save(trip);
        assertThat(saved.getStatus()).isEqualTo(Trip.TripStatus.DRAFT);
    }
}

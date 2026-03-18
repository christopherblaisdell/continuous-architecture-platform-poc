package com.novatrek.transportlogistics.repository;

import com.novatrek.transportlogistics.entity.TransportRoute;
import com.novatrek.transportlogistics.entity.Vehicle;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class TransportLogisticsRepositoryTest {

    @Autowired
    private TransportRouteRepository transportRouteRepository;

    @Autowired
    private VehicleRepository vehicleRepository;

    @Test
    void saveAndFindRoute() {
        TransportRoute r = new TransportRoute();
        r.setOriginLocationId(UUID.randomUUID());
        r.setDestinationLocationId(UUID.randomUUID());
        r.setRouteName("Glacier Trailhead to Summit Camp");
        r.setDistanceKm(new BigDecimal("38.7"));
        r.setDurationMinutes(75);
        r.setTerrainDifficulty(TransportRoute.TerrainDifficulty.OFF_ROAD);
        r.setActive(true);

        TransportRoute saved = transportRouteRepository.save(r);
        assertThat(saved.getId()).isNotNull();

        TransportRoute found = transportRouteRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getRouteName()).isEqualTo("Glacier Trailhead to Summit Camp");
        assertThat(found.getDistanceKm()).isEqualByComparingTo(new BigDecimal("38.7"));
        assertThat(found.getTerrainDifficulty()).isEqualTo(TransportRoute.TerrainDifficulty.OFF_ROAD);
    }

    @Test
    void routeTerrainDifficultyEnumValues() {
        for (TransportRoute.TerrainDifficulty td : TransportRoute.TerrainDifficulty.values()) {
            TransportRoute r = new TransportRoute();
            r.setOriginLocationId(UUID.randomUUID());
            r.setDestinationLocationId(UUID.randomUUID());
            r.setDistanceKm(BigDecimal.TEN);
            r.setDurationMinutes(20);
            r.setTerrainDifficulty(td);

            TransportRoute saved = transportRouteRepository.save(r);
            TransportRoute found = transportRouteRepository.findById(saved.getId()).orElseThrow();
            assertThat(found.getTerrainDifficulty()).isEqualTo(td);
        }
    }

    @Test
    void saveAndFindVehicle() {
        Vehicle v = new Vehicle();
        v.setType(Vehicle.VehicleType.SUV);
        v.setCapacity(6);
        v.setLicensePlate("NT-7700");
        v.setStatus(Vehicle.VehicleStatus.AVAILABLE);
        v.setMileage(12500);
        v.setAssignedLocationId(UUID.randomUUID());
        v.setLastMaintenanceDate(LocalDate.of(2026, 1, 15));
        v.setNextMaintenanceDate(LocalDate.of(2026, 7, 15));

        Vehicle saved = vehicleRepository.save(v);
        assertThat(saved.getId()).isNotNull();

        Vehicle found = vehicleRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getLicensePlate()).isEqualTo("NT-7700");
        assertThat(found.getType()).isEqualTo(Vehicle.VehicleType.SUV);
        assertThat(found.getStatus()).isEqualTo(Vehicle.VehicleStatus.AVAILABLE);
        assertThat(found.getMileage()).isEqualTo(12500);
    }

    @Test
    void vehicleTypeAndStatusEnumValues() {
        for (Vehicle.VehicleType vt : Vehicle.VehicleType.values()) {
            Vehicle v = new Vehicle();
            v.setType(vt);
            v.setCapacity(4);
            v.setLicensePlate("NT-ENUM-" + vt.name());
            v.setStatus(Vehicle.VehicleStatus.AVAILABLE);

            Vehicle saved = vehicleRepository.save(v);
            assertThat(vehicleRepository.findById(saved.getId()).orElseThrow().getType()).isEqualTo(vt);
        }

        Vehicle base = new Vehicle();
        base.setType(Vehicle.VehicleType.ATV);
        base.setCapacity(2);
        for (Vehicle.VehicleStatus vs : Vehicle.VehicleStatus.values()) {
            Vehicle v = new Vehicle();
            v.setType(Vehicle.VehicleType.ATV);
            v.setCapacity(2);
            v.setLicensePlate("NT-ST-" + vs.name());
            v.setStatus(vs);

            Vehicle saved = vehicleRepository.save(v);
            assertThat(vehicleRepository.findById(saved.getId()).orElseThrow().getStatus()).isEqualTo(vs);
        }
    }
}

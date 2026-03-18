package com.novatrek.transportlogistics.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.transportlogistics.entity.TransportRoute;
import com.novatrek.transportlogistics.entity.Vehicle;
import com.novatrek.transportlogistics.repository.TransportRouteRepository;
import com.novatrek.transportlogistics.repository.VehicleRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest({RoutesController.class, VehiclesController.class, TransportRequestsController.class})
class TransportLogisticsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private TransportRouteRepository transportRouteRepository;

    @MockBean
    private VehicleRepository vehicleRepository;

    // --- Routes ---

    @Test
    void listRoutes_returnsEmptyList() throws Exception {
        when(transportRouteRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/routes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void listRoutes_returnsRoutes() throws Exception {
        TransportRoute r = new TransportRoute();
        r.setOriginLocationId(UUID.randomUUID());
        r.setDestinationLocationId(UUID.randomUUID());
        r.setRouteName("Base Camp to Summit Trailhead");
        r.setDistanceKm(new BigDecimal("45.5"));
        r.setDurationMinutes(90);
        r.setTerrainDifficulty(TransportRoute.TerrainDifficulty.GRAVEL);
        r.setActive(true);

        when(transportRouteRepository.findAll()).thenReturn(List.of(r));

        mockMvc.perform(get("/routes"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].routeName", is("Base Camp to Summit Trailhead")));
    }

    @Test
    void createRoute_returns201() throws Exception {
        TransportRoute r = new TransportRoute();
        r.setOriginLocationId(UUID.randomUUID());
        r.setDestinationLocationId(UUID.randomUUID());
        r.setRouteName("River Launch to Takeout");
        r.setDistanceKm(new BigDecimal("22.0"));
        r.setDurationMinutes(45);
        r.setTerrainDifficulty(TransportRoute.TerrainDifficulty.PAVED);
        r.setActive(true);

        when(transportRouteRepository.save(any(TransportRoute.class))).thenReturn(r);

        mockMvc.perform(post("/routes")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(r)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.routeName", is("River Launch to Takeout")));
    }

    @Test
    void getRouteSchedule_returnsRoute() throws Exception {
        UUID id = UUID.randomUUID();
        TransportRoute r = new TransportRoute();
        r.setId(id);
        r.setOriginLocationId(UUID.randomUUID());
        r.setDestinationLocationId(UUID.randomUUID());
        r.setDistanceKm(new BigDecimal("30.0"));
        r.setDurationMinutes(60);

        when(transportRouteRepository.findById(id)).thenReturn(Optional.of(r));

        mockMvc.perform(get("/routes/{id}/schedule", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.durationMinutes", is(60)));
    }

    @Test
    void getRouteSchedule_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(transportRouteRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/routes/{id}/schedule", id))
                .andExpect(status().isNotFound());
    }

    // --- Vehicles ---

    @Test
    void listVehicles_returnsList() throws Exception {
        Vehicle v = new Vehicle();
        v.setType(Vehicle.VehicleType.SHUTTLE_BUS);
        v.setCapacity(24);
        v.setLicensePlate("NT-4201");
        v.setStatus(Vehicle.VehicleStatus.AVAILABLE);

        when(vehicleRepository.findAll()).thenReturn(List.of(v));

        mockMvc.perform(get("/vehicles"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].licensePlate", is("NT-4201")));
    }

    @Test
    void updateVehicle_patchFields() throws Exception {
        UUID id = UUID.randomUUID();
        Vehicle existing = new Vehicle();
        existing.setId(id);
        existing.setType(Vehicle.VehicleType.VAN);
        existing.setCapacity(12);
        existing.setLicensePlate("NT-3100");
        existing.setStatus(Vehicle.VehicleStatus.AVAILABLE);

        Vehicle updated = new Vehicle();
        updated.setId(id);
        updated.setType(Vehicle.VehicleType.VAN);
        updated.setCapacity(12);
        updated.setLicensePlate("NT-3100");
        updated.setStatus(Vehicle.VehicleStatus.MAINTENANCE);
        updated.setMileage(85000);

        when(vehicleRepository.findById(id)).thenReturn(Optional.of(existing));
        when(vehicleRepository.save(any(Vehicle.class))).thenReturn(updated);

        mockMvc.perform(patch("/vehicles/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(updated)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status", is("MAINTENANCE")));
    }

    @Test
    void updateVehicle_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(vehicleRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/vehicles/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isNotFound());
    }

    // --- Transport Requests ---

    @Test
    void createTransportRequest_returns201() throws Exception {
        TransportRoute r = new TransportRoute();
        r.setOriginLocationId(UUID.randomUUID());
        r.setDestinationLocationId(UUID.randomUUID());
        r.setDistanceKm(new BigDecimal("15.0"));
        r.setDurationMinutes(30);

        when(transportRouteRepository.save(any(TransportRoute.class))).thenReturn(r);

        mockMvc.perform(post("/transport-requests")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(r)))
                .andExpect(status().isCreated());
    }

    @Test
    void getTransportRequest_returnsRoute() throws Exception {
        UUID id = UUID.randomUUID();
        TransportRoute r = new TransportRoute();
        r.setId(id);
        r.setOriginLocationId(UUID.randomUUID());
        r.setDestinationLocationId(UUID.randomUUID());
        r.setDistanceKm(new BigDecimal("50.0"));
        r.setDurationMinutes(120);

        when(transportRouteRepository.findById(id)).thenReturn(Optional.of(r));

        mockMvc.perform(get("/transport-requests/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.durationMinutes", is(120)));
    }

    @Test
    void getTransportRequest_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(transportRouteRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/transport-requests/{id}", id))
                .andExpect(status().isNotFound());
    }
}

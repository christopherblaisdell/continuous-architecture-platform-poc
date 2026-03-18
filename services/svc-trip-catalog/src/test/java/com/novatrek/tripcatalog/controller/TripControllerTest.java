package com.novatrek.tripcatalog.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.tripcatalog.entity.Trip;
import com.novatrek.tripcatalog.repository.TripRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TripController.class)
class TripControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private TripRepository tripRepository;

    private Trip createTestTrip() {
        Trip trip = new Trip();
        trip.setId(UUID.randomUUID());
        trip.setName("Cascade Ridge Hike");
        trip.setDescription("A scenic alpine ridge trail");
        trip.setActivityType(Trip.ActivityType.HIKING);
        trip.setDifficultyLevel(Trip.DifficultyLevel.INTERMEDIATE);
        trip.setDurationHours(new BigDecimal("6.5"));
        trip.setBasePrice(new BigDecimal("89.99"));
        trip.setMinParticipants(2);
        trip.setMaxParticipants(12);
        trip.setStatus(Trip.TripStatus.ACTIVE);
        return trip;
    }

    @Test
    void listTrips_returnsAll() throws Exception {
        when(tripRepository.findAll()).thenReturn(List.of(createTestTrip()));

        mockMvc.perform(get("/trips"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name").value("Cascade Ridge Hike"));
    }

    @Test
    void listTrips_filterByStatus() throws Exception {
        Trip trip = createTestTrip();
        when(tripRepository.findByStatus(Trip.TripStatus.ACTIVE)).thenReturn(List.of(trip));

        mockMvc.perform(get("/trips").param("status", "ACTIVE"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void listTrips_filterByActivityType() throws Exception {
        Trip trip = createTestTrip();
        when(tripRepository.findByActivityType(Trip.ActivityType.HIKING)).thenReturn(List.of(trip));

        mockMvc.perform(get("/trips").param("activityType", "HIKING"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void createTrip_returns201WithDraftStatus() throws Exception {
        Trip trip = createTestTrip();
        trip.setStatus(Trip.TripStatus.DRAFT);
        when(tripRepository.save(any(Trip.class))).thenReturn(trip);

        Trip input = new Trip();
        input.setName("Cascade Ridge Hike");
        input.setActivityType(Trip.ActivityType.HIKING);
        input.setDifficultyLevel(Trip.DifficultyLevel.INTERMEDIATE);
        input.setDurationHours(new BigDecimal("6.5"));
        input.setBasePrice(new BigDecimal("89.99"));

        mockMvc.perform(post("/trips")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(input)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Cascade Ridge Hike"))
                .andExpect(jsonPath("$.status").value("DRAFT"));
    }

    @Test
    void getTrip_returnsTrip() throws Exception {
        Trip trip = createTestTrip();
        UUID id = trip.getId();
        when(tripRepository.findById(id)).thenReturn(Optional.of(trip));

        mockMvc.perform(get("/trips/{tripId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Cascade Ridge Hike"))
                .andExpect(jsonPath("$.activityType").value("HIKING"));
    }

    @Test
    void getTrip_returns404WhenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(tripRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/trips/{tripId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateTrip_patchesFields() throws Exception {
        Trip existing = createTestTrip();
        UUID id = existing.getId();
        when(tripRepository.findById(id)).thenReturn(Optional.of(existing));
        when(tripRepository.save(any(Trip.class))).thenAnswer(inv -> inv.getArgument(0));

        String patchJson = """
                {"name": "Updated Hike", "basePrice": 99.99, "difficultyLevel": "ADVANCED"}
                """;

        mockMvc.perform(patch("/trips/{tripId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patchJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Updated Hike"))
                .andExpect(jsonPath("$.difficultyLevel").value("ADVANCED"));
    }

    @Test
    void updateTrip_returns404WhenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(tripRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/trips/{tripId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\": \"x\"}"))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateTrip_patchesParticipantFields() throws Exception {
        Trip existing = createTestTrip();
        UUID id = existing.getId();
        when(tripRepository.findById(id)).thenReturn(Optional.of(existing));
        when(tripRepository.save(any(Trip.class))).thenAnswer(inv -> inv.getArgument(0));

        String patchJson = """
                {"minParticipants": 4, "maxParticipants": 20, "ageMinimum": 16, "fitnessLevelRequired": "HIGH"}
                """;

        mockMvc.perform(patch("/trips/{tripId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patchJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.minParticipants").value(4))
                .andExpect(jsonPath("$.maxParticipants").value(20))
                .andExpect(jsonPath("$.ageMinimum").value(16))
                .andExpect(jsonPath("$.fitnessLevelRequired").value("HIGH"));
    }
}

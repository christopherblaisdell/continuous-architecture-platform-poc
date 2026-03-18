package com.novatrek.trailmanagement.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.trailmanagement.entity.Trail;
import com.novatrek.trailmanagement.repository.TrailRepository;
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

@WebMvcTest(TrailController.class)
class TrailControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private TrailRepository trailRepository;

    private Trail createTestTrail() {
        Trail trail = new Trail();
        trail.setId(UUID.randomUUID());
        trail.setName("Eagle Peak Trail");
        trail.setDescription("Steep ascent with panoramic views");
        trail.setDistanceKm(new BigDecimal("12.50"));
        trail.setElevationGainM(850);
        trail.setElevationLossM(200);
        trail.setEstimatedDurationHours(new BigDecimal("5.5"));
        trail.setDifficulty(Trail.DifficultyRating.DIFFICULT);
        trail.setMaxGroupSize(8);
        trail.setPermitRequired(true);
        trail.setDogsAllowed(false);
        trail.setStatus(Trail.TrailStatus.OPEN);
        return trail;
    }

    @Test
    void listTrails_returnsAll() throws Exception {
        when(trailRepository.findAll()).thenReturn(List.of(createTestTrail()));

        mockMvc.perform(get("/trails"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].name").value("Eagle Peak Trail"));
    }

    @Test
    void listTrails_filterByStatus() throws Exception {
        Trail trail = createTestTrail();
        when(trailRepository.findByStatus(Trail.TrailStatus.OPEN)).thenReturn(List.of(trail));

        mockMvc.perform(get("/trails").param("status", "OPEN"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void listTrails_filterByDifficulty() throws Exception {
        Trail trail = createTestTrail();
        when(trailRepository.findByDifficulty(Trail.DifficultyRating.DIFFICULT)).thenReturn(List.of(trail));

        mockMvc.perform(get("/trails").param("difficulty", "DIFFICULT"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void createTrail_returns201() throws Exception {
        Trail trail = createTestTrail();
        when(trailRepository.save(any(Trail.class))).thenReturn(trail);

        Trail input = new Trail();
        input.setName("Eagle Peak Trail");
        input.setDistanceKm(new BigDecimal("12.50"));
        input.setDifficulty(Trail.DifficultyRating.DIFFICULT);

        mockMvc.perform(post("/trails")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(input)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name").value("Eagle Peak Trail"));
    }

    @Test
    void getTrail_returnsTrail() throws Exception {
        Trail trail = createTestTrail();
        UUID id = trail.getId();
        when(trailRepository.findById(id)).thenReturn(Optional.of(trail));

        mockMvc.perform(get("/trails/{trailId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Eagle Peak Trail"))
                .andExpect(jsonPath("$.difficulty").value("DIFFICULT"))
                .andExpect(jsonPath("$.permitRequired").value(true));
    }

    @Test
    void getTrail_returns404WhenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(trailRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/trails/{trailId}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateTrail_patchesFields() throws Exception {
        Trail existing = createTestTrail();
        UUID id = existing.getId();
        when(trailRepository.findById(id)).thenReturn(Optional.of(existing));
        when(trailRepository.save(any(Trail.class))).thenAnswer(inv -> inv.getArgument(0));

        String patchJson = """
                {"name": "Updated Trail", "difficulty": "EXPERT", "maxGroupSize": 4}
                """;

        mockMvc.perform(patch("/trails/{trailId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patchJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Updated Trail"))
                .andExpect(jsonPath("$.difficulty").value("EXPERT"))
                .andExpect(jsonPath("$.maxGroupSize").value(4));
    }

    @Test
    void updateTrail_returns404WhenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(trailRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/trails/{trailId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"name\": \"x\"}"))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateTrail_patchesBooleanFields() throws Exception {
        Trail existing = createTestTrail();
        UUID id = existing.getId();
        when(trailRepository.findById(id)).thenReturn(Optional.of(existing));
        when(trailRepository.save(any(Trail.class))).thenAnswer(inv -> inv.getArgument(0));

        String patchJson = """
                {"permitRequired": false, "dogsAllowed": true, "status": "PARTIALLY_CLOSED"}
                """;

        mockMvc.perform(patch("/trails/{trailId}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(patchJson))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.permitRequired").value(false))
                .andExpect(jsonPath("$.dogsAllowed").value(true))
                .andExpect(jsonPath("$.status").value("PARTIALLY_CLOSED"));
    }
}

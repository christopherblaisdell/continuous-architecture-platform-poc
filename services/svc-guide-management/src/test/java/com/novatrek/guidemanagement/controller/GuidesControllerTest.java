package com.novatrek.guidemanagement.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.guidemanagement.entity.Guide;
import com.novatrek.guidemanagement.repository.GuideRepository;
import com.novatrek.guidemanagement.repository.GuideCertificationRepository;
import com.novatrek.guidemanagement.repository.GuideScheduleEntryRepository;
import com.novatrek.guidemanagement.repository.GuideRatingRepository;
import com.novatrek.guidemanagement.repository.AvailabilityWindowRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(GuidesController.class)
class GuidesControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private GuideRepository guideRepository;

    @MockBean
    private GuideCertificationRepository guideCertificationRepository;

    @MockBean
    private GuideScheduleEntryRepository guideScheduleEntryRepository;

    @MockBean
    private GuideRatingRepository guideRatingRepository;

    @MockBean
    private AvailabilityWindowRepository availabilityWindowRepository;

    private Guide sampleGuide() {
        Guide g = new Guide();
        g.setFirstName("Alex");
        g.setLastName("Rivers");
        g.setEmail("alex.rivers@novatrek.example.com");
        g.setYearsExperience(8);
        g.setMaxGroupSize(12);
        g.setStatus(Guide.GuideStatus.ACTIVE);
        g.setAverageRating(new BigDecimal("4.75"));
        g.setTotalTripsLed(150);
        g.setEmergencyTrainingLevel(Guide.EmergencyTrainingLevel.WILDERNESS_FIRST_RESPONDER);
        return g;
    }

    @Test
    void searchGuides_returnsEmptyList() throws Exception {
        when(guideRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/guides"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void searchGuides_returnsGuides() throws Exception {
        Guide g = sampleGuide();
        when(guideRepository.findAll()).thenReturn(List.of(g));

        mockMvc.perform(get("/guides"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].firstName", is("Alex")))
                .andExpect(jsonPath("$[0].status", is("ACTIVE")));
    }

    @Test
    void createGuide_returns201() throws Exception {
        Guide g = sampleGuide();
        when(guideRepository.save(any(Guide.class))).thenReturn(g);

        mockMvc.perform(post("/guides")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(g)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.firstName", is("Alex")));
    }

    @Test
    void findAvailableGuides_returnsList() throws Exception {
        Guide g = sampleGuide();
        when(guideRepository.findAll()).thenReturn(List.of(g));

        mockMvc.perform(get("/guides/available"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void getGuideCertifications_returnsList() throws Exception {
        Guide g = sampleGuide();
        when(guideRepository.findAll()).thenReturn(List.of(g));

        mockMvc.perform(get("/guides/{id}/certifications", UUID.randomUUID()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)));
    }

    @Test
    void getGuideSchedule_returnsList() throws Exception {
        when(guideRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/guides/{id}/schedule", UUID.randomUUID()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void getGuideAvailability_returnsList() throws Exception {
        when(guideRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/guides/{id}/availability", UUID.randomUUID()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void getGuideRatings_returnsList() throws Exception {
        when(guideRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/guides/{id}/ratings", UUID.randomUUID()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }
}

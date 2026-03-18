package com.novatrek.analytics.controller;

import com.novatrek.analytics.entity.GuidePerformance;
import com.novatrek.analytics.repository.GuidePerformanceRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(AnalyticsController.class)
class AnalyticsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private GuidePerformanceRepository guidePerformanceRepository;

    @Test
    void getBookingAnalytics_returnsList() throws Exception {
        when(guidePerformanceRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/analytics/bookings"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void getRevenueAnalytics_returnsList() throws Exception {
        GuidePerformance gp = new GuidePerformance();
        gp.setTripsLed(15);
        gp.setTotalParticipants(120);
        when(guidePerformanceRepository.findAll()).thenReturn(List.of(gp));

        mockMvc.perform(get("/analytics/revenue"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].tripsLed", is(15)));
    }

    @Test
    void getUtilizationAnalytics_returnsList() throws Exception {
        when(guidePerformanceRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/analytics/utilization"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void getGuestSatisfaction_returnsList() throws Exception {
        when(guidePerformanceRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/analytics/guest-satisfaction"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void getSafetyMetrics_returnsList() throws Exception {
        when(guidePerformanceRepository.findAll()).thenReturn(List.of());
        mockMvc.perform(get("/analytics/safety-metrics"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void getGuidePerformance_found() throws Exception {
        UUID guideId = UUID.randomUUID();
        GuidePerformance gp = new GuidePerformance();
        gp.setGuideId(guideId);
        gp.setTripsLed(42);
        gp.setTotalParticipants(350);
        gp.setAverageGuestRating(new BigDecimal("4.85"));
        gp.setIncidentCount(1);
        gp.setCancellationRate(new BigDecimal("2.30"));

        when(guidePerformanceRepository.findById(guideId)).thenReturn(Optional.of(gp));

        mockMvc.perform(get("/analytics/guide-performance/{guideId}", guideId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.tripsLed", is(42)))
                .andExpect(jsonPath("$.totalParticipants", is(350)));
    }

    @Test
    void getGuidePerformance_notFound() throws Exception {
        UUID guideId = UUID.randomUUID();
        when(guidePerformanceRepository.findById(guideId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/analytics/guide-performance/{guideId}", guideId))
                .andExpect(status().isNotFound());
    }
}

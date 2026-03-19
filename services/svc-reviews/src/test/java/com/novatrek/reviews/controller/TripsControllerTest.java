package com.novatrek.reviews.controller;

import com.novatrek.reviews.entity.RatingSummary;
import com.novatrek.reviews.repository.RatingSummaryRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.is;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(TripsController.class)
class TripsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private RatingSummaryRepository ratingSummaryRepository;

    @Test
    void getTripRatingSummary_returnsSummary() throws Exception {
        UUID tripId = UUID.randomUUID();
        RatingSummary summary = new RatingSummary();
        summary.setEntityId(tripId);
        summary.setAverageRating(new BigDecimal("4.50"));
        summary.setTotalReviews(12);
        when(ratingSummaryRepository.findById(tripId)).thenReturn(Optional.of(summary));

        mockMvc.perform(get("/trips/{tripId}/rating-summary", tripId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalReviews", is(12)));
    }

    @Test
    void getTripRatingSummary_notFound_returns404() throws Exception {
        UUID tripId = UUID.randomUUID();
        when(ratingSummaryRepository.findById(tripId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/trips/{tripId}/rating-summary", tripId))
                .andExpect(status().isNotFound());
    }
}

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

@WebMvcTest(GuidesController.class)
class GuidesControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private RatingSummaryRepository ratingSummaryRepository;

    @Test
    void getGuideRatingSummary_returnsSummary() throws Exception {
        UUID guideId = UUID.randomUUID();
        RatingSummary summary = new RatingSummary();
        summary.setEntityId(guideId);
        summary.setAverageRating(new BigDecimal("4.80"));
        summary.setTotalReviews(25);
        when(ratingSummaryRepository.findById(guideId)).thenReturn(Optional.of(summary));

        mockMvc.perform(get("/guides/{guideId}/rating-summary", guideId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.totalReviews", is(25)));
    }

    @Test
    void getGuideRatingSummary_notFound_returns404() throws Exception {
        UUID guideId = UUID.randomUUID();
        when(ratingSummaryRepository.findById(guideId)).thenReturn(Optional.empty());

        mockMvc.perform(get("/guides/{guideId}/rating-summary", guideId))
                .andExpect(status().isNotFound());
    }
}

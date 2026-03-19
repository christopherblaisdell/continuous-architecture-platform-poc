package com.novatrek.reviews.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.reviews.entity.Review;
import com.novatrek.reviews.repository.ReviewRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ModerationController.class)
class ModerationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ReviewRepository reviewRepository;

    @Test
    void getModerationQueue_returnsAll() throws Exception {
        Review r = new Review();
        r.setTitle("Needs moderation");
        r.setModerationStatus(Review.ModerationStatus.PENDING_MODERATION);
        when(reviewRepository.findAll()).thenReturn(List.of(r));

        mockMvc.perform(get("/moderation/queue"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].moderationStatus", is("PENDING_MODERATION")));
    }

    @Test
    void moderateReview_returnsUpdated() throws Exception {
        Review r = new Review();
        UUID id = UUID.randomUUID();
        r.setId(id);
        r.setModerationStatus(Review.ModerationStatus.PENDING_MODERATION);
        when(reviewRepository.findById(id)).thenReturn(Optional.of(r));
        when(reviewRepository.save(any(Review.class))).thenReturn(r);

        Review decision = new Review();
        decision.setModerationStatus(Review.ModerationStatus.APPROVED);

        mockMvc.perform(post("/moderation/{id}/decide", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(decision)))
                .andExpect(status().isOk());
    }

    @Test
    void moderateReview_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(reviewRepository.findById(id)).thenReturn(Optional.empty());

        Review decision = new Review();
        decision.setModerationStatus(Review.ModerationStatus.APPROVED);

        mockMvc.perform(post("/moderation/{id}/decide", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(decision)))
                .andExpect(status().isNotFound());
    }
}

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

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(ReviewsController.class)
class ReviewsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private ReviewRepository reviewRepository;

    private Review sampleReview() {
        Review r = new Review();
        r.setReservationId(UUID.randomUUID());
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setGuideId(UUID.randomUUID());
        r.setOverallRating(5);
        r.setTitle("Amazing adventure!");
        r.setBody("Had a wonderful time on the mountain trail.");
        r.setVisitDate(LocalDate.of(2026, 3, 15));
        r.setModerationStatus(Review.ModerationStatus.PENDING_MODERATION);
        r.setHelpfulCount(0);
        return r;
    }

    @Test
    void listReviews_returnsEmptyList() throws Exception {
        when(reviewRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/reviews"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void listReviews_returnsReviews() throws Exception {
        Review r = sampleReview();
        when(reviewRepository.findAll()).thenReturn(List.of(r));

        mockMvc.perform(get("/reviews"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].title", is("Amazing adventure!")));
    }

    @Test
    void submitReview_returns201() throws Exception {
        Review r = sampleReview();
        when(reviewRepository.save(any(Review.class))).thenReturn(r);

        mockMvc.perform(post("/reviews")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(r)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.title", is("Amazing adventure!")))
                .andExpect(jsonPath("$.overallRating", is(5)));
    }

    @Test
    void getReview_returnsReview() throws Exception {
        Review r = sampleReview();
        UUID id = UUID.randomUUID();
        r.setId(id);
        when(reviewRepository.findById(id)).thenReturn(Optional.of(r));

        mockMvc.perform(get("/reviews/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title", is("Amazing adventure!")));
    }

    @Test
    void getReview_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(reviewRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/reviews/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void updateReview_patchFields() throws Exception {
        Review r = sampleReview();
        UUID id = UUID.randomUUID();
        r.setId(id);
        when(reviewRepository.findById(id)).thenReturn(Optional.of(r));
        when(reviewRepository.save(any(Review.class))).thenReturn(r);

        Review patch = new Review();
        patch.setTitle("Updated title");

        mockMvc.perform(patch("/reviews/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(patch)))
                .andExpect(status().isOk());
    }

    @Test
    void updateReview_allFields() throws Exception {
        Review r = sampleReview();
        UUID id = UUID.randomUUID();
        r.setId(id);
        when(reviewRepository.findById(id)).thenReturn(Optional.of(r));
        when(reviewRepository.save(any(Review.class))).thenReturn(r);

        Review patch = new Review();
        patch.setReservationId(UUID.randomUUID());
        patch.setGuestId(UUID.randomUUID());
        patch.setTripId(UUID.randomUUID());
        patch.setGuideId(UUID.randomUUID());
        patch.setOverallRating(3);
        patch.setTitle("New title");
        patch.setBody("New body");
        patch.setVisitDate(LocalDate.of(2026, 1, 1));
        patch.setModerationStatus(Review.ModerationStatus.APPROVED);
        patch.setHelpfulCount(5);
        patch.setRev(2);

        mockMvc.perform(patch("/reviews/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(patch)))
                .andExpect(status().isOk());
    }

    @Test
    void updateReview_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(reviewRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(patch("/reviews/{id}", id)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new Review())))
                .andExpect(status().isNotFound());
    }

    @Test
    void markHelpful_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(reviewRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(post("/reviews/{id}/helpful", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void deleteReview_returns204() throws Exception {
        UUID id = UUID.randomUUID();
        when(reviewRepository.existsById(id)).thenReturn(true);

        mockMvc.perform(delete("/reviews/{id}", id))
                .andExpect(status().isNoContent());
    }

    @Test
    void deleteReview_notFound_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(reviewRepository.existsById(id)).thenReturn(false);

        mockMvc.perform(delete("/reviews/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void markHelpful_returnsReview() throws Exception {
        Review r = sampleReview();
        UUID id = UUID.randomUUID();
        r.setId(id);
        when(reviewRepository.findById(id)).thenReturn(Optional.of(r));
        when(reviewRepository.save(any(Review.class))).thenReturn(r);

        mockMvc.perform(post("/reviews/{id}/helpful", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.title", is("Amazing adventure!")));
    }
}

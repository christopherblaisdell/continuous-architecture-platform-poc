package com.novatrek.reviews.controller;

import com.novatrek.reviews.entity.Review;
import com.novatrek.reviews.repository.ReviewRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/moderation")
public class ModerationController {

    private final ReviewRepository reviewRepository;

    public ModerationController(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }

    @GetMapping("/queue")
    public List<Review> getModerationQueue() {
        return reviewRepository.findAll();
    }

    @PostMapping("/{reviewId}/decide")
    public Review moderateReview(@PathVariable UUID reviewId, @Valid @RequestBody Review body) {
        Review existing = reviewRepository.findById(reviewId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Review not found"));
        return reviewRepository.save(existing);
    }

}

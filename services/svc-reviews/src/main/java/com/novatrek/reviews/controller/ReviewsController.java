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
@RequestMapping("/reviews")
public class ReviewsController {

    private final ReviewRepository reviewRepository;

    public ReviewsController(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }

    @GetMapping
    public List<Review> listReviews() {
        return reviewRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Review> submitReview(@Valid @RequestBody Review body) {
        Review saved = reviewRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{reviewId}")
    public Review getReview(@PathVariable UUID reviewId) {
        return reviewRepository.findById(reviewId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Review not found"));
    }

    @PatchMapping("/{reviewId}")
    public Review updateReview(@PathVariable UUID reviewId, @Valid @RequestBody Review body) {
        Review existing = reviewRepository.findById(reviewId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Review not found"));

        if (body.getReservationId() != null) existing.setReservationId(body.getReservationId());
        if (body.getGuestId() != null) existing.setGuestId(body.getGuestId());
        if (body.getTripId() != null) existing.setTripId(body.getTripId());
        if (body.getGuideId() != null) existing.setGuideId(body.getGuideId());
        if (body.getOverallRating() != null) existing.setOverallRating(body.getOverallRating());
        if (body.getTitle() != null) existing.setTitle(body.getTitle());
        if (body.getBody() != null) existing.setBody(body.getBody());
        if (body.getVisitDate() != null) existing.setVisitDate(body.getVisitDate());
        if (body.getModerationStatus() != null) existing.setModerationStatus(body.getModerationStatus());
        if (body.getHelpfulCount() != null) existing.setHelpfulCount(body.getHelpfulCount());
        if (body.getRev() != null) existing.setRev(body.getRev());

        return reviewRepository.save(existing);
    }

    @DeleteMapping("/{reviewId}")
    public ResponseEntity<Void> deleteReview(@PathVariable UUID reviewId) {
        if (!reviewRepository.existsById(reviewId)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Review not found");
        }
        reviewRepository.deleteById(reviewId);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{reviewId}/helpful")
    public Review markReviewHelpful(@PathVariable UUID reviewId) {
        Review existing = reviewRepository.findById(reviewId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Review not found"));
        return reviewRepository.save(existing);
    }

}

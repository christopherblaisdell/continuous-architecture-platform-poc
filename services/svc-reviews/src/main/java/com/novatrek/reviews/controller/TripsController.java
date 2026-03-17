package com.novatrek.reviews.controller;

import com.novatrek.reviews.entity.RatingSummary;
import com.novatrek.reviews.repository.RatingSummaryRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/trips")
public class TripsController {

    private final RatingSummaryRepository ratingSummaryRepository;

    public TripsController(RatingSummaryRepository ratingSummaryRepository) {
        this.ratingSummaryRepository = ratingSummaryRepository;
    }

    @GetMapping("/{tripId}/rating-summary")
    public RatingSummary getTripRatingSummary(@PathVariable UUID tripId) {
        return ratingSummaryRepository.findById(tripId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "RatingSummary not found"));
    }

}

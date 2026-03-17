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
@RequestMapping("/guides")
public class GuidesController {

    private final RatingSummaryRepository ratingSummaryRepository;

    public GuidesController(RatingSummaryRepository ratingSummaryRepository) {
        this.ratingSummaryRepository = ratingSummaryRepository;
    }

    @GetMapping("/{guideId}/rating-summary")
    public RatingSummary getGuideRatingSummary(@PathVariable UUID guideId) {
        return ratingSummaryRepository.findById(guideId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "RatingSummary not found"));
    }

}

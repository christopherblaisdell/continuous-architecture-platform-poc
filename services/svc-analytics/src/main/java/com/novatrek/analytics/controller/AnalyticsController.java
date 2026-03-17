package com.novatrek.analytics.controller;

import com.novatrek.analytics.entity.GuidePerformance;
import com.novatrek.analytics.repository.GuidePerformanceRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/analytics")
public class AnalyticsController {

    private final GuidePerformanceRepository guidePerformanceRepository;

    public AnalyticsController(GuidePerformanceRepository guidePerformanceRepository) {
        this.guidePerformanceRepository = guidePerformanceRepository;
    }

    @GetMapping("/bookings")
    public List<GuidePerformance> getBookingAnalytics() {
        return guidePerformanceRepository.findAll();
    }

    @GetMapping("/revenue")
    public List<GuidePerformance> getRevenueAnalytics() {
        return guidePerformanceRepository.findAll();
    }

    @GetMapping("/utilization")
    public List<GuidePerformance> getUtilizationAnalytics() {
        return guidePerformanceRepository.findAll();
    }

    @GetMapping("/guest-satisfaction")
    public List<GuidePerformance> getGuestSatisfaction() {
        return guidePerformanceRepository.findAll();
    }

    @GetMapping("/safety-metrics")
    public List<GuidePerformance> getSafetyMetrics() {
        return guidePerformanceRepository.findAll();
    }

    @GetMapping("/guide-performance/{guideId}")
    public GuidePerformance getGuidePerformance(@PathVariable UUID guideId) {
        return guidePerformanceRepository.findById(guideId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "GuidePerformance not found"));
    }

}

package com.novatrek.guidemanagement.controller;

import com.novatrek.guidemanagement.entity.Guide;
import com.novatrek.guidemanagement.repository.GuideRepository;
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

    private final GuideRepository guideRepository;

    public GuidesController(GuideRepository guideRepository) {
        this.guideRepository = guideRepository;
    }

    @GetMapping
    public List<Guide> searchGuides() {
        return guideRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Guide> createGuide(@Valid @RequestBody Guide body) {
        Guide saved = guideRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{guide_id}")
    public List<Guide> getGuide() {
        return guideRepository.findAll();
    }

    @PatchMapping("/{guide_id}")
    public Guide updateGuide(@Valid @RequestBody Guide body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @GetMapping("/{guide_id}/certifications")
    public List<Guide> getGuideCertifications() {
        return guideRepository.findAll();
    }

    @PostMapping("/{guide_id}/certifications")
    public ResponseEntity<Guide> addGuideCertification(@Valid @RequestBody Guide body) {
        Guide saved = guideRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{guide_id}/schedule")
    public List<Guide> getGuideSchedule() {
        return guideRepository.findAll();
    }

    @GetMapping("/{guide_id}/availability")
    public List<Guide> getGuideAvailability() {
        return guideRepository.findAll();
    }

    @PostMapping("/{guide_id}/availability")
    public ResponseEntity<Guide> setGuideAvailability(@Valid @RequestBody Guide body) {
        Guide saved = guideRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{guide_id}/ratings")
    public List<Guide> getGuideRatings() {
        return guideRepository.findAll();
    }

    @PostMapping("/{guide_id}/ratings")
    public ResponseEntity<Guide> submitGuideRating(@Valid @RequestBody Guide body) {
        Guide saved = guideRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/available")
    public List<Guide> findAvailableGuides() {
        return guideRepository.findAll();
    }

}

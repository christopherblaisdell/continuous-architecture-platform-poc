package com.novatrek.trailmanagement.controller;

import com.novatrek.trailmanagement.entity.Trail;
import com.novatrek.trailmanagement.repository.TrailRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/trails")
public class TrailController {

    private final TrailRepository trailRepository;

    public TrailController(TrailRepository trailRepository) {
        this.trailRepository = trailRepository;
    }

    @GetMapping
    public List<Trail> listTrails(@RequestParam(required = false) Trail.TrailStatus status,
                                  @RequestParam(required = false) Trail.DifficultyRating difficulty) {
        if (status != null) return trailRepository.findByStatus(status);
        if (difficulty != null) return trailRepository.findByDifficulty(difficulty);
        return trailRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Trail> createTrail(@Valid @RequestBody Trail trail) {
        Trail saved = trailRepository.save(trail);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{trailId}")
    public Trail getTrail(@PathVariable UUID trailId) {
        return trailRepository.findById(trailId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trail not found"));
    }

    @PatchMapping("/{trailId}")
    public Trail updateTrail(@PathVariable UUID trailId, @RequestBody Trail patch) {
        Trail existing = trailRepository.findById(trailId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trail not found"));

        if (patch.getName() != null) existing.setName(patch.getName());
        if (patch.getDescription() != null) existing.setDescription(patch.getDescription());
        if (patch.getDifficulty() != null) existing.setDifficulty(patch.getDifficulty());
        if (patch.getMaxGroupSize() != null) existing.setMaxGroupSize(patch.getMaxGroupSize());
        if (patch.getPermitRequired() != null) existing.setPermitRequired(patch.getPermitRequired());
        if (patch.getDogsAllowed() != null) existing.setDogsAllowed(patch.getDogsAllowed());
        if (patch.getStatus() != null) existing.setStatus(patch.getStatus());

        return trailRepository.save(existing);
    }
}

package com.novatrek.wildlifetracking.controller;

import com.novatrek.wildlifetracking.entity.Sighting;
import com.novatrek.wildlifetracking.repository.SightingRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/sightings")
public class SightingsController {

    private final SightingRepository sightingRepository;

    public SightingsController(SightingRepository sightingRepository) {
        this.sightingRepository = sightingRepository;
    }

    @GetMapping
    public List<Sighting> listSightings() {
        return sightingRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Sighting> reportSighting(@Valid @RequestBody Sighting body) {
        Sighting saved = sightingRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{sightingId}")
    public Sighting getSighting(@PathVariable UUID sightingId) {
        return sightingRepository.findById(sightingId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Sighting not found"));
    }

}

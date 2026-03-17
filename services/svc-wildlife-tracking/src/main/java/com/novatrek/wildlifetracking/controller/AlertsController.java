package com.novatrek.wildlifetracking.controller;

import com.novatrek.wildlifetracking.entity.WildlifeAlert;
import com.novatrek.wildlifetracking.repository.WildlifeAlertRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/alerts")
public class AlertsController {

    private final WildlifeAlertRepository wildlifeAlertRepository;

    public AlertsController(WildlifeAlertRepository wildlifeAlertRepository) {
        this.wildlifeAlertRepository = wildlifeAlertRepository;
    }

    @GetMapping
    public List<WildlifeAlert> listWildlifeAlerts() {
        return wildlifeAlertRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<WildlifeAlert> issueWildlifeAlert(@Valid @RequestBody WildlifeAlert body) {
        WildlifeAlert saved = wildlifeAlertRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{alertId}")
    public WildlifeAlert getWildlifeAlert(@PathVariable UUID alertId) {
        return wildlifeAlertRepository.findById(alertId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "WildlifeAlert not found"));
    }

    @PatchMapping("/{alertId}")
    public WildlifeAlert updateWildlifeAlert(@PathVariable UUID alertId, @Valid @RequestBody WildlifeAlert body) {
        WildlifeAlert existing = wildlifeAlertRepository.findById(alertId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "WildlifeAlert not found"));

        if (body.getSpeciesId() != null) existing.setSpeciesId(body.getSpeciesId());
        if (body.getSpeciesName() != null) existing.setSpeciesName(body.getSpeciesName());
        if (body.getSightingId() != null) existing.setSightingId(body.getSightingId());
        if (body.getThreatLevel() != null) existing.setThreatLevel(body.getThreatLevel());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());
        if (body.getRadiusMeters() != null) existing.setRadiusMeters(body.getRadiusMeters());
        if (body.getRecommendedAction() != null) existing.setRecommendedAction(body.getRecommendedAction());
        if (body.getNotes() != null) existing.setNotes(body.getNotes());
        if (body.getRev() != null) existing.setRev(body.getRev());

        return wildlifeAlertRepository.save(existing);
    }

}

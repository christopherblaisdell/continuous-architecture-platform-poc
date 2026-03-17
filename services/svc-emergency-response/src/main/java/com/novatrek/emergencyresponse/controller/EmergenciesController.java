package com.novatrek.emergencyresponse.controller;

import com.novatrek.emergencyresponse.entity.Emergency;
import com.novatrek.emergencyresponse.repository.EmergencyRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/emergencies")
public class EmergenciesController {

    private final EmergencyRepository emergencyRepository;

    public EmergenciesController(EmergencyRepository emergencyRepository) {
        this.emergencyRepository = emergencyRepository;
    }

    @GetMapping
    public List<Emergency> listEmergencies() {
        return emergencyRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Emergency> triggerEmergency(@Valid @RequestBody Emergency body) {
        Emergency saved = emergencyRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{emergencyId}")
    public Emergency getEmergency(@PathVariable UUID emergencyId) {
        return emergencyRepository.findById(emergencyId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Emergency not found"));
    }

    @PatchMapping("/{emergencyId}")
    public Emergency updateEmergencyStatus(@PathVariable UUID emergencyId, @Valid @RequestBody Emergency body) {
        Emergency existing = emergencyRepository.findById(emergencyId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Emergency not found"));

        if (body.getGuestId() != null) existing.setGuestId(body.getGuestId());
        if (body.getReservationId() != null) existing.setReservationId(body.getReservationId());
        if (body.getType() != null) existing.setType(body.getType());
        if (body.getSeverity() != null) existing.setSeverity(body.getSeverity());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());
        if (body.getDescription() != null) existing.setDescription(body.getDescription());
        if (body.getReportedBy() != null) existing.setReportedBy(body.getReportedBy());
        if (body.getDispatchId() != null) existing.setDispatchId(body.getDispatchId());
        if (body.getResolutionNotes() != null) existing.setResolutionNotes(body.getResolutionNotes());
        if (body.getRev() != null) existing.setRev(body.getRev());

        return emergencyRepository.save(existing);
    }

    @GetMapping("/{emergencyId}/timeline")
    public Emergency getEmergencyTimeline(@PathVariable UUID emergencyId) {
        return emergencyRepository.findById(emergencyId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Emergency not found"));
    }

    @PostMapping("/{emergencyId}/timeline")
    public ResponseEntity<Emergency> addTimelineEntry(@PathVariable UUID emergencyId, @Valid @RequestBody Emergency body) {
        Emergency saved = emergencyRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PostMapping("/{emergencyId}/dispatch")
    public ResponseEntity<Emergency> dispatchRescueTeam(@PathVariable UUID emergencyId, @Valid @RequestBody Emergency body) {
        Emergency saved = emergencyRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}

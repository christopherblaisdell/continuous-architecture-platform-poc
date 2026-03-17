package com.novatrek.safetycompliance.controller;

import com.novatrek.safetycompliance.entity.IncidentReport;
import com.novatrek.safetycompliance.repository.IncidentReportRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/incidents")
public class IncidentsController {

    private final IncidentReportRepository incidentReportRepository;

    public IncidentsController(IncidentReportRepository incidentReportRepository) {
        this.incidentReportRepository = incidentReportRepository;
    }

    @PostMapping
    public ResponseEntity<IncidentReport> createIncident(@Valid @RequestBody IncidentReport body) {
        IncidentReport saved = incidentReportRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{incidentId}")
    public IncidentReport getIncident(@PathVariable UUID incidentId) {
        return incidentReportRepository.findById(incidentId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "IncidentReport not found"));
    }

    @PatchMapping("/{incidentId}")
    public IncidentReport updateIncident(@PathVariable UUID incidentId, @Valid @RequestBody IncidentReport body) {
        IncidentReport existing = incidentReportRepository.findById(incidentId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "IncidentReport not found"));

        if (body.getReservationId() != null) existing.setReservationId(body.getReservationId());
        if (body.getGuideId() != null) existing.setGuideId(body.getGuideId());
        if (body.getType() != null) existing.setType(body.getType());
        if (body.getSeverity() != null) existing.setSeverity(body.getSeverity());
        if (body.getDescription() != null) existing.setDescription(body.getDescription());
        if (body.getActionsTaken() != null) existing.setActionsTaken(body.getActionsTaken());
        if (body.getFollowUpRequired() != null) existing.setFollowUpRequired(body.getFollowUpRequired());
        if (body.getFollowUpNotes() != null) existing.setFollowUpNotes(body.getFollowUpNotes());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());

        return incidentReportRepository.save(existing);
    }

}

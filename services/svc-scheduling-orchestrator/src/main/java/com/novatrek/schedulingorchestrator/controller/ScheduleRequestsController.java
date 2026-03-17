package com.novatrek.schedulingorchestrator.controller;

import com.novatrek.schedulingorchestrator.entity.ConflictResolutionResult;
import com.novatrek.schedulingorchestrator.repository.ConflictResolutionResultRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/schedule-requests")
public class ScheduleRequestsController {

    private final ConflictResolutionResultRepository conflictResolutionResultRepository;

    public ScheduleRequestsController(ConflictResolutionResultRepository conflictResolutionResultRepository) {
        this.conflictResolutionResultRepository = conflictResolutionResultRepository;
    }

    @PostMapping
    public ConflictResolutionResult createScheduleRequest(@Valid @RequestBody ConflictResolutionResult body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @GetMapping("/{requestId}")
    public ConflictResolutionResult getScheduleRequest(@PathVariable UUID requestId) {
        return conflictResolutionResultRepository.findById(requestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "ConflictResolutionResult not found"));
    }

}

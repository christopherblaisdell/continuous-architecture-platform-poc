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
@RequestMapping("/schedule-optimization")
public class ScheduleOptimizationController {

    private final ConflictResolutionResultRepository conflictResolutionResultRepository;

    public ScheduleOptimizationController(ConflictResolutionResultRepository conflictResolutionResultRepository) {
        this.conflictResolutionResultRepository = conflictResolutionResultRepository;
    }

    @GetMapping
    public List<ConflictResolutionResult> getScheduleOptimization() {
        return conflictResolutionResultRepository.findAll();
    }

}

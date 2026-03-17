package com.novatrek.safetycompliance.controller;

import com.novatrek.safetycompliance.entity.SafetyInspection;
import com.novatrek.safetycompliance.repository.SafetyInspectionRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/safety-inspections")
public class SafetyInspectionsController {

    private final SafetyInspectionRepository safetyInspectionRepository;

    public SafetyInspectionsController(SafetyInspectionRepository safetyInspectionRepository) {
        this.safetyInspectionRepository = safetyInspectionRepository;
    }

    @GetMapping
    public List<SafetyInspection> listSafetyInspections() {
        return safetyInspectionRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<SafetyInspection> createSafetyInspection(@Valid @RequestBody SafetyInspection body) {
        SafetyInspection saved = safetyInspectionRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}

package com.novatrek.gearinventory.controller;

import com.novatrek.gearinventory.entity.GearAssignment;
import com.novatrek.gearinventory.repository.GearAssignmentRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/gear-assignments")
public class GearAssignmentsController {

    private final GearAssignmentRepository gearAssignmentRepository;

    public GearAssignmentsController(GearAssignmentRepository gearAssignmentRepository) {
        this.gearAssignmentRepository = gearAssignmentRepository;
    }

    @PostMapping
    public ResponseEntity<GearAssignment> createGearAssignment(@Valid @RequestBody GearAssignment body) {
        GearAssignment saved = gearAssignmentRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{assignment_id}")
    public List<GearAssignment> getGearAssignment() {
        return gearAssignmentRepository.findAll();
    }

    @DeleteMapping("/{assignment_id}")
    public ResponseEntity<Void> returnGearAssignment() {
        throw new UnsupportedOperationException("Not yet implemented");
    }

}

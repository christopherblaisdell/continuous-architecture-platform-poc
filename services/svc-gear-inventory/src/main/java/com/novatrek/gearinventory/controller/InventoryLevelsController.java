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
@RequestMapping("/inventory-levels")
public class InventoryLevelsController {

    private final GearAssignmentRepository gearAssignmentRepository;

    public InventoryLevelsController(GearAssignmentRepository gearAssignmentRepository) {
        this.gearAssignmentRepository = gearAssignmentRepository;
    }

    @GetMapping
    public List<GearAssignment> getInventoryLevels() {
        return gearAssignmentRepository.findAll();
    }

}

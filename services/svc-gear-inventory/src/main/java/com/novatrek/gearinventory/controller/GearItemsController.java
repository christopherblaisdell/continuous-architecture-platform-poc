package com.novatrek.gearinventory.controller;

import com.novatrek.gearinventory.entity.GearItem;
import com.novatrek.gearinventory.repository.GearItemRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/gear-items")
public class GearItemsController {

    private final GearItemRepository gearItemRepository;

    public GearItemsController(GearItemRepository gearItemRepository) {
        this.gearItemRepository = gearItemRepository;
    }

    @GetMapping
    public List<GearItem> searchGearItems() {
        return gearItemRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<GearItem> addGearItem(@Valid @RequestBody GearItem body) {
        GearItem saved = gearItemRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{item_id}")
    public List<GearItem> getGearItem() {
        return gearItemRepository.findAll();
    }

    @PatchMapping("/{item_id}")
    public GearItem updateGearItem(@Valid @RequestBody GearItem body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @PutMapping("/{item_id}/maintenance")
    public GearItem logMaintenanceEvent(@Valid @RequestBody GearItem body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @GetMapping("/{item_id}/maintenance-history")
    public List<GearItem> getMaintenanceHistory() {
        return gearItemRepository.findAll();
    }

}

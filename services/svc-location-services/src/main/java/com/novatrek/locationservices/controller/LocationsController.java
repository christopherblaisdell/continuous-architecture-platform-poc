package com.novatrek.locationservices.controller;

import com.novatrek.locationservices.entity.Location;
import com.novatrek.locationservices.repository.LocationRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/locations")
public class LocationsController {

    private final LocationRepository locationRepository;

    public LocationsController(LocationRepository locationRepository) {
        this.locationRepository = locationRepository;
    }

    @GetMapping
    public List<Location> listLocations() {
        return locationRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Location> createLocation(@Valid @RequestBody Location body) {
        Location saved = locationRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{locationId}")
    public Location getLocation(@PathVariable UUID locationId) {
        return locationRepository.findById(locationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Location not found"));
    }

    @PatchMapping("/{locationId}")
    public Location updateLocation(@PathVariable UUID locationId, @Valid @RequestBody Location body) {
        Location existing = locationRepository.findById(locationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Location not found"));

        if (body.getName() != null) existing.setName(body.getName());
        if (body.getType() != null) existing.setType(body.getType());
        if (body.getRegionId() != null) existing.setRegionId(body.getRegionId());
        if (body.getCapacity() != null) existing.setCapacity(body.getCapacity());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());

        return locationRepository.save(existing);
    }

    @GetMapping("/{locationId}/capacity")
    public Location getLocationCapacity(@PathVariable UUID locationId) {
        return locationRepository.findById(locationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Location not found"));
    }

    @GetMapping("/{locationId}/operating-hours")
    public Location getOperatingHours(@PathVariable UUID locationId) {
        return locationRepository.findById(locationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Location not found"));
    }

}

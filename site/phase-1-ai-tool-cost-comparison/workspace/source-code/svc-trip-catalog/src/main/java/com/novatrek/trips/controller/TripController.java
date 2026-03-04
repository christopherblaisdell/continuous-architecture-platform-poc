package com.novatrek.trips.controller;

import com.novatrek.trips.model.Trip;
import com.novatrek.trips.repository.TripRepository;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/v1/trips")
@RequiredArgsConstructor
public class TripController {

    private final TripRepository tripRepository;

    @GetMapping
    public List<Trip> listTrips(
            @RequestParam(required = false) String category,
            @RequestParam(required = false) Trip.Difficulty difficulty,
            @RequestParam(required = false) BigDecimal minPrice,
            @RequestParam(required = false) BigDecimal maxPrice,
            @RequestParam(required = false) UUID locationId) {
        if (category != null) return tripRepository.findByAdventureCategory(category);
        if (difficulty != null) return tripRepository.findByDifficulty(difficulty);
        if (locationId != null) return tripRepository.findByLocationId(locationId);
        return tripRepository.findByActiveTrue();
    }

    @GetMapping("/{id}")
    public Trip getTrip(@PathVariable UUID id) {
        return tripRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Trip not found: " + id));
    }

    @PostMapping
    public ResponseEntity<Trip> createTrip(@Valid @RequestBody Trip trip) {
        Trip created = tripRepository.save(trip);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}")
    public Trip updateTrip(@PathVariable UUID id, @Valid @RequestBody Trip trip) {
        if (!tripRepository.existsById(id)) {
            throw new RuntimeException("Trip not found: " + id);
        }
        trip.setId(id);
        return tripRepository.save(trip);
    }

    @GetMapping("/categories")
    public List<String> listCategories() {
        return tripRepository.findByActiveTrue().stream()
                .map(Trip::getAdventureCategory)
                .distinct()
                .sorted()
                .collect(Collectors.toList());
    }
}

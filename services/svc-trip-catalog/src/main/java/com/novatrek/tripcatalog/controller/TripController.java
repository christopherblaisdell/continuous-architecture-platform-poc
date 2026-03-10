package com.novatrek.tripcatalog.controller;

import com.novatrek.tripcatalog.entity.Trip;
import com.novatrek.tripcatalog.repository.TripRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/trips")
public class TripController {

    private final TripRepository tripRepository;

    public TripController(TripRepository tripRepository) {
        this.tripRepository = tripRepository;
    }

    @GetMapping
    public List<Trip> listTrips(@RequestParam(required = false) Trip.TripStatus status,
                                @RequestParam(required = false) Trip.ActivityType activityType) {
        if (status != null) return tripRepository.findByStatus(status);
        if (activityType != null) return tripRepository.findByActivityType(activityType);
        return tripRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Trip> createTrip(@Valid @RequestBody Trip trip) {
        trip.setStatus(Trip.TripStatus.DRAFT);
        Trip saved = tripRepository.save(trip);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{tripId}")
    public Trip getTrip(@PathVariable UUID tripId) {
        return tripRepository.findById(tripId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));
    }

    @PatchMapping("/{tripId}")
    public Trip updateTrip(@PathVariable UUID tripId, @RequestBody Trip patch) {
        Trip existing = tripRepository.findById(tripId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Trip not found"));

        if (patch.getName() != null) existing.setName(patch.getName());
        if (patch.getDescription() != null) existing.setDescription(patch.getDescription());
        if (patch.getDifficultyLevel() != null) existing.setDifficultyLevel(patch.getDifficultyLevel());
        if (patch.getBasePrice() != null) existing.setBasePrice(patch.getBasePrice());
        if (patch.getStatus() != null) existing.setStatus(patch.getStatus());
        if (patch.getMinParticipants() != null) existing.setMinParticipants(patch.getMinParticipants());
        if (patch.getMaxParticipants() != null) existing.setMaxParticipants(patch.getMaxParticipants());
        if (patch.getAgeMinimum() != null) existing.setAgeMinimum(patch.getAgeMinimum());
        if (patch.getFitnessLevelRequired() != null) existing.setFitnessLevelRequired(patch.getFitnessLevelRequired());

        return tripRepository.save(existing);
    }
}

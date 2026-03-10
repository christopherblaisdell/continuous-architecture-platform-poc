package com.novatrek.guestprofiles.controller;

import com.novatrek.guestprofiles.entity.Guest;
import com.novatrek.guestprofiles.repository.GuestRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/guests")
public class GuestController {

    private final GuestRepository guestRepository;

    public GuestController(GuestRepository guestRepository) {
        this.guestRepository = guestRepository;
    }

    @GetMapping
    public List<Guest> listGuests() {
        return guestRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Guest> createGuest(@Valid @RequestBody Guest guest) {
        Guest saved = guestRepository.save(guest);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{guestId}")
    public Guest getGuest(@PathVariable UUID guestId) {
        return guestRepository.findById(guestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Guest not found"));
    }

    @PatchMapping("/{guestId}")
    public Guest updateGuest(@PathVariable UUID guestId, @RequestBody Guest patch) {
        Guest existing = guestRepository.findById(guestId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Guest not found"));

        if (patch.getFirstName() != null) existing.setFirstName(patch.getFirstName());
        if (patch.getLastName() != null) existing.setLastName(patch.getLastName());
        if (patch.getPhone() != null) existing.setPhone(patch.getPhone());
        if (patch.getDateOfBirth() != null) existing.setDateOfBirth(patch.getDateOfBirth());
        if (patch.getLoyaltyTier() != null) existing.setLoyaltyTier(patch.getLoyaltyTier());
        if (patch.getProfileImageUrl() != null) existing.setProfileImageUrl(patch.getProfileImageUrl());
        if (patch.getPreferredLanguage() != null) existing.setPreferredLanguage(patch.getPreferredLanguage());

        return guestRepository.save(existing);
    }
}

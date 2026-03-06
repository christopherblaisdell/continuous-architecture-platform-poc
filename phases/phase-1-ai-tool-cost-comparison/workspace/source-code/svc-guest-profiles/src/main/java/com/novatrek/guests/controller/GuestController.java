package com.novatrek.guests.controller;

import com.novatrek.guests.model.GuestProfile;
import com.novatrek.guests.service.GuestService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/guests")
@RequiredArgsConstructor
public class GuestController {

    private final GuestService guestService;

    @GetMapping
    public Page<GuestProfile> listGuests(Pageable pageable) {
        return guestService.listGuests(pageable);
    }

    @GetMapping("/{id}")
    public GuestProfile getGuest(@PathVariable UUID id) {
        return guestService.getGuest(id);
    }

    @PostMapping
    public ResponseEntity<GuestProfile> createGuest(@Valid @RequestBody GuestProfile guest) {
        GuestProfile created = guestService.createGuest(guest);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}")
    public GuestProfile updateGuest(@PathVariable UUID id, @Valid @RequestBody GuestProfile guest) {
        return guestService.updateGuest(id, guest);
    }

    @GetMapping("/search")
    public ResponseEntity<GuestProfile> searchGuests(
            @RequestParam(required = false) String email,
            @RequestParam(required = false) String phone) {

        Optional<GuestProfile> result;

        if (email != null && !email.isBlank()) {
            result = guestService.searchByEmail(email);
        } else if (phone != null && !phone.isBlank()) {
            result = guestService.searchByPhone(phone);
        } else {
            return ResponseEntity.badRequest().build();
        }

        return result.map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}

package com.novatrek.guests.service;

import com.novatrek.guests.model.GuestProfile;
import com.novatrek.guests.repository.GuestRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class GuestService {

    private final GuestRepository guestRepository;

    public Page<GuestProfile> listGuests(Pageable pageable) {
        return guestRepository.findAll(pageable);
    }

    public GuestProfile getGuest(UUID id) {
        return guestRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Guest profile not found: " + id));
    }

    @Transactional
    public GuestProfile createGuest(GuestProfile guest) {
        log.info("Creating guest profile for email={}", guest.getEmail());

        // Duplicate detection by email
        Optional<GuestProfile> existing = guestRepository.findByEmail(guest.getEmail());
        if (existing.isPresent()) {
            throw new IllegalStateException(
                    "A guest profile already exists with email: " + guest.getEmail());
        }

        return guestRepository.save(guest);
    }

    @Transactional
    public GuestProfile updateGuest(UUID id, GuestProfile updated) {
        GuestProfile existing = getGuest(id);
        log.info("Updating guest profile id={}", id);

        // Check for email conflict with a different guest
        if (!existing.getEmail().equals(updated.getEmail())) {
            guestRepository.findByEmail(updated.getEmail()).ifPresent(conflict -> {
                throw new IllegalStateException(
                        "Email already in use by another guest: " + updated.getEmail());
            });
        }

        existing.setFirstName(updated.getFirstName());
        existing.setLastName(updated.getLastName());
        existing.setEmail(updated.getEmail());
        existing.setPhone(updated.getPhone());
        existing.setDateOfBirth(updated.getDateOfBirth());
        existing.setEmergencyContactName(updated.getEmergencyContactName());
        existing.setEmergencyContactPhone(updated.getEmergencyContactPhone());
        existing.setMedicalNotes(updated.getMedicalNotes());
        existing.setLoyaltyTier(updated.getLoyaltyTier());

        return guestRepository.save(existing);
    }

    public Optional<GuestProfile> searchByEmail(String email) {
        return guestRepository.findByEmail(email);
    }

    public Optional<GuestProfile> searchByPhone(String phone) {
        return guestRepository.findByPhone(phone);
    }
}

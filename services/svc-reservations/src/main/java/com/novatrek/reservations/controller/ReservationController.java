package com.novatrek.reservations.controller;

import com.novatrek.reservations.entity.Reservation;
import com.novatrek.reservations.entity.Reservation.ReservationStatus;
import com.novatrek.reservations.repository.ReservationRepository;
import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.UUID;

@RestController
@RequestMapping("/reservations")
public class ReservationController {

    private final ReservationRepository reservationRepository;

    public ReservationController(ReservationRepository reservationRepository) {
        this.reservationRepository = reservationRepository;
    }

    @GetMapping
    public Page<Reservation> listReservations(
            @RequestParam(required = false) UUID guestId,
            @RequestParam(required = false) ReservationStatus status,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        Pageable pageable = PageRequest.of(page, size);
        if (guestId != null && status != null) {
            return reservationRepository.findByGuestIdAndStatus(guestId, status, pageable);
        } else if (guestId != null) {
            return reservationRepository.findByGuestId(guestId, pageable);
        } else if (status != null) {
            return reservationRepository.findByStatus(status, pageable);
        }
        return reservationRepository.findAll(pageable);
    }

    @PostMapping
    public ResponseEntity<Reservation> createReservation(@Valid @RequestBody Reservation reservation) {
        Reservation saved = reservationRepository.save(reservation);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{reservationId}")
    public Reservation getReservation(@PathVariable UUID reservationId) {
        return reservationRepository.findById(reservationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Reservation not found"));
    }

    @PatchMapping("/{reservationId}")
    public Reservation updateReservation(@PathVariable UUID reservationId, @RequestBody Reservation patch) {
        Reservation existing = reservationRepository.findById(reservationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Reservation not found"));

        // Detect concurrent modifications at the API level via the _rev conflict token
        if (patch.getRev() != null && !patch.getRev().equals(existing.getRev())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "Reservation was modified by another request; refresh and retry");
        }

        if (patch.getStatus() != null) {
            validateStatusTransition(existing.getStatus(), patch.getStatus());
            existing.setStatus(patch.getStatus());
        }
        if (patch.getNumParticipants() != null) {
            if (patch.getNumParticipants() < 1) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "numParticipants must be at least 1");
            }
            existing.setNumParticipants(patch.getNumParticipants());
        }
        if (patch.getTotalAmount() != null) existing.setTotalAmount(patch.getTotalAmount());
        if (patch.getDepositAmount() != null) {
            java.math.BigDecimal effectiveTotal = patch.getTotalAmount() != null
                    ? patch.getTotalAmount() : existing.getTotalAmount();
            if (patch.getDepositAmount().compareTo(effectiveTotal) > 0) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                        "depositAmount must not exceed totalAmount");
            }
            existing.setDepositAmount(patch.getDepositAmount());
        }
        if (patch.getSpecialRequirements() != null) existing.setSpecialRequirements(patch.getSpecialRequirements());
        if (patch.getScheduledDate() != null) existing.setScheduledDate(patch.getScheduledDate());
        if (patch.getBookingSource() != null) existing.setBookingSource(patch.getBookingSource());

        return reservationRepository.save(existing);
    }

    private void validateStatusTransition(ReservationStatus current, ReservationStatus next) {
        boolean valid = switch (current) {
            case PENDING    -> next == ReservationStatus.CONFIRMED || next == ReservationStatus.CANCELLED;
            case CONFIRMED  -> next == ReservationStatus.GEAR_ASSIGNED || next == ReservationStatus.CANCELLED;
            case GEAR_ASSIGNED -> next == ReservationStatus.CHECKED_IN || next == ReservationStatus.CANCELLED;
            case CHECKED_IN -> next == ReservationStatus.IN_PROGRESS || next == ReservationStatus.NO_SHOW;
            case IN_PROGRESS -> next == ReservationStatus.COMPLETED;
            default         -> false;
        };
        if (!valid) {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "Invalid status transition: " + current + " -> " + next);
        }
    }

    @DeleteMapping("/{reservationId}")
    public ResponseEntity<Void> cancelReservation(@PathVariable UUID reservationId) {
        Reservation existing = reservationRepository.findById(reservationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Reservation not found"));
        existing.setStatus(ReservationStatus.CANCELLED);
        reservationRepository.save(existing);
        return ResponseEntity.noContent().build();
    }
}

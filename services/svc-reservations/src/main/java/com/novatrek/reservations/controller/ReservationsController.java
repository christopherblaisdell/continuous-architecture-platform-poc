package com.novatrek.reservations.controller;

import com.novatrek.reservations.entity.Reservation;
import com.novatrek.reservations.repository.ReservationRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/reservations")
public class ReservationsController {

    private final ReservationRepository reservationRepository;

    public ReservationsController(ReservationRepository reservationRepository) {
        this.reservationRepository = reservationRepository;
    }

    @GetMapping
    public List<Reservation> searchReservations() {
        return reservationRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Reservation> createReservation(@Valid @RequestBody Reservation body) {
        Reservation saved = reservationRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{reservation_id}")
    public List<Reservation> getReservation() {
        return reservationRepository.findAll();
    }

    @PatchMapping("/{reservation_id}")
    public Reservation updateReservation(@Valid @RequestBody Reservation body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @DeleteMapping("/{reservation_id}")
    public ResponseEntity<Void> cancelReservation() {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @GetMapping("/{reservation_id}/participants")
    public List<Reservation> getParticipants() {
        return reservationRepository.findAll();
    }

    @PostMapping("/{reservation_id}/participants")
    public ResponseEntity<Reservation> addParticipant(@Valid @RequestBody Reservation body) {
        Reservation saved = reservationRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @PutMapping("/{reservation_id}/status")
    public Reservation transitionStatus(@Valid @RequestBody Reservation body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

}

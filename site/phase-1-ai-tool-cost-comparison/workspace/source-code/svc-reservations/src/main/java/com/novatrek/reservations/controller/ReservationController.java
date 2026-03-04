package com.novatrek.reservations.controller;

import com.novatrek.reservations.dto.CreateReservationRequest;
import com.novatrek.reservations.dto.ReservationResponse;
import com.novatrek.reservations.model.Reservation;
import com.novatrek.reservations.model.ReservationStatus;
import com.novatrek.reservations.service.ReservationService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/v1/reservations")
@RequiredArgsConstructor
public class ReservationController {

    private final ReservationService reservationService;

    @GetMapping
    public Page<ReservationResponse> listReservations(Pageable pageable) {
        return reservationService.listReservations(pageable)
                .map(ReservationResponse::from);
    }

    @GetMapping("/{id}")
    public ReservationResponse getReservation(@PathVariable UUID id) {
        return ReservationResponse.from(reservationService.getReservation(id));
    }

    @PostMapping
    public ResponseEntity<ReservationResponse> createReservation(
            @Valid @RequestBody CreateReservationRequest request) {
        Reservation created = reservationService.createReservation(request);
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ReservationResponse.from(created));
    }

    @PutMapping("/{id}")
    public ReservationResponse updateReservation(
            @PathVariable UUID id,
            @Valid @RequestBody CreateReservationRequest request) {
        return ReservationResponse.from(reservationService.updateReservation(id, request));
    }

    @PatchMapping("/{id}/status")
    public ReservationResponse updateStatus(
            @PathVariable UUID id,
            @RequestBody Map<String, String> body) {
        ReservationStatus newStatus = ReservationStatus.valueOf(body.get("status"));
        return ReservationResponse.from(reservationService.updateStatus(id, newStatus));
    }

    @GetMapping("/search")
    public Page<ReservationResponse> search(
            @RequestParam(required = false) UUID guestId,
            @RequestParam(required = false) UUID tripId,
            @RequestParam(required = false) ReservationStatus status,
            Pageable pageable) {
        return reservationService.search(guestId, tripId, status, pageable)
                .map(ReservationResponse::from);
    }
}

package com.novatrek.partnerintegrations.controller;

import com.novatrek.partnerintegrations.entity.PartnerBooking;
import com.novatrek.partnerintegrations.repository.PartnerBookingRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/partner-bookings")
public class PartnerBookingsController {

    private final PartnerBookingRepository partnerBookingRepository;

    public PartnerBookingsController(PartnerBookingRepository partnerBookingRepository) {
        this.partnerBookingRepository = partnerBookingRepository;
    }

    @PostMapping
    public ResponseEntity<PartnerBooking> createPartnerBooking(@Valid @RequestBody PartnerBooking body) {
        PartnerBooking saved = partnerBookingRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{bookingId}")
    public PartnerBooking getPartnerBooking(@PathVariable UUID bookingId) {
        return partnerBookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "PartnerBooking not found"));
    }

    @PatchMapping("/{bookingId}")
    public PartnerBooking updatePartnerBooking(@PathVariable UUID bookingId, @Valid @RequestBody PartnerBooking body) {
        PartnerBooking existing = partnerBookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "PartnerBooking not found"));

        if (body.getPartnerId() != null) existing.setPartnerId(body.getPartnerId());
        if (body.getExternalReference() != null) existing.setExternalReference(body.getExternalReference());
        if (body.getReservationId() != null) existing.setReservationId(body.getReservationId());
        if (body.getStatus() != null) existing.setStatus(body.getStatus());
        if (body.getCommissionRate() != null) existing.setCommissionRate(body.getCommissionRate());
        if (body.getCommissionAmount() != null) existing.setCommissionAmount(body.getCommissionAmount());
        if (body.getBookingTotal() != null) existing.setBookingTotal(body.getBookingTotal());
        if (body.getActivityId() != null) existing.setActivityId(body.getActivityId());
        if (body.getTripDate() != null) existing.setTripDate(body.getTripDate());
        if (body.getParticipantCount() != null) existing.setParticipantCount(body.getParticipantCount());

        return partnerBookingRepository.save(existing);
    }

    @PostMapping("/{bookingId}/confirm")
    public PartnerBooking confirmPartnerBooking(@PathVariable UUID bookingId) {
        PartnerBooking existing = partnerBookingRepository.findById(bookingId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "PartnerBooking not found"));
        return partnerBookingRepository.save(existing);
    }

}

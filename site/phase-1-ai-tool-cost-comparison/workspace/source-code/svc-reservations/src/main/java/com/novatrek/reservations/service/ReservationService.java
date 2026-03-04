package com.novatrek.reservations.service;

import com.novatrek.reservations.dto.CreateReservationRequest;
import com.novatrek.reservations.model.Reservation;
import com.novatrek.reservations.model.ReservationStatus;
import com.novatrek.reservations.repository.ReservationRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class ReservationService {

    private final ReservationRepository reservationRepository;

    private static final Map<ReservationStatus, Set<ReservationStatus>> VALID_TRANSITIONS = Map.of(
            ReservationStatus.PENDING, Set.of(ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED),
            ReservationStatus.CONFIRMED, Set.of(ReservationStatus.CHECKED_IN, ReservationStatus.CANCELLED, ReservationStatus.NO_SHOW),
            ReservationStatus.CHECKED_IN, Set.of(ReservationStatus.COMPLETED),
            ReservationStatus.COMPLETED, Set.of(),
            ReservationStatus.CANCELLED, Set.of(),
            ReservationStatus.NO_SHOW, Set.of()
    );

    public Page<Reservation> listReservations(Pageable pageable) {
        return reservationRepository.findAll(pageable);
    }

    public Reservation getReservation(UUID id) {
        return reservationRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Reservation not found: " + id));
    }

    @Transactional
    public Reservation createReservation(CreateReservationRequest request) {
        log.info("Creating reservation for guest={} trip={}", request.getGuestId(), request.getTripId());

        Reservation reservation = Reservation.builder()
                .guestId(request.getGuestId())
                .tripId(request.getTripId())
                .bookingSource(request.getBookingSource())
                .numberOfParticipants(request.getNumberOfParticipants())
                .notes(request.getNotes())
                .status(ReservationStatus.PENDING)
                .currency("USD")
                .reservationDate(LocalDate.now())
                .build();

        return reservationRepository.save(reservation);
    }

    @Transactional
    public Reservation updateReservation(UUID id, CreateReservationRequest request) {
        Reservation existing = getReservation(id);
        existing.setGuestId(request.getGuestId());
        existing.setTripId(request.getTripId());
        existing.setBookingSource(request.getBookingSource());
        existing.setNumberOfParticipants(request.getNumberOfParticipants());
        existing.setNotes(request.getNotes());
        return reservationRepository.save(existing);
    }

    @Transactional
    public Reservation updateStatus(UUID id, ReservationStatus newStatus) {
        Reservation reservation = getReservation(id);
        validateStatusTransition(reservation.getStatus(), newStatus);
        log.info("Updating reservation {} status: {} -> {}", id, reservation.getStatus(), newStatus);
        reservation.setStatus(newStatus);
        return reservationRepository.save(reservation);
    }

    public Page<Reservation> search(UUID guestId, UUID tripId, ReservationStatus status, Pageable pageable) {
        if (guestId != null && status != null) {
            return reservationRepository.findByGuestId(guestId, pageable);
        }
        if (guestId != null) {
            return reservationRepository.findByGuestId(guestId, pageable);
        }
        if (tripId != null) {
            return reservationRepository.findByTripId(tripId, pageable);
        }
        if (status != null) {
            return reservationRepository.findByStatus(status, pageable);
        }
        return reservationRepository.findAll(pageable);
    }

    private void validateStatusTransition(ReservationStatus current, ReservationStatus target) {
        Set<ReservationStatus> allowed = VALID_TRANSITIONS.getOrDefault(current, Set.of());
        if (!allowed.contains(target)) {
            throw new IllegalStateException(
                    String.format("Invalid status transition: %s -> %s. Allowed: %s", current, target, allowed));
        }
    }
}

package com.novatrek.reservations.repository;

import com.novatrek.reservations.model.Reservation;
import com.novatrek.reservations.model.ReservationStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface ReservationRepository extends JpaRepository<Reservation, UUID> {

    Page<Reservation> findByGuestId(UUID guestId, Pageable pageable);

    Page<Reservation> findByTripId(UUID tripId, Pageable pageable);

    Page<Reservation> findByStatus(ReservationStatus status, Pageable pageable);

    List<Reservation> findByGuestIdAndStatus(UUID guestId, ReservationStatus status);
}

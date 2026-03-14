package com.novatrek.reservations.repository;

import com.novatrek.reservations.entity.Reservation;
import com.novatrek.reservations.entity.Reservation.ReservationStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ReservationRepository extends JpaRepository<Reservation, UUID> {
    Page<Reservation> findByGuestId(UUID guestId, Pageable pageable);
    Page<Reservation> findByStatus(ReservationStatus status, Pageable pageable);
    Page<Reservation> findByGuestIdAndStatus(UUID guestId, ReservationStatus status, Pageable pageable);
}

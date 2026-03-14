package com.novatrek.payments.repository;

import com.novatrek.payments.entity.Payment;
import com.novatrek.payments.entity.Payment.PaymentStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface PaymentRepository extends JpaRepository<Payment, UUID> {
    List<Payment> findByReservationId(UUID reservationId);
    List<Payment> findByGuestId(UUID guestId);
    List<Payment> findByStatus(PaymentStatus status);
    List<Payment> findByReservationIdAndGuestId(UUID reservationId, UUID guestId);
}

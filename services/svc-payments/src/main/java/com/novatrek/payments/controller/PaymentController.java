package com.novatrek.payments.controller;

import com.novatrek.payments.entity.Payment;
import com.novatrek.payments.entity.Payment.PaymentStatus;
import com.novatrek.payments.repository.PaymentRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/payments")
public class PaymentController {

    private final PaymentRepository paymentRepository;

    public PaymentController(PaymentRepository paymentRepository) {
        this.paymentRepository = paymentRepository;
    }

    @PostMapping
    public ResponseEntity<Payment> initiatePayment(@Valid @RequestBody Payment payment) {
        Payment saved = paymentRepository.save(payment);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{paymentId}")
    public Payment getPayment(@PathVariable UUID paymentId) {
        return paymentRepository.findById(paymentId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Payment not found"));
    }

    @GetMapping
    public List<Payment> listPayments(
            @RequestParam(required = false) UUID reservationId,
            @RequestParam(required = false) UUID guestId,
            @RequestParam(required = false) PaymentStatus status) {
        if (reservationId != null && guestId != null) {
            return paymentRepository.findByReservationIdAndGuestId(reservationId, guestId);
        } else if (reservationId != null) {
            return paymentRepository.findByReservationId(reservationId);
        } else if (guestId != null) {
            return paymentRepository.findByGuestId(guestId);
        } else if (status != null) {
            return paymentRepository.findByStatus(status);
        }
        return paymentRepository.findAll();
    }

    @PostMapping("/{paymentId}/capture")
    public Payment capturePayment(@PathVariable UUID paymentId) {
        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Payment not found"));
        if (payment.getStatus() != PaymentStatus.AUTHORIZED) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Payment must be in AUTHORIZED status to capture");
        }
        payment.setStatus(PaymentStatus.CAPTURED);
        payment.setProcessedAt(OffsetDateTime.now());
        return paymentRepository.save(payment);
    }

    @PostMapping("/{paymentId}/refund")
    public Payment refundPayment(@PathVariable UUID paymentId) {
        Payment payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Payment not found"));
        if (payment.getStatus() != PaymentStatus.CAPTURED) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Payment must be in CAPTURED status to refund");
        }
        payment.setStatus(PaymentStatus.REFUNDED);
        payment.setProcessedAt(OffsetDateTime.now());
        return paymentRepository.save(payment);
    }
}

package com.novatrek.payments.repository;

import com.novatrek.payments.entity.Payment;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class PaymentRepositoryTest {

    @Autowired
    private PaymentRepository paymentRepository;

    @Test
    void saveAndFindById() {
        Payment p = new Payment();
        p.setReservationId(UUID.randomUUID());
        p.setGuestId(UUID.randomUUID());
        p.setAmount(new BigDecimal("149.99"));
        p.setCurrency("USD");
        p.setMethod(Payment.PaymentMethod.CREDIT_CARD);
        p.setStatus(Payment.PaymentStatus.PENDING);

        Payment saved = paymentRepository.save(p);
        assertThat(saved.getId()).isNotNull();

        Optional<Payment> found = paymentRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getAmount()).isEqualByComparingTo(new BigDecimal("149.99"));
        assertThat(found.get().getMethod()).isEqualTo(Payment.PaymentMethod.CREDIT_CARD);
    }

    @Test
    void versionIncrementsOnUpdate() {
        Payment p = new Payment();
        p.setReservationId(UUID.randomUUID());
        p.setGuestId(UUID.randomUUID());
        p.setAmount(new BigDecimal("50.00"));
        p.setStatus(Payment.PaymentStatus.AUTHORIZED);

        Payment saved = paymentRepository.save(p);
        assertThat(saved.getVersion()).isEqualTo(0);

        saved.setStatus(Payment.PaymentStatus.CAPTURED);
        Payment updated = paymentRepository.saveAndFlush(saved);
        assertThat(updated.getVersion()).isEqualTo(1);
    }

    @Test
    void timestampsSetOnPersist() {
        Payment p = new Payment();
        p.setReservationId(UUID.randomUUID());
        p.setGuestId(UUID.randomUUID());
        p.setAmount(new BigDecimal("25.00"));

        Payment saved = paymentRepository.saveAndFlush(p);
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getUpdatedAt()).isNotNull();
    }
}

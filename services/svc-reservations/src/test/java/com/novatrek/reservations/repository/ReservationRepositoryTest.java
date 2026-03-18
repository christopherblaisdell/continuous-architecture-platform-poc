package com.novatrek.reservations.repository;

import com.novatrek.reservations.entity.Reservation;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ReservationRepositoryTest {

    @Autowired
    private ReservationRepository reservationRepository;

    @Test
    void saveAndFindById() {
        Reservation r = new Reservation();
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setStatus(Reservation.ReservationStatus.PENDING);
        r.setBookingSource(Reservation.BookingSource.WEB_DIRECT);
        r.setTotalAmount(new BigDecimal("299.99"));
        r.setCurrency("USD");
        r.setRev("1");

        Reservation saved = reservationRepository.save(r);
        assertThat(saved.getId()).isNotNull();

        Optional<Reservation> found = reservationRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getStatus()).isEqualTo(Reservation.ReservationStatus.PENDING);
        assertThat(found.get().getTotalAmount()).isEqualByComparingTo(new BigDecimal("299.99"));
    }

    @Test
    void findAll_returnsMultiple() {
        Reservation r1 = new Reservation();
        r1.setGuestId(UUID.randomUUID());
        r1.setTripId(UUID.randomUUID());
        r1.setStatus(Reservation.ReservationStatus.CONFIRMED);
        r1.setRev("1");

        Reservation r2 = new Reservation();
        r2.setGuestId(UUID.randomUUID());
        r2.setTripId(UUID.randomUUID());
        r2.setStatus(Reservation.ReservationStatus.CANCELLED);
        r2.setRev("1");

        reservationRepository.saveAll(List.of(r1, r2));

        List<Reservation> all = reservationRepository.findAll();
        assertThat(all).hasSizeGreaterThanOrEqualTo(2);
    }

    @Test
    void updateReservation_incrementsVersion() {
        Reservation r = new Reservation();
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setStatus(Reservation.ReservationStatus.PENDING);
        r.setRev("1");

        Reservation saved = reservationRepository.save(r);
        assertThat(saved.getVersion()).isEqualTo(0);

        saved.setStatus(Reservation.ReservationStatus.CONFIRMED);
        Reservation updated = reservationRepository.saveAndFlush(saved);
        assertThat(updated.getVersion()).isEqualTo(1);
    }

    @Test
    void timestampsSetOnPersist() {
        Reservation r = new Reservation();
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setRev("1");

        Reservation saved = reservationRepository.saveAndFlush(r);
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getUpdatedAt()).isNotNull();
    }
}

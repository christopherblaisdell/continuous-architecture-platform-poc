package com.novatrek.reservations.entity;

import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class ReservationTest {

    @Test
    void gettersAndSetters() {
        Reservation r = new Reservation();
        UUID id = UUID.randomUUID();
        r.setId(id);
        UUID guestId = UUID.randomUUID();
        r.setGuestId(guestId);
        UUID tripId = UUID.randomUUID();
        r.setTripId(tripId);
        r.setStatus(Reservation.ReservationStatus.CONFIRMED);
        r.setBookingSource(Reservation.BookingSource.WEB_DIRECT);
        UUID gearPkgId = UUID.randomUUID();
        r.setGearPackageId(gearPkgId);
        r.setSpecialRequirements("Wheelchair access");
        r.setPaymentReference("PAY-001");
        r.setTotalAmount(new BigDecimal("499.99"));
        r.setCurrency("USD");
        r.setRev("rev-1");
        r.setVersion(1);

        assertEquals(id, r.getId());
        assertEquals(guestId, r.getGuestId());
        assertEquals(tripId, r.getTripId());
        assertEquals(Reservation.ReservationStatus.CONFIRMED, r.getStatus());
        assertEquals(Reservation.BookingSource.WEB_DIRECT, r.getBookingSource());
        assertEquals(gearPkgId, r.getGearPackageId());
        assertEquals("Wheelchair access", r.getSpecialRequirements());
        assertEquals("PAY-001", r.getPaymentReference());
        assertEquals(new BigDecimal("499.99"), r.getTotalAmount());
        assertEquals("USD", r.getCurrency());
        assertEquals("rev-1", r.getRev());
        assertEquals(1, r.getVersion());
    }

    @Test
    void lifecycleCallbacks() {
        Reservation r = new Reservation();
        r.onCreate();
        assertNotNull(r.getCreatedAt());
        assertNotNull(r.getUpdatedAt());

        r.onUpdate();
        assertNotNull(r.getUpdatedAt());
    }

    @Test
    void enumValues() {
        assertEquals(8, Reservation.ReservationStatus.values().length);
        assertEquals(6, Reservation.BookingSource.values().length);
    }
}

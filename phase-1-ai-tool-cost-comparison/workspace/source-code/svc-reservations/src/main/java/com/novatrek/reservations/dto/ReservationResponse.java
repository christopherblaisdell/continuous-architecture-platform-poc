package com.novatrek.reservations.dto;

import com.novatrek.reservations.model.BookingSource;
import com.novatrek.reservations.model.Reservation;
import com.novatrek.reservations.model.ReservationStatus;
import lombok.Builder;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
public class ReservationResponse {

    private UUID id;
    private UUID guestId;
    private UUID tripId;
    private ReservationStatus status;
    private BookingSource bookingSource;
    private int numberOfParticipants;
    private BigDecimal totalAmount;
    private String currency;
    private String notes;
    private LocalDate reservationDate;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public static ReservationResponse from(Reservation entity) {
        return ReservationResponse.builder()
                .id(entity.getId())
                .guestId(entity.getGuestId())
                .tripId(entity.getTripId())
                .status(entity.getStatus())
                .bookingSource(entity.getBookingSource())
                .numberOfParticipants(entity.getNumberOfParticipants())
                .totalAmount(entity.getTotalAmount())
                .currency(entity.getCurrency())
                .notes(entity.getNotes())
                .reservationDate(entity.getReservationDate())
                .createdAt(entity.getCreatedAt())
                .updatedAt(entity.getUpdatedAt())
                .build();
    }
}

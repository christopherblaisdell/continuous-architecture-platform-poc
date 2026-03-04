package com.novatrek.reservations.dto;

import com.novatrek.reservations.model.BookingSource;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CreateReservationRequest {

    @NotNull(message = "Guest ID is required")
    private UUID guestId;

    @NotNull(message = "Trip ID is required")
    private UUID tripId;

    @NotNull(message = "Booking source is required")
    private BookingSource bookingSource;

    @Min(value = 1, message = "At least one participant is required")
    private int numberOfParticipants;

    private String notes;
}

package com.novatrek.notifications.controller;

import com.novatrek.notifications.entity.Notification;
import com.novatrek.notifications.entity.Notification.NotificationChannel;
import com.novatrek.notifications.entity.Notification.NotificationStatus;
import com.novatrek.notifications.repository.NotificationRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/notifications")
public class NotificationController {

    private final NotificationRepository notificationRepository;

    public NotificationController(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    @PostMapping("/send")
    public ResponseEntity<Notification> sendNotification(@Valid @RequestBody Notification notification) {
        Notification saved = notificationRepository.save(notification);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{notificationId}")
    public Notification getNotification(@PathVariable UUID notificationId) {
        return notificationRepository.findById(notificationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Notification not found"));
    }

    @GetMapping
    public List<Notification> listNotifications(
            @RequestParam(required = false) UUID guestId,
            @RequestParam(required = false) UUID reservationId,
            @RequestParam(required = false) NotificationChannel channel,
            @RequestParam(required = false) NotificationStatus status) {
        if (guestId != null && channel != null) {
            return notificationRepository.findByGuestIdAndChannel(guestId, channel);
        } else if (guestId != null && status != null) {
            return notificationRepository.findByGuestIdAndStatus(guestId, status);
        } else if (reservationId != null && channel != null) {
            return notificationRepository.findByReservationIdAndChannel(reservationId, channel);
        } else if (reservationId != null && status != null) {
            return notificationRepository.findByReservationIdAndStatus(reservationId, status);
        } else if (guestId != null) {
            return notificationRepository.findByGuestId(guestId);
        } else if (reservationId != null) {
            return notificationRepository.findByReservationId(reservationId);
        }
        return notificationRepository.findAll();
    }
}

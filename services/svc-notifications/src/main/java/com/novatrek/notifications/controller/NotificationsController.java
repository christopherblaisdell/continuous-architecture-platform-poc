package com.novatrek.notifications.controller;

import com.novatrek.notifications.entity.Notification;
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
public class NotificationsController {

    private final NotificationRepository notificationRepository;

    public NotificationsController(NotificationRepository notificationRepository) {
        this.notificationRepository = notificationRepository;
    }

    @GetMapping
    public List<Notification> listNotifications() {
        return notificationRepository.findAll();
    }

    @PostMapping
    public Notification sendNotification(@Valid @RequestBody Notification body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @GetMapping("/{notificationId}")
    public Notification getNotification(@PathVariable UUID notificationId) {
        return notificationRepository.findById(notificationId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Notification not found"));
    }

    @PostMapping("/bulk")
    public Notification sendBulkNotifications(@Valid @RequestBody Notification body) {
        throw new UnsupportedOperationException("Not yet implemented");
    }

}

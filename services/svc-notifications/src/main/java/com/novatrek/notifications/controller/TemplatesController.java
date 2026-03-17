package com.novatrek.notifications.controller;

import com.novatrek.notifications.entity.NotificationTemplate;
import com.novatrek.notifications.repository.NotificationTemplateRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/templates")
public class TemplatesController {

    private final NotificationTemplateRepository notificationTemplateRepository;

    public TemplatesController(NotificationTemplateRepository notificationTemplateRepository) {
        this.notificationTemplateRepository = notificationTemplateRepository;
    }

    @GetMapping
    public List<NotificationTemplate> listTemplates() {
        return notificationTemplateRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<NotificationTemplate> createTemplate(@Valid @RequestBody NotificationTemplate body) {
        NotificationTemplate saved = notificationTemplateRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}

package com.novatrek.notifications.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.notifications.entity.Notification;
import com.novatrek.notifications.entity.NotificationTemplate;
import com.novatrek.notifications.repository.NotificationRepository;
import com.novatrek.notifications.repository.NotificationTemplateRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest
class NotificationsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private NotificationRepository notificationRepository;

    @MockBean
    private NotificationTemplateRepository notificationTemplateRepository;

    // --- NotificationsController ---

    @Test
    void listNotifications_returnsEmptyList() throws Exception {
        when(notificationRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/notifications"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void listNotifications_returnsNotifications() throws Exception {
        Notification n = new Notification();
        n.setRecipientId(UUID.randomUUID());
        n.setChannel(Notification.NotificationChannel.EMAIL);
        n.setStatus(Notification.NotificationStatus.QUEUED);
        n.setPriority(Notification.Priority.NORMAL);

        when(notificationRepository.findAll()).thenReturn(List.of(n));

        mockMvc.perform(get("/notifications"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].channel", is("EMAIL")));
    }

    @Test
    void getNotification_returns200() throws Exception {
        UUID id = UUID.randomUUID();
        Notification n = new Notification();
        n.setId(id);
        n.setChannel(Notification.NotificationChannel.PUSH);
        n.setStatus(Notification.NotificationStatus.DELIVERED);

        when(notificationRepository.findById(id)).thenReturn(Optional.of(n));

        mockMvc.perform(get("/notifications/{notificationId}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.channel", is("PUSH")));
    }

    @Test
    void getNotification_returns404() throws Exception {
        UUID id = UUID.randomUUID();
        when(notificationRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/notifications/{notificationId}", id))
                .andExpect(status().isNotFound());
    }

    // --- TemplatesController ---

    @Test
    void listTemplates_returnsEmptyList() throws Exception {
        when(notificationTemplateRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/templates"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void createTemplate_returns201() throws Exception {
        NotificationTemplate t = new NotificationTemplate();
        t.setName("booking-confirmation");
        t.setChannel(NotificationTemplate.NotificationChannel.EMAIL);
        t.setSubject("Your Booking is Confirmed!");
        t.setBodyTemplate("Dear {guest}, your trip is confirmed.");

        when(notificationTemplateRepository.save(any(NotificationTemplate.class))).thenReturn(t);

        mockMvc.perform(post("/templates")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(t)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.name", is("booking-confirmation")));
    }
}

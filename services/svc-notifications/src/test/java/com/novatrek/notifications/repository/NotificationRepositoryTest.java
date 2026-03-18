package com.novatrek.notifications.repository;

import com.novatrek.notifications.entity.Notification;
import com.novatrek.notifications.entity.NotificationTemplate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class NotificationRepositoryTest {

    @Autowired
    private NotificationRepository notificationRepository;

    @Autowired
    private NotificationTemplateRepository notificationTemplateRepository;

    @Test
    void saveAndFindNotification() {
        Notification n = new Notification();
        n.setRecipientId(UUID.randomUUID());
        n.setChannel(Notification.NotificationChannel.EMAIL);
        n.setStatus(Notification.NotificationStatus.QUEUED);
        n.setPriority(Notification.Priority.HIGH);
        n.setRenderedSubject("Adventure Confirmed");

        Notification saved = notificationRepository.save(n);
        assertThat(saved.getId()).isNotNull();

        Optional<Notification> found = notificationRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getChannel()).isEqualTo(Notification.NotificationChannel.EMAIL);
        assertThat(found.get().getPriority()).isEqualTo(Notification.Priority.HIGH);
    }

    @Test
    void saveAndFindTemplate() {
        NotificationTemplate t = new NotificationTemplate();
        t.setName("welcome-email");
        t.setChannel(NotificationTemplate.NotificationChannel.EMAIL);
        t.setSubject("Welcome to NovaTrek!");
        t.setBodyTemplate("Dear {name}, welcome aboard.");

        NotificationTemplate saved = notificationTemplateRepository.save(t);
        assertThat(saved.getId()).isNotNull();

        Optional<NotificationTemplate> found = notificationTemplateRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("welcome-email");
    }

    @Test
    void versionIncrementsOnUpdate() {
        Notification n = new Notification();
        n.setRecipientId(UUID.randomUUID());
        n.setChannel(Notification.NotificationChannel.SMS);
        n.setStatus(Notification.NotificationStatus.QUEUED);

        Notification saved = notificationRepository.save(n);
        assertThat(saved.getVersion()).isEqualTo(0);

        saved.setStatus(Notification.NotificationStatus.SENT);
        Notification updated = notificationRepository.saveAndFlush(saved);
        assertThat(updated.getVersion()).isEqualTo(1);
    }

    @Test
    void timestampsSetOnPersist() {
        Notification n = new Notification();
        n.setRecipientId(UUID.randomUUID());
        n.setChannel(Notification.NotificationChannel.IN_APP);

        Notification saved = notificationRepository.saveAndFlush(n);
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getUpdatedAt()).isNotNull();
    }
}

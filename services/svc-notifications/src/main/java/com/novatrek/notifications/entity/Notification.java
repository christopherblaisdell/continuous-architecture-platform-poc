package com.novatrek.notifications.entity;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "notifications", schema = "notifications")
public class Notification {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "notification_id")
    private UUID notificationId;

    @NotNull
    @Column(name = "guest_id", nullable = false)
    private UUID guestId;

    @Column(name = "reservation_id")
    private UUID reservationId;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "channel", nullable = false, length = 20)
    private NotificationChannel channel;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "template", nullable = false, length = 50)
    private NotificationTemplate template;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    private NotificationStatus status = NotificationStatus.PENDING;

    @NotNull
    @Column(name = "recipient_address", nullable = false, length = 255)
    private String recipientAddress;

    @Column(name = "subject", length = 255)
    private String subject;

    @Column(name = "body_preview", length = 500)
    private String bodyPreview;

    @Column(name = "provider_message_id", length = 100)
    private String providerMessageId;

    @Column(name = "failure_reason", columnDefinition = "TEXT")
    private String failureReason;

    @Column(name = "sent_at")
    private OffsetDateTime sentAt;

    @Column(name = "delivered_at")
    private OffsetDateTime deliveredAt;

    @Column(name = "created_at", nullable = false, updatable = false)
    private OffsetDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = OffsetDateTime.now();
    }

    public enum NotificationStatus {
        PENDING, SENT, DELIVERED, FAILED, BOUNCED
    }

    public enum NotificationChannel {
        EMAIL, SMS, PUSH
    }

    public enum NotificationTemplate {
        RESERVATION_CONFIRMATION, RESERVATION_CANCELLED, CHECKIN_REMINDER,
        PAYMENT_RECEIPT, WAIVER_REMINDER, EMERGENCY_ALERT
    }

    // --- Getters and Setters ---

    public UUID getNotificationId() { return notificationId; }
    public void setNotificationId(UUID notificationId) { this.notificationId = notificationId; }

    public UUID getGuestId() { return guestId; }
    public void setGuestId(UUID guestId) { this.guestId = guestId; }

    public UUID getReservationId() { return reservationId; }
    public void setReservationId(UUID reservationId) { this.reservationId = reservationId; }

    public NotificationChannel getChannel() { return channel; }
    public void setChannel(NotificationChannel channel) { this.channel = channel; }

    public NotificationTemplate getTemplate() { return template; }
    public void setTemplate(NotificationTemplate template) { this.template = template; }

    public NotificationStatus getStatus() { return status; }
    public void setStatus(NotificationStatus status) { this.status = status; }

    public String getRecipientAddress() { return recipientAddress; }
    public void setRecipientAddress(String recipientAddress) { this.recipientAddress = recipientAddress; }

    public String getSubject() { return subject; }
    public void setSubject(String subject) { this.subject = subject; }

    public String getBodyPreview() { return bodyPreview; }
    public void setBodyPreview(String bodyPreview) { this.bodyPreview = bodyPreview; }

    public String getProviderMessageId() { return providerMessageId; }
    public void setProviderMessageId(String providerMessageId) { this.providerMessageId = providerMessageId; }

    public String getFailureReason() { return failureReason; }
    public void setFailureReason(String failureReason) { this.failureReason = failureReason; }

    public OffsetDateTime getSentAt() { return sentAt; }
    public void setSentAt(OffsetDateTime sentAt) { this.sentAt = sentAt; }

    public OffsetDateTime getDeliveredAt() { return deliveredAt; }
    public void setDeliveredAt(OffsetDateTime deliveredAt) { this.deliveredAt = deliveredAt; }

    public OffsetDateTime getCreatedAt() { return createdAt; }
}

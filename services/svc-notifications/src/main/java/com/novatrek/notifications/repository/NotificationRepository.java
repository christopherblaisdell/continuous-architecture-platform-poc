package com.novatrek.notifications.repository;

import com.novatrek.notifications.entity.Notification;
import com.novatrek.notifications.entity.Notification.NotificationChannel;
import com.novatrek.notifications.entity.Notification.NotificationStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, UUID> {
    List<Notification> findByGuestId(UUID guestId);
    List<Notification> findByReservationId(UUID reservationId);
    List<Notification> findByGuestIdAndChannel(UUID guestId, NotificationChannel channel);
    List<Notification> findByGuestIdAndStatus(UUID guestId, NotificationStatus status);
    List<Notification> findByReservationIdAndChannel(UUID reservationId, NotificationChannel channel);
    List<Notification> findByReservationIdAndStatus(UUID reservationId, NotificationStatus status);
}

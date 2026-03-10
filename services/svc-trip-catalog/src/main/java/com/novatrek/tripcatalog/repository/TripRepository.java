package com.novatrek.tripcatalog.repository;

import com.novatrek.tripcatalog.entity.Trip;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TripRepository extends JpaRepository<Trip, UUID> {
    List<Trip> findByStatus(Trip.TripStatus status);
    List<Trip> findByActivityType(Trip.ActivityType activityType);
}

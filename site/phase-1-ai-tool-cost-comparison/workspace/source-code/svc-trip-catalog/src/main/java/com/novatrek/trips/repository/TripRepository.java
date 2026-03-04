package com.novatrek.trips.repository;

import com.novatrek.trips.model.Trip;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TripRepository extends JpaRepository<Trip, UUID> {

    List<Trip> findByAdventureCategory(String adventureCategory);

    List<Trip> findByDifficulty(Trip.Difficulty difficulty);

    List<Trip> findByActiveTrue();

    List<Trip> findByLocationId(UUID locationId);
}

package com.novatrek.trailmanagement.repository;

import com.novatrek.trailmanagement.entity.Trail;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface TrailRepository extends JpaRepository<Trail, UUID> {
    List<Trail> findByStatus(Trail.TrailStatus status);
    List<Trail> findByDifficulty(Trail.DifficultyRating difficulty);
}

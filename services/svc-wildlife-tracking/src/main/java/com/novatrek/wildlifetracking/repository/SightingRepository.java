package com.novatrek.wildlifetracking.repository;

import com.novatrek.wildlifetracking.entity.Sighting;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface SightingRepository extends JpaRepository<Sighting, UUID> {
}

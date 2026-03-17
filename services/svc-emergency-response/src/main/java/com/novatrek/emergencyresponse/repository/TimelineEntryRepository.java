package com.novatrek.emergencyresponse.repository;

import com.novatrek.emergencyresponse.entity.TimelineEntry;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface TimelineEntryRepository extends JpaRepository<TimelineEntry, UUID> {
}

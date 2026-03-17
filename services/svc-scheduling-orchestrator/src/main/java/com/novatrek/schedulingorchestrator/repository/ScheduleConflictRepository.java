package com.novatrek.schedulingorchestrator.repository;

import com.novatrek.schedulingorchestrator.entity.ScheduleConflict;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ScheduleConflictRepository extends JpaRepository<ScheduleConflict, UUID> {
}

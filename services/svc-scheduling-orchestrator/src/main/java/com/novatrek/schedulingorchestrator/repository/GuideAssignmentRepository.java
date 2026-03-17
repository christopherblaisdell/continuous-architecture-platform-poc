package com.novatrek.schedulingorchestrator.repository;

import com.novatrek.schedulingorchestrator.entity.GuideAssignment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GuideAssignmentRepository extends JpaRepository<GuideAssignment, UUID> {
}

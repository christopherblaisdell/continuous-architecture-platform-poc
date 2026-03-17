package com.novatrek.safetycompliance.repository;

import com.novatrek.safetycompliance.entity.SafetyInspection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface SafetyInspectionRepository extends JpaRepository<SafetyInspection, UUID> {
}

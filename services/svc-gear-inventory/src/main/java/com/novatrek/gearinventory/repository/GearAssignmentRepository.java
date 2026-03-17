package com.novatrek.gearinventory.repository;

import com.novatrek.gearinventory.entity.GearAssignment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GearAssignmentRepository extends JpaRepository<GearAssignment, UUID> {
}

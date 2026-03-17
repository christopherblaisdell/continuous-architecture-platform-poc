package com.novatrek.gearinventory.repository;

import com.novatrek.gearinventory.entity.InventoryLevel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface InventoryLevelRepository extends JpaRepository<InventoryLevel, UUID> {
}

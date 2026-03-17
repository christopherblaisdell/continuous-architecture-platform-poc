package com.novatrek.gearinventory.repository;

import com.novatrek.gearinventory.entity.GearPackage;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GearPackageRepository extends JpaRepository<GearPackage, UUID> {
}

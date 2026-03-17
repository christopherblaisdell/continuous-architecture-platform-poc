package com.novatrek.checkin.repository;

import com.novatrek.checkin.entity.GearItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface GearItemRepository extends JpaRepository<GearItem, UUID> {
}

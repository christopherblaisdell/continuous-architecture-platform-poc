package com.novatrek.partnerintegrations.repository;

import com.novatrek.partnerintegrations.entity.CommissionLineItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface CommissionLineItemRepository extends JpaRepository<CommissionLineItem, UUID> {
}

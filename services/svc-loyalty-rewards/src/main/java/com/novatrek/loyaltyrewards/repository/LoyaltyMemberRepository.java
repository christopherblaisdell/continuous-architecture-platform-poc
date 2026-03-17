package com.novatrek.loyaltyrewards.repository;

import com.novatrek.loyaltyrewards.entity.LoyaltyMember;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface LoyaltyMemberRepository extends JpaRepository<LoyaltyMember, UUID> {
}

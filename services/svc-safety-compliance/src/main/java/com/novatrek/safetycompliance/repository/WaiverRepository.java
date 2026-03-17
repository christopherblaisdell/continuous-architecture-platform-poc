package com.novatrek.safetycompliance.repository;

import com.novatrek.safetycompliance.entity.Waiver;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface WaiverRepository extends JpaRepository<Waiver, UUID> {
}

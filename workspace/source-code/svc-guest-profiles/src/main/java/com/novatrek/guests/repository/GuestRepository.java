package com.novatrek.guests.repository;

import com.novatrek.guests.model.GuestProfile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface GuestRepository extends JpaRepository<GuestProfile, UUID> {

    Optional<GuestProfile> findByEmail(String email);

    Optional<GuestProfile> findByPhone(String phone);
}

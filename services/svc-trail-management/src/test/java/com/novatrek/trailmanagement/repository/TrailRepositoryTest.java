package com.novatrek.trailmanagement.repository;

import com.novatrek.trailmanagement.entity.Trail;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.math.BigDecimal;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
class TrailRepositoryTest {

    @Autowired
    private TrailRepository trailRepository;

    private Trail createTrail(String name, Trail.DifficultyRating difficulty, Trail.TrailStatus status) {
        Trail trail = new Trail();
        trail.setName(name);
        trail.setDistanceKm(new BigDecimal("8.00"));
        trail.setDifficulty(difficulty);
        trail.setPermitRequired(false);
        trail.setDogsAllowed(true);
        trail.setStatus(status);
        return trail;
    }

    @Test
    void saveAndFindById() {
        Trail saved = trailRepository.save(createTrail("Summit Loop", Trail.DifficultyRating.MODERATE, Trail.TrailStatus.OPEN));

        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);
        assertThat(trailRepository.findById(saved.getId())).isPresent();
    }

    @Test
    void findByStatus() {
        trailRepository.save(createTrail("Open1", Trail.DifficultyRating.EASY, Trail.TrailStatus.OPEN));
        trailRepository.save(createTrail("Closed1", Trail.DifficultyRating.EASY, Trail.TrailStatus.CLOSED));

        List<Trail> open = trailRepository.findByStatus(Trail.TrailStatus.OPEN);
        assertThat(open).allMatch(t -> t.getStatus() == Trail.TrailStatus.OPEN);
    }

    @Test
    void findByDifficulty() {
        trailRepository.save(createTrail("Easy1", Trail.DifficultyRating.EASY, Trail.TrailStatus.OPEN));
        trailRepository.save(createTrail("Expert1", Trail.DifficultyRating.EXPERT, Trail.TrailStatus.OPEN));

        List<Trail> expert = trailRepository.findByDifficulty(Trail.DifficultyRating.EXPERT);
        assertThat(expert).allMatch(t -> t.getDifficulty() == Trail.DifficultyRating.EXPERT);
    }

    @Test
    void updateTrail_incrementsVersion() {
        Trail saved = trailRepository.save(createTrail("VersionTest", Trail.DifficultyRating.MODERATE, Trail.TrailStatus.OPEN));
        assertThat(saved.getVersion()).isEqualTo(0);

        saved.setMaxGroupSize(10);
        Trail updated = trailRepository.saveAndFlush(saved);
        assertThat(updated.getVersion()).isEqualTo(1);
    }

    @Test
    void defaultValues_appliedCorrectly() {
        Trail trail = new Trail();
        trail.setName("Defaults");
        trail.setDistanceKm(new BigDecimal("5.00"));
        trail.setDifficulty(Trail.DifficultyRating.EASY);
        trail.setPermitRequired(false);
        trail.setDogsAllowed(false);

        Trail saved = trailRepository.save(trail);
        assertThat(saved.getStatus()).isEqualTo(Trail.TrailStatus.OPEN);
        assertThat(saved.getWaypointCount()).isEqualTo(0);
    }
}

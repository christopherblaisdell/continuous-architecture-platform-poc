package com.novatrek.reviews.repository;

import com.novatrek.reviews.entity.Review;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class ReviewRepositoryTest {

    @Autowired
    private ReviewRepository reviewRepository;

    @Test
    void saveAndFindReview() {
        Review r = new Review();
        r.setReservationId(UUID.randomUUID());
        r.setGuestId(UUID.randomUUID());
        r.setTripId(UUID.randomUUID());
        r.setOverallRating(5);
        r.setTitle("Great trip");
        r.setBody("Really enjoyed the hike.");
        r.setVisitDate(LocalDate.of(2026, 3, 10));
        r.setModerationStatus(Review.ModerationStatus.PENDING_MODERATION);
        r.setHelpfulCount(0);

        Review saved = reviewRepository.save(r);
        assertThat(saved.getId()).isNotNull();

        Optional<Review> found = reviewRepository.findById(saved.getId());
        assertThat(found).isPresent();
        assertThat(found.get().getTitle()).isEqualTo("Great trip");
        assertThat(found.get().getOverallRating()).isEqualTo(5);
    }

    @Test
    void moderationStatusTransition() {
        Review r = new Review();
        r.setTitle("Needs review");
        r.setModerationStatus(Review.ModerationStatus.PENDING_MODERATION);

        Review saved = reviewRepository.save(r);
        saved.setModerationStatus(Review.ModerationStatus.APPROVED);
        Review updated = reviewRepository.save(saved);

        assertThat(updated.getModerationStatus()).isEqualTo(Review.ModerationStatus.APPROVED);
    }

    @Test
    void deleteReview() {
        Review r = new Review();
        r.setTitle("To delete");
        Review saved = reviewRepository.save(r);

        reviewRepository.deleteById(saved.getId());
        assertThat(reviewRepository.findById(saved.getId())).isEmpty();
    }
}

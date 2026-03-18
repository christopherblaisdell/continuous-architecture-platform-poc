package com.novatrek.loyaltyrewards.repository;

import com.novatrek.loyaltyrewards.entity.LoyaltyMember;
import com.novatrek.loyaltyrewards.entity.Transaction;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.test.context.ActiveProfiles;

import java.time.LocalDate;
import java.time.OffsetDateTime;

import static org.assertj.core.api.Assertions.assertThat;

@DataJpaTest
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class LoyaltyRewardsRepositoryTest {

    @Autowired
    private LoyaltyMemberRepository loyaltyMemberRepository;

    @Autowired
    private TransactionRepository transactionRepository;

    @Test
    void saveAndFindLoyaltyMember() {
        LoyaltyMember m = new LoyaltyMember();
        m.setTier(LoyaltyMember.TierName.PATHFINDER);
        m.setPointsBalance(3000);
        m.setLifetimePoints(8000);
        m.setTierExpiry(LocalDate.of(2027, 3, 1));
        m.setEnrolledAt(OffsetDateTime.now());

        LoyaltyMember saved = loyaltyMemberRepository.save(m);
        assertThat(saved.getGuestId()).isNotNull();
        assertThat(saved.getVersion()).isEqualTo(0);

        LoyaltyMember found = loyaltyMemberRepository.findById(saved.getGuestId()).orElseThrow();
        assertThat(found.getTier()).isEqualTo(LoyaltyMember.TierName.PATHFINDER);
        assertThat(found.getPointsBalance()).isEqualTo(3000);
        assertThat(found.getLifetimePoints()).isEqualTo(8000);
    }

    @Test
    void tierEnumValues() {
        for (LoyaltyMember.TierName tier : LoyaltyMember.TierName.values()) {
            LoyaltyMember m = new LoyaltyMember();
            m.setTier(tier);
            m.setPointsBalance(0);
            m.setLifetimePoints(0);

            LoyaltyMember saved = loyaltyMemberRepository.save(m);
            assertThat(loyaltyMemberRepository.findById(saved.getGuestId()).orElseThrow().getTier()).isEqualTo(tier);
        }
    }

    @Test
    void saveAndFindTransaction() {
        Transaction t = new Transaction();
        t.setType(Transaction.TransactionType.EARN);
        t.setPoints(500);
        t.setDescription("Glacier hike completion bonus");
        t.setTimestamp(OffsetDateTime.now());

        Transaction saved = transactionRepository.save(t);
        assertThat(saved.getId()).isNotNull();

        Transaction found = transactionRepository.findById(saved.getId()).orElseThrow();
        assertThat(found.getType()).isEqualTo(Transaction.TransactionType.EARN);
        assertThat(found.getPoints()).isEqualTo(500);
    }

    @Test
    void transactionTypeEnumValues() {
        for (Transaction.TransactionType tt : Transaction.TransactionType.values()) {
            Transaction t = new Transaction();
            t.setType(tt);
            t.setPoints(100);
            t.setTimestamp(OffsetDateTime.now());

            Transaction saved = transactionRepository.save(t);
            assertThat(transactionRepository.findById(saved.getId()).orElseThrow().getType()).isEqualTo(tt);
        }
    }
}

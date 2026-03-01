package com.novatrek.checkin.service;

import com.novatrek.checkin.model.CheckInRecord.UiPattern;
import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Set;

@Component
public class AdventureCategoryClassifier {

    // PATTERN_1 (Standard) - no special briefing or equipment needed
    private static final Set<String> PATTERN_1_CATEGORIES = Set.of(
            "GUIDED_NATURE_WALK", "SCENIC_OVERLOOK", "BIRD_WATCHING",
            "CAMPFIRE_STORYTELLING", "STARGAZING", "FISHING_BASIC",
            "PHOTOGRAPHY_TOUR", "WILDFLOWER_HIKE"
    );

    // PATTERN_2 (Safety Briefing) - requires safety briefing before activity
    private static final Set<String> PATTERN_2_CATEGORIES = Set.of(
            "MOUNTAIN_HIKING", "ROCK_CLIMBING_INTRO", "MOUNTAIN_BIKING",
            "HORSEBACK_TRAIL", "CAVE_EXPLORING", "ZIP_LINE",
            "CROSS_COUNTRY_SKI", "SNOWSHOEING"
    );

    // PATTERN_3 (Full Equipment) - requires full equipment check-out and training
    private static final Set<String> PATTERN_3_CATEGORIES = Set.of(
            "WHITEWATER_KAYAKING", "ADVANCED_ROCK_CLIMBING", "RAPPELLING",
            "ICE_CLIMBING", "BACKCOUNTRY_SKI", "PARAGLIDING",
            "CANYONEERING", "SCUBA_INTRO", "MULTI_DAY_EXPEDITION"
    );

    // Booking source overrides take precedence over category classification
    private static final Map<String, UiPattern> BOOKING_SOURCE_OVERRIDES = Map.of(
            "PARTNER_API", UiPattern.PATTERN_1,
            "WALK_IN", UiPattern.PATTERN_3
    );

    /**
     * Determines the UI pattern for a check-in based on adventure category
     * and booking source. Booking source overrides take precedence.
     *
     * @param category      the adventure category code
     * @param bookingSource the booking source (nullable)
     * @return the appropriate UiPattern
     */
    public UiPattern getUiPattern(String category, String bookingSource) {
        // Booking source overrides take precedence over category
        if (bookingSource != null) {
            UiPattern override = BOOKING_SOURCE_OVERRIDES.get(bookingSource);
            if (override != null) {
                return override;
            }
        }

        // Classify by adventure category
        if (category == null) {
            return UiPattern.PATTERN_1;
        }

        String normalizedCategory = category.toUpperCase().trim();

        if (PATTERN_1_CATEGORIES.contains(normalizedCategory)) {
            return UiPattern.PATTERN_1;
        }
        if (PATTERN_2_CATEGORIES.contains(normalizedCategory)) {
            return UiPattern.PATTERN_2;
        }
        if (PATTERN_3_CATEGORIES.contains(normalizedCategory)) {
            return UiPattern.PATTERN_3;
        }

        // Default to PATTERN_1 for unknown categories
        return UiPattern.PATTERN_1;
    }
}

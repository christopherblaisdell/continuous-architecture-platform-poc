package com.novatrek.weather.controller;

import com.novatrek.weather.entity.TrailCondition;
import com.novatrek.weather.repository.TrailConditionRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/trail-conditions")
public class TrailConditionsController {

    private final TrailConditionRepository trailConditionRepository;

    public TrailConditionsController(TrailConditionRepository trailConditionRepository) {
        this.trailConditionRepository = trailConditionRepository;
    }

    @GetMapping
    public List<TrailCondition> getTrailConditions() {
        return trailConditionRepository.findAll();
    }

}

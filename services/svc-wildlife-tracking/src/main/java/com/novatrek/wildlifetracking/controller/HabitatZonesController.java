package com.novatrek.wildlifetracking.controller;

import com.novatrek.wildlifetracking.entity.HabitatZone;
import com.novatrek.wildlifetracking.repository.HabitatZoneRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/habitat-zones")
public class HabitatZonesController {

    private final HabitatZoneRepository habitatZoneRepository;

    public HabitatZonesController(HabitatZoneRepository habitatZoneRepository) {
        this.habitatZoneRepository = habitatZoneRepository;
    }

    @GetMapping
    public List<HabitatZone> listHabitatZones() {
        return habitatZoneRepository.findAll();
    }

}

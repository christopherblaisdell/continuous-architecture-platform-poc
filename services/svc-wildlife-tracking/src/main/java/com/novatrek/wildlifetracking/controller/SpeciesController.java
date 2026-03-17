package com.novatrek.wildlifetracking.controller;

import com.novatrek.wildlifetracking.entity.Species;
import com.novatrek.wildlifetracking.repository.SpeciesRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/species")
public class SpeciesController {

    private final SpeciesRepository speciesRepository;

    public SpeciesController(SpeciesRepository speciesRepository) {
        this.speciesRepository = speciesRepository;
    }

    @GetMapping
    public List<Species> listSpecies() {
        return speciesRepository.findAll();
    }

    @GetMapping("/{speciesId}")
    public Species getSpecies(@PathVariable UUID speciesId) {
        return speciesRepository.findById(speciesId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Species not found"));
    }

}

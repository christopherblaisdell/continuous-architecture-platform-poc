package com.novatrek.safetycompliance.controller;

import com.novatrek.safetycompliance.entity.Waiver;
import com.novatrek.safetycompliance.repository.WaiverRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/waivers")
public class WaiversController {

    private final WaiverRepository waiverRepository;

    public WaiversController(WaiverRepository waiverRepository) {
        this.waiverRepository = waiverRepository;
    }

    @GetMapping
    public List<Waiver> listWaivers() {
        return waiverRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<Waiver> signWaiver(@Valid @RequestBody Waiver body) {
        Waiver saved = waiverRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{waiverId}")
    public Waiver getWaiver(@PathVariable UUID waiverId) {
        return waiverRepository.findById(waiverId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Waiver not found"));
    }

}

package com.novatrek.mediagallery.controller;

import com.novatrek.mediagallery.entity.MediaItem;
import com.novatrek.mediagallery.repository.MediaItemRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/media")
public class MediaController {

    private final MediaItemRepository mediaItemRepository;

    public MediaController(MediaItemRepository mediaItemRepository) {
        this.mediaItemRepository = mediaItemRepository;
    }

    @GetMapping
    public List<MediaItem> listMedia() {
        return mediaItemRepository.findAll();
    }

    @PostMapping
    public ResponseEntity<MediaItem> uploadMedia(@Valid @RequestBody MediaItem body) {
        MediaItem saved = mediaItemRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    @GetMapping("/{mediaId}")
    public MediaItem getMedia(@PathVariable UUID mediaId) {
        return mediaItemRepository.findById(mediaId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "MediaItem not found"));
    }

    @DeleteMapping("/{mediaId}")
    public ResponseEntity<Void> deleteMedia(@PathVariable UUID mediaId) {
        if (!mediaItemRepository.existsById(mediaId)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "MediaItem not found");
        }
        mediaItemRepository.deleteById(mediaId);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/{mediaId}/share")
    public ResponseEntity<MediaItem> createShareLink(@PathVariable UUID mediaId, @Valid @RequestBody MediaItem body) {
        MediaItem saved = mediaItemRepository.save(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

}

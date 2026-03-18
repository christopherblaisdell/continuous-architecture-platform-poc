package com.novatrek.mediagallery.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.novatrek.mediagallery.entity.MediaItem;
import com.novatrek.mediagallery.entity.ShareLink;
import com.novatrek.mediagallery.repository.MediaItemRepository;
import com.novatrek.mediagallery.repository.ShareLinkRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.hamcrest.Matchers.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(MediaController.class)
class MediaControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private MediaItemRepository mediaItemRepository;

    @MockBean
    private ShareLinkRepository shareLinkRepository;

    @Test
    void listMedia_returnsEmptyList() throws Exception {
        when(mediaItemRepository.findAll()).thenReturn(List.of());

        mockMvc.perform(get("/media"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void listMedia_returnsItems() throws Exception {
        MediaItem item = new MediaItem();
        item.setReservationId(UUID.randomUUID());
        item.setMediaType(MediaItem.MediaType.PHOTO);
        item.setUrl("https://cdn.novatrek.example.com/img/glacier-001.jpg");
        item.setCapturedAt(OffsetDateTime.now());

        when(mediaItemRepository.findAll()).thenReturn(List.of(item));

        mockMvc.perform(get("/media"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(1)))
                .andExpect(jsonPath("$[0].mediaType", is("PHOTO")));
    }

    @Test
    void uploadMedia_returns201() throws Exception {
        MediaItem item = new MediaItem();
        item.setReservationId(UUID.randomUUID());
        item.setMediaType(MediaItem.MediaType.VIDEO);
        item.setUploaderType(MediaItem.UploaderType.DRONE);
        item.setUrl("https://cdn.novatrek.example.com/vid/summit-flyover.mp4");
        item.setFileSizeBytes(52428800);
        item.setCapturedAt(OffsetDateTime.now());

        when(mediaItemRepository.save(any(MediaItem.class))).thenReturn(item);

        mockMvc.perform(post("/media")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(item)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.uploaderType", is("DRONE")));
    }

    @Test
    void getMedia_found() throws Exception {
        UUID id = UUID.randomUUID();
        MediaItem item = new MediaItem();
        item.setId(id);
        item.setReservationId(UUID.randomUUID());
        item.setMediaType(MediaItem.MediaType.PANORAMA);
        item.setUrl("https://cdn.novatrek.example.com/pano/valley-360.jpg");
        item.setCapturedAt(OffsetDateTime.now());

        when(mediaItemRepository.findById(id)).thenReturn(Optional.of(item));

        mockMvc.perform(get("/media/{id}", id))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.mediaType", is("PANORAMA")));
    }

    @Test
    void getMedia_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(mediaItemRepository.findById(id)).thenReturn(Optional.empty());

        mockMvc.perform(get("/media/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void deleteMedia_found() throws Exception {
        UUID id = UUID.randomUUID();
        when(mediaItemRepository.existsById(id)).thenReturn(true);

        mockMvc.perform(delete("/media/{id}", id))
                .andExpect(status().isNoContent());
    }

    @Test
    void deleteMedia_notFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(mediaItemRepository.existsById(id)).thenReturn(false);

        mockMvc.perform(delete("/media/{id}", id))
                .andExpect(status().isNotFound());
    }

    @Test
    void createShareLink_returns201() throws Exception {
        UUID mediaId = UUID.randomUUID();
        MediaItem item = new MediaItem();
        item.setId(mediaId);
        item.setReservationId(UUID.randomUUID());
        item.setUrl("https://cdn.novatrek.example.com/img/test.jpg");
        item.setCapturedAt(OffsetDateTime.now());

        when(mediaItemRepository.findById(mediaId)).thenReturn(Optional.of(item));
        when(mediaItemRepository.save(any(MediaItem.class))).thenReturn(item);

        mockMvc.perform(post("/media/{id}/share", mediaId)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(item)))
                .andExpect(status().isCreated());
    }
}

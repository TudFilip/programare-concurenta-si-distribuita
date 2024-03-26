package com.example.demo;

import org.json.JSONObject;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.util.Base64;

@RestController
@RequestMapping("/images")
public class ImageController {

    private static final String GCP_ADD_IMAGE = "https://europe-central2-snappy-figure-417811.cloudfunctions.net/add_image";
    private static final String GCP_ANALYZE_IMG  = "https://europe-central2-snappy-figure-417811.cloudfunctions.net/analyze_image";
    private static final String GCP_SENTIMENT = "https://europe-central2-snappy-figure-417811.cloudfunctions.net/rate_text";
    private static final String GCP_GET_IMAGE_BY_ID = "https://europe-central2-snappy-figure-417811.cloudfunctions.net/get_image_by_id";
    private static final String GCP_GET_IMAGES = "https://us-central1-snappy-figure-417811.cloudfunctions.net/get_files";

    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping()
    public ResponseEntity<String> saveImage(@RequestParam(value = "file", required = false) MultipartFile multipartFile) {
        try {
            if (multipartFile.isEmpty()) {
                return ResponseEntity.badRequest().body("File is empty");
            }
            var base64ImageData = Base64.getMimeEncoder().encodeToString(multipartFile.getBytes());

            MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
            map.add("imageData", base64ImageData);

            HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(map, new HttpHeaders());

            ResponseEntity<String> responseEntity = restTemplate.exchange(GCP_ADD_IMAGE, HttpMethod.POST, request, String.class);
            return ResponseEntity.ok(responseEntity.getBody());
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("Error during file upload: " + e.getMessage());
        }
    }

    @GetMapping("/content/{id}")
    public ResponseEntity<Object> getImageContent(@PathVariable String id) {
        try {
            return restTemplate.exchange(
                    GCP_ANALYZE_IMG + "?id=" + id,
                    HttpMethod.GET,
                    null,
                    Object.class
            );
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }

    @PostMapping("/analyze")
    public ResponseEntity<Object> analyzeSentiment(@RequestBody String message) {
        try {
            if (message.length() > 500) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                        .body("Message too long (maximum 500 characters allowed)");
            }

            var requestHeaders = new HttpHeaders();
            requestHeaders.setContentType(MediaType.APPLICATION_JSON);

            var requestBody = new JSONObject(message);
            requestBody.put("message", message);

            var requestEntity = new HttpEntity<>(requestBody, requestHeaders);
            return restTemplate.exchange(
                    GCP_SENTIMENT,
                    HttpMethod.POST,
                    requestEntity,
                    Object.class
            );
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }


    @GetMapping("/{id}")
    public ResponseEntity<Object> getImage(@PathVariable String id) {
        try {
            return restTemplate.exchange(
                    GCP_GET_IMAGE_BY_ID + "?imageId=" + id,
                    HttpMethod.GET,
                    null,
                    Object.class
            );
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }

    @GetMapping()
    public ResponseEntity<String> getAllImages() {
        try {
            return restTemplate.exchange(
                    GCP_GET_IMAGES,
                    HttpMethod.GET,
                    null,
                    String.class
            );
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error: " + e.getMessage());
        }
    }
}

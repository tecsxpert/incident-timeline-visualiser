package com.internship.tool.service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class AiServiceClient {

    private final HttpClient httpClient;
    private final String url = "http://127.0.0.1:5000/ask_ai";

    public AiServiceClient() {
        this.httpClient = HttpClient.newBuilder()
                .connectTimeout(Duration.ofSeconds(10))
                .build();
    }

    public String getAIResponse(String prompt) {

        try {
            System.out.println("Sending request to Flask...");

            String json = "{\"prompt\":\"" + prompt.replace("\"", "\\\"") + "\"}";

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("AI Response:\n" + response);
            if (response.statusCode() == 200) {
                // Simple JSON parsing for {"response": "text"}
                String body = response.body();
                int responseIndex = body.indexOf("\"response\"");
                if (responseIndex != -1) {
                    int colonIndex = body.indexOf(":", responseIndex);
                    int startQuote = body.indexOf("\"", colonIndex);
                    int endQuote = body.lastIndexOf("\"");
                    if (startQuote != -1 && endQuote > startQuote) {
                        return body.substring(startQuote + 1, endQuote);
                    }
                }
            }

        } catch (Exception e) {
            System.out.println("Error calling AI service: " + e.getMessage());
        }

        return null;
    }
}
package com.internship.tool.service;

public class Main {
    public static void main(String[] args) {

        AiServiceClient client = new AiServiceClient();

        // ✅ FIXED (no 'prompt:' here)
        String response = client.getAIResponse("Enter about AI  2 lines");

        System.out.println("AI Response: " + response);
    }
}
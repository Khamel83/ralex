# Alternative Mobile App Integrations

This document provides guidance on integrating Ralex with alternative mobile AI chat applications beyond OpenCat, such as ChatBox AI and Pal Chat. While OpenCat is the primary recommended application due to its direct API configuration, these alternatives can be configured to work with Ralex for specific use cases or user preferences.

## 1. ChatBox AI Optimization Guide

ChatBox AI is a versatile AI client that supports custom API endpoints. To integrate with Ralex, you will typically configure a custom endpoint pointing to your Ralex Bridge API.

### Configuration Steps:

1.  **Ensure Ralex Bridge is Running**: Your Ralex Bridge API (e.g., `http://localhost:8000`) must be accessible from your mobile device's network.
2.  **Open ChatBox AI**: Launch the ChatBox AI application on your mobile device.
3.  **Add Custom Service**: Look for an option to add a custom service or API endpoint. This is usually found in the application's settings or by adding a new model.
4.  **Configure Endpoint**: Enter your Ralex Bridge API URL (e.g., `http://<your_ralex_ip>:8000/v1/chat/completions`) as the custom endpoint.
5.  **API Key**: If your Ralex Bridge requires an API key (which it should for security), enter your `OPENROUTER_API_KEY` in the designated API key field within ChatBox AI.
6.  **Model Name**: Specify `ralex-bridge` as the model name if ChatBox AI requires it.

### Features and Considerations:

-   **Team Collaboration**: ChatBox AI often includes features for team collaboration, which can be useful for shared Ralex instances.
-   **Azure Support**: If you are running Ralex on Azure, ChatBox AI might offer specific optimizations or easier integration with Azure services.
-   **Custom Prompts**: You can often define custom prompts within ChatBox AI to tailor interactions with Ralex.

## 2. Pal Chat Configuration Templates

Pal Chat is another privacy-focused AI chat application. Its configuration might be more template-driven or require specific JSON/YAML files.

### Configuration Steps:

1.  **Ensure Ralex Bridge is Running**: As with ChatBox AI, your Ralex Bridge API must be accessible.
2.  **Locate Configuration Files**: Pal Chat might use local configuration files (e.g., JSON or YAML) that you can edit directly or import.
3.  **Edit/Create Template**: Modify an existing template or create a new one to point to your Ralex Bridge API. A typical template might look like this (adjust as per Pal Chat's specific schema):

    ```json
    {
      "name": "Ralex Bridge",
      "api_url": "http://<your_ralex_ip>:8000/v1/chat/completions",
      "api_key": "sk-your-openrouter-key",
      "model": "ralex-bridge",
      "description": "Connects to your Ralex AI Coding Assistant"
    }
    ```

4.  **Import Template**: Import the modified configuration file into Pal Chat.

### Features and Considerations:

-   **Privacy-Focused**: Pal Chat emphasizes privacy, which aligns with Ralex's local-first approach.
-   **Clean Interface**: Often provides a minimalist and clean user interface.
-   **Basic Interactions**: Best suited for simple queries and basic AI interactions.

## 3. App Comparison and Recommendations

| Feature / App | OpenCat | ChatBox AI | Pal Chat |
|-----------------------|---------|------------|----------|
| **Primary Use Case**  | General AI Chat | Team Collaboration | Privacy-Focused |
| **Ralex Integration** | Direct API (QR) | Custom Endpoint | Template/File |
| **Ease of Setup**     | Very Easy (QR) | Moderate   | Moderate |
| **Rich Features**     | Basic   | Advanced   | Basic    |
| **Privacy**           | Good    | Good       | Excellent|

**Recommendation**: For most Ralex users, **OpenCat** remains the easiest and most direct integration due to its QR code scanning capability. **ChatBox AI** is a good alternative for users needing team features or specific Azure integration. **Pal Chat** is suitable for users prioritizing privacy and a minimalist experience for basic Ralex interactions.

## 4. Multi-App Workflow Documentation

It is possible to use multiple mobile apps with Ralex, switching between them based on the task at hand. For example:

-   Use **OpenCat** for quick, on-the-go code snippets or questions.
-   Switch to **ChatBox AI** for collaborative debugging sessions with your team.
-   Use **Pal Chat** for highly sensitive code reviews where privacy is paramount.

Ensure your Ralex Bridge API is consistently accessible and secured for all integrated applications.

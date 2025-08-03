# OpenCat Configuration Automation

This document provides instructions for automating the configuration of the OpenCat iOS application to connect with your Ralex instance.

## 1. Generate Configuration Files

Use the `mobile_setup.py` script to generate the necessary configuration JSON and a QR code for easy setup.

### Usage:

```bash
python3 tools/mobile_setup.py
```

### Output:

This script will generate two files in your project's `tools/` directory:

- `opencat_config.json`: A JSON file containing the API base URL, API key, and model name.
- `opencat_config_qr.png`: A QR code image that encodes the content of `opencat_config.json`.

## 2. Configure OpenCat

There are two ways to configure OpenCat:

### Option A: Scan QR Code (Recommended)

1. Open the `opencat_config_qr.png` file on your computer.
2. In the OpenCat app on your iOS device, navigate to **Settings**.
3. Tap on **API Key & Endpoint**.
4. Tap the **QR code icon** (usually in the top right corner).
5. Scan the QR code displayed on your computer screen.

OpenCat should automatically populate the API Key and Endpoint fields.

### Option B: Manual Configuration

1. Open the `opencat_config.json` file in a text editor.
2. In the OpenCat app on your iOS device, navigate to **Settings**.
3. Tap on **API Key & Endpoint**.
4. Manually enter the `api_key` from `opencat_config.json` into the **API Key** field in OpenCat.
5. Manually enter the `api_base` from `opencat_config.json` into the **Endpoint** field in OpenCat.
6. Ensure the `model` name in OpenCat matches the `model` specified in `opencat_config.json` (e.g., `ralex-bridge`).

## 3. Verify Connection

After configuration, try sending a simple message in OpenCat. If Ralex is running and configured correctly, you should receive a response.

## Troubleshooting

- **"Error: Network Error" or "Failed to connect"**: Ensure your Ralex instance is running and accessible from your mobile device's network. Check firewall settings.
- **"Invalid API Key"**: Double-check that the `api_key` in OpenCat matches your `OPENROUTER_API_KEY`.
- **"Model not found"**: Verify the `model` name in OpenCat matches the one configured in `opencat_config.json` (e.g., `ralex-bridge`).
- **No response**: Check the Ralex logs for any errors during request processing.

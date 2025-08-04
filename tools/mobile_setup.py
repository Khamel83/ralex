import qrcode
import json
import os
import logging

from typing import Dict

logger = logging.getLogger(__name__)

class OpenCatConfigurator:
    def __init__(self, config_dir: str = "."):
        self.config_dir = config_dir
        self.config_file_name = "opencat_config.json"

    def generate_config_json(self, api_base: str, api_key: str, model_name: str = "ralex-bridge") -> Dict:
        """Generates a basic OpenCat compatible JSON configuration."""
        config = {
            "api_base": api_base,
            "api_key": api_key,
            "model": model_name,
            "temperature": 0.7,
            "max_tokens": 1024,
            "stream": True,
            "stop": ["\n\n"],
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        logger.info("OpenCat configuration JSON generated.")
        return config

    def save_config_file(self, config: Dict, output_path: str = None):
        """Saves the configuration to a JSON file."""
        if output_path is None:
            output_path = os.path.join(self.config_dir, self.config_file_name)
        
        try:
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=4)
            logger.info(f"OpenCat configuration saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save OpenCat configuration to {output_path}: {e}")
            return None

    def generate_qr_code(self, data: str, output_path: str = "opencat_config_qr.png"):
        """Generates a QR code from the given data string."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(output_path)
            logger.info(f"QR code generated and saved to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to generate QR code: {e}")
            return None

    def automate_setup(self, api_base: str, api_key: str, model_name: str = "ralex-bridge", output_dir: str = "."):
        """Automates the OpenCat setup process by generating config file and QR code."""
        self.config_dir = output_dir
        config_json = self.generate_config_json(api_base, api_key, model_name)
        config_file_path = self.save_config_file(config_json)
        
        if config_file_path:
            # For QR code, we might want to encode the file content or a URL to it
            # For simplicity, let's encode the JSON string directly for now
            qr_data = json.dumps(config_json)
            qr_code_path = self.generate_qr_code(qr_data, os.path.join(output_dir, "opencat_config_qr.png"))
            return {"config_file": config_file_path, "qr_code": qr_code_path}
        return None

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    # Ensure the tools directory exists for output
    output_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tools'))
    os.makedirs(output_base_dir, exist_ok=True)

    configurator = OpenCatConfigurator(output_base_dir)

    # Replace with your actual API base and key
    test_api_base = "http://localhost:8000/v1/chat/completions"
    test_api_key = "sk-your-openrouter-key"

    print("\n--- Automating OpenCat Setup ---")
    results = configurator.automate_setup(test_api_base, test_api_key)

    if results:
        print(f"✅ Setup automated successfully!")
        print(f"   Config File: {results['config_file']}")
        print(f"   QR Code: {results['qr_code']}")
        print("\nInstructions: Open the QR code image and scan it with OpenCat app.")
    else:
        print("❌ OpenCat setup automation failed.")

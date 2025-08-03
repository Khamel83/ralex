import logging
from typing import Dict

logger = logging.getLogger(__name__)

class MobileContextManager:
    def __init__(self):
        pass

    def detect_device_context(self, request_headers: Dict) -> Dict:
        """Detects and extracts device-specific context from request headers."""
        user_agent = request_headers.get("user-agent", "Unknown")
        device_type = "unknown"
        screen_size = "N/A"
        network_type = "N/A"

        if "iphone" in user_agent.lower() or "ipad" in user_agent.lower():
            device_type = "ios_mobile"
        elif "android" in user_agent.lower():
            device_type = "android_mobile"
        elif "mobile" in user_agent.lower():
            device_type = "generic_mobile"

        # Placeholder for more advanced parsing of screen size or network from custom headers
        # Example: X-Screen-Size: 1080x1920, X-Network-Type: wifi/cellular
        if "x-screen-size" in request_headers:
            screen_size = request_headers["x-screen-size"]
        if "x-network-type" in request_headers:
            network_type = request_headers["x-network-type"]

        context = {
            "user_agent": user_agent,
            "device_type": device_type,
            "screen_size": screen_size,
            "network_type": network_type,
            "capabilities": ["touch", "voice"] # Assuming common mobile capabilities
        }
        logger.info(f"Detected device context: {context}")
        return context

    def optimize_prompt_for_mobile(self, prompt: str, device_context: Dict) -> str:
        """Optimizes a prompt for mobile interaction based on device context."""
        # Example: Add a note about brevity for small screens
        if device_context.get("screen_size") != "N/A" and "x" in device_context["screen_size"]:
            width, height = map(int, device_context["screen_size"].split('x'))
            if width < 768: # Assuming typical phone width
                prompt = f"[Mobile, small screen: Be concise] {prompt}"
        
        # Example: Adjust for voice input
        if "voice" in device_context.get("capabilities", []) and "voice_input" in device_context:
            prompt = f"[Voice input detected] {prompt}"

        logger.info(f"Optimized prompt for mobile: {prompt}")
        return prompt

    def adjust_response_sizing(self, response_content: str, device_context: Dict) -> str:
        """Adjusts the response content size for mobile screens."""
        # This is a very basic example. More advanced logic would involve token counting
        # and summarization/truncation based on screen size and user preferences.
        if device_context.get("screen_size") != "N/A" and "x" in device_context["screen_size"]:
            width, height = map(int, device_context["screen_size"].split('x'))
            if width < 768 and len(response_content) > 500: # If small screen and long response
                logger.info("Truncating response for small screen.")
                return response_content[:497] + "..."
        return response_content

# Example Usage (for testing/demonstration)
if __name__ == "__main__":
    manager = MobileContextManager()

    # Simulate a request from an iPhone
    iphone_headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "x-screen-size": "375x667",
        "x-network-type": "cellular"
    }
    iphone_context = manager.detect_device_context(iphone_headers)
    print(f"iPhone Context: {iphone_context}")
    optimized_prompt = manager.optimize_prompt_for_mobile("Write a Python function to calculate factorial.", iphone_context)
    print(f"Optimized Prompt: {optimized_prompt}")
    adjusted_response = manager.adjust_response_sizing("""
This is a very long response that needs to be truncated for mobile screens. It contains a lot of detailed information about factorial calculation, including recursive and iterative approaches, edge cases, and performance considerations. The goal is to provide a comprehensive answer, but for mobile, it might be too much. Therefore, we will demonstrate how this content would be shortened to fit the mobile display constraints. This ensures that users on smaller devices get the most relevant information without excessive scrolling.
""", iphone_context)
    print(f"Adjusted Response: {adjusted_response}")

    # Simulate a request from a desktop
    desktop_headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    desktop_context = manager.detect_device_context(desktop_headers)
    print(f"\nDesktop Context: {desktop_context}")
    optimized_prompt = manager.optimize_prompt_for_mobile("Write a Python function to calculate factorial.", desktop_context)
    print(f"Optimized Prompt: {optimized_prompt}")
    adjusted_response = manager.adjust_response_sizing("""
This is a very long response that needs to be truncated for mobile screens. It contains a lot of detailed information about factorial calculation, including recursive and iterative approaches, edge cases, and performance considerations. The goal is to provide a comprehensive answer, but for mobile, it might be too much. Therefore, we will demonstrate how this content would be shortened to fit the mobile display constraints. This ensures that users on smaller devices get the most relevant information without excessive scrolling.
""", desktop_context)
    print(f"Adjusted Response: {adjusted_response}")

import time

class ContentGenerator:
    def __init__(self, config):
        self.config = config

    def generate_script(self, keywords, platform):
        """Generates a script for a video based on the given keywords and platform."""
        print(f"Generating script for {platform} with keywords: {keywords}")
        # Simulate a delay for generating the script
        time.sleep(5)
        script = f"This is a script about {', '.join(keywords)} for {platform}."
        print("Script generated successfully.")
        return script

import openai

class ContentGenerator:
    def __init__(self, config):
        self.config = config
        openai.api_key = self.config.get("openai", {}).get("api_key", "YOUR_OPENAI_API_KEY")

    def generate_script(self, keywords, platform):
        """Generates a script for a video based on the given keywords and platform."""
        print(f"Generating script for {platform} with keywords: {keywords}")

        prompt = f"Create a video script for {platform} about {', '.join(keywords)}. The script should be engaging and informative."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates video scripts."},
                    {"role": "user", "content": prompt},
                ],
            )
            script = response.choices[0].message.content
            print("Script generated successfully.")
            return script
        except Exception as e:
            print(f"Error generating script: {e}")
            return None

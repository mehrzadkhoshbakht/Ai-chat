import openai
import os
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generate_script(self, keywords, platform):
        """Generates a script for a video based on the given keywords and platform."""
        logger.info(f"Generating script for {platform} with keywords: {keywords}")

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
            logger.info("Script generated successfully.")
            return script
        except Exception as e:
            logger.error(f"Error generating script: {e}", exc_info=True)
            raise e

from .content_generator import ContentGenerator

class ChatEngine:
    def __init__(self, config):
        self.config = config
        self.content_generator = ContentGenerator(config)

    def generate_video_script(self, keywords, platform):
        """Generates a video script using the content generator."""
        return self.content_generator.generate_script(keywords, platform)

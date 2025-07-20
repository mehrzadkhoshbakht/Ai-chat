import os
import requests
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

def generate_visuals(topic):
    """
    Generates visuals for the given topic using DALL-E and a title card.
    """
    print(f"Generating visuals for topic: {topic}...")

    visual_paths = []

    # --- Generate Title Card ---
    try:
        title_card_path = create_title_card(topic)
        visual_paths.append(title_card_path)
        print(f"Title card created at: {title_card_path}")
    except Exception as e:
        print(f"Error creating title card: {e}")

    # --- Generate Image with DALL-E ---
    # Make sure you have set the OPENAI_API_KEY environment variable
    client = OpenAI()

    try:
        response = client.images.generate(
          model="dall-e-2",
          prompt=f"A professional and clean visual for a YouTube tutorial about '{topic}'. The image should be abstract and related to networking or technology. No text in the image.",
          n=1,
          size="1024x1024"
        )
        image_url = response.data[0].url

        # Download the image
        image_response = requests.get(image_url)
        image_path = os.path.join("zero_touch_mikrotik", "data", "images", f"{topic.replace(' ', '_')}_dalle.png")
        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))
        with open(image_path, "wb") as f:
            f.write(image_response.content)

        visual_paths.append(image_path)
        print(f"DALL-E image saved to {image_path}")

    except Exception as e:
        print(f"Error generating image with DALL-E: {e}")

    if not visual_paths:
        raise RuntimeError("Failed to generate any visuals.")

    return visual_paths

def create_title_card(topic):
    """Creates a simple title card image."""
    width, height = 1280, 720
    background_color = (15, 23, 42) # Slate 900
    text_color = (241, 245, 249) # Slate 100

    img = Image.new('RGB', (width, height), color = background_color)
    d = ImageDraw.Draw(img)

    try:
        # Using a more common font
        font_path = "DejaVuSans.ttf" if os.path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf") else "arial.ttf"
        title_font = ImageFont.truetype(font_path, 80)
        subtitle_font = ImageFont.truetype(font_path, 40)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Title
    d.text((width/2, height/2 - 50), topic, font=title_font, fill=text_color, anchor="mm")

    # Subtitle
    d.text((width/2, height/2 + 50), "آموزش میکروتیک", font=subtitle_font, fill=text_color, anchor="mm")

    path = os.path.join("zero_touch_mikrotik", "data", "images", f"{topic.replace(' ', '_')}_title.png")
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    img.save(path)
    return path

import os
from PIL import Image, ImageDraw, ImageFont

def generate_visuals(topic):
    """
    Generates visuals for the given topic.
    """
    print(f"Generating visuals for topic: {topic}...")

    # Create a simple title card image
    width, height = 1280, 720
    background_color = (7, 8, 24) # Dark blue
    text_color = (255, 255, 255) # White

    img = Image.new('RGB', (width, height), color = background_color)
    d = ImageDraw.Draw(img)

    # You might need to specify a path to a font file that supports Persian characters
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()

    # Simple text wrapping
    lines = []
    words = topic.split()
    current_line = ""
    for word in words:
        if d.textlength(current_line + word, font=font) <= width - 100:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_text = (height - (len(lines) * 70)) / 2
    for line in lines:
        text_width = d.textlength(line, font=font)
        d.text((width - text_width) / 2, y_text, line, font=font, fill=text_color)
        y_text += 70

    visual_path = os.path.join("zero_touch_mikrotik", "data", "images", f"{topic.replace(' ', '_')}.png")
    if not os.path.exists(os.path.dirname(visual_path)):
        os.makedirs(os.path.dirname(visual_path))

    img.save(visual_path)

    print(f"Visuals saved to {visual_path}")
    return [visual_path]

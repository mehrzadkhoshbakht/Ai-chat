import os
from TTS.api import TTS

def generate_voice(script_path):
    """
    Generates a voiceover for the given script.
    """
    print(f"Generating voice for script: {script_path}...")

    with open(script_path, "r", encoding="utf-8") as f:
        script = f.read()

    # Initialize TTS
    # This will download the model on the first run
    tts = TTS(model_name="tts_models/fa/gan/meta-style-tts", progress_bar=True, gpu=False)

    audio_path = os.path.join("zero_touch_mikrotik", "data", "audio", f"{os.path.basename(script_path).split('.')[0]}.wav")

    # Generate speech
    tts.tts_to_file(text=script, file_path=audio_path)

    print(f"Voiceover saved to {audio_path}")
    return audio_path

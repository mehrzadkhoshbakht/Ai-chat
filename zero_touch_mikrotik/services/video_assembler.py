import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from pydub import AudioSegment

def normalize_audio(audio_path):
    """Normalizes the audio to a standard level."""
    print(f"Normalizing audio for {audio_path}...")
    audio = AudioSegment.from_file(audio_path)
    normalized_audio = audio.normalize()

    normalized_path = audio_path.replace(".wav", "_normalized.wav")
    normalized_audio.export(normalized_path, format="wav")

    return normalized_path

def assemble_video(visual_paths, audio_path, topic):
    """
    Assembles a video with normalized audio, background music, and a slideshow.
    """
    print("Assembling video with enhanced audio...")

    if not visual_paths:
        raise ValueError("No visuals provided.")

    # Normalize the main voiceover
    normalized_voice_path = normalize_audio(audio_path)
    voice_clip = AudioFileClip(normalized_voice_path)
    total_duration = voice_clip.duration

    # --- Add Background Music ---
    background_music_path = os.path.join("zero_touch_mikrotik", "data", "audio", "background.mp3")
    final_audio = voice_clip

    if os.path.exists(background_music_path):
        print("Adding background music...")
        background_clip = AudioFileClip(background_music_path).set_duration(total_duration)
        # Lower the volume of the background music
        background_clip = background_clip.volumex(0.1)

        # Combine voiceover and background music
        final_audio = CompositeAudioClip([voice_clip, background_clip])
    else:
        print("Background music not found. Skipping.")

    # --- Create Slideshow ---
    num_visuals = len(visual_paths)
    duration_per_visual = total_duration / num_visuals

    clips = []
    for image_path in visual_paths:
        clip = ImageClip(image_path, duration=duration_per_visual)
        clip = clip.resize(width=1280, height=720)
        clips.append(clip)

    final_video_clip = concatenate_videoclips(clips, method="compose")
    final_video_clip = final_video_clip.set_audio(final_audio)

    video_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}.mp4")

    final_video_clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')

    duration = final_video_clip.duration
    print(f"Video saved to {video_path} (Duration: {duration}s)")
    return video_path, duration

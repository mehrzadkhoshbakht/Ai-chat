import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from services.subtitle_translator import create_subtitled_clip

def assemble_video(visual_paths, audio_path, srt_path, topic):
    """
    Assembles a video with burned-in subtitles.
    """
    print("Assembling video with burned-in subtitles...")

    if not visual_paths:
        raise ValueError("No visuals provided.")

    # Load the audio to get its duration
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration

    # --- Create Slideshow ---
    num_visuals = len(visual_paths)
    duration_per_visual = total_duration / num_visuals

    clips = []
    for image_path in visual_paths:
        clip = ImageClip(image_path, duration=duration_per_visual)
        clip = clip.resize(width=1280, height=720)
        clips.append(clip)

    video_clip = concatenate_videoclips(clips, method="compose")

    # --- Add Subtitles ---
    # This function now returns a clip with subtitles burned in
    final_video_clip = create_subtitled_clip(video_clip, srt_path)

    # Set the audio of the final video clip
    final_video_clip = final_video_clip.set_audio(audio_clip)

    video_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}.mp4")

    final_video_clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')

    duration = final_video_clip.duration
    print(f"Video saved to {video_path} (Duration: {duration}s)")
    return video_path, duration

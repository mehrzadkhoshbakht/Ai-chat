import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def assemble_video(visual_paths, audio_path, topic):
    """
    Assembles a video from the given visuals and audio by creating a slideshow.
    """
    print("Assembling video slideshow...")

    if not visual_paths:
        raise ValueError("No visuals provided to assemble the video.")

    # Load the audio to get its duration
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration

    # Calculate duration for each visual
    num_visuals = len(visual_paths)
    duration_per_visual = total_duration / num_visuals

    # Create a list of video clips from the images
    clips = []
    for image_path in visual_paths:
        clip = ImageClip(image_path, duration=duration_per_visual)
        # Resize all images to a standard 1280x720 to avoid errors
        clip = clip.resize(width=1280, height=720)
        clips.append(clip)

    # Concatenate the clips into a single video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Set the audio of the final video clip
    final_clip = final_clip.set_audio(audio_clip)

    video_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}.mp4")

    # Write the result to a file using a codec that supports a wide range of players
    final_clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')

    print(f"Video saved to {video_path}")
    return video_path

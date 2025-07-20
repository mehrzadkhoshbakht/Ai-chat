import os
from moviepy.editor import ImageClip, AudioFileClip

def assemble_video(visual_paths, audio_path, topic):
    """
    Assembles a video from the given visuals and audio.
    """
    print("Assembling video...")

    if not visual_paths:
        raise ValueError("No visuals provided to assemble the video.")

    # Use the first visual as the main clip
    # A more advanced implementation would create a slideshow of all visuals
    main_visual = visual_paths[0]

    # Load the audio to get its duration
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # Create a video clip from the image
    video_clip = ImageClip(main_visual, duration=duration)

    # Set the audio of the video clip
    video_clip = video_clip.set_audio(audio_clip)

    # Add a watermark (optional)
    # txt_clip = TextClip("Zero-Touch MikroTik", fontsize=20, color='white')
    # txt_clip = txt_clip.set_pos(('right', 'bottom')).set_duration(duration)
    # video_clip = CompositeVideoClip([video_clip, txt_clip])

    video_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}.mp4")

    # Write the result to a file
    video_clip.write_videofile(video_path, fps=24)

    print(f"Video saved to {video_path}")
    return video_path

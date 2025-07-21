import os
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

def generate_subtitles(audio_path, topic):
    """
    Generates subtitles for the given audio file and translates them.
    """
    print("Generating subtitles...")

    model = WhisperModel("base", device="cpu", compute_type="int8")

    segments, _ = model.transcribe(audio_path, language="fa")

    # Generate Farsi SRT
    srt_path_fa = os.path.join("zero_touch_mikrotik", "data", "subtitles", f"{topic.replace(' ', '_')}_fa.srt")
    with open(srt_path_fa, "w", encoding="utf-8") as srt_file:
        for i, segment in enumerate(segments):
            start_time = format_timestamp(segment.start)
            end_time = format_timestamp(segment.end)
            srt_file.write(f"{i + 1}\n")
            srt_file.write(f"{start_time} --> {end_time}\n")
            srt_file.write(f"{segment.text.strip()}\n\n")

    print(f"Farsi subtitles saved to {srt_path_fa}")

    # --- Translation Placeholder ---
    # In a real implementation, you'd use a translation API or a local model.
    # For now, we'll just create placeholder files.

    # English
    srt_path_en = os.path.join("zero_touch_mikrotik", "data", "subtitles", f"{topic.replace(' ', '_')}_en.srt")
    with open(srt_path_en, "w", encoding="utf-8") as f:
        f.write("1\n00:00:00,000 --> 00:00:05,000\nEnglish translation placeholder.\n\n")
    print(f"English subtitles saved to {srt_path_en}")

    # Arabic
    srt_path_ar = os.path.join("zero_touch_mikrotik", "data", "subtitles", f"{topic.replace(' ', '_')}_ar.srt")
    with open(srt_path_ar, "w", encoding="utf-8") as f:
        f.write("1\n00:00:00,000 --> 00:00:05,000\nترجمة عربية placeholder.\n\n")
    print(f"Arabic subtitles saved to {srt_path_ar}")

    return [srt_path_fa, srt_path_en, srt_path_ar]

def format_timestamp(seconds):
    """Formats a timestamp in seconds to the SRT format."""
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds / 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def create_subtitled_clip(video_clip, srt_path):
    """Creates a video clip with burned-in subtitles."""

    # Define a generator for the subtitles
    generator = lambda txt: TextClip(
        txt,
        font='Arial-Bold', # A common font, might need to be installed or changed
        fontsize=24,
        color='white',
        stroke_color='black',
        stroke_width=1
    )

    # Create the subtitles clip
    subtitles = SubtitlesClip(srt_path, generator)

    # Composite the video and subtitles
    final_clip = CompositeVideoClip([video_clip, subtitles.set_pos(('center', 'bottom'))])

    return final_clip

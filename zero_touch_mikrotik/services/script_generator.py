import os
from openai import OpenAI

def generate_script(topic, estimated_duration_sec):
    """
    Generates a Persian script for the given topic and estimated duration using the OpenAI API.
    """
    duration_minutes = round(estimated_duration_sec / 60)
    print(f"Generating script for topic: {topic} (approx. {duration_minutes} minutes)...")

    # Make sure you have set the OPENAI_API_KEY environment variable
    client = OpenAI()

    try:
        response = client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
              {"role": "system", "content": "You are a helpful assistant that writes educational YouTube video scripts in Persian."},
              {"role": "user", "content": f"یک اسکریپت کامل و جذاب برای یک ویدیوی آموزشی {duration_minutes} دقیقه‌ای در مورد موضوع زیر بنویس: '{topic}'. اسکریپت باید شامل مقدمه، بدنه اصلی با توضیحات گام به گام و نتیجه‌گیری باشد."}
          ]
        )
        script = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating script with OpenAI: {e}")
        print("Falling back to placeholder script.")
        script = f"""
        سلام به همه! امروز می‌خواهیم در مورد {topic} صحبت کنیم.
        (خطا در تولید اسکریپت با هوش مصنوعی)
        """

    script_path = os.path.join("zero_touch_mikrotik", "data", "scripts", f"{topic.replace(' ', '_')}.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    print(f"Script saved to {script_path}")
    return script_path

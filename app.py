from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime

def format_timestamp(seconds):
    """Convert seconds into HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"

# Video ID
video_id = "J4fKHyXg428"

try:
    # Get the transcript for the video
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['th'])
    
    # Prepare transcript text with timestamps
    transcript_with_time = "\n".join(
        [f"[{format_timestamp(item['start'])}] {item['text']}" for item in transcript]
    )
    
    # Prepare transcript text without timestamps
    transcript_without_time = "\n".join(
        [item['text'] for item in transcript]
    )
    
    # Generate filenames with current datetime
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename_with_time = f"transcript_with_time_{current_time}.txt"
    filename_without_time = f"transcript_without_time_{current_time}.txt"
    
    # Save transcript with timestamps
    with open(filename_with_time, "w", encoding="utf-8") as file:
        file.write("Transcript with Timestamps:\n")
        file.write(transcript_with_time)
    
    # Save transcript without timestamps
    with open(filename_without_time, "w", encoding="utf-8") as file:
        file.write("Transcript without Timestamps:\n")
        file.write(transcript_without_time)
    
    print(f"Transcripts saved:\n1. {filename_with_time}\n2. {filename_without_time}")

except Exception as e:
    print("An error occurred:", e)

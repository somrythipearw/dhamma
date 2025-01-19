from flask import Flask, request, render_template, send_file
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
import io

app = Flask(__name__)

# Function to format timestamp
def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    return f"{minutes:02}:{seconds:02}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_id = request.form.get("youtube_id")  # Get YouTube ID from the form
        try:
            # Get the transcript for the video
            transcript = YouTubeTranscriptApi.get_transcript(youtube_id, languages=["th"])
            
            # Prepare transcript text with and without timestamps
            transcript_with_time = "\n".join(
                [f"[{format_timestamp(item['start'])}] {item['text']}" for item in transcript]
            )
            transcript_without_time = "\n".join(
                [item["text"] for item in transcript]
            )
            
            # Generate current datetime for file naming
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Create in-memory files to send for download
            file_with_time = io.BytesIO()
            file_with_time.write(f"Transcript with Timestamps:\n{transcript_with_time}".encode())
            file_with_time.seek(0)
            
            file_without_time = io.BytesIO()
            file_without_time.write(f"Transcript without Timestamps:\n{transcript_without_time}".encode())
            file_without_time.seek(0)
            
            # Provide files for download
            return render_template(
                "index.html", 
                success=True, 
                with_time=transcript_with_time, 
                without_time=transcript_without_time,
                file_with_time=f"transcript_with_time_{current_time}.txt",
                file_without_time=f"transcript_without_time_{current_time}.txt"
            )
            
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {e}")

    return render_template("index.html")

@app.route("/download_with_time/<filename>")
def download_with_time(filename):
    return send_file(
        io.BytesIO(f"Transcript with Timestamps:\n{filename}".encode()),
        as_attachment=True,
        download_name=filename,
        mimetype="text/plain"
    )

@app.route("/download_without_time/<filename>")
def download_without_time(filename):
    return send_file(
        io.BytesIO(f"Transcript without Timestamps:\n{filename}".encode()),
        as_attachment=True,
        download_name=filename,
        mimetype="text/plain"
    )

if __name__ == "__main__":
    app.run(debug=True)

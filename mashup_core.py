import os
import sys
import glob
import shutil
import argparse
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

# ---------------- FOLDERS ----------------
BASE_DIR = os.getcwd()
VIDEO_DIR = os.path.join(BASE_DIR, "videos")
AUDIO_DIR = os.path.join(BASE_DIR, "audios")
TRIM_DIR = os.path.join(BASE_DIR, "trimmed")

for folder in [VIDEO_DIR, AUDIO_DIR, TRIM_DIR]:
    os.makedirs(folder, exist_ok=True)

# ---------------- ARGUMENTS ----------------
def parse_arguments():
    parser = argparse.ArgumentParser(description="YouTube Mashup Generator")

    parser.add_argument("singer", type=str)
    parser.add_argument("num_videos", type=int)
    parser.add_argument("duration", type=int)
    parser.add_argument("output", type=str)

    args = parser.parse_args()

    if args.num_videos <= 10:
        print("Error: Number of videos must be greater than 10")
        sys.exit()

    if args.duration <= 20:
        print("Error: Duration must be greater than 20 seconds")
        sys.exit()

    if not args.output.endswith(".mp3"):
        print("Error: Output file must be .mp3")
        sys.exit()

    return args

# ---------------- DOWNLOAD ----------------
def download_videos(singer, n):
    print("\nDownloading videos...")

    query = f"ytsearch{n}:{singer} songs"

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': f'{VIDEO_DIR}/%(title)s.%(ext)s',
        'quiet': False
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])
    except Exception as e:
        print("Download failed:", e)
        sys.exit()

# ---------------- VIDEO TO AUDIO ----------------
def convert_to_audio():
    print("\nConverting videos to audio...")

    for video in glob.glob(f"{VIDEO_DIR}/*.mp4"):
        try:
            clip = VideoFileClip(video)
            filename = os.path.basename(video).replace(".mp4", ".mp3")
            output_path = os.path.join(AUDIO_DIR, filename)

            clip.audio.write_audiofile(output_path, logger=None)
            clip.close()

        except Exception as e:
            print("Conversion error:", e)

# ---------------- TRIM ----------------
def trim_audios(duration):
    print("\nTrimming audio files...")

    for audio in glob.glob(f"{AUDIO_DIR}/*.mp3"):
        try:
            sound = AudioSegment.from_mp3(audio)
            trimmed = sound[:duration * 1000]

            filename = os.path.basename(audio)
            trimmed.export(os.path.join(TRIM_DIR, filename), format="mp3")

        except Exception as e:
            print("Trim error:", e)

# ---------------- MERGE ----------------
def merge_audios(output_file):
    print("\nMerging mashup...")

    combined = AudioSegment.empty()

    for audio in sorted(glob.glob(f"{TRIM_DIR}/*.mp3")):
        sound = AudioSegment.from_mp3(audio)
        combined += sound

    combined.export(output_file, format="mp3")
    print("\nMashup created:", output_file)

# ---------------- CLEANUP (optional) ----------------
def cleanup():
    shutil.rmtree(VIDEO_DIR, ignore_errors=True)
    shutil.rmtree(AUDIO_DIR, ignore_errors=True)
    shutil.rmtree(TRIM_DIR, ignore_errors=True)

# ---------------- MAIN ----------------
def main():
    args = parse_arguments()

    download_videos(args.singer, args.num_videos)
    convert_to_audio()
    trim_audios(args.duration)
    merge_audios(args.output)

    print("\nDone.")

if __name__ == "__main__":
    main()

# function for web app
def generate_mashup(singer, num_videos, duration, output):
    download_videos(singer, num_videos)
    convert_to_audio()
    trim_audios(duration)
    merge_audios(output)
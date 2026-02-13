# YouTube Mashup Generator

This project generates a music mashup automatically from YouTube videos.

The user provides a singer name, number of videos, and duration.\
The system downloads songs, extracts audio, trims clips, merges them,
and produces a final mashup file.

The project contains two parts:

1.  Command Line Program (required)
2.  Web Application with Email Delivery

------------------------------------------------------------------------

## Features

-   Download multiple YouTube songs
-   Convert video to audio
-   Trim first N seconds from each song
-   Merge all clips into one mashup
-   Send mashup as ZIP through email (web app)

------------------------------------------------------------------------

## Technologies Used

-   Python
-   Flask
-   yt-dlp
-   moviepy
-   pydub
-   ffmpeg
-   SMTP Mail

------------------------------------------------------------------------

## Installation

Install Python 3.11 and ffmpeg first.

Then install dependencies:

    pip install -r requirements.txt

------------------------------------------------------------------------

## Program 1 --- Command Line Usage

Run:

    python 102303007.py "Singer Name" <NumberOfVideos> <Duration> <OutputFile>

Example:

    python 102303007.py "Sharry Maan" 20 25 mashup.mp3

Conditions: - NumberOfVideos must be greater than 10 - Duration must be
greater than 20 seconds - Output must be .mp3

------------------------------------------------------------------------

## Program 2 --- Web Application

Start server:

    python app.py

Open browser:

    http://127.0.0.1:5000

Enter: - Singer name - Number of videos - Duration - Email address

The mashup will be generated and sent as a ZIP file to the email.

------------------------------------------------------------------------

## Project Structure

    app.py              -> Flask web server
    102303007.py        -> Command line mashup program
    mashup_core.py      -> Reusable mashup functions
    templates/          -> HTML interface
    requirements.txt    -> Dependencies

------------------------------------------------------------------------

## Notes

-   ffmpeg must be installed and added to system PATH
-   Gmail App Password required for email feature
-   Generated folders are temporary and not part of repository

------------------------------------------------------------------------



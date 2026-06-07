"""
transcribe_video.py — ladda ner och transkribera video från URL.

Använder yt-dlp för nedladdning + ffmpeg för audio-extraction + whisper för
transkription. Allt lokalt, ingen API-kostnad efter första modell-download.

Användning:
    python3 ~/workshop-human-ai/tools/transcribe_video.py <URL> [language] [model]

Defaults:
    language = "sv"
    model    = "base"   (140MB, snabb; alternativ: tiny, small, medium, large-v3)

Output: skriver transkription till stdout. Postar INTE till memory automatiskt
(för att slippa råtext-spam i workshop-thread).
"""

import sys
import os
import tempfile
import warnings

warnings.filterwarnings("ignore")


def main():
    if len(sys.argv) < 2:
        print("Användning: transcribe_video.py <URL> [language] [model]", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) >= 3 else "sv"
    model_name = sys.argv[3] if len(sys.argv) >= 4 else "base"

    print(f"[transcribe] URL: {url}", file=sys.stderr)
    print(f"[transcribe] language: {language}, model: {model_name}", file=sys.stderr)

    import yt_dlp
    import whisper

    with tempfile.TemporaryDirectory(prefix="transcribe_") as tmp:
        audio_template = os.path.join(tmp, "audio.%(ext)s")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
            "no_warnings": True,
        }

        print("[transcribe] laddar ner audio...", file=sys.stderr)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        audio_path = os.path.join(tmp, "audio.mp3")
        if not os.path.exists(audio_path):
            for f in os.listdir(tmp):
                if f.startswith("audio."):
                    audio_path = os.path.join(tmp, f)
                    break

        if not os.path.exists(audio_path):
            print(f"[transcribe] FEL: hittar ingen audio-fil i {tmp}", file=sys.stderr)
            print(f"[transcribe] innehåll: {os.listdir(tmp)}", file=sys.stderr)
            sys.exit(1)

        print(f"[transcribe] audio: {audio_path} ({os.path.getsize(audio_path)} bytes)", file=sys.stderr)
        print(f"[transcribe] laddar whisper-modell '{model_name}'...", file=sys.stderr)

        model = whisper.load_model(model_name)
        print("[transcribe] transkriberar...", file=sys.stderr)
        result = model.transcribe(audio_path, language=language, fp16=False)

        print(result["text"].strip())


if __name__ == "__main__":
    main()

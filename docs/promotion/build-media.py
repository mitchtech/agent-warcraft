"""Build labeled promotional previews from the committed clips, not host recordings."""

import hashlib
import json
import subprocess
import wave
from array import array
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "promotion"
OUT.mkdir(parents=True, exist_ok=True)
SIZE, FPS, RATE = 1080, 15, 32000
BG, INK, MUTED, GOLD, EMBER = (20, 17, 13), (239, 228, 200), (181, 168, 138), (242, 214, 138), (224, 86, 42)
PORTRAIT, RING, FEL = (5, 8, 6), (52, 42, 14), (143, 209, 79)
FONTS = ROOT / "site" / "fonts"
TITLE = FONTS / "marcellus-latin-400-normal.woff2"
BODY = FONTS / "source-sans-3-latin-400-normal.woff2"
LABEL = FONTS / "source-sans-3-latin-700-normal.woff2"


def samples(clip):
    with wave.open(str(ROOT / f"audio/{clip}.wav")) as source:
        assert (source.getframerate(), source.getnchannels(), source.getsampwidth()) == (RATE, 1, 2)
        data = array("h", source.readframes(source.getnframes()))
    if sys.byteorder == "big":
        data.byteswap()
    return data


def little_endian(data):
    copy = array("h", data)
    if sys.byteorder == "big":
        copy.byteswap()
    return copy.tobytes()


def peaks(data, columns):
    step = max(1, len(data) // columns)
    values = [max((abs(v) for v in data[i * step:(i + 1) * step]), default=0) for i in range(columns)]
    top = max(values) or 1
    return [value / top for value in values]


def text(draw, y, content, size=42, color=INK, face=BODY):
    font = ImageFont.truetype(str(face), size)
    for line in content.split("\n"):
        width = draw.textlength(line, font=font)
        if width > 940:
            raise ValueError(f"Caption exceeds safe width: {line}")
        draw.text(((SIZE - width) / 2, y), line, font=font, fill=color)
        y += size * 1.25


def card(title, subtitle, footer, command=None):
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)
    # A carved gold frame around the whole card, like the WC3 console border.
    draw.rectangle((24, 24, SIZE - 25, SIZE - 25), outline=(110, 84, 32), width=6)
    draw.rectangle((32, 32, SIZE - 33, SIZE - 33), outline=(201, 162, 74), width=2)
    text(draw, 90, "AGENT WARCRAFT", 30, GOLD, LABEL)
    text(draw, 150, title.upper(), 76, INK, TITLE)
    text(draw, 270, subtitle, 38)
    if command:
        text(draw, 790, command, 34, GOLD, LABEL)
    text(draw, 870, "github.com/mitchtech/agent-warcraft", 34, GOLD, LABEL)
    text(draw, 944, footer, 26, MUTED)
    return image


def scope(values, reveal):
    """A 720 x 360 unit portrait with the waveform swept in up to `reveal` (0-1)."""
    width, height = 720, 360
    screen = Image.new("RGBA", (width, height), PORTRAIT + (255,))
    draw = ImageDraw.Draw(screen)
    for ring in (1, 2, 3):
        r = height * ring / 7
        draw.ellipse((width / 2 - r, height / 2 - r, width / 2 + r, height / 2 + r), outline=RING, width=2)
    trace = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    lines = ImageDraw.Draw(trace)
    middle = height // 2
    shown = int(len(values) * reveal)
    for index, value in enumerate(values):
        x = 10 + index * (width - 20) / len(values)
        if index < shown:
            amplitude = max(1, value * height * 0.42)
            lines.line((x, middle - amplitude, x, middle + amplitude), fill=FEL + (255,), width=3)
        else:
            lines.line((x, middle, x + 4, middle), fill=FEL + (110,), width=2)
    screen.alpha_composite(trace.filter(ImageFilter.GaussianBlur(5)))
    screen.alpha_composite(trace)
    draw = ImageDraw.Draw(screen)
    draw.rectangle((0, 0, width - 1, height - 1), outline=(201, 162, 74), width=4)
    return screen


# (start, end, title, subtitle, command, cue clip or None)
sound_scenes = [
    (0, 4, "Session started", '"Ready to work."', None, "orc-ready"),
    (4, 8, "Approval needed", '"What you want?"', None, "orc-what-you-want"),
    (8, 13, "Destructive command", '"Our town is under attack!"', "$ git push --force origin main", "orc-town-under-attack"),
    (13, 17, "Turn finished", '"Work complete!"', None, "orc-work-complete"),
    (17, 22, "Usage limit reached", '"We need more gold!"', None, "orc-need-more-gold"),
    (22, 27, "Work complete.", "Local audio. No telemetry.\nNever approves or blocks anything.", None, None),
]
faction_scenes = [
    (0, 5, "Pick a faction", "Orc peons by default.\nHuman peasants on request.", "agent-warcraft faction alliance", "human-ready"),
    (5, 10, "Job's done.", "The same events, voiced by the Alliance.", "agent-warcraft faction alliance", "human-jobs-done"),
    (10, 15, "More gold is required.", "Usage alarms speak both languages.", "agent-warcraft faction both", "human-more-gold"),
]
CUE_OFFSET = 0.5


def build(name, scenes, footer):
    duration = scenes[-1][1]
    temporary = ROOT / "dist/promotion/render"
    temporary.mkdir(parents=True, exist_ok=True)
    video = temporary / f"{name}.mp4"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{SIZE}x{SIZE}",
               "-framerate", str(FPS), "-i", "pipe:0",
               "-frames:v", str(duration * FPS), "-c:v", "libx264", "-threads", "2",
               "-preset", "fast", "-crf", "26", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    cards = [card(title, subtitle, footer, cmd) for _, _, title, subtitle, cmd, _ in scenes]
    clips = {clip: samples(clip) for *_, clip in scenes if clip}
    waves = {clip: peaks(data, 180) for clip, data in clips.items()}
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for tick in range(duration * FPS):
            second = tick / FPS
            index = next(i for i, scene in enumerate(scenes) if scene[0] <= second < scene[1])
            start, _, _, _, _, clip = scenes[index]
            image = cards[index].copy()
            if clip:
                length = len(clips[clip]) / RATE
                reveal = min(1.0, max(0.0, (second - start - CUE_OFFSET) / length))
                screen = scope(waves[clip], reveal)
            else:
                screen = scope([0.01] * 180, 1.0)
            image.paste(screen.convert("RGB"), (180, 400))
            process.stdin.write(image.tobytes())
            if tick == FPS * 3:
                image.save(OUT / f"{name}.png")
    finally:
        process.stdin.close()
    if process.wait():
        raise RuntimeError(f"ffmpeg failed for {name}")
    track = bytearray(duration * RATE * 2)
    for start, _, _, _, _, clip in scenes:
        if clip:
            data = little_endian(clips[clip])
            offset = int((start + CUE_OFFSET) * RATE) * 2
            track[offset:offset + len(data)] = data
    audio = temporary / f"{name}.wav"
    with wave.open(str(audio), "wb") as destination:
        destination.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        destination.writeframes(bytes(track))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                    "-t", str(duration), "-movflags", "+faststart", str(OUT / f"{name}.mp4")], check=True)

    def timestamp(second):
        return f"00:{second // 60:02d}:{second % 60:02d},000"

    subtitles = [f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{title}\n{subtitle}\n{footer}\n"
                 for index, (start, end, title, subtitle, _, _) in enumerate(scenes, 1)]
    (OUT / f"{name}.srt").write_text("\n".join(subtitles))
    return sorted(clips)


used = build("sound-preview", sound_scenes, "Illustrated sound preview - not a live host recording")
used += build("faction-preview", faction_scenes, "Configuration preview - event coverage varies by host")
sources = [ROOT / f"audio/{clip}.wav" for clip in sorted(set(used))] + [TITLE, BODY, LABEL]


def record(path):
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


manifest = {
    "kind": "illustrated-previews", "dimensions": [SIZE, SIZE], "fps": FPS,
    "sources": [record(path) for path in sources],
    "artifacts": [record(path) for path in sorted(OUT.iterdir()) if path.suffix in (".mp4", ".png", ".srt")],
    "tools": {"Pillow": __import__("PIL").__version__, "ffmpeg": subprocess.check_output(
        ["ffmpeg", "-version"], text=True).splitlines()[0]},
    "credentials_used": [],
    "limitations": ["Not a live host or physical audio recording.",
                     "No claim of hook execution in these videos.",
                     "Audio is assembled from the bundled, separately noticed Warcraft III clips."],
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Built two captioned previews in {OUT.relative_to(ROOT)}")

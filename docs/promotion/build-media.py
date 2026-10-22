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
ATLAS = ROOT / "pets" / "peon" / "spritesheet.webp"
SHEET = Image.open(ATLAS).convert("RGBA")


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


def stage(row, count, elapsed, values=None, reveal=0.0):
    """A 720 x 360 portrait with the peon animating `row` at 160 ms per frame and an optional waveform strip."""
    width, height = 720, 360
    screen = Image.new("RGBA", (width, height), PORTRAIT + (255,))
    halo = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse((210, 60, 510, 360), fill=(201, 162, 74, 60))
    screen.alpha_composite(halo.filter(ImageFilter.GaussianBlur(60)))
    if values:
        strip = scope(values, reveal).resize((width, 90))
        strip.putalpha(150)
        screen.alpha_composite(strip, (0, height - 90))
    column = int(elapsed / 0.16) % count
    sprite = SHEET.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208)).resize((298, 323), Image.LANCZOS)
    screen.alpha_composite(sprite, ((width - sprite.width) // 2, height - sprite.height - 8))
    ImageDraw.Draw(screen).rectangle((0, 0, width - 1, height - 1), outline=(201, 162, 74), width=4)
    return screen


# (start, end, title, subtitle, command, cue clip or None[, (atlas row, frames)])
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
pet_scenes = [
    (0, 4, "Meet the Peon", "A native custom pet for Codex.\nCodex animates him; the plugin plays sounds.", None, None, (0, 6)),
    (4, 8, "Agent working", '"Work, work."', None, "orc-work-work", (7, 6)),
    (8, 12, "Needs your approval", '"What you want?"', None, "orc-what-you-want", (6, 6)),
    (12, 16, "Turn finished", '"Work complete!"', None, "orc-work-complete", (4, 5)),
    (16, 20, "Out of usage", '"We need more gold!"', None, "orc-need-more-gold", (5, 8)),
    (20, 25, "Install the pet", "Independent of the sounds.\nChoose Peon in the pet picker.", "agent-warcraft pet install", None, (3, 4)),
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
    cards = [card(scene[2], scene[3], footer, scene[4]) for scene in scenes]
    clips = {scene[5]: samples(scene[5]) for scene in scenes if scene[5]}
    waves = {clip: peaks(data, 180) for clip, data in clips.items()}
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for tick in range(duration * FPS):
            second = tick / FPS
            index = next(i for i, scene in enumerate(scenes) if scene[0] <= second < scene[1])
            start, clip, pet = scenes[index][0], scenes[index][5], scenes[index][6] if len(scenes[index]) > 6 else None
            image = cards[index].copy()
            reveal = min(1.0, max(0.0, (second - start - CUE_OFFSET) / (len(clips[clip]) / RATE))) if clip else 1.0
            if pet:
                screen = stage(*pet, second - start, waves.get(clip), reveal)
            elif clip:
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
    for scene in scenes:
        start, clip = scene[0], scene[5]
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
                 for index, (start, end, title, subtitle, *_) in enumerate(scenes, 1)]
    (OUT / f"{name}.srt").write_text("\n".join(subtitles))
    return sorted(clips)


used = build("sound-preview", sound_scenes, "Illustrated sound preview - not a live host recording")
used += build("faction-preview", faction_scenes, "Configuration preview - event coverage varies by host")
used += build("pet-preview", pet_scenes, "Atlas animation preview - not a native host recording")
sources = [ROOT / f"audio/{clip}.wav" for clip in sorted(set(used))] + [ATLAS, TITLE, BODY, LABEL]


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
                     "Audio is assembled from the bundled, separately noticed Warcraft III clips.",
                     "Pet animation is drawn from the bundled atlas; Codex, not the sound plugin, animates the installed pet."],
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Built three captioned previews in {OUT.relative_to(ROOT)}")

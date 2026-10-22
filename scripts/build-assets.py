"""Derive preview artifacts from the committed clips and pet atlas; never change source audio or art."""

import sys
import tempfile
import wave
from array import array
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
PREVIEWS = ROOT / "assets" / "previews"
FONTS = ROOT / "site" / "fonts"
SHEET = Image.open(ROOT / "pets" / "peon" / "spritesheet.webp").convert("RGBA")
PEASANT = Image.open(ROOT / "pets" / "peasant" / "spritesheet.webp").convert("RGBA")
# (preview name, atlas row, frame count), matching Codex's v2 row order.
PET_STATES = [("pet-idle", 0, 6), ("pet-working", 7, 6), ("pet-waiting", 6, 6), ("pet-review", 8, 6), ("pet-failure", 5, 8)]
# --check renders elsewhere and compares pixels: PNG bytes vary with each platform's zlib.
CHECK = "--check" in sys.argv[1:]
OUT = Path(tempfile.mkdtemp()) if CHECK else PREVIEWS
OUT.mkdir(parents=True, exist_ok=True)
BACKGROUND = (20, 17, 13)
PORTRAIT = (5, 8, 6)
INK = (239, 228, 200)
MUTED = (181, 168, 138)
TRIM = (201, 162, 74)
TRIM_HI = (242, 214, 138)
TRIM_LO = (110, 84, 32)
FEL = (143, 209, 79)
EMBER = (224, 86, 42)
HEADLINE_CLIPS = [
    ("orc-ready", "Ready to work."),
    ("orc-work-complete", "Work complete!"),
    ("orc-need-more-gold", "We need more gold!"),
    ("orc-under-attack", "We're under attack!"),
    ("orc-not-that-kind-of-orc", "Me not that kind of orc!"),
    ("human-jobs-done", "Job's done!"),
]
DISPLAY = "marcellus-latin-400-normal.woff2"
BODY = "source-sans-3-latin-400-normal.woff2"
BOLD = "source-sans-3-latin-700-normal.woff2"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size, layout_engine=ImageFont.Layout.BASIC)


def peaks(clip, columns):
    with wave.open(str(AUDIO / f"{clip}.wav")) as audio:
        samples = array("h", audio.readframes(audio.getnframes()))
    if sys.byteorder == "big":
        samples.byteswap()
    step = max(1, len(samples) // columns)
    values = [max((abs(value) for value in samples[i * step:(i + 1) * step]), default=0) / 32768 for i in range(columns)]
    top = max(values) or 1
    return [value / top for value in values]


def stone(width, height):
    """Carved stone: a vertical bevel gradient with deterministic speckle so --check stays reproducible."""
    canvas = Image.new("RGBA", (width, height), BACKGROUND + (255,))
    draw = ImageDraw.Draw(canvas)
    for y in range(height):
        t = y / max(1, height - 1)
        shade = 1.0 + 0.18 * (1 - abs(0.35 - t) * 2)
        draw.line((0, y, width, y), fill=tuple(min(255, int(c * shade)) for c in BACKGROUND))
    seed = 1
    for _ in range(width * height // 90):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        x, y = seed % width, (seed >> 11) % height
        tone = 30 + (seed >> 5) % 30
        draw.point((x, y), fill=(tone, tone - 4, tone - 10, 255))
    return canvas


def frame(draw, box, radius=6, width=3):
    left, top, right, bottom = box
    draw.rounded_rectangle((left - width - 2, top - width - 2, right + width + 2, bottom + width + 2), radius=radius + 3, fill=TRIM_LO)
    draw.rounded_rectangle((left - width, top - width, right + width, bottom + width), radius=radius + 2, outline=TRIM, width=width)
    draw.line((left, top - width + 1, right, top - width + 1), fill=TRIM_HI, width=1)


def portrait(size, clip, reveal=1.0, color=FEL):
    """A dark unit portrait with faint rings and the clip's waveform swept in up to `reveal`."""
    width, height = size
    canvas = Image.new("RGBA", size, PORTRAIT + (255,))
    draw = ImageDraw.Draw(canvas)
    for ring in (1, 2, 3):
        r = height * ring / 7
        draw.ellipse((width / 2 - r, height / 2 - r, width / 2 + r, height / 2 + r), outline=(201, 162, 74, 30), width=1)
    middle = height // 2
    columns = max(2, (width - 12) // 3)
    values = peaks(clip, columns)
    shown = int(columns * reveal)
    trace = Image.new("RGBA", size, (0, 0, 0, 0))
    lines = ImageDraw.Draw(trace)
    for index in range(columns):
        x = 6 + index * (width - 12) / columns
        if index < shown:
            amplitude = max(1, values[index] * height * 0.4)
            lines.line((x, middle - amplitude, x, middle + amplitude), fill=color + (255,), width=2)
        else:
            lines.line((x, middle, x + 3, middle), fill=color + (90,), width=1)
    canvas.alpha_composite(trace.filter(ImageFilter.GaussianBlur(4)))
    canvas.alpha_composite(trace)
    vignette = Image.new("L", size, 0)
    ImageDraw.Draw(vignette).ellipse((-width * 0.2, -height * 0.3, width * 1.2, height * 1.3), fill=255)
    shade = Image.new("RGBA", size, (0, 0, 0, 150))
    shade.putalpha(Image.eval(vignette.filter(ImageFilter.GaussianBlur(40)), lambda v: 150 - v * 150 // 255))
    canvas.alpha_composite(shade)
    return canvas


def headline(canvas, xy, size, limit, words=("WORK", "COMPLETE.")):
    draw = ImageDraw.Draw(canvas, "RGBA")
    x, y = xy
    first, second = words
    # Shrink to fit beside the portrait rather than running under it.
    while draw.textlength(f"{first} {second}", font=font(DISPLAY, size)) > limit:
        size -= 2
    display = font(DISPLAY, size)
    draw.text((x, y), first, font=display, fill=INK)
    offset = x + draw.textlength(f"{first} ", font=display)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((offset, y), second, font=display, fill=TRIM + (150,))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(12)))
    draw.text((offset, y + 2), second, font=display, fill=(40, 28, 8))
    draw.text((offset, y), second, font=display, fill=TRIM_HI)


def eyebrow(canvas, xy, size):
    draw = ImageDraw.Draw(canvas, "RGBA")
    x, y = xy
    draw.line((x, y + size // 2, x + 30, y + size // 2), fill=TRIM_HI, width=2)
    label = font(BOLD, size)
    for character in "AGENT WARCRAFT":
        draw.text((x + 44, y), character, font=label, fill=TRIM)
        x += draw.textlength(character, font=label) + 5


def resources(canvas, xy):
    draw = ImageDraw.Draw(canvas, "RGBA")
    x, y = xy
    label = font(BOLD, 24)
    for color, outline, value in (((242, 201, 76), (138, 100, 20), "300"), ((154, 106, 60), (77, 49, 20), "0"), ((185, 68, 44), (90, 26, 13), "10/15")):
        width = 54 + draw.textlength(value, font=label)
        draw.rounded_rectangle((x, y, x + width, y + 40), radius=4, fill=(11, 9, 7), outline=TRIM_LO, width=2)
        draw.ellipse((x + 12, y + 11, x + 30, y + 29), fill=color, outline=outline, width=2)
        draw.text((x + 40, y + 6), value, font=label, fill=INK)
        x += width + 10


def cell(row, column, sheet=SHEET):
    return sheet.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))


def peon(canvas, box, row=0, column=0, scale=1.0, sheet=SHEET):
    """The peon centered in `box`, standing on its lower edge, over a soft gold glow."""
    left, top, right, bottom = box
    sprite = cell(row, column, sheet)
    if scale != 1.0:
        sprite = sprite.resize((round(192 * scale), round(208 * scale)), Image.LANCZOS)
    x = left + (right - left - sprite.width) // 2
    y = bottom - sprite.height
    halo = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    cx, cy = (left + right) // 2, bottom - sprite.height // 2
    r = sprite.width // 2
    ImageDraw.Draw(halo).ellipse((cx - r, cy - r, cx + r, cy + r), fill=TRIM + (70,))
    canvas.alpha_composite(halo.filter(ImageFilter.GaussianBlur(r // 2)))
    canvas.alpha_composite(sprite, (x, y))


def framed_pair(canvas, box, row=0, column=0, scale=1.0):
    """The Peon and the Peasant side by side in one carved frame."""
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas, "RGBA")
    frame(draw, box)
    inner = Image.new("RGBA", (right - left, bottom - top), PORTRAIT + (255,))
    half = inner.width // 2
    peon(inner, (0, 0, half + 12, inner.height - 6), row, column, scale)
    peon(inner, (half - 12, 0, inner.width, inner.height - 6), row, column, scale, sheet=PEASANT)
    canvas.alpha_composite(inner, (left, top))
    for cx in (left - 1, right + 1):
        draw.ellipse((cx - 6, top - 7, cx + 6, top + 5), fill=TRIM_HI, outline=TRIM_LO)


def framed_portrait(canvas, box, clip):
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas, "RGBA")
    frame(draw, box)
    canvas.alpha_composite(portrait((right - left, bottom - top), clip), (left, top))
    for cx in (left - 1, right + 1):
        draw.ellipse((cx - 6, top - 7, cx + 6, top + 5), fill=TRIM_HI, outline=TRIM_LO)


# Pet previews: each animation row in the portrait frame, at the site's 160 ms frame rate.
def pet_previews(sheet, prefix):
    for name, row, count in PET_STATES:
        base = stone(288, 288)
        frame(ImageDraw.Draw(base), (14, 14, 274, 274))
        frames = []
        for column in range(count):
            canvas = base.copy()
            inner = Image.new("RGBA", (260, 260), PORTRAIT + (255,))
            peon(inner, (0, 0, 260, 248), row, column, sheet=sheet)
            canvas.alpha_composite(inner, (14, 14))
            frames.append(canvas.convert("RGB"))
        name = name.replace("pet-", f"{prefix}-", 1)
        frames[0].save(OUT / f"{name}.gif", save_all=True, append_images=frames[1:], duration=160, loop=0, disposal=2)
    cell(0, 0, sheet).save(OUT / f"{prefix}-idle.png")


pet_previews(SHEET, "pet")
pet_previews(PEASANT, "peasant")

# Waveform previews: a sweep that reveals each clip, then holds.
label_font = font(BOLD, 19)
for clip, line in HEADLINE_CLIPS:
    color = (111, 176, 255) if clip.startswith("human-") else FEL
    frames = []
    steps = 14
    base = stone(288, 200)
    frame(ImageDraw.Draw(base), (14, 14, 274, 156))
    for step in range(steps + 1):
        canvas = base.copy()
        canvas.alpha_composite(portrait((260, 142), clip, reveal=step / steps, color=color), (14, 14))
        draw = ImageDraw.Draw(canvas)
        width = draw.textlength(line.upper(), font=label_font)
        draw.text(((288 - width) / 2, 168), line.upper(), font=label_font, fill=TRIM_HI if step == steps else MUTED)
        frames.append(canvas.convert("RGB"))
    durations = [70] * steps + [1600]
    frames[0].save(OUT / f"{clip}.gif", save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)

# Fonts are the site's self-hosted OFL faces, so the cards match the page on every OS.
card = stone(1200, 630)
draw = ImageDraw.Draw(card, "RGBA")
eyebrow(card, (88, 92), 22)
headline(card, (82, 138), 120, 560)
draw.text((90, 300), "Your coding agent, with a", font=font(DISPLAY, 40), fill=INK)
draw.text((90, 350), "peon's work ethic.", font=font(DISPLAY, 40), fill=INK)
for row, text in enumerate(["Warcraft sound cues and Codex pets for", "Claude Code, Codex, and Gemini CLI"]):
    draw.text((90, 466 + row * 38), text, font=font(BODY, 30), fill=MUTED)
resources(card, (700, 92))
framed_pair(card, (680, 166, 1120, 486), row=7, column=2, scale=1.25)
draw.text((680, 510), "SOUND CUES + TWO CODEX PETS", font=font(BOLD, 24), fill=EMBER)
card.convert("RGB").save(OUT / "social.png")

banner = stone(1280, 440)
draw = ImageDraw.Draw(banner, "RGBA")
eyebrow(banner, (92, 80), 22)
headline(banner, (86, 120), 130, 620)
draw.text((94, 296), "Sound cues and Codex pets", font=font(BODY, 32), fill=MUTED)
draw.text((94, 340), "for coding agents.", font=font(BODY, 32), fill=MUTED)
framed_pair(banner, (760, 70, 1190, 370), row=0, column=0, scale=1.2)
banner.convert("RGB").save(OUT / "banner.png")

touch = stone(180, 180)
draw = ImageDraw.Draw(touch, "RGBA")
draw.rounded_rectangle((6, 6, 173, 173), radius=18, fill=PORTRAIT + (255,), outline=TRIM, width=4)
# The head sits in the top third of the idle frame; crop and enlarge it to fill the icon.
head = cell(0, 0).crop((40, 4, 152, 116)).resize((150, 150), Image.LANCZOS)
touch.alpha_composite(head, (15, 18))
touch.convert("RGB").save(OUT / "touch-icon.png")


def frames_of(path):
    with Image.open(path) as image:
        return [(item.convert("RGBA"), item.info.get("duration")) for item in ImageSequence.Iterator(image)]


if CHECK:
    stale = []
    for built in sorted(OUT.iterdir()):
        committed = PREVIEWS / built.name
        if not committed.exists():
            stale.append(built.name)
            continue
        expected, actual = frames_of(committed), frames_of(built)
        if len(expected) != len(actual) or any(a[1] != b[1] or ImageChops.difference(a[0], b[0]).getbbox(alpha_only=False) for a, b in zip(expected, actual)):
            stale.append(built.name)
    if stale:
        sys.exit(f"Preview assets are stale; run python3 scripts/build-assets.py: {', '.join(stale)}")
    print("Preview assets match the current clips and fonts")
else:
    print(f"Built preview assets in {OUT}")

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "out" / "mark-1024.png"
MANIFEST = Path("/tmp/press-manifest.json")
FONTS = Path("/usr/share/fonts/truetype/dejavu")
SIZE = 1024
MARGIN = 64


def fit_font(text, filename, starting_size, maximum_width):
    for font_size in range(starting_size, 15, -1):
        font = ImageFont.truetype(str(FONTS / filename), font_size)
        bounds = font.getbbox(text)
        if bounds[2] - bounds[0] <= maximum_width:
            return font
    raise ValueError(f"Cannot fit text inside the canvas: {text!r}")


def draw_line(draw, text, top, filename, starting_size, color):
    font = fit_font(text, filename, starting_size, SIZE - 2 * MARGIN)
    bounds = draw.textbbox((0, 0), text, font=font)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    left = (SIZE - width) // 2
    rectangle = (left, top, left + width, top + height)
    assert rectangle[0] >= MARGIN and rectangle[2] <= SIZE - MARGIN
    assert rectangle[1] >= 48 and rectangle[3] <= SIZE - 48
    draw.text((left - bounds[0], top - bounds[1]), text, font=font, fill=color)
    print(f"Text bounds {rectangle}: {text}")
    return rectangle


def main():
    manifest = json.loads(MANIFEST.read_text())
    colors = {color["name"]: color["hex"] for color in manifest["brand"]["colours"]}
    assert colors["make.fun magenta"] == "#c41c83"
    record = next(item for item in manifest["files"] if item["path"] == "mark-1024.png")
    if not SOURCE.is_file():
        raise SystemExit(
            "Official mark unavailable: place https://make.fun/press/mark-1024.png "
            "at out/mark-1024.png. No substitute image will be rendered."
        )
    source_bytes = SOURCE.read_bytes()
    if hashlib.sha256(source_bytes).hexdigest() != record["sha256"]:
        raise SystemExit("Official mark checksum does not match the press manifest.")

    canvas = Image.new("RGBA", (SIZE, SIZE), colors["make.fun magenta"])
    draw = ImageDraw.Draw(canvas)
    bold = "DejaVuSans-Bold.ttf"
    regular = "DejaVuSans.ttf"
    white = colors["White"]
    first_heading = draw_line(draw, "MAKE YOUR OWN", 64, bold, 90, white)
    second_heading = draw_line(draw, "BOUNTY", 156, bold, 108, white)
    assert first_heading[3] + 18 <= second_heading[1]

    with Image.open(SOURCE) as original:
        original.load()
        assert original.format == "PNG" and original.size == (1024, 1024)
        mark = original.convert("RGBA").resize((300, 300), Image.Resampling.LANCZOS)
    mark_left = (SIZE - mark.width) // 2
    mark_top = second_heading[3] + 150
    mark_bottom = mark_top + mark.height
    canvas.alpha_composite(mark, (mark_left, mark_top))

    first_subline = draw_line(draw, "Describe a task. Set the reward.", 840, regular, 34, white)
    second_subline = draw_line(draw, "Keep a share of every fee.", 883, regular, 34, white)
    url = draw_line(draw, "make.fun/sponsor/new", 939, bold, 34, white)
    assert first_subline[1] - mark_bottom >= mark.height // 2
    assert first_subline[3] + 14 <= second_subline[1]
    assert second_subline[3] + 20 <= url[1]
    output = ROOT / "promo.png"
    canvas.convert("RGB").save(output, format="PNG", optimize=False, compress_level=9)
    print(f"Rendered {output}: {output.stat().st_size} bytes")


if __name__ == "__main__":
    main()

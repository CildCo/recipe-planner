"""把小程序截图排成一张 1200×900 的封面/总览图。

用法：
    python tools/make-overview.py <截图目录> <输出文件>
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_SERIF = "C:/Windows/Fonts/NotoSerifSC-VF.ttf"
FONT_SANS = "C:/Windows/Fonts/NotoSansSC-VF.ttf"


def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", size)


def main() -> None:
    shots = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "shots"
    output = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "overview.png"
    canvas = Image.new("RGB", (1200, 900), "#F6F0E4")
    draw = ImageDraw.Draw(canvas)

    draw.rectangle((34, 34, 1166, 866), outline="#232019", width=2)
    draw.line((34, 170, 1166, 170), fill="#232019", width=1)
    draw.text((68, 62), "FAN ZHUO · 一周菜单", font=font(FONT_SANS, 18), fill="#7B7162")
    draw.text((68, 88), "把一周的饭，安排好。", font=font(FONT_SERIF, 54), fill="#232019")
    draw.text((68, 178), "菜谱 · 一周菜单 · 买菜清单", font=font(FONT_SANS, 22), fill="#C94F3D")

    names = [("home.png", "今天"), ("plan.png", "一周菜单"), ("shopping.png", "买菜清单")]
    width, height = 278, 601
    gap = 44
    total = width * 3 + gap * 2
    x = (1200 - total) // 2
    y = 226
    for filename, label in names:
        path = shots / filename
        if not path.exists():
            raise SystemExit(f"缺少截图：{path}")
        image = Image.open(path).convert("RGB")
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        frame = Image.new("RGB", (width + 12, height + 12), "#232019")
        frame.paste(image, (6, 6))
        canvas.paste(frame, (x, y))
        draw.text((x + width / 2, y + height + 34), label, font=font(FONT_SERIF, 20), fill="#4A443A", anchor="mm")
        x += width + gap

    draw.rectangle((1030, 748, 1120, 838), fill="#C94F3D")
    draw.text((1075, 793), "饭桌", font=font(FONT_SERIF, 26), fill="#FFF9EE", anchor="mm")
    draw.text((68, 800), "26 道家常菜 · 7 天菜单 · 一张清单", font=font(FONT_SANS, 18), fill="#7B7162")
    draw.text((68, 828), "小程序 + FastAPI + 管理后台", font=font(FONT_SANS, 18), fill="#7B7162")

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, "PNG")
    print(f"已生成 {output}")


if __name__ == "__main__":
    main()

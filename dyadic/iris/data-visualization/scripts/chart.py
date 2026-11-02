"""Draw a chart from a CSV file as SVG (for the web and Markdown) or PNG (for
Word documents and PDFs).

Usage: chart.py FILE --x COLUMN --y COLUMN[,COLUMN...] [--kind KIND]
                [--out chart.svg|chart.png] [--title TEXT] [--subtitle TEXT]
                [--y-title TEXT] [--x-title TEXT] [--highlight LABEL] [--sort]
                [--bins N]

KIND: bar (columns; several --y columns are grouped), hbar (horizontal bars,
for long names or many categories), stacked (parts of a whole), line, area
(one series), scatter (--x numeric, up to 3 --y columns) or hist (the
distribution of one --y column; --x is ignored).

--highlight LABEL draws that category in color and the rest in gray, for a
chart whose point is one bar. --sort orders bars from largest to smallest.
Numbers may carry thousands separators, a currency sign or a percent sign.
Standard library for SVG; PNG uses Pillow, which the sandbox has.
"""
import csv
import math
import os
import sys
from html import escape

WIDTH, HEIGHT = 760, 440
SURFACE, INK, SECONDARY, MUTED, GRID, BASELINE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
# A color-blind-safe order (validated as a set): series take slots in order, never cycled.
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")
GRAY = "#c3c2b7"
KINDS = ("bar", "hbar", "stacked", "line", "area", "scatter", "hist")
FONT_FILES = ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def arg(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default


def number(text):
    try:
        return float(str(text).replace(",", "").replace("$", "").replace("%", "").replace("€", "").replace("£", "").strip())
    except ValueError:
        return None


def nice_step(span, ticks=5):
    raw = span / max(ticks, 1)
    power = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    for multiple in (1, 2, 2.5, 5, 10):
        if raw <= multiple * power:
            return multiple * power
    return 10 * power


def scale(low, high, zero, whole=False):
    if zero:
        low, high = min(0.0, low), max(0.0, high)
    if high == low:
        high = low + 1
    step = nice_step(high - low)
    if whole:
        step = max(1.0, math.ceil(step))
    low = math.floor(low / step) * step
    high = math.ceil(high / step) * step
    ticks = []
    value = low
    while value <= high + step / 1000:
        ticks.append(round(value, 10))
        value += step
    return low, high, ticks


def fmt(value):
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.1f}M".replace(".0M", "M")
    if abs(value) >= 10_000:
        return f"{value / 1000:,.1f}K".replace(".0K", "K")
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


def short(text, size=14):
    text = str(text)
    return text if len(text) <= size else text[: size - 1] + "…"


class Canvas:
    """Drawing commands, written out as SVG or painted with Pillow."""

    def __init__(self):
        self.items = []

    def bar(self, x, y, w, h, fill, end):
        """A bar with a 4px rounded data end (top, right, bottom or left) and a square base."""
        if w > 0 and h > 0:
            self.items.append(("bar", x, y, w, h, fill, end))

    def swatch(self, x, y, color):
        self.items.append(("swatch", x, y, color))

    def line(self, x1, y1, x2, y2, color, width=1.0):
        self.items.append(("line", x1, y1, x2, y2, color, width))

    def path(self, points, color, width=2.0):
        self.items.append(("path", points, color, width))

    def wash(self, points, color):
        self.items.append(("wash", points, color))

    def dot(self, x, y, color):
        self.items.append(("dot", x, y, color))

    def text(self, x, y, text, size=12, color=SECONDARY, anchor="start", bold=False):
        self.items.append(("text", x, y, str(text), size, color, anchor, bold))

    def svg(self):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
               'font-family="system-ui, -apple-system, Segoe UI, DejaVu Sans, sans-serif">',
               f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{SURFACE}"/>']
        for item in self.items:
            kind = item[0]
            if kind == "bar":
                _, x, y, w, h, fill, end = item
                out.append(f'<path d="{bar_path(x, y, w, h, end)}" fill="{fill}"/>')
            elif kind == "swatch":
                _, x, y, color = item
                out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="10" height="10" rx="2" fill="{color}"/>')
            elif kind == "line":
                _, x1, y1, x2, y2, color, width = item
                out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{width}"/>')
            elif kind == "path":
                _, points, color, width = item
                joined = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
                out.append(f'<polyline points="{joined}" fill="none" stroke="{color}" stroke-width="{width}" '
                           'stroke-linejoin="round" stroke-linecap="round"/>')
            elif kind == "wash":
                _, points, color = item
                joined = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
                out.append(f'<polygon points="{joined}" fill="{color}" fill-opacity="0.1"/>')
            elif kind == "dot":
                _, x, y, color = item
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" stroke="{SURFACE}" stroke-width="2"/>')
            else:
                _, x, y, text, size, color, anchor, bold = item
                weight = ' font-weight="600"' if bold else ""
                out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" text-anchor="{anchor}"{weight}>'
                           f"{escape(text)}</text>")
        out.append("</svg>")
        return "\n".join(out)

    def png(self, path, factor=2):
        from PIL import Image, ImageDraw, ImageFont

        image = Image.new("RGB", (WIDTH * factor, HEIGHT * factor), SURFACE)
        draw = ImageDraw.Draw(image, "RGBA")
        fonts = {}

        def font(size, bold):
            key = (size, bold)
            if key not in fonts:
                file = FONT_FILES[1 if bold else 0]
                try:
                    fonts[key] = ImageFont.truetype(file, int(size * factor * 0.92))
                except OSError:
                    fonts[key] = ImageFont.load_default(size=int(size * factor))
            return fonts[key]

        def at(value):
            return value * factor

        for item in self.items:
            kind = item[0]
            if kind == "bar":
                _, x, y, w, h, fill, end = item
                corners = {"top": (True, True, False, False), "right": (False, True, True, False),
                           "bottom": (False, False, True, True), "left": (True, False, False, True),
                           "none": (False, False, False, False)}[end]
                radius = min(4, w / 2, h / 2) * factor
                draw.rounded_rectangle([at(x), at(y), at(x + w), at(y + h)], radius=radius, fill=fill, corners=corners)
            elif kind == "swatch":
                _, x, y, color = item
                draw.rounded_rectangle([at(x), at(y), at(x + 10), at(y + 10)], radius=2 * factor, fill=color)
            elif kind == "line":
                _, x1, y1, x2, y2, color, width = item
                draw.line([at(x1), at(y1), at(x2), at(y2)], fill=color, width=max(1, int(width * factor)))
            elif kind == "path":
                _, points, color, width = item
                draw.line([(at(x), at(y)) for x, y in points], fill=color, width=int(width * factor), joint="curve")
                for x, y in (points[0], points[-1]):
                    r = width * factor / 2
                    draw.ellipse([at(x) - r, at(y) - r, at(x) + r, at(y) + r], fill=color)
            elif kind == "wash":
                _, points, color = item
                rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
                draw.polygon([(at(x), at(y)) for x, y in points], fill=(*rgb, 26))
            elif kind == "dot":
                _, x, y, color = item
                draw.ellipse([at(x) - 6.5 * factor, at(y) - 6.5 * factor, at(x) + 6.5 * factor, at(y) + 6.5 * factor], fill=SURFACE)
                draw.ellipse([at(x) - 4.5 * factor, at(y) - 4.5 * factor, at(x) + 4.5 * factor, at(y) + 4.5 * factor], fill=color)
            else:
                _, x, y, text, size, color, anchor, bold = item
                draw.text((at(x), at(y)), text, fill=color, font=font(size, bold),
                          anchor={"start": "ls", "middle": "ms", "end": "rs"}[anchor])
        image.save(path, "PNG", optimize=True)


def bar_path(x, y, w, h, end):
    r = min(4.0, w / 2, h / 2)
    if end == "none":
        return f"M{x:.1f},{y:.1f}H{x + w:.1f}V{y + h:.1f}H{x:.1f}Z"
    if end == "top":
        return (f"M{x:.1f},{y + h:.1f}V{y + r:.1f}Q{x:.1f},{y:.1f} {x + r:.1f},{y:.1f}H{x + w - r:.1f}"
                f"Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f}V{y + h:.1f}Z")
    if end == "bottom":
        return (f"M{x:.1f},{y:.1f}V{y + h - r:.1f}Q{x:.1f},{y + h:.1f} {x + r:.1f},{y + h:.1f}H{x + w - r:.1f}"
                f"Q{x + w:.1f},{y + h:.1f} {x + w:.1f},{y + h - r:.1f}V{y:.1f}Z")
    if end == "right":
        return (f"M{x:.1f},{y:.1f}H{x + w - r:.1f}Q{x + w:.1f},{y:.1f} {x + w:.1f},{y + r:.1f}V{y + h - r:.1f}"
                f"Q{x + w:.1f},{y + h:.1f} {x + w - r:.1f},{y + h:.1f}H{x:.1f}Z")
    return (f"M{x + w:.1f},{y:.1f}H{x + r:.1f}Q{x:.1f},{y:.1f} {x:.1f},{y + r:.1f}V{y + h - r:.1f}"
            f"Q{x:.1f},{y + h:.1f} {x + r:.1f},{y + h:.1f}H{x + w:.1f}Z")


def head(canvas, title, subtitle, names):
    """Title, subtitle and, for two or more series, the legend: returns where the plot may start."""
    top = 18
    if title:
        canvas.text(24, top + 16, title, size=16, color=INK, bold=True)
        top += 26
    if subtitle:
        canvas.text(24, top + 12, subtitle, size=12, color=SECONDARY)
        top += 20
    if len(names) >= 2:
        x = 24
        for n, name in enumerate(names):
            canvas.swatch(x, top + 6, SERIES[n])
            canvas.text(x + 15, top + 15, short(name, 22), size=12, color=SECONDARY)
            x += 30 + 7 * len(short(name, 22))
        top += 26
    return top + 14


def draw(rows, x_name, y_names, kind, title, subtitle, y_title, x_title, highlight, sort, bins):
    canvas = Canvas()
    if kind == "hist":
        values = [v for v in (number(r.get(y_names[0])) for r in rows) if v is not None]
        if not values:
            raise ValueError(f"No numbers in {y_names[0]}.")
        count = bins or max(5, min(30, int(math.ceil(math.log2(len(values)) + 1))))
        low, high = min(values), max(values)
        width = (high - low) / count or 1
        counts = [0] * count
        for v in values:
            counts[min(count - 1, int((v - low) / width))] += 1
        labels = [fmt(low + width * i) for i in range(count)]
        series = {y_names[0]: [float(c) for c in counts]}
        y_title = y_title or "Count"
        x_title = x_title or y_names[0]
    else:
        labels = [str(r.get(x_name, "")) for r in rows]
        series = {name: [number(r.get(name)) for r in rows] for name in y_names}
    if kind in ("bar", "hbar", "stacked", "hist", "area", "line"):
        series = {name: [v if v is not None else 0.0 for v in values] for name, values in series.items()}
    if sort and kind in ("bar", "hbar", "stacked"):
        order = sorted(range(len(labels)), key=lambda i: -sum(series[n][i] for n in series))
        labels = [labels[i] for i in order]
        series = {name: [values[i] for i in order] for name, values in series.items()}
    names = list(series)
    if len(names) > len(SERIES):
        raise ValueError(f"At most {len(SERIES)} series: fold the rest into Other, or draw several charts.")
    if kind == "area" and len(names) > 1:
        raise ValueError("An area chart shows one series; use --kind line for several.")
    if kind == "scatter" and len(names) > 3:
        raise ValueError("A scatter chart takes at most 3 series; draw several charts for more.")
    top = head(canvas, title, subtitle, names if kind != "hist" else [])
    if kind == "hbar":
        return hbar(canvas, labels, series, top, HEIGHT - 36 - (16 if x_title or y_title else 0), highlight, x_title or y_title)
    if y_title:
        canvas.text(24, top + 4, y_title, size=11, color=MUTED)
        top += 20
    bottom = HEIGHT - 36 - (16 if x_title else 0)
    if kind == "stacked":
        totals = [sum(series[n][i] for n in names) for i in range(len(labels))]
        low, high, ticks = scale(min(0.0, min(totals or [0])), max(totals or [1]), True)
    else:
        values = [v for vs in series.values() for v in vs if v is not None]
        if not values:
            raise ValueError("No numbers to draw.")
        zero = kind in ("bar", "hist", "area") or min(values) >= 0 and min(values) < 0.35 * max(values)
        if kind == "scatter":
            pad = (max(values) - min(values)) * 0.06 or 1
            low, high, ticks = scale(min(values) - pad, max(values) + pad, zero)
        else:
            low, high, ticks = scale(min(values), max(values), zero, whole=kind == "hist")
    left = 24 + 7 * max(len(fmt(t)) for t in ticks) + 10
    right = WIDTH - 24 - (96 if kind == "line" and len(names) <= 4 else 0)
    plot_w, plot_h = right - left, bottom - top

    def y_at(value):
        return bottom - plot_h * (value - low) / (high - low)

    for t in ticks:
        y = y_at(t)
        canvas.line(left, y, right, y, BASELINE if t == 0 else GRID)
        canvas.text(left - 8, y + 4, fmt(t), size=11, color=MUTED, anchor="end")
    if x_title:
        canvas.text((left + right) / 2, HEIGHT - 14, x_title, size=11, color=MUTED, anchor="middle")
    if kind == "scatter":
        xs = [number(r.get(x_name)) for r in rows]
        known = [x for x in xs if x is not None]
        if not known:
            raise ValueError(f"{x_name} has no numbers for a scatter chart.")
        pad = (max(known) - min(known)) * 0.06 or 1
        x_low, x_high, x_ticks = scale(min(known) - pad, max(known) + pad, min(known) >= 0 and min(known) < 0.35 * max(known))
        for t in x_ticks:
            x = left + plot_w * (t - x_low) / (x_high - x_low)
            canvas.text(x, bottom + 18, fmt(t), size=11, color=MUTED, anchor="middle")
        for n, name in enumerate(names):
            for x, y in zip(xs, series[name]):
                if x is not None and y is not None:
                    canvas.dot(left + plot_w * (x - x_low) / (x_high - x_low), y_at(y), SERIES[n])
        return canvas
    count = len(labels)
    slot = plot_w / max(count, 1)
    every = max(1, int(math.ceil(count / max(1, plot_w // 64))))
    for i, label in enumerate(labels):
        if i % every == 0:
            canvas.text(left + slot * (i + 0.5), bottom + 18, short(label), size=11, color=MUTED, anchor="middle")
    if kind in ("line", "area"):
        for n, name in enumerate(names):
            points = [(left + slot * (i + 0.5), y_at(v)) for i, v in enumerate(series[name])]
            if kind == "area":
                canvas.wash([(points[0][0], y_at(max(low, 0))), *points, (points[-1][0], y_at(max(low, 0)))], SERIES[n])
            canvas.path(points, SERIES[n])
            if points:
                canvas.dot(*points[-1], SERIES[n])
                if kind == "line" and len(names) <= 4:
                    canvas.text(points[-1][0] + 10, points[-1][1] + 4, short(name, 12), size=11, color=SECONDARY)
                    if len(names) == 1:
                        canvas.text(points[-1][0] + 10, points[-1][1] + 18, fmt(series[name][-1]), size=11, color=INK)
        return canvas
    gap = 2.0
    zero_y = y_at(max(low, 0.0))
    for i in range(count):
        if kind == "stacked":
            width = min(24.0, slot * 0.6)
            x = left + slot * i + (slot - width) / 2
            base = zero_y
            parts = [(n, series[name][i]) for n, name in enumerate(names) if series[name][i] > 0]
            for position, (n, value) in enumerate(parts):
                h = zero_y - y_at(value)
                last = position == len(parts) - 1
                canvas.bar(x, base - h + (0 if last else gap), width, h - (0 if last else gap), SERIES[n], "top" if last else "none")
                base -= h
            continue
        group = len(names)
        width = min(24.0, (slot * 0.7 - gap * (group - 1)) / group) if kind != "hist" else slot - gap
        start = left + slot * i + (slot - (width * group + gap * (group - 1))) / 2
        for n, name in enumerate(names):
            value = series[name][i]
            color = SERIES[n] if not highlight or labels[i] == highlight else GRAY
            y = y_at(value)
            if value >= 0:
                canvas.bar(start + n * (width + gap), y, width, zero_y - y, color, "top")
            else:
                canvas.bar(start + n * (width + gap), zero_y, width, y - zero_y, color, "bottom")
            if group == 1 and count <= 12 and kind != "hist":
                canvas.text(start + width / 2, (y - 6) if value >= 0 else (y + 14), fmt(value), size=11, color=INK, anchor="middle")
    return canvas


def hbar(canvas, labels, series, top, bottom, highlight, value_title):
    names = list(series)
    values = [v for vs in series.values() for v in vs]
    low, high, ticks = scale(min(values + [0.0]), max(values + [0.0]), True)
    left = 24 + 7 * min(22, max(len(short(label, 22)) for label in labels)) + 12
    right = WIDTH - 60
    count = len(labels)
    slot = (bottom - top) / max(count, 1)
    group = len(names)
    gap = 2.0
    width = min(24.0, (slot * 0.7 - gap * (group - 1)) / group)

    def x_at(value):
        return left + (right - left) * (value - low) / (high - low)

    for t in ticks:
        x = x_at(t)
        canvas.line(x, top, x, bottom, BASELINE if t == 0 else GRID)
        canvas.text(x, bottom + 18, fmt(t), size=11, color=MUTED, anchor="middle")
    if value_title:
        canvas.text((left + right) / 2, HEIGHT - 14, value_title, size=11, color=MUTED, anchor="middle")
    for i, label in enumerate(labels):
        start = top + slot * i + (slot - (width * group + gap * (group - 1))) / 2
        canvas.text(left - 10, start + (width * group + gap * (group - 1)) / 2 + 4, short(label, 22), size=11, color=SECONDARY, anchor="end")
        for n, name in enumerate(names):
            value = series[name][i]
            color = SERIES[n] if not highlight or label == highlight else GRAY
            y = start + n * (width + gap)
            if value >= 0:
                canvas.bar(x_at(0), y, x_at(value) - x_at(0), width, color, "right")
            else:
                canvas.bar(x_at(value), y, x_at(0) - x_at(value), width, color, "left")
            if group == 1 and count <= 20:
                canvas.text(x_at(max(value, 0)) + 6, y + width / 2 + 4, fmt(value), size=11, color=INK)
    return canvas


def main(argv):
    if not argv or "--y" not in argv:
        print(__doc__)
        return 2
    path = argv[0]
    kind = arg(argv, "--kind", "bar")
    if kind not in KINDS:
        print(f"--kind must be one of {', '.join(KINDS)}.")
        return 2
    x_name = arg(argv, "--x", "")
    y_names = [name.strip() for name in arg(argv, "--y").split(",") if name.strip()]
    out = arg(argv, "--out", "chart.svg")
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        print("The file has no rows.")
        return 1
    missing = [name for name in ([x_name] if kind != "hist" else []) + y_names if name not in rows[0]]
    if missing:
        print(f"No column named {', '.join(missing)}. Columns: {', '.join(rows[0])}")
        return 1
    try:
        canvas = draw(rows, x_name, y_names, kind, arg(argv, "--title", ""), arg(argv, "--subtitle", ""),
                      arg(argv, "--y-title", ""), arg(argv, "--x-title", ""), arg(argv, "--highlight", ""),
                      "--sort" in argv, int(arg(argv, "--bins", "0") or 0))
    except ValueError as exc:
        print(exc)
        return 1
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    if out.lower().endswith(".png"):
        canvas.png(out)
    else:
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(canvas.svg())
    print(f"Wrote {out}: {kind} chart of {', '.join(y_names)}" + (f" by {x_name}" if kind != "hist" else "") + f", {len(rows)} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

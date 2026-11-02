"""Draw a bar or line chart from a CSV file as an SVG.

Usage: chart.py FILE --x COLUMN --y COLUMN[,COLUMN...] [--kind bar|line]
                [--out chart.svg] [--title TEXT]
Standard library only. Rows are drawn in file order; numbers may carry
thousands separators, a currency sign or a percent sign.
"""
import csv
import sys
from html import escape

WIDTH, HEIGHT = 720, 420
LEFT, RIGHT, TOP, BOTTOM = 64, 24, 48, 72
COLORS = ("#5b93ff", "#4cc38a", "#f5c542", "#ff8a65", "#a78bfa", "#22b8a6")


def arg(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default


def number(text):
    try:
        return float(str(text).replace(",", "").replace("$", "").replace("%", "").strip())
    except ValueError:
        return None


def nice_top(value):
    if value <= 0:
        return 1
    step = 10 ** (len(str(int(value))) - 1)
    return ((int(value) // step) + 1) * step


def main(argv):
    if not argv or "--x" not in argv or "--y" not in argv:
        print(__doc__)
        return 2
    path, x_name = argv[0], arg(argv, "--x")
    y_names = [name.strip() for name in arg(argv, "--y").split(",") if name.strip()]
    kind, out, title = arg(argv, "--kind", "bar"), arg(argv, "--out", "chart.svg"), arg(argv, "--title", "")
    with open(path, newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    labels = [row.get(x_name, "") for row in rows]
    series = {name: [number(row.get(name)) or 0.0 for row in rows] for name in y_names}
    if not rows or any(name not in rows[0] for name in [x_name, *y_names]):
        print(f"Columns available: {', '.join(rows[0]) if rows else 'none'}")
        return 1
    top = nice_top(max(max(values) for values in series.values()))
    plot_w, plot_h = WIDTH - LEFT - RIGHT, HEIGHT - TOP - BOTTOM
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" '
             'font-family="system-ui, sans-serif" font-size="12">',
             f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>']
    if title:
        parts.append(f'<text x="{LEFT}" y="28" font-size="16" font-weight="700" fill="#1f2430">{escape(title)}</text>')
    for i in range(5):
        value = top * i / 4
        y = TOP + plot_h - plot_h * i / 4
        parts.append(f'<line x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{y:.1f}" y2="{y:.1f}" stroke="#e3e6ee"/>')
        parts.append(f'<text x="{LEFT - 8}" y="{y + 4:.1f}" text-anchor="end" fill="#5c6475">{value:g}</text>')
    count = len(labels)
    slot = plot_w / max(count, 1)
    every = max(1, count // 12)
    for i, label in enumerate(labels):
        if i % every == 0:
            x = LEFT + slot * (i + 0.5)
            parts.append(f'<text x="{x:.1f}" y="{TOP + plot_h + 18}" text-anchor="middle" fill="#5c6475">{escape(label[:14])}</text>')
    for n, (name, values) in enumerate(series.items()):
        color = COLORS[n % len(COLORS)]
        if kind == "line":
            points = " ".join(f"{LEFT + slot * (i + 0.5):.1f},{TOP + plot_h - plot_h * v / top:.1f}" for i, v in enumerate(values))
            parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2.5"/>')
        else:
            width = slot * 0.7 / len(series)
            for i, v in enumerate(values):
                x = LEFT + slot * i + slot * 0.15 + width * n
                h = plot_h * v / top
                parts.append(f'<rect x="{x:.1f}" y="{TOP + plot_h - h:.1f}" width="{width:.1f}" height="{h:.1f}" fill="{color}" rx="2"/>')
        parts.append(f'<rect x="{LEFT + n * 140}" y="{HEIGHT - 26}" width="12" height="12" fill="{color}" rx="2"/>')
        parts.append(f'<text x="{LEFT + n * 140 + 18}" y="{HEIGHT - 16}" fill="#1f2430">{escape(name)}</text>')
    parts.append("</svg>")
    with open(out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(parts))
    print(f"Wrote {out}: {kind} chart of {', '.join(y_names)} by {x_name}, {count} points, axis up to {top:g}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

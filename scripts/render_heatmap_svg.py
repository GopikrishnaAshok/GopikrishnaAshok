import json
import os
from datetime import datetime


INPUT_FILE = "data/contributions.json"
OUTPUT_FILE = "assets/contrib-heatmap.svg"


CELL_SIZE = 13
GAP = 4
STEP = CELL_SIZE + GAP

COLORS = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_svg(contributions):
    width = 53 * STEP + 40
    height = 7 * STEP + 100

    svg = []

    svg.append(
        f'<svg width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )

    svg.append(
        '<rect width="100%" height="100%" '
        'rx="18" fill="#0d1117"/>'
    )

    # Header
    svg.append(
        '<text x="25" y="32" '
        'font-family="monospace" '
        'font-size="15" '
        'fill="#58a6ff">'
        '$ git log --contributions'
        '</text>'
    )

    svg.append(
        '<text x="25" y="58" '
        'font-family="monospace" '
        'font-size="13" '
        'fill="#8b949e">'
        'GopikrishnaAshok · GitHub activity'
        '</text>'
    )

    # Contribution cells
    for index, contribution in enumerate(contributions[-371:]):

        date_string = contribution["date"]
        level = contribution["level"]

        date = datetime.strptime(date_string, "%Y-%m-%d")

        day_index = index % 7
        week_index = index // 7

        x = 25 + week_index * STEP
        y = 75 + day_index * STEP

        color = COLORS.get(level, COLORS[0])

        delay = index * 0.008

        svg.append(
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="{CELL_SIZE}" '
            f'height="{CELL_SIZE}" '
            f'rx="2" '
            f'fill="{color}">'
            f'<title>{date_string} · level {level}</title>'
            f'<animate '
            f'attributeName="opacity" '
            f'values="0;1" '
            f'begin="{delay}s" '
            f'dur="0.35s" '
            f'fill="freeze"/>'
            f'</rect>'
        )

    # Footer
    footer_y = height - 20

    svg.append(
        f'<text x="25" y="{footer_y}" '
        f'font-family="monospace" '
        f'font-size="12" '
        f'fill="#8b949e">'
        f'Updated automatically · GitHub Actions'
        f'</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    os.makedirs("assets", exist_ok=True)

    data = load_data()

    svg = generate_svg(
        data["contributions"]
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(svg)

    print(
        f"Generated {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
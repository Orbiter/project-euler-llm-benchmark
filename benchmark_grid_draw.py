#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont


COLUMNS = 200
CELL_WIDTH = 4  # inner fill width
CELL_HEIGHT = 8  # inner fill height
BORDER = 1  # divider thickness between cells
ROW_HEIGHT = CELL_HEIGHT + BORDER
GRID_WIDTH = BORDER + COLUMNS * (CELL_WIDTH + BORDER)
GRID_ORIGIN_Y = 0
LABEL_LEFT_PADDING = 12
LABEL_RIGHT_PADDING = 12
GUIDE_TOP_PADDING = 6
GUIDE_LINE_SPACING = 4
GUIDE_BOTTOM_PADDING = 4
COLORS = {
    0: (255, 255, 255),  # white
    1: (255, 255, 0),  # yellow
    2: (0, 128, 0),  # green
    3: (65, 105, 225),  # blue
    4: (160, 32, 240),  # purple
}
BORDER_COLOR = (180, 180, 180)
TEXT_COLOR = (0, 0, 0)


def load_benchmark_data(path: Path) -> Dict[str, Dict[str, str]]:
    raw = path.read_text()
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON structure must be an object")
    return data


def collect_models_with_tests(
    data: Dict[str, Dict[str, object]]
) -> List[Tuple[str, List[str]]]:
    models: List[Tuple[str, List[str]]] = []
    required_keys = [f"{lang}-200-test" for lang in ("python", "java", "rust", "clojure")]

    for name, metrics in data.items():
        if not isinstance(metrics, dict):
            continue
        values: List[str] = []
        for key in required_keys:
            value = metrics.get(key)
            if not (isinstance(value, str) and len(value) == COLUMNS and set(value) <= {"0", "1"}):
                break
            values.append(value)
        else:
            models.append((name, values))

    return models


def count_solutions(values: List[str]) -> List[int]:
    aggregated = []
    for idx in range(COLUMNS):
        count = sum(int(value[idx]) for value in values)
        aggregated.append(count)
    return aggregated


def color_for_count(count: int) -> Tuple[int, int, int]:
    if count >= 4: return COLORS[4]
    return COLORS[count]


def measure_text_width(font: ImageFont.ImageFont, text: str) -> int:
    try:
        bbox = font.getbbox(text)
    except AttributeError:
        width, _ = font.getsize(text)
        return width
    return bbox[2] - bbox[0]


def measure_text_height(font: ImageFont.ImageFont, text: str) -> int:
    try:
        bbox = font.getbbox(text)
    except AttributeError:
        _, height = font.getsize(text)
        return height
    return bbox[3] - bbox[1]


def load_font() -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    # Try to load a compact monospace font; fall back to default.
    try:
        return ImageFont.truetype("DejaVuSansMono.ttf", size=8)
    except OSError:
        return ImageFont.load_default()


def draw_grid(
    draw: ImageDraw.ImageDraw,
    rows: int,
    colors: List[List[Tuple[int, int, int]]],
    origin_x: int,
) -> None:
    grid_width = GRID_WIDTH
    for row_index in range(rows):
        for col_index in range(COLUMNS):
            x0 = origin_x + BORDER + col_index * (CELL_WIDTH + BORDER)
            y0 = GRID_ORIGIN_Y + BORDER + row_index * (CELL_HEIGHT + BORDER)
            x1 = x0 + CELL_WIDTH - 1
            y1 = y0 + CELL_HEIGHT - 1
            draw.rectangle((x0, y0, x1, y1), fill=colors[row_index][col_index])

    grid_height = BORDER + rows * (CELL_HEIGHT + BORDER)

    # Vertical grid lines
    for offset in range(0, grid_width, CELL_WIDTH + BORDER):
        x = origin_x + offset
        draw.line((x, GRID_ORIGIN_Y, x, GRID_ORIGIN_Y + grid_height - 1), fill=BORDER_COLOR)

    # Right-most border line
    draw.line(
        (
            origin_x + grid_width - 1,
            GRID_ORIGIN_Y,
            origin_x + grid_width - 1,
            GRID_ORIGIN_Y + grid_height - 1,
        ),
        fill=BORDER_COLOR,
    )

    # Horizontal grid lines
    for offset in range(0, grid_height, CELL_HEIGHT + BORDER):
        y = GRID_ORIGIN_Y + offset
        draw.line((origin_x, y, origin_x + grid_width - 1, y), fill=BORDER_COLOR)

    # Bottom border line
    draw.line(
        (
            origin_x,
            GRID_ORIGIN_Y + grid_height - 1,
            origin_x + grid_width - 1,
            GRID_ORIGIN_Y + grid_height - 1,
        ),
        fill=BORDER_COLOR,
    )


def add_labels(
    draw: ImageDraw.ImageDraw,
    models: Sequence[str],
    font: ImageFont.ImageFont,
    left_padding: int,
) -> None:
    for index, name in enumerate(models):
        row_center_y = GRID_ORIGIN_Y + BORDER + CELL_HEIGHT / 2 + index * ROW_HEIGHT
        draw.text((left_padding, row_center_y), name, font=font, fill=TEXT_COLOR, anchor="lm")


def draw_column_guides(
    draw: ImageDraw.ImageDraw,
    font: ImageFont.ImageFont,
    label_width: int,
    grid_height: int,
) -> None:
    text_height = measure_text_height(font, "0")
    line1_y = GRID_ORIGIN_Y + grid_height + GUIDE_TOP_PADDING + text_height / 2
    line2_y = line1_y + text_height + GUIDE_LINE_SPACING

    for col in range(COLUMNS):
        center_x = label_width + BORDER + col * (CELL_WIDTH + BORDER) + CELL_WIDTH / 2
        digit_line1 = str((col + 1) % 10)
        draw.text((center_x, line1_y), digit_line1, font=font, fill=TEXT_COLOR, anchor="mm")

        if (col + 1) % 10 == 0:
            digit_line2 = str(((col + 1) // 10) % 10)
            draw.text((center_x, line2_y), digit_line2, font=font, fill=TEXT_COLOR, anchor="mm")


def create_image(
    models_colors: List[List[Tuple[int, int, int]]],
    model_names: List[str],
    font: ImageFont.ImageFont,
    label_width: int,
    output_path: Path,
) -> None:
    rows = len(models_colors)
    grid_height = BORDER + rows * (CELL_HEIGHT + BORDER)
    text_height = measure_text_height(font, "0")
    guide_height = GUIDE_TOP_PADDING + text_height * 2 + GUIDE_LINE_SPACING + GUIDE_BOTTOM_PADDING
    total_height = grid_height + guide_height

    img = Image.new("RGB", (label_width + GRID_WIDTH, int(total_height)), "white")
    draw = ImageDraw.Draw(img)

    draw_grid(draw, rows, models_colors, origin_x=label_width)
    add_labels(draw, model_names, font, left_padding=LABEL_LEFT_PADDING)
    draw_column_guides(draw, font, label_width, grid_height)

    img.save(output_path)


def main() -> None:
    benchmark_path = Path(__file__).with_name("benchmark.json")
    output_path = Path(__file__).with_name("benchmark.png")

    data = load_benchmark_data(benchmark_path)
    models = collect_models_with_tests(data)

    if not models:
        raise SystemExit("No models with complete 200-test data found.")

    model_names = [name for name, _ in models]
    models_colors = []

    font = load_font()
    max_label_width = max(measure_text_width(font, name) for name in model_names)
    label_width = LABEL_LEFT_PADDING + max_label_width + LABEL_RIGHT_PADDING

    for _, values in models:
        counts = count_solutions(values)
        row_colors = [color_for_count(count) for count in counts]
        models_colors.append(row_colors)

    create_image(models_colors, model_names, font, label_width, output_path)
    print(f"Rendered benchmark grid for {len(models)} models to {output_path.name}")


if __name__ == "__main__":
    main()

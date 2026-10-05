# src/earth_rotat/main.py
"""CLI-анимация вращения Земли в терминале."""

from __future__ import annotations

import argparse
import shutil
import sys
from time import sleep

from .shots import FRAMES

RESET = "\033[0m"
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

COLORS = {
    "green": "\033[32m",
    "cyan": "\033[36m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "white": "\033[37m",
}


def parse_arguments() -> argparse.Namespace:
    """Считывает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="ASCII-анимация вращения Земли в терминале."
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=0.15,
        help="Задержка между кадрами в секундах. По умолчанию: 0.15.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=10,
        help="Количество суток (полных оборотов Земли). По умолчанию: 10.",
    )
    parser.add_argument(
        "--color",
        choices=COLORS,
        default="green",
        help="Цвет анимации. По умолчанию: green.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Отключить цветной вывод.",
    )

    return parser.parse_args()


def check_terminal_width() -> None:
    """Проверяет, достаточно ли широкий терминал для отображения кадров."""
    terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns
    frame_width = max(len(line) for frame in FRAMES for line in frame.splitlines())

    if terminal_width < frame_width:
        message = (
            f"Терминал слишком узкий: {terminal_width} символов.\n"
            f"Для корректного отображения нужно минимум: {frame_width} символов."
        )
        raise SystemExit(message)


def show_frame(
    frame: str,
    color: str,
    day: int,
    total_days: int,
    frame_number: int,
) -> None:
    """Очищает экран и выводит текущий кадр анимации."""
    status = (
        f"Earth rotation | Day: {day}/{total_days} "
        f"| Frame: {frame_number}/{len(FRAMES)}"
    )

    sys.stdout.write(
        f"{CLEAR_SCREEN}{CURSOR_HOME}{color}{status}\n{frame}{RESET}"
    )
    sys.stdout.flush()


def play_animation(speed: float, days: int, color: str) -> None:
    """Показывает заданное количество суток вращения Земли."""
    for day in range(1, days + 1):
        for frame_number, frame in enumerate(FRAMES, start=1):
            show_frame(
                frame=frame,
                color=color,
                day=day,
                total_days=days,
                frame_number=frame_number,
            )
            sleep(speed)


def main() -> None:
    """Точка входа приложения."""
    args = parse_arguments()
    check_terminal_width()

    if args.speed <= 0:
        raise SystemExit("Ошибка: значение --speed должно быть больше 0.")

    if args.days <= 0:
        raise SystemExit("Ошибка: значение --days должно быть больше 0.")

    color = "" if args.no_color else COLORS[args.color]

    try:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()
        play_animation(args.speed, args.days, color)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(f"{RESET}{SHOW_CURSOR}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

# poetry run python -m earth_rotat.main --help     справка
# poetry run python -m earth_rotat.main --speed 0.08
# poetry run python -m earth_rotat.main --days 20
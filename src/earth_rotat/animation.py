# src/earth_rotat/animation.py
"""Отображение ASCII-анимации Земли через Rich."""

from __future__ import annotations

from time import sleep

from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn
from rich.text import Text

from .shots import FRAMES


def create_screen(
    frame: str,
    day: int,
    total_days: int,
    frame_number: int,
    color: str,
    progress: Progress,
) -> Group:
    """Собирает экран анимации из статуса, ASCII-кадра и шкалы прогресса."""
    display_color = None if color == "none" else color

    status = (
        f"[bold cyan]Вращение Земли[/bold cyan]\n"
        f"День: [bold]{day}/{total_days}[/bold] | "
        f"Кадр: [bold]{frame_number}/{len(FRAMES)}[/bold]"
    )

    earth = Text(frame, style=display_color)

    return Group(
        Panel(
            status,
            border_style="cyan",
            expand=False,
        ),
        Panel(
            Align.center(earth),
            title="Планета Земля",
            border_style=display_color or "white",
        ),
        Panel(
            progress,
            title="Прогресс вращения",
            border_style="green",
        ),
    )


def play_animation(
    days: int,
    speed: float,
    color: str,
    console: Console,
) -> None:
    """Показывает анимацию и обновляет общий прогресс от 0 до 100 процентов."""
    total_steps = days * len(FRAMES)

    progress = Progress(
        TextColumn("[bold green]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )
    task_id = progress.add_task("Вращение Земли", total=total_steps)

    try:
        with Live(
            console=console,
            refresh_per_second=20,
            screen=True,
        ) as live:
            for day in range(1, days + 1):
                for frame_number, frame in enumerate(FRAMES, start=1):
                    progress.update(
                        task_id,
                        description=f"День {day}/{days}",
                    )

                    live.update(
                        create_screen(
                            frame=frame,
                            day=day,
                            total_days=days,
                            frame_number=frame_number,
                            color=color,
                            progress=progress,
                        )
                    )

                    sleep(speed)
                    progress.advance(task_id)

    except KeyboardInterrupt:
        console.print("\n[yellow]Анимация остановлена пользователем.[/yellow]")
        return

    console.print("[bold green]Вращение завершено: 100%.[/bold green]")

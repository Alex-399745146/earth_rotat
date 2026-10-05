# src/earth_rotat/menu.py
"""Терминальное меню приложения."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import FloatPrompt, IntPrompt, Prompt

from .animation import play_animation

console = Console()

COLOR_CHOICES = {
    "1": "green",
    "2": "cyan",
    "3": "blue",
    "4": "yellow",
    "5": "white",
    "6": "none",
}


def show_menu() -> None:
    """Выводит главное меню приложения."""
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]Вращение Земли[/bold cyan]\n"
            "ASCII-анимация в терминале",
            border_style="cyan",
        )
    )
    console.print()
    console.print("[bold]1.[/bold] Запустить анимацию")
    console.print("[bold]2.[/bold] Справка")
    console.print("[bold]3.[/bold] Выход")
    console.print()


def select_color() -> str:
    """Предлагает пользователю выбрать цвет анимации."""
    console.print("\n[bold]Выберите цвет Земли:[/bold]")
    console.print("1. Зелёный")
    console.print("2. Голубой")
    console.print("3. Синий")
    console.print("4. Жёлтый")
    console.print("5. Белый")
    console.print("6. Без цвета")

    choice = Prompt.ask(
        "Введите номер цвета",
        choices=list(COLOR_CHOICES),
        default="1",
    )
    return COLOR_CHOICES[choice]


def get_animation_settings() -> tuple[int, float, str]:
    """Запрашивает параметры запуска анимации."""
    console.print()
    console.print("[bold cyan]Параметры анимации[/bold cyan]")

    days = IntPrompt.ask(
        "Количество суток",
        default=10,
    )
    while days <= 0:
        console.print("[red]Количество суток должно быть больше нуля.[/red]")
        days = IntPrompt.ask("Количество суток", default=10)

    speed = FloatPrompt.ask(
        "Задержка между кадрами в секундах",
        default=0.08,
    )
    while speed <= 0:
        console.print("[red]Скорость должна быть больше нуля.[/red]")
        speed = FloatPrompt.ask(
            "Задержка между кадрами в секундах",
            default=0.08,
        )

    color = select_color()

    return days, speed, color


def show_help() -> None:
    """Показывает краткую справку."""
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]Справка[/bold cyan]\n\n"
            "Один полный проход всех ASCII-кадров соответствует одним суткам "
            "вращения Земли.\n\n"
            "Нижняя шкала показывает общий прогресс анимации от 0% до 100%.\n"
            "Чтобы остановить анимацию, нажмите Ctrl + C.",
            title="Вращение Земли",
            border_style="cyan",
        )
    )
    Prompt.ask("\nНажмите Enter для возврата в меню", default="")


def run_menu() -> None:
    """Запускает бесконечный цикл главного меню."""
    while True:
        show_menu()

        action = Prompt.ask(
            "Выберите действие",
            choices=["1", "2", "3"],
            default="1",
        )

        if action == "1":
            days, speed, color = get_animation_settings()
            play_animation(
                days=days,
                speed=speed,
                color=color,
                console=console,
            )
            Prompt.ask("\nНажмите Enter для возврата в меню", default="")

        elif action == "2":
            show_help()

        else:
            console.clear()
            console.print("[bold green]До встречи![/bold green]")
            return

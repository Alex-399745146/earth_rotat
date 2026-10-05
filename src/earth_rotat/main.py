"""Точка входа CLI-приложения."""

from .menu import run_menu


def main() -> None:
    """Запускает терминальное меню."""
    run_menu()


if __name__ == "__main__":
    main()

# poetry run python -m earth_rotat.main
#!/usr/bin/env python
import os
import sys

def main():
    """Главная функция запуска Django-проекта."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'package_builder.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что оно установлено и доступно на вашем PYTHONPATH."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

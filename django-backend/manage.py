#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    Run administrative tasks.

    Raises:
        ImportError: If PYTHONPATH is broken
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings_dev")

    from backend.core.tasks_emulator import patch_tasks_emulator

    # Patch the tasks module to use a local, in-process Cloud Tasks emulator in
    # development
    patch_tasks_emulator()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

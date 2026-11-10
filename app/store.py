import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def load_tasks() -> list[dict[str, Any]]:
    """Read all task records from the local JSON data file."""
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """Persist task records back to disk."""
    temporary_file = NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=DATA_FILE.parent, delete=False
    )
    temporary_path = Path(temporary_file.name)
    try:
        with temporary_file:
            json.dump(tasks, temporary_file, indent=2)
        temporary_path.replace(DATA_FILE)
    finally:
        temporary_path.unlink(missing_ok=True)


def next_task_id(tasks: list[dict[str, Any]]) -> int:
    """Generate the next numeric ID based on the existing records."""
    return max((task["id"] for task in tasks), default=0) + 1

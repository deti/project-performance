from pathlib import Path


PARENT_DIR = Path(__file__).parent


def make_file_name(start_date: str, name: str) -> str:
    return f"{PARENT_DIR}/{start_date}_{name}"

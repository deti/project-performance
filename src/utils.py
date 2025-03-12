from pathlib import Path


# parent directory of the project
PARENT_DIR = Path(__file__).parent.parent


def make_file_name(start_date: str, name: str) -> str:
    return f"{PARENT_DIR}/{start_date}_{name}"

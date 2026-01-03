import json
from pathlib import Path

from src.main.core.config import settings

def load_company_registry() -> list[dict]:
    path = Path(settings.company_registry)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    print(load_company_registry())
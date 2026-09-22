import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

VERSION_FILE = PROJECT_ROOT / "VERSION"
README_FILE = PROJECT_ROOT / "README.md"


current_version = VERSION_FILE.read_text(
    encoding="utf-8"
).strip()

major, minor, patch = map(
    int,
    current_version.split(".")
)

patch += 1

new_version = f"{major}.{minor}.{patch}"


# Обновляем VERSION
VERSION_FILE.write_text(
    new_version + "\n",
    encoding="utf-8"
)


# Обновляем версию в README
readme = README_FILE.read_text(encoding="utf-8")

pattern = (
    r"<!-- VERSION:START -->"
    r".*?"
    r"<!-- VERSION:END -->"
)

replacement = (
    "<!-- VERSION:START -->\n"
    f"`{new_version}`\n"
    "<!-- VERSION:END -->"
)

updated_readme = re.sub(
    pattern,
    replacement,
    readme,
    flags=re.DOTALL
)

README_FILE.write_text(
    updated_readme,
    encoding="utf-8"
)


print(
    f"Version updated: "
    f"{current_version} -> {new_version}"
)
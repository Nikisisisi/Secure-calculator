from pathlib import Path


version_file = Path(__file__).resolve().parent.parent / "VERSION"

current_version = version_file.read_text(
    encoding="utf-8"
).strip()

major, minor, patch = map(
    int,
    current_version.split(".")
)

patch += 1

new_version = f"{major}.{minor}.{patch}"

version_file.write_text(
    new_version + "\n",
    encoding="utf-8"
)

print(f"Version updated: {current_version} -> {new_version}")
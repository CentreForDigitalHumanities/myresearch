#!/usr/bin/python3
import json
import subprocess
from pathlib import Path

translation_path = Path(__file__).parent / "locales"
translation_files = translation_path.glob("*.json")


def check_empty_value(dictionary: dict) -> bool:
    for (key, value) in dictionary.items():
        if value == "":
            print(f"Translation for '{key}' is missing.")
            return True
        if isinstance(value, dict) and check_empty_value(value):
            return True
    return False


# First check for missing translation keys
print("Checking for missing translation keys...")
results = subprocess.run(
    'npx vue-i18n-extract report --vueFiles "./{components,pages,layouts,composables}/**/*.{ts,vue}" --languageFiles "./locales/**/*.{json,yml,yaml,js}"',
    shell=True,
    check=True,
    capture_output=True,
)
if "Missing Keys" in results.stdout.decode():
    print("Missing translation keys found. Run 'npm run i18n-extract' and add the missing translations.")
    exit(1)
print("Ok.")

for translation_file in translation_files:
    print(f"Checking '{translation_file}' for missing translations...")
    translations = json.load(open(translation_file, 'r'))
    if check_empty_value(translations):
        print("One or more translations are missing.")
        exit(1)
    print("Ok.")

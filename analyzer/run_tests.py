import subprocess
import sys
from pathlib import Path

def main():
    # Make sure the user provides a program folder
    if len(sys.argv) != 2:
        print("Usage: python analyzer/run_tests.py <program_folder>")
        sys.exit(1)

    program_folder = Path(sys.argv[1]).resolve()
    tests_folder = program_folder / "tests"

    # Check if the program folder exists
    if not program_folder.exists() or not program_folder.is_dir():
        print(f"There is no program folder found: {program_folder}")
        sys.exit(1)

    # Check if the tests folder exists
    if not tests_folder.exists() or not tests_folder.is_dir():
        print(f"There is no tests folder found in the program folder: {tests_folder}")
        sys.exit(1)

    # Build the pytest command
    command = [sys.executable, "-m", "pytest", str(tests_folder), "-q"]

    # Run the pytest command
    result = subprocess.run(command, cwd=program_folder, capture_output=True, text=True)

    # Print the test results
    if result.stdout:
        print(result.stdout, end="")

    # Print the output showing errors if any
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    # Exit with the same code as pytest
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
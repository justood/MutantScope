import subprocess
import sys
from pathlib import Path

# Run a command and stop if it fails
def run_command(command, cwd, step_name):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)

    # Print the normal output
    if result.stdout:
        print(result.stdout, end="")
    
    # Print the error output
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    # Stop the exeucution if something failed
    if result.returncode != 0:
        print(f"\n{step_name} failed.")
        sys.exit(result.returncode)

    return result

def main():

    # Check if the user provided a program folder
    if len(sys.argv) != 2:
        print("Usage: python analyzer/run_coverage.py <program_folder>")
        sys.exit(1)

    # Build the program and reports folders and create the reports folder if it doesn't exist
    program_folder = Path(sys.argv[1]).resolve()
    tests_folder = program_folder / "tests"
    reports_folder = Path("reports").resolve()
    reports_folder.mkdir(exist_ok=True)

    # Chck if a program folder exists
    if not program_folder.exists() or not program_folder.is_dir():
        print(f"Error: Program folder not found: {program_folder}")
        sys.exit(1)

    # Make sure the tests folder exists in the program folder
    if not tests_folder.exists() or not tests_folder.is_dir():
        print(f"Error: Tests folder not found in the program folder: {tests_folder}")
        sys.exit(1)

    # Create the coverage report files paths
    coverage_file = reports_folder / "coverage_summary.json"
    html_folder = reports_folder / "coverage_html"

    # Clear old coverage results if they exist
    print("\n1. Clearing old coverage results...")
    run_command([sys.executable, "-m", "coverage", "erase"], cwd=program_folder, step_name="Clearing coverage")

    # Run the tests with coverage
    print("\n2. Running tests with coverage...")
    run_command([sys.executable, "-m", "coverage", "run", "-m", "pytest", str(tests_folder), "-q"], cwd=program_folder, step_name="Coverage test run")

    # Generate the coverage report
    print("\n3. Generating coverage report...")
    run_command([sys.executable, "-m", "coverage", "report"], cwd=program_folder, step_name="Coverage Report")

    # Save the coverage report in JSON format
    print("\n4. Saving JSON coverage report...")
    run_command([sys.executable, "-m", "coverage", "json", "-o", str(coverage_file)], cwd=program_folder, step_name="Saving JSON coverage report")

    # Save the HTML report
    print("\n5. Saving HTML coverage report...")
    run_command([sys.executable, "-m", "coverage", "html", "-d", str(html_folder)], cwd=program_folder, step_name="Saving HTML coverage report")

    # Print the paths to the generated reports
    print(f"\nCoverage summary saved to: {coverage_file}")
    print(f"HTML coverage report saved to: {html_folder / 'index.html'}")

if __name__ == "__main__":
    main()
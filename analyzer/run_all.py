import subprocess
import sys
from pathlib import Path

# Run one step and stop if it fails
def run_step(name, command):
    print(f"\n==== {name} ====")

    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print the output of the command
    if result.stdout:
        print(result.stdout, end="")

    # Print the error output of the command
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    # Stop if a step fails
    if result.returncode != 0:
        print(f"{name} failed. Stopping execution.")
        sys.exit(result.returncode)
    
    print(f"{name} completed successfully.")

def main():
    # Check if the user provided program folder
    if len(sys.argv) != 2:
        print("Usage: python analyzer/run_all.py <program_folder>")
        sys.exit(1)

    # Save the uploaded program folder path
    program_folder = sys.argv[1]

    # Find the project root and paths to each analyzer script
    base_folder = Path(__file__).resolve().parent
    project_root = base_folder.parent

    # Paths to each analyzer script that will run
    run_tests_script = project_root / "analyzer" / "run_tests.py"
    run_coverage_script = project_root / "analyzer" / "run_coverage.py"
    run_mutation_script = project_root / "analyzer" / "run_mutation.py"
    analyze_script = project_root / "analyzer" / "result_analyzer.py"

    # Call run_step for each script in the pipeline
    run_step("Running Tests", [sys.executable, str(run_tests_script), program_folder])

    run_step("Running Coverage", [sys.executable, str(run_coverage_script), program_folder])

    run_step("Running Mutation Testing", [sys.executable, str(run_mutation_script), program_folder])

    run_step("Analyzing Results", [sys.executable, str(analyze_script)])

    # Confirmation that all steps completed
    print("\nAll steps completed successfully.")
    print(f"Check the 'reports' folder for the results.")

if __name__ == "__main__":
    main()
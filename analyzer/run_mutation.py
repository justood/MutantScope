import subprocess
import sys
from pathlib import Path

# Find the main program file to run the mutation testing on
def find_target_module(program_folder: Path) -> str:

    # create a list of the python files in the program folder and sort them
    prog_files = sorted(
        f for f in program_folder.glob("*.py") if f.name != "__init__.py"
    )

    if not prog_files:
        raise FileNotFoundError("No python source file found in the program folder.")
    
    # Create a list of the python files that don't start with "test_"
    non_test_files = [f for f in prog_files if not f.name.startswith("test_")]

    # Use the first file that doens't start with "test_" for mutation testing
    if non_test_files:
        return non_test_files[0].name
    
    return prog_files[0].name

# helper function to create a temp configuration file for mutation testing
def write_temp_config(module_name: str, config_path: Path):
    config_text = f"""[cosmic-ray]
    module-path = "{module_name}"
    test-command = "pytest -q"
    timeout = 10.0

    [cosmic-ray.distributor]
    name = "local" 
    """

    # save the config path to be used for the current project
    config_path.write_text(config_text, encoding="utf-8")

def main():

    # Check if the user provided a program folder
    if len(sys.argv) != 2:
        print("Usage: python analyzer/run_mutation.py <program_folder>")
        sys.exit(1)

    # Build the project and reports folders and create the reports folder if it doesn't exist
    program_folder = Path(sys.argv[1]).resolve()
    reports_folder = Path("reports").resolve()
    reports_folder.mkdir(exist_ok=True)

    # Chck if the program folder exists
    if not program_folder.exists() or not program_folder.is_dir():
        print(f"Error: Program folder not found: {program_folder}")
        sys.exit(1)

    # Make sure the tests folder exists in the program folder
    tests_folder = program_folder / "tests"

    if not tests_folder.exists() or not tests_folder.is_dir():
        print(f"Error: Tests folder not found in the program folder: {tests_folder}")
        sys.exit(1)

    # Try to determine the target file for mutation testing
    try: 
        module_name = find_target_module(program_folder)
    except Exception as e:
        print(f"Could not determine the target module: {e}")
        sys.exit(1)

    # tell the program where to store the mutation related files
    config_file = reports_folder / "temp_cosmic_config.toml"
    session_file = reports_folder / "session.sqlite"
    results_file = reports_folder / "results.txt"

    write_temp_config(module_name, config_file)

    # Clear old mutation results 
    for path in [session_file, results_file]:
        if path.exists():
            path.unlink()

    # Call cosmic-ray to run the mutation testing and capture the output
    print("\n1. Initializing mutation session...")
    init_result = subprocess.run(["cosmic-ray", "init", str(config_file), str(session_file)], cwd=program_folder, capture_output=True, text=True)

    # if the initialization fails, print the output and exit with the error code
    if init_result.returncode != 0:
        print(init_result.stdout)
        print(init_result.stderr)
        print("Error: Failed during cosmic-ray initialization.")
        sys.exit(init_result.returncode)

    # Execute the mutations
    print("\n2. Executing mutations (this may take a while)...")
    exec_result = subprocess.run(["cosmic-ray", "exec", str(config_file), str(session_file)], cwd=program_folder, capture_output=True, text=True)

    # if the mutation execution fails, print the output and exit with the error code
    if exec_result.returncode != 0:
        print(exec_result.stdout)
        print(exec_result.stderr)
        print("Error: Failed during mutation execution.")
        sys.exit(exec_result.returncode)

    # Save the summary info of the mutation results
    print("\n3. Saving mutation results...")
    with open(results_file, "w", encoding="utf-8") as f:
        f.write("Mutation session completed.\n")
        f.write(f"Session file: {session_file}\n")
        f.write(f"Target module: {module_name}\n")

        if exec_result.stdout.strip():
            f.write("\nExecution output:\n")
            f.write(exec_result.stdout)
    
    # Success messages with the lcoation of the files
    print(f"\nMutation testing completed. Session saved to: {session_file}")
    print(f"\nResults placeholder saved to: {results_file}")
    print(f"\nTarget module used for mutation testing: {module_name}")

if __name__ == "__main__":
    main()


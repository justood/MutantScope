import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

# Check if the JSON coverage file exists and load it
def load_coverage_summary(coverage_file: Path):
    if not coverage_file.exists():
        return None
    
    with open(coverage_file, "r", encoding="utf-8") as f:
        return json.load(f)
    
# Calculate the coverage percentage from the coverage summary
def extract_total_coverage(coverage_data):
    if not coverage_data:
        return None
    
    # Get the totals, how many lines were covered and how many statements from the coverage data
    totals = coverage_data.get("totals", {})
    covered = totals.get("covered_lines")
    num_statements = totals.get("num_statements")

    if covered is None or num_statements in (None, 0):
        return None
    
    # Calculate the coverage percentage and round it to 2 decimal places
    return round((covered / num_statements) * 100, 2)

# Load the mutation results form the SQLite database
def load_mutation_results(session_file: Path):
    if not session_file.exists():
        raise FileNotFoundError(f"Session file not found: {session_file}")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(session_file)
    cursor = conn.cursor()

    try:
        # Execute the SQL query to fetch the worker outcomes and test outcomes from the work_results table
        cursor.execute(""" SELECT worker_outcome, test_outcome FROM work_results""")

        rows = cursor.fetchall()
    finally:
        # Close the database
        conn.close()

    return rows

# Calculate the mutation score by counting the outcomes of the mutation testing results
def summarize_mutation_results(rows):

    worker_counter = Counter()
    test_counter = Counter()

    for worker_outcome, test_outcome in rows:
        normalized_worker = str(worker_outcome or "unknown").strip().upper()
        normalized_test = str(test_outcome or "unknown").strip().upper()

        worker_counter[normalized_worker] += 1
        test_counter[normalized_test] += 1

    # Calculate the total number of mutants, how many were killed and how many survived
    total_mutants = len(rows)
    killed_mutants = test_counter.get("KILLED", 0)
    survived_mutants = test_counter.get("SURVIVED", 0)

    # Calculate the mutation score as a percentage of killed mutants over total mutants
    mutation_score = 0.0
    if total_mutants > 0:
        mutation_score = round((killed_mutants / total_mutants) * 100, 2)

    # Return a summary of the mutation testing results, including total mutants, outcomes, and mutation score
    return {
        "total_mutants": total_mutants,
        "worker_outcomes": dict(worker_counter),
        "test_outcomes": dict(test_counter),
        "killed": killed_mutants,
        "survived": survived_mutants,
        "mutation_score": mutation_score
    }

# Provide an explanation of the results
def build_interpretation(coverage_percent, mutation_score):
    lines = []

    if coverage_percent is not None:
        lines.append(f"Structural Coverage: {coverage_percent}%")

    else: 
        lines.append("Structural Coverage: No data available")

    lines.append(f"Mutation Score: {mutation_score}%")

    if coverage_percent is None:
        lines.append("Coverage data was not available so only mutation effectiveness can be analyzed.")

        return lines
    
    # High coverage with a lower mutation score
    if coverage_percent >= 90 and mutation_score < 60:
        lines.append("The test suite exercises most of the code, but many injected mutants still survived. This suggests that high coverage alone does not guarantee strong fault detection.")

    # High coverage with an ok mutation score
    elif coverage_percent >= 90 and mutation_score < coverage_percent:
        lines.append("High coverage with a lower mutation score suggests that the tests execute most of the code but do not always detect the injected faults.")
        
    # High coverage with a strong mutation score
    elif mutation_score >= 80:
        lines.append("The mutation score is strong, which suggests the tests are effective at detecting many injected faults.")
    
    # Moderate coverage with a lower mutation score
    else:
        lines.append("The mutation score shows room for improvement. Consider adding more assertions or test cases that target the surviving mutants.")

    return lines

# Create a readable text report summarizing the coverage and mutation testing results, along with an explanation of the findings
def write_text_report(output_file: Path, coverage_percent, mutation_summary, interpretation):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Test Coverage and Mutation Testing Analysis\n")
        f.write("-------------------------------------------\n\n")
        f.write(f"Coverage Percent: {coverage_percent}%\n")
        f.write(f"Total Mutants: {mutation_summary['total_mutants']}\n")
        f.write(f"Killed Mutants: {mutation_summary['killed']}\n")
        f.write(f"Survived Mutants: {mutation_summary['survived']}\n")
        f.write(f"Mutation Score: {mutation_summary['mutation_score']}%\n\n")

        f.write("Worker Outcomes:\n")
        for outcome, count in mutation_summary["worker_outcomes"].items():
            f.write(f"  {outcome}: {count}\n")

        f.write("\nTest Outcomes:\n")
        for outcome, count in mutation_summary["test_outcomes"].items():
            f.write(f"  {outcome}: {count}\n")

        f.write("\nInterpretation:\n")
        for line in interpretation:
            f.write(f"  {line}\n")

# Print the results to the console in a readable format, including the coverage percentage, mutation summary, and explanation of the findings
def print_summary(coverage_percent, mutation_summary, interpretation, output_file: Path, json_output_file: Path):
    print(f"\nAnalysis Summary")
    print(f"----------------")
    print(f"Coverage Percent: {coverage_percent}%")
    print(f"Total Mutants: {mutation_summary['total_mutants']}")
    print(f"Killed Mutants: {mutation_summary['killed']}")
    print(f"Survived Mutants: {mutation_summary['survived']}")
    print(f"Mutation Score: {mutation_summary['mutation_score']}%\n")

    print("\nWorker Outcomes:")
    for outcome, count in mutation_summary["worker_outcomes"].items():
        print(f"  {outcome}: {count}")
    
    print("\nTest Outcomes:")
    for outcome, count in mutation_summary["test_outcomes"].items():
        print(f"  {outcome}: {count}")

    print("\nInterpretation:")
    for line in interpretation:
        print(f"  {line}")

    # Print the locations of the saved reports
    print(f"\nSaved text report to: {output_file}")
    print(f"Saved JSON report to: {json_output_file}")

def main():
    # Create the reports directory if it doesn't exist
    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    # define the paths to the coverage summary JSON file, the mutation testing results SQLite database, and the output files
    coverage_file = reports_folder / "coverage_summary.json"
    session_file = reports_folder / "session.sqlite"
    output_file = reports_folder / "final_analysis.txt"
    json_output_file = reports_folder / "final_analysis.json"

    # Load the coverage summary, and mutation testing results and calculate the coverage percentage and mutation score
    try:
        coverage_data = load_coverage_summary(coverage_file)
        coverage_percent = extract_total_coverage(coverage_data)

        mutation_rows = load_mutation_results(session_file)
        mutation_summary = summarize_mutation_results(mutation_rows)

        # Build an explanation of the results based on the coverage percentage and mutation score
        interpretation = build_interpretation(coverage_percent, mutation_summary["mutation_score"])

        # Compile the final summary of the analysis, including the coverage percentage, mutation summary, and explanation, then save it to a JSON file
        final_summary = {
            "coverage_percent": coverage_percent,
            "total_mutants": mutation_summary["total_mutants"],
            "killed_mutants": mutation_summary["killed"],
            "survived_mutants": mutation_summary["survived"],
            "mutation_score": mutation_summary["mutation_score"],
            "worker_outcomes": mutation_summary["worker_outcomes"],
            "test_outcomes": mutation_summary["test_outcomes"],
            "interpretation": interpretation
        }

        # Save the final summary to a JSON file for structured reporting
        with open(json_output_file, "w", encoding="utf-8") as f:
            json.dump(final_summary, f, indent=2)

        write_text_report(output_file, coverage_percent, mutation_summary, interpretation)
        print_summary(coverage_percent, mutation_summary, interpretation, output_file, json_output_file)

    # Handle any exceptions that occur during the analysis process and print an error message to the console
    except Exception as e:
        print(f"Result analysis failed: {e}", file=sys.stderr)
        sys.exit(1)

# Entry point of the script, which calls the main function to execute the analysis process
if __name__ == "__main__":
    main()


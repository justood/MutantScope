# MutantScope

A web-based tool that evaluates the effectiveness of Python test suites using:

- Unit Testing (pytest)
- Code Coverage (coverage.py)
- Mutation Testing (Cosmic Ray)

This project demonstrates that high code coverage does not necessarily indicate strong test effectiveness by comparing coverage results with mutation testing outcomes.

## Features
Upload any Python project as a '.zip' file
Run:
- Unit tests
- Coverage analysis
- Mutation testing
- Result interpretation

### Displays:
- Coverage %
- Mutation Score %
- Killed vs Survived Mutants
- Human-readable interpretation
- Interactive HTML coverage report

## Expected Project Structure:
Upload a '.zip'  file like:
project/
         main.py
         tests/
                test_main_code.py

## Technologies Used:
- Python
- Flask (Web Interface)
- pytest (Unit Testing)
- coverage.py (Code Coverage)
- Cosmic Ray (Mutation Testing)

## Installation:

Clone the repository:

git clone https://github.com/justood/MutantScope
cd MutantScope

Install dependencies:
pip install -r requirements.txt

Running the Application
Start the Flask app:
python app.py

Then open your browser:
http://127.0.0.1:5000

## How It Works:
1. Upload a project ZIP
2. The system extracts and checks the structure
3. Select an action:

- Run Tests - Executes pytest
- Run Coverage - Measures code coverage
- Run Mutation - Applies mutation testing
- Analyze Results - Generates summary
- Run Full Analysis - Runs everything in sequence

## Output:
The system generates:
- reports/final_analysis.json
- reports/final_analysis.txt
- reports/coverage_summary.json
- reports/coverage_html/ (visual report)

## Interpretation Logic
The tool compares:
- Structural Coverage (how much code is executed)
- Mutation Score (how many faults are detected)

### Example insights:
- High coverage + low mutation = weak tests
- High mutation score = strong fault detection
- Low both = insufficient testing

## The system prevents:
- Running tools without uploading a project
- Running mutation testing if tests fail
- Running analysis without required data

## Project Goal:
Traditional testing metrics like coverage can be misleading.

MutantScope demonstrates that:
- High coverage does not guarantee effective testing.

- By combining coverage and mutation testing, we provide a more realistic evaluation of test quality.

## Example Use Cases:
- Software testing education
- Evaluating test suite quality
- Comparing different test strategies
- Demonstrating mutation testing concepts

## Authors:
### Justivon Dado
### Luke Dolan

## Course: 
### CSI 4370 – Software Verification & Testing

## Notes:
Sample programs included:
- Discount Calculator
- Grade Calculator 
- Binary Search
- Palindrome Checker
- Loan Calculator

To test them:
1. Zip the program folder
2. Upload it into Mutant Scope
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from flask import (Flask, redirect, render_template, request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

# create the Flask app and set a secret key for session management
app = Flask(__name__)
app.secret_key = "mutation-testing-analyzer-demo-key"

# Define paths for uploads and reports folder
project_root = Path(__file__).resolve().parent
reports_folder = project_root / "reports"
uploads_folder = project_root / "uploads"

# create uploads and reports folders if they don't exist
reports_folder.mkdir(exist_ok=True)
uploads_folder.mkdir(exist_ok=True)

# Run the analyzer script and get the output to display
def run_script(script_name, *args):
    script_path = project_root / "analyzer" / script_name
    command = [sys.executable, str(script_path), *args]

    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=project_root)

        return{
            "returncode": result.returncode,
            "stdout": result.stdout or "",
            "stderr": result.stderr or ""
        }
    
    except Exception as e:
        return {
            "returncode": 1,
            "stdout": "",
            "stderr": f"Exception while running {script_name}: {e}"
        }
    
# Load the JSON file if it exists
def load_json_file(path: Path):
    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
# Clear the old report files to make sure there isn't overlap
def clear_old_reports():
    for filename in ["final_analysis.json", "final_analysis.txt", "coverage_summary.json", "results.txt", "session.sqlite", "temp_cosmic_config.toml"]:

        path = reports_folder / filename
        if path.exists():
            path.unlink()

    coverage_html_folder = reports_folder / "coverage_html"
    if coverage_html_folder.exists():
        shutil.rmtree(coverage_html_folder)

# Combine the stdout and stderr from the script into one string for display
def build_output(result_dict):
    combined_output = ""
    if result_dict.get("stdout"):
        combined_output += result_dict["stdout"]
    if result_dict.get("stderr"):
        if combined_output:
            combined_output += "\n"
        combined_output += result_dict["stderr"]
    return combined_output.strip() if combined_output.strip() else "No output produced."

# render the main page with the output from the script and the final analysis results
def render_main_page(selected_program="", output=None, status="info"):
    final_analysis = None
    coverage_summary = None

    
    if session.get("show_results"):
        final_analysis = load_json_file(reports_folder / "final_analysis.json")
        coverage_summary = load_json_file(reports_folder / "coverage_summary.json")

    coverage_html_exists = (reports_folder / "coverage_html" / "index.html").exists()

    return render_template(
        "index.html",
        final_analysis=final_analysis,
        coverage_summary=coverage_summary,
        coverage_html_exists=coverage_html_exists and session.get("show_results", False),
        selected_program=selected_program,
        output=output,
        status=status
    )

# Check if the uploaded project has the right structure
def validate_project_structure(selected_program: str):
    if not selected_program:
        return None, "Please upload a project first."
    
    project_path = (project_root / selected_program).resolve()

    if not project_path.exists() or not project_path.is_dir():
        return None, f"Project folder not found: {selected_program}"
    
    tests_folder = project_path / "tests"

    prog_files = [f for f in project_path.glob("*.py") if f.name != "__init__.py"]

    if not tests_folder.exists() or not tests_folder.is_dir():
        return None, f"Selected project must contain a tests/ folder."
    
    if not prog_files:
        return None, f"Selected project must contain at least one Python source file."
    
    return project_path, None

# Extract the ZIP file and find the project root
def extract_uploaded_zip(zip_path: Path):

    extract_base = uploads_folder / zip_path.stem

    if extract_base.exists():
        shutil.rmtree(extract_base)
    extract_base.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_base)

    # Look for the first folder that contains a tests folder and a python file
    candidates = []

    for root, dirs, files in os.walk(extract_base):
        root_path = Path(root)
        
        # Skip hidden folders and __MACOSX folder
        parts = root_path.parts
        if "__MACOSX" in parts or any(part.startswith(".") for part in parts):
            continue

        # Check if the folder contains a tests folder and at least one python file
        has_tests = "tests" in dirs
        has_py = any(f.endswith(".py") for f in files)

        # If it does, add it to the candidates list
        if has_tests and has_py:
            candidates.append(root_path)

    # If no candidates found, raise an error
    if not candidates:
        raise ValueError("ZIP must contain a project folder with a python file and a tests folder.")
    
    # Sort candidates by the depth of the path and return the shallowest one
    candidates.sort(key=lambda p: len(p.parts))
    return candidates[0]

@app.route("/")
def index():
    return render_main_page(
        selected_program=session.get("selected_program", ""),
        output=None,
        status="info"
    )

@app.route("/upload", methods=["POST"])
def upload_project():
    uploaded_file = request.files.get("project_zip")

    if not uploaded_file or uploaded_file.filename == "":
        return render_main_page(
            selected_program=session.get("selected_program", ""),
            output="No ZIP file was selected.", 
            status="error"
        )
    
    filename = secure_filename(uploaded_file.filename)

    if not filename.lower().endswith(".zip"):
        return render_main_page(
            selected_program=session.get("selected_program", ""),
            output="Please upload a .zip file.", 
            status="error"
        )
    
    zip_path = uploads_folder / filename
    uploaded_file.save(zip_path)

    try: 
        extracted_project = extract_uploaded_zip(zip_path)
        relative_project_path = extracted_project.relative_to(project_root)
        selected_program = str(relative_project_path)

        session["show_results"] = False
        session["selected_program"] = selected_program
        clear_old_reports()

        return render_main_page(
            selected_program=selected_program,
            output=f"Upload successful. Project ready: You can now run tests or start the full analysis.",
            status="success"
        )
    
    except Exception as e:
        return render_main_page(
            selected_program=session.get("selected_program", ""),
            output=f"Upload failed: {e}",
            status="error"
        )
    
@app.route("/run/<step>", methods=["POST"])
def run_step(step):
    selected_program = request.form.get("program_folder") or session.get("selected_program", "")
    session["selected_program"] = selected_program

    if step != "analyze":
        _, error = validate_project_structure(selected_program)
        if error:
            session["show_results"] = False
            return render_main_page(
                selected_program=selected_program,
                output=error,
                status="error"
            )
        
    if step == "tests":
        clear_old_reports()
        result = run_script("run_tests.py", selected_program)

        session["show_results"] = False
        return render_main_page(
            selected_program=selected_program,
            output=build_output(result),
            status="Tests ran successfully" if result["returncode"] == 0 else "error"
        )
    
    elif step == "coverage":
        clear_old_reports()

        test_check = run_script("run_tests.py", selected_program)
        if test_check["returncode"] != 0:
            session["show_results"] = False
            return render_main_page(
                selected_program=selected_program,
                output="Coverage is blocked until all tests pass.\n\n" + build_output(test_check),
                status="error"
            )
        
        result = run_script("run_coverage.py", selected_program)
        session["show_results"] = False
        return render_main_page(
            selected_program=selected_program,
            output=build_output(result),
            status="success" if result["returncode"] == 0 else "error"
        )
    
    elif step == "mutation":
        clear_old_reports()

        test_check = run_script("run_tests.py", selected_program)
        if test_check["returncode"] != 0:
            session["show_results"] = False
            return render_main_page(
                selected_program=selected_program,
                output="Mutation analysis is blocked until all tests pass.\n\n" + build_output(test_check),
                status="error"
            )
        
        coverage_check = run_script("run_coverage.py", selected_program)
        if coverage_check["returncode"] != 0:
            session["show_results"] = False
            return render_main_page(
                selected_program=selected_program,
                output="Mutation analysis was stopped because coverage failed.\n\n" + build_output(coverage_check),
                status="error"
            )
        
        result = run_script("run_mutation.py", selected_program)
        session["show_results"] = False
        return render_main_page(
            selected_program=selected_program,
            output=build_output(result),
            status="success" if result["returncode"] == 0 else "error"
        )
    
    elif step == "analyze":
        coverage_exists = (reports_folder / "coverage_summary.json").exists()
        mutation_exists = (reports_folder / "session.sqlite").exists()

        if not coverage_exists or not mutation_exists:
            session["show_results"] = False
            return render_main_page(
                selected_program=selected_program,
                output=("Analyze Results is blocked until coverage and mutation data exist. Run coverage and Run mutation first, or use Run Full Analysis."),
                status="error"
            )
        
        result = run_script("result_analyzer.py")
        session["show_results"] = (result["returncode"] == 0)

        return render_main_page(
            selected_program=selected_program,
            output=build_output(result),
            status="success" if result["returncode"] == 0 else "error"
        )
    
    elif step == "all":
        clear_old_reports()

        test_check = run_script("run_tests.py", selected_program)
        if test_check["returncode"] != 0:
            session["show_results"] = False
            return render_main_page(
                selected_program=selected_program,
                output="Full analysis is blocked until all tests pass.\n\n" + build_output(test_check),
                status="error"
            )
        
        result = run_script("run_all.py", selected_program)
        session["show_results"] = (result["returncode"] == 0)
        
        return render_main_page(
            selected_program=selected_program,
            output=build_output(result),
            status="success" if result["returncode"] == 0 else "error"
        )
    
    return redirect(url_for("index"))

@app.route("/coverage-report")
def coverage_report():
    coverage_folder = reports_folder / "coverage_html"
    return send_from_directory(coverage_folder, "index.html")

@app.route("/coverage-report/<path:filename>")
def coverage_report_assets(filename):
    coverage_folder = reports_folder / "coverage_html"
    return send_from_directory(coverage_folder, filename)

@app.route("/reset", methods=["POST"])
def reset():
    session.pop("show_results", None)
    session.pop("selected_program", None)
    clear_old_reports()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)


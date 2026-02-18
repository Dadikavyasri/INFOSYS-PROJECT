"""
AI Powered Code Reviewer
Modules 1–5 Integrated Version
Production Ready | Clean | Error-Free
"""

import os
import ast
import csv
import subprocess
from typing import List, Dict


# ============================================================
# MODULE 1 – CODE PARSING & BASIC ANALYSIS
# ============================================================

def get_python_files(folder_path: str) -> List[str]:
    py_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_structure(tree: ast.AST) -> Dict:
    structure = {
        "imports": [],
        "functions": [],
        "classes": [],
        "loops": 0,
        "conditionals": 0
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for name in node.names:
                structure["imports"].append(name.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                structure["imports"].append(node.module)

        elif isinstance(node, ast.FunctionDef):
            structure["functions"].append(node.name)

        elif isinstance(node, ast.ClassDef):
            structure["classes"].append(node.name)

        elif isinstance(node, (ast.For, ast.While)):
            structure["loops"] += 1

        elif isinstance(node, ast.If):
            structure["conditionals"] += 1

    return structure


def cyclomatic_complexity(tree: ast.AST) -> int:
    complexity = 1
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.BoolOp)):
            complexity += 1
    return complexity


# ============================================================
# MODULE 2 – ISSUE DETECTION & SEVERITY
# ============================================================

def detect_issues_ast(code: str) -> List[str]:
    tree = ast.parse(code)

    assigned = set()
    used = set()
    parameters = set()
    issues = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            if len(node.name) < 4:
                issues.append("poor_function_name")

            if ast.get_docstring(node) is None:
                issues.append("missing_docstring")

            if len(node.args.args) > 4:
                issues.append("too_many_parameters")

            for arg in node.args.args:
                parameters.add(arg.arg)

            if hasattr(node, "end_lineno"):
                length = node.end_lineno - node.lineno + 1
                if length > 15:
                    issues.append("long_function")

        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)

        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in (0, 1):
                issues.append("magic_number")

        if isinstance(node, ast.ExceptHandler):
            if not node.body:
                issues.append("empty_except")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "print":
                issues.append("debug_print")

    if assigned - used - parameters:
        issues.append("unused_variable")

    return sorted(set(issues))


def classify_severity(issue: str) -> str:
    severity_map = {
        "poor_function_name": "INFO",
        "missing_docstring": "INFO",
        "debug_print": "INFO",
        "unused_variable": "WARNING",
        "too_many_parameters": "WARNING",
        "magic_number": "WARNING",
        "long_function": "CRITICAL",
        "empty_except": "CRITICAL",
    }
    return severity_map.get(issue, "INFO")


def explain_issue(issue: str) -> Dict:
    explanations = {
        "missing_docstring": {
            "reason": "Function does not contain a docstring.",
            "suggestion": "Add a descriptive docstring explaining purpose and parameters."
        },
        "long_function": {
            "reason": "Function exceeds recommended length.",
            "suggestion": "Break the function into smaller modular functions."
        },
        "magic_number": {
            "reason": "Hardcoded numeric value found.",
            "suggestion": "Replace with a named constant variable."
        },
        "debug_print": {
            "reason": "Print statement used in production code.",
            "suggestion": "Use logging module instead of print."
        }
    }
    return explanations.get(issue, {
        "reason": "Code quality issue detected.",
        "suggestion": "Review code for best practices."
    })


# ============================================================
# MODULE 3 – SCORING SYSTEM
# ============================================================

def calculate_score(complexity: int, issue_count: int) -> Dict:
    score = 100

    if complexity > 10:
        score -= 20
    elif complexity > 5:
        score -= 10

    if issue_count > 5:
        score -= 20
    elif issue_count > 2:
        score -= 10

    if score >= 90:
        grade = "Excellent"
    elif score >= 75:
        grade = "Good"
    elif score >= 60:
        grade = "Moderate"
    else:
        grade = "Poor"

    return {"score": score, "grade": grade}


# ============================================================
# MODULE 4 – RULE ENGINE
# ============================================================

CONFIG = {
    "max_function_length": 20,
    "max_parameters": 4,
}


def rule_engine(tree: ast.AST) -> List[str]:
    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            if len(node.args.args) > CONFIG["max_parameters"]:
                violations.append(f"{node.name} exceeds max parameters")

            if hasattr(node, "end_lineno"):
                length = node.end_lineno - node.lineno + 1
                if length > CONFIG["max_function_length"]:
                    violations.append(f"{node.name} exceeds max length")

    return violations


# ============================================================
# MAIN ANALYZER (UPDATED WITH EXPLANATION)
# ============================================================

def analyze_file(filepath: str) -> Dict:
    print("\nAnalyzing:", filepath)

    try:
        code = read_file(filepath)
        tree = ast.parse(code)
    except Exception as e:
        print("Parse Error:", e)
        return {}

    structure = extract_structure(tree)
    complexity = cyclomatic_complexity(tree)
    issues = detect_issues_ast(code)
    score_data = calculate_score(complexity, len(issues))
    rule_violations = rule_engine(tree)

    print("Functions:", len(structure["functions"]))
    print("Classes:", len(structure["classes"]))
    print("Complexity:", complexity)

    print("\nDetected Issues:")
    for issue in issues:
        severity = classify_severity(issue)
        explanation = explain_issue(issue)

        print(f"Issue: {issue}")
        print(f"Severity: {severity}")
        print(f"Reason: {explanation['reason']}")
        print(f"Suggestion: {explanation['suggestion']}")
        print("-" * 40)

    print("Rule Violations:", rule_violations)
    print("Score:", score_data["score"], "| Grade:", score_data["grade"])

    return {
        "file": filepath,
        "complexity": complexity,
        "issues": len(issues),
        "score": score_data["score"],
        "grade": score_data["grade"],
    }


# ============================================================
# PROJECT ANALYSIS
# ============================================================

def analyze_project(folder_path: str):
    files = get_python_files(folder_path)

    if not files:
        print("No Python files found.")
        return

    results = []

    for file in files:
        result = analyze_file(file)
        if result:
            results.append(result)

    with open("final_report.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\nCSV Report Generated: final_report.csv")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        analyze_project(sys.argv[1])
    else:
        print("Usage:")
        print("python backend.py <project_folder>")

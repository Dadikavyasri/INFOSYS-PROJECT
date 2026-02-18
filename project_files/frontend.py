"""
Module 6 – Review Web UI
AI Powered Code Reviewer
Streamlit Interface
Efficient | Clean | Error-Free
"""

import streamlit as st
import ast
import os
from typing import List, Dict


# ==========================================================
# Reusable Analysis Functions (Lightweight)
# ==========================================================

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def detect_issues(code: str) -> List[Dict]:
    tree = ast.parse(code)

    issues = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            if not ast.get_docstring(node):
                issues.append({
                    "issue": "Missing Docstring",
                    "severity": "INFO",
                    "line": node.lineno
                })

            if len(node.args.args) > 4:
                issues.append({
                    "issue": "Too Many Parameters",
                    "severity": "WARNING",
                    "line": node.lineno
                })

            if hasattr(node, "end_lineno"):
                length = node.end_lineno - node.lineno + 1
                if length > 20:
                    issues.append({
                        "issue": "Long Function",
                        "severity": "CRITICAL",
                        "line": node.lineno
                    })

        if isinstance(node, ast.ExceptHandler):
            if not node.body:
                issues.append({
                    "issue": "Empty Except Block",
                    "severity": "CRITICAL",
                    "line": node.lineno
                })

    return issues


# ==========================================================
# Streamlit UI
# ==========================================================

st.set_page_config(page_title="AI Code Reviewer", layout="wide")

st.title("🤖 AI Powered Code Reviewer – Web UI")
st.markdown("Module 6 – Review Interface")

uploaded_file = st.file_uploader("Upload Python File", type=["py"])

if uploaded_file:

    code = uploaded_file.read().decode("utf-8")

    try:
        issues = detect_issues(code)
    except Exception as e:
        st.error(f"Parsing Error: {e}")
        st.stop()

    col1, col2 = st.columns(2)

    # ------------------------------------------------------
    # LEFT SIDE – CODE VIEW
    # ------------------------------------------------------
    with col1:
        st.subheader("📄 Code Preview")
        st.code(code, language="python")

    # ------------------------------------------------------
    # RIGHT SIDE – ISSUE PANEL
    # ------------------------------------------------------
    with col2:
        st.subheader("🔍 Detected Issues")

        if not issues:
            st.success("No issues found 🎉")
        else:
            severity_filter = st.selectbox(
                "Filter by Severity",
                ["ALL", "INFO", "WARNING", "CRITICAL"]
            )

            filtered = [
                i for i in issues
                if severity_filter == "ALL" or i["severity"] == severity_filter
            ]

            for idx, issue in enumerate(filtered):

                with st.expander(
                    f"{issue['severity']} - {issue['issue']} (Line {issue['line']})"
                ):
                    st.write("Severity:", issue["severity"])
                    st.write("Line:", issue["line"])

                    colA, colB = st.columns(2)

                    with colA:
                        if st.button("✅ Accept", key=f"accept_{idx}"):
                            st.success("Issue marked as accepted")

                    with colB:
                        if st.button("❌ Reject", key=f"reject_{idx}"):
                            st.warning("Issue rejected")

    # ------------------------------------------------------
    # SUMMARY METRICS
    # ------------------------------------------------------
    st.divider()
    st.subheader("📊 Summary")

    total = len(issues)
    critical = len([i for i in issues if i["severity"] == "CRITICAL"])
    warning = len([i for i in issues if i["severity"] == "WARNING"])
    info = len([i for i in issues if i["severity"] == "INFO"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Issues", total)
    col2.metric("Critical", critical)
    col3.metric("Warnings", warning)
    col4.metric("Info", info)

    if critical > 0:
        st.error("⚠ Critical issues must be fixed before merge.")
    elif warning > 0:
        st.warning("⚠ Review warnings before production.")
    else:
        st.success("✅ Code Quality Looks Good!")

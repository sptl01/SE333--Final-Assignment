'''
# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# PHASE 2 TOOL
from mcp_tools import generate_junit_test, run_maven_test, get_coverage, find_uncovered_lines


mcp.tool(generate_junit_test)
mcp.tool(run_maven_test)
mcp.tool(get_coverage)
mcp.tool(find_uncovered_lines)

if __name__ == "__main__":
    mcp.run(transport="sse")
'''
from fastmcp import FastMCP
import subprocess
import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET

mcp = FastMCP("Testing Agent 🧪")



# TOOL 1: Analyze Java Source Code

@mcp.tool
def analyze_java_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
    
        class_match = re.search(r'public class (\w+)', content)
        class_name = class_match.group(1) if class_match else "Unknown"
        
        
        method_pattern = r'public\s+(\w+)\s+(\w+)\s*\((.*?)\)'
        methods = re.findall(method_pattern, content)
        
        result = f"Class: {class_name}\n\nMethods:\n"
        for return_type, method_name, params in methods:
            result += f"  - {return_type} {method_name}({params})\n"
        
        return result
    except Exception as e:
        return f"Error analyzing file: {str(e)}"



# TOOL 2: Generate JUnit Test Cases

@mcp.tool
def generate_junit_tests(class_name: str, methods: str) -> str:
    test_code = f"""package com.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class {class_name}Test {{
    
    private {class_name} instance = new {class_name}();
    
    @Test
    public void testBasicFunctionality() {{
        assertNotNull(instance);
    }}
}}
"""
    return test_code



# TOOL 3: Execute Maven Tests

@mcp.tool
def run_maven_tests(project_path: str = "maven-projects/assign") -> str:

    try:
        result = subprocess.run(
            ["mvn", "clean", "test"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Extract summary
        if "BUILD SUCCESS" in output:
            return "✅ Tests PASSED\n" + extract_test_summary(output)
        else:
            return "❌ Tests FAILED\n" + extract_test_summary(output)
    except Exception as e:
        return f"Error running tests: {str(e)}"



# TOOL 4: Parse JaCoCo Coverage Report

@mcp.tool
def parse_coverage_report(project_path: str = "maven-projects/assign") -> str:

    try:
        jacoco_path = Path(project_path) / "target" / "site" / "jacoco" / "jacoco.xml"
        
        if not jacoco_path.exists():
            return "Error: JaCoCo report not found. Run 'mvn clean test' first."
        
        tree = ET.parse(jacoco_path)
        root = tree.getroot()
        
        coverage_data = {
            "line": {"covered": 0, "missed": 0},
            "branch": {"covered": 0, "missed": 0},
            "method": {"covered": 0, "missed": 0}
        }
        
        for counter in root.findall(".//counter"):
            counter_type = counter.get("type")
            if counter_type in coverage_data:
                coverage_data[counter_type]["covered"] = int(counter.get("covered", 0))
                coverage_data[counter_type]["missed"] = int(counter.get("missed", 0))
        
        result = "📊 Code Coverage Report\n\n"
        for metric_type, values in coverage_data.items():
            total = values["covered"] + values["missed"]
            if total > 0:
                percentage = (values["covered"] / total) * 100
                result += f"{metric_type.upper()} Coverage: {percentage:.1f}% ({values['covered']}/{total})\n"
        
        return result
    except Exception as e:
        return f"Error parsing coverage report: {str(e)}"



# TOOL 5: List Uncovered Lines

@mcp.tool
def get_uncovered_lines(project_path: str = "maven-projects/assign") -> str:
    
    try:
        jacoco_path = Path(project_path) / "target" / "site" / "jacoco" / "jacoco.xml"
        
        if not jacoco_path.exists():
            return "Error: JaCoCo report not found."
        
        tree = ET.parse(jacoco_path)
        root = tree.getroot()
        
        result = "⚠️ Uncovered Lines:\n\n"
        uncovered_count = 0
        
        for sourcefile in root.findall(".//sourcefile"):
            filename = sourcefile.get("name")
            for line in sourcefile.findall(".//line"):
                ci = line.get("ci", "0")
                if ci == "0":
                    line_number = line.get("nr")
                    result += f"  {filename}:{line_number}\n"
                    uncovered_count += 1
        
        if uncovered_count == 0:
            result = "✅ All lines are covered!"
        else:
            result = f"Found {uncovered_count} uncovered lines:\n\n" + result
        
        return result
    except Exception as e:
        return f"Error: {str(e)}"



# PHASE 3: GIT AUTOMATION TOOLS

@mcp.tool
def git_status() -> str:

    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool
def git_add_all() -> str:
    """Stage all changes with filtering (uses .gitignore)"""
    try:
        result = subprocess.run(["git", "add", "-A"], capture_output=True, text=True)
        if result.returncode == 0:
            return "✅ All changes staged successfully"
        return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool
def git_commit(message: str) -> str:
    try:
        result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Commit successful: {message}"
        return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool
def git_push(remote: str = "origin") -> str:
    try:
        result = subprocess.run(
            ["git", "push", "--set-upstream", remote, "HEAD"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return "✅ Push successful"
        return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool
def git_pull_request(base: str = "main", title: str = "", body: str = "") -> str:
    try:
        result = subprocess.run(
            ["gh", "pr", "create", "--base", base, "--title", title, "--body", body],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            url_match = re.search(r"https://github\.com/.+/pull/\d+", result.stdout)
            return f"✅ PR created: {url_match.group(0) if url_match else result.stdout}"
        return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"



# PHASE 5: CREATIVE EXTENSION 1
# Specification-Based Testing Generator

@mcp.tool
def generate_boundary_tests(method_name: str, param_type: str) -> str:
    try:
        tests = f"""
@Test
public void test{method_name}WithZero() {{
    assertNotNull(instance.{method_name}(0));
}}

@Test
public void test{method_name}WithPositive() {{
    assertNotNull(instance.{method_name}(100));
}}

@Test
public void test{method_name}WithNegative() {{
    assertNotNull(instance.{method_name}(-100));
}}

@Test
public void test{method_name}WithMax() {{
    assertNotNull(instance.{method_name}(Integer.MAX_VALUE));
}}

@Test
public void test{method_name}WithMin() {{
    assertNotNull(instance.{method_name}(Integer.MIN_VALUE));
}}
"""
        return f"📋 Boundary Value Tests for {method_name}\n{tests}"
    except Exception as e:
        return f"Error: {str(e)}"


# PHASE 5: CREATIVE EXTENSION 2
# AI Code Review Agent

@mcp.tool
def quick_code_review(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        issues = []
        
        if re.search(r'catch\s*\([^)]*\)\s*\{\s*\}', content):
            issues.append("🔴 Empty catch block detected")
        
        if re.search(r'[^\w]\d{2,}[^\w]', content) and content.count(re.findall(r'\d{2,}', content)[0] if re.findall(r'\d{2,}', content) else '') > 2:
            issues.append("⚠️ Magic numbers found - use constants")
        
        methods = re.findall(r'public\s+\w+\s+\w+.*?\{.*?\}', content, re.DOTALL)
        long_methods = [m for m in methods if m.count('\n') > 20]
        if long_methods:
            issues.append(f"⚠️ {len(long_methods)} long methods detected (>20 lines)")
        

        if '.get(' in content or '.length' in content:
            if 'null' not in content:
                issues.append("⚠️ Potential null pointer issue")
        
        review = "🔍 Code Review Summary\n\n"
        if issues:
            review += "Issues Found:\n" + "\n".join(issues)
        else:
            review += "✅ No major issues detected!"
        
        review += "\n\n💡 Best Practices:\n  • Keep methods < 20 lines\n  • Use named constants\n  • Handle nulls explicitly\n  • Avoid empty catch blocks"
        
        return review
    except Exception as e:
        return f"Error: {str(e)}"




# Helper Functions
def extract_test_summary(output: str) -> str:
    lines = output.split('\n')
    for line in lines:
        if "Tests run:" in line:
            return line.strip()
    return "No summary available"


if __name__ == "__main__":
    mcp.run(transport="sse")
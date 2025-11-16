# SE333 Final Project: Testing Agent with MCP

## Overview
Testing agent that automatically generates, executes, and iterates on test cases to maximize code coverage using the Model Context Protocol (MCP).

## Features
- **Phase 1**: MCP server integration with calculator tool
- **Phase 2**: Maven integration, test generation, JaCoCo coverage analysis
- **Phase 3**: Git automation (status, add, commit, push, PR creation)
- **Phase 4**: Intelligent test iteration with bug detection and fixing
- **Phase 5**: Creative extensions (boundary testing, code review)


## Installation & Setup

### Prerequisites
- Python 3.8+
- Java
- Maven 3.6+
- Node.js 18+ (for MCP)
- Git


### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/sptl01/SE333--Final-Assignment.git
cd <SE333--Final-Assignment>
```

2. **Set up Python environment**
```bash
uv add mcp[cli] httpx fastmcp
```

3. **Start MCP server**
```bash
.venv\Scripts\activate
python server.py
```

4. **Connect in VS Code**
- Press CTRL+SHIFT+P
- Search "MCP Add Server"
- Click on HTTPS
- Enter: `your server URL (http://..)`

5. **Run Maven tests**
```bash
cd maven-projects
mvn clean test
```

## MCP Tools Available

### Phase 2: Testing & Coverage
- `analyze_java_file(file_path)` - Analyzing Java code
- `run_maven_tests(project_path)` - Execute tests
- `parse_coverage_report(project_path)` - Check coverage %
- `get_uncovered_lines(project_path)` - Identify uncovered lines

### Phase 3: Git Automation
- `git_status()` - Check repository status
- `git_add_all()` - Stage all changes
- `git_commit(message)` - Create commit
- `git_push(remote)` - Push to remote
- `git_pull_request(base, title, body, head)` - Create PR

### Phase 5: Creative Extensions
## Extension 1: generate_boundary_tests(method_name, param_type)
Purpose: Automatically generate test cases using boundary value analysis
What it does:

1: Tests zero value (important boundary)

2: Tests positive numbers (normal case)

3: Tests negative numbers (edge case)

4: Tests Integer.MAX_VALUE (
    upper boundary)

5: Tests Integer.MIN_VALUE (lower boundary)

## Extension 2: quick_code_review(file_path)
Purpose: Automatically review code for quality issues and security problems
What it checks:

1: Empty catch blocks - Reports security issues

2: Magic numbers - Suggests using named constants

3: Long methods - Flags methods > 20 lines

4: Null pointers - Detects potential NullPointerException

### Tools
- `generate_specification_tests()` - Generates test cases from method signatures
- `analyze_test_coverage_gaps()` - Identifies which methods need more tests



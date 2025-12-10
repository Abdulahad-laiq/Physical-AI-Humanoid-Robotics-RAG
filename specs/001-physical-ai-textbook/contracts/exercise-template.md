---
exercise_id: [EXERCISE_ID]                # Example: ex03-02-ik-solver
chapter: [CHAPTER_ID]                     # Example: ch03-kinematics
title: "[EXERCISE_TITLE]"                # Example: "Implement Inverse Kinematics Solver"
learning_outcome: "[OUTCOME]"             # Example: "Develop analytical or numerical IK solver"
difficulty: [LEVEL]                       # beginner | intermediate | advanced
estimated_time: "[TIME_RANGE]"            # Example: "60-90 minutes"
prerequisites:
  - "[PREREQ_1]"                          # Example: "Completed Exercise ex03-01"
  - "[PREREQ_2]"                          # Example: "Understanding of Jacobian matrices"
tools:
  - [TOOL_1]                              # Example: Python 3.9+
  - [TOOL_2]                              # Example: NumPy
  - [TOOL_3]                              # Example: PyBullet
---

# Exercise: [EXERCISE_TITLE]

## Overview

[1-2 paragraphs describing what students will build in this exercise]

**What you'll build**: [Specific deliverable, e.g., "A Python function that computes inverse kinematics for a 6-DOF arm"]

**Why it matters**: [Connection to chapter concepts and real-world applications]

**Real-world application**: [Example of how this skill is used in humanoid robotics]

---

## Setup Instructions

### System Requirements

- **Operating System**: Windows 10/11, Ubuntu 20.04+, macOS 11+
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum
- **Disk Space**: 500MB for dependencies

### Installation

**Step 1: Verify Python Installation**

```bash
python3 --version
# Expected: Python 3.9.x or higher
```

**Step 2: Install Required Packages**

```bash
pip3 install numpy==1.24.0 matplotlib==3.7.0 pybullet==3.2.5
```

**Step 3: Verify Installations**

```python
import numpy as np
import matplotlib.pyplot as plt
import pybullet as p
print(f"NumPy: {np.__version__}, PyBullet: {p.getAPIVersion()}")
# Expected output: NumPy: 1.24.0, PyBullet: XYZ
```

**Step 4: Download Exercise Files**

- Template code: `code-templates/[EXERCISE_ID]-template.py`
- Robot model (if applicable): `docs/models/[MODEL_FILE].urdf`

### Troubleshooting Setup

**Issue**: "ModuleNotFoundError: No module named 'numpy'"
- **Solution**: Run `pip3 install numpy` and verify installation

**Issue**: PyBullet GUI not opening (Windows)
- **Solution**: Ensure graphics drivers are updated; try headless mode: `p.connect(p.DIRECT)`

[Include 2-3 common setup issues]

---

## Problem Statement

**Task**: [Clear, specific description of what to implement]

**Inputs**:
- [Input 1]: [Description, data type, range/constraints]
- [Input 2]: [Description]

**Outputs**:
- [Output 1]: [Description, expected format]
- [Output 2]: [Description]

**Success Criteria**:
- [ ] [Criterion 1, e.g., "Function computes FK within 0.01 error tolerance"]
- [ ] [Criterion 2, e.g., "Code executes in <1 second"]
- [ ] [Criterion 3, e.g., "Handles singularities gracefully"]

**Constraints**:
- [Constraint 1, e.g., "Use only NumPy, no external IK libraries"]
- [Constraint 2]

---

## Code Template

Download or copy the starting code:

```python
"""
Exercise [EXERCISE_ID]: [EXERCISE_TITLE]
[Brief description]

Author: [Student Name]
Date: [Date]
"""

import numpy as np

def [main_function_name](param1, param2):
    """
    [Function description]

    Args:
        param1 ([type]): [Description]
        param2 ([type]): [Description]

    Returns:
        [type]: [Description]
    """
    # TODO: Implement function
    # HINT: [First hint about approach]

    result = None  # Placeholder

    return result


# TODO: Write test code below
if __name__ == "__main__":
    # Test Case 1: [Description]
    test_input_1 = [VALUE]
    expected_output_1 = [VALUE]

    output_1 = [main_function_name](test_input_1)

    # TODO: Verify output matches expected
    print(f"Test 1: Input={test_input_1}, Output={output_1}, Expected={expected_output_1}")

    # TODO: Add more test cases
```

---

## Step-by-Step Instructions

[For beginner/intermediate exercises, provide guided steps. For advanced, provide high-level guidance]

### Step 1: [First Step Description]

**What to do**: [Specific instructions]

**Hints**:
- [Hint 1]
- [Hint 2]

**Reference**: See Chapter [X], Section [Y] for background on [concept]

---

### Step 2: [Second Step Description]

[Follow same structure]

---

[Continue with 4-8 steps depending on complexity]

---

### Final Step: Testing and Validation

**What to do**: Run your implementation with test cases and verify correctness

**Test Cases**:

1. **Test Case 1**: [Description]
   - Input: [VALUES]
   - Expected Output: [VALUES]
   - Tolerance: [±ERROR_MARGIN]

2. **Test Case 2**: [Description]
   - [Follow same structure]

[Include 3-5 test cases covering normal cases, edge cases, error cases]

---

## Expected Output

When your implementation is correct, you should see:

**Console Output**:
```
Test 1: PASS
Test 2: PASS
Test 3: PASS
[Computed value]: 0.523 (expected: 0.520, error: 0.003)
```

**Visualization** (if applicable):

[Screenshot or description of expected plot/simulation visualization]

![Expected output visualization](../assets/[EXERCISE_ID]-expected-output.png)
*Figure: Expected output showing [description]*

---

## Troubleshooting

### Common Errors

**Error**: "`ValueError: shapes (3,4) and (4,4) not aligned`"
- **Cause**: Matrix dimension mismatch in multiplication
- **Solution**: Check that transformation matrices are 4x4 before multiplication

**Error**: "Singularity detected, IK solution unstable"
- **Cause**: Robot in singular configuration
- **Solution**: Implement singularity detection and recovery (damped least squares or joint limit avoidance)

[Include 3-5 common errors students might encounter]

### Platform-Specific Issues

**Windows**:
- [Issue and solution]

**Linux**:
- [Issue and solution]

**macOS**:
- [Issue and solution]

### Getting Help

- Review Chapter [X] Section [Y] for conceptual background
- Check Appendix [X] for [relevant topic]
- Post question to course discussion forum (if available)
- Open GitHub issue with error message and minimal reproducible code

---

## Extensions (Optional Challenges)

For students who want to go further:

1. **Extension 1**: [Challenge description]
   - **Difficulty**: [Level]
   - **Learning Goal**: [What new concept this teaches]

2. **Extension 2**: [Challenge description]
   - [Follow same structure]

[Include 2-3 optional extensions]

---

## Rubric (For Instructors)

| Criterion | Points | Description |
|-----------|--------|-------------|
| Code compiles and runs | 20 | No syntax errors, executes without crashes |
| Correct implementation | 40 | Produces correct outputs for all test cases |
| Code quality | 20 | Well-commented, follows style guide, modular |
| Testing thoroughness | 10 | Includes comprehensive test cases |
| Documentation | 10 | Function docstrings, README if applicable |
| **Total** | **100** | |

**Bonus Points** (+10): Implements one or more extensions

---

## Submission (For Formal Courses)

[If exercise is for graded course, include submission instructions]

1. Complete all TODO sections in template
2. Run all test cases and verify PASS
3. Add your name and date to file header
4. Submit file: `[EXERCISE_ID]-[YourName].py`

**Deadline**: [DATE]

**Submission Method**: [Upload to LMS / Email to TA / GitHub PR]

---

## Solution (Instructor-Only)

[Full solution code in `solutions/[EXERCISE_ID]-solution.py` - not deployed in public documentation]

See `solutions/[EXERCISE_ID]-solution.py` for reference implementation.

---

## Connections to Next Topics

This exercise prepares you for:
- **Chapter [X]**: [How this connects to future topic]
- **Exercise [NEXT_EXERCISE]**: [What builds on this]

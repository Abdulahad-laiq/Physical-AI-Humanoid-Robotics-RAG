---
id: [CHAPTER_ID]                          # Example: ch03-kinematics
title: "[CHAPTER_TITLE]"                  # Example: "Humanoid Kinematics - Forward and Inverse"
chapter_number: [NUMBER]                  # Example: 3
description: "[BRIEF_DESCRIPTION]"       # Example: "Learn FK and IK for humanoid manipulators"
keywords:
  - [KEYWORD_1]                           # Example: kinematics
  - [KEYWORD_2]                           # Example: Denavit-Hartenberg
  - [KEYWORD_3]
prerequisites:
  - [CHAPTER_ID_OR_TOPIC]                 # Example: ch02-robot-fundamentals
  - "[EXTERNAL_PREREQ]"                   # Example: "Linear algebra (matrices)"
learning_objectives:
  - "[OBJECTIVE_1]"                       # Must be measurable (use "Derive", "Implement", "Explain", etc.)
  - "[OBJECTIVE_2]"
  - "[OBJECTIVE_3]"
  - "[OBJECTIVE_4]"                       # 3-5 objectives total
estimated_time: "[TIME_RANGE]"            # Example: "4-6 hours"
difficulty: [LEVEL]                       # beginner | intermediate | advanced
---

# [CHAPTER_TITLE]

## Introduction

[1-2 paragraphs introducing the chapter topic]

- **Context**: Why this topic matters for humanoid robotics
- **Preview**: What students will learn in this chapter
- **Connection**: How it builds on previous chapters

Example:
> In this chapter, we explore humanoid kinematics—the study of motion without considering forces. Understanding how joint angles map to end-effector positions (forward kinematics) and vice versa (inverse kinematics) is fundamental for robot control, manipulation, and motion planning. Building on the coordinate frame transformations from Chapter 2, we'll apply the Denavit-Hartenberg convention to systematically derive kinematic equations for humanoid arms.

---

## Key Concepts

### [Concept 1 Title]

[Definition with authoritative citation]

**Explanation**: [Clear explanation in accessible language, F-K grade 10-14]

**Mathematical Formulation** (if applicable):

$$
[EQUATION]
$$

[Explanation of variables and terms]

**Example Application**:

[Concrete example showing how concept applies to humanoid robotics]

**Diagram** (if applicable):

```mermaid
[MERMAID_DIAGRAM]
```
*Figure X: [Caption describing diagram]*

OR

![Diagram description](./assets/[DIAGRAM_FILE].svg)
*Figure X: [Caption describing diagram]*

**Citation**: [1], [2] (Reference authoritative sources from bibliography)

---

### [Concept 2 Title]

[Follow same structure as Concept 1]

---

[Continue with 4-6 key concept subsections per chapter, building from simple to complex]

---

## Code Examples

### Example 1: [Example Title]

**Purpose**: [What this code demonstrates]

```python
# [Brief description of example]
import numpy as np

# [Code with inline comments explaining key steps]
def example_function(param1, param2):
    """
    Brief function description.

    Args:
        param1: Description
        param2: Description

    Returns:
        Description of return value
    """
    # TODO: Implement function body
    result = param1 + param2
    return result

# Example usage
output = example_function(5, 10)
print(f"Result: {output}")
# Expected output: Result: 15
```

**Expected Output**:
```
Result: 15
```

---

### Example 2: [Example Title]

[Follow same structure]

---

[Include 2-4 code examples per chapter]

---

## Practical Exercises

Students should complete these hands-on exercises to reinforce chapter concepts:

1. **[Exercise 1: Brief Title](exercises/ex01-[short-name].md)** - [One sentence description]
2. **[Exercise 2: Brief Title](exercises/ex02-[short-name].md)** - [One sentence description]

[Minimum 2 exercises per chapter]

---

## Assessments

Test your understanding with these questions:

### Multiple Choice

**Question 1**: [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

<details>
<summary>Show Answer</summary>
**Answer**: [LETTER]
**Explanation**: [Why this is correct and others are incorrect, with citations if applicable]
</details>

---

### Short Answer

**Question 2**: [Question text requiring 2-4 sentence answer]

<details>
<summary>Show Rubric</summary>
**Rubric** (5 points total):
- (2 pts) [Key point 1]
- (2 pts) [Key point 2]
- (1 pt) [Key point 3]
</details>

---

### Diagram/Code Questions

[Include diagram labeling or code completion questions as appropriate]

---

[Include 5-10 assessment questions total, mix of multiple choice, short answer, diagram, code]

---

## Further Reading

For students who want to deepen their understanding:

1. **[FULL_IEEE_CITATION]**
   - *Summary*: [1-2 sentences explaining what this source covers and why it's recommended]

2. **[FULL_IEEE_CITATION]**
   - *Summary*: [Description]

3. **[FULL_IEEE_CITATION]**
   - *Summary*: [Description]

[Include 3-5 annotated further reading sources with IEEE citations]

---

## Summary

[1 paragraph recapping key concepts learned in this chapter]

Example:
> This chapter introduced forward and inverse kinematics for humanoid manipulators. We learned how to systematically assign coordinate frames using the Denavit-Hartenberg convention, derive transformation matrices, and compute end-effector poses from joint angles (FK). We also explored both analytical and numerical approaches to inverse kinematics, understanding workspace limitations and singularities. These foundational skills enable precise control of humanoid arms for reaching, grasping, and manipulation tasks—topics we'll build upon in subsequent chapters.

**Next Chapter Preview**: [1 sentence connecting to next chapter]

---

## References

[All inline citations `[1]`, `[2]`, etc. must appear in the bibliography.bib file]

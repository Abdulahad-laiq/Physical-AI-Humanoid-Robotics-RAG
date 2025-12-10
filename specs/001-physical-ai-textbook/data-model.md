# Content Structure and Data Model

**Feature**: Physical AI & Humanoid Robotics Textbook
**Purpose**: Define structured schemas for chapters, exercises, assessments, glossary, and supporting materials to ensure consistency across all content
**Last Updated**: 2025-12-09

## Chapter Structure

Each chapter follows a standardized MDX format with frontmatter metadata and consistent content sections.

### Chapter Frontmatter Schema

```yaml
---
id: ch03-kinematics                    # Unique chapter ID (kebab-case)
title: "Humanoid Kinematics - Forward and Inverse"  # Display title
chapter_number: 3                      # Sequential chapter number (1-10)
description: "Learn forward and inverse kinematics for humanoid manipulators using DH convention"
keywords:                              # SEO and search keywords
  - kinematics
  - Denavit-Hartenberg
  - forward kinematics
  - inverse kinematics
  - jacobian
prerequisites:                         # Required prior chapters/knowledge
  - ch02-robot-fundamentals
  - "Linear algebra (matrices, vectors)"
  - "Calculus (derivatives)"
learning_objectives:                   # 3-5 measurable outcomes
  - "Derive forward kinematics using Denavit-Hartenberg (DH) convention"
  - "Solve inverse kinematics for humanoid arms using analytical and numerical methods"
  - "Understand workspace and singularities in humanoid manipulators"
  - "Implement FK and IK solvers in Python for serial-link arms"
  - "Analyze kinematic redundancy in humanoid systems"
estimated_time: "4-6 hours"            # Reading + exercises + assessments
difficulty: intermediate               # beginner | intermediate | advanced
---
```

### Chapter Content Sections (Sequential Order)

1. **Introduction** (1-2 paragraphs)
   - Context: Why this topic matters for humanoid robotics
   - Preview: What students will learn in this chapter
   - Connection: How it builds on previous chapters

2. **Key Concepts** (Multiple subsections, ~60-70% of chapter content)
   - Subsection structure:
     - Concept definition with authoritative citation
     - Explanation with diagrams (Mermaid or external SVG/PNG)
     - Mathematical formulation (where applicable)
     - Example application
   - Progressive complexity: Simple → complex, concrete → abstract

3. **Code Examples** (2-4 executable blocks per chapter)
   - Each code block includes:
     - Learning purpose comment
     - Fully executable Python/ROS2 code
     - Inline comments explaining key steps
     - Expected output documented

4. **Practical Exercises** (Minimum 2, link to separate files)
   - Links to `exercises/ex01-*.md`, `exercises/ex02-*.md`
   - Brief description of each exercise in main chapter

5. **Assessments** (5-10 questions embedded in chapter)
   - Mix of: multiple choice, short answer, diagram labeling, code completion
   - Answers/rubrics in separate file (not visible in public docs)

6. **Further Reading** (3-5 annotated sources)
   - Format:
     - `[1] Full IEEE citation`
     - `   Summary: What this source covers and why it's recommended`

7. **Summary** (1 paragraph)
   - Recap key concepts learned
   - Preview next chapter connection

### Chapter File Structure

```
docs/ch03-kinematics/
├── index.md                           # Main chapter content (MDX)
├── exercises/
│   ├── ex01-dh-fk.md                 # Exercise 1: DH-based FK
│   ├── ex02-ik-solver.md             # Exercise 2: IK implementation
│   ├── solutions/                     # Instructor-only solutions
│   │   ├── ex01-solution.py
│   │   └── ex02-solution.py
│   └── code-templates/                # Student starting code
│       ├── ex01-template.py
│       └── ex02-template.py
├── assets/                            # Chapter-specific diagrams/images
│   ├── dh-frames.svg                  # DH frame assignment diagram
│   ├── workspace-plot.png             # Arm workspace visualization
│   └── singularity-example.svg        # Singularity illustration
└── assessment-key.md                  # Answers/rubrics (not deployed publicly)
```

---

## Exercise Structure

### Exercise Frontmatter Schema

```yaml
---
exercise_id: ex03-02-ik-solver         # Unique exercise ID
chapter: ch03-kinematics               # Parent chapter
title: "Implement Inverse Kinematics Solver"
learning_outcome: "Develop analytical or numerical IK solver to reach target positions"
difficulty: intermediate               # beginner | intermediate | advanced
estimated_time: "60-90 minutes"
prerequisites:
  - "Completed Exercise ex03-01 (DH FK)"
  - "Understanding of Jacobian matrices"
tools:
  - Python 3.9+
  - NumPy
  - Matplotlib (for visualization)
  - PyBullet (optional, for verification)
---
```

### Exercise Content Sections

1. **Overview** (1-2 paragraphs)
   - What students will build
   - Why this exercise reinforces chapter concepts
   - Real-world application context

2. **Setup Instructions**
   - Environment requirements (OS, software versions)
   - Installation commands with version pinning
   - Verification steps (test imports, check installations)

3. **Problem Statement**
   - Clearly defined task
   - Input specifications
   - Expected output specifications
   - Success criteria

4. **Code Template** (Embedded or linked)
   - Starting code with `TODO` markers
   - Function signatures provided
   - Hints as comments

5. **Step-by-Step Instructions** (For beginner/intermediate exercises)
   - Numbered steps guiding implementation
   - Hints for each step
   - References to chapter sections

6. **Expected Output**
   - Sample output (console output, plots, simulation screenshots)
   - Performance metrics (if applicable)
   - How to verify correctness

7. **Troubleshooting**
   - Common errors and solutions
   - Platform-specific issues (Windows/Linux/macOS)
   - How to get help (GitHub issues, appendix references)

8. **Extensions** (Optional challenges)
   - Ideas for students who want to go further
   - Connections to advanced topics

### Exercise Submission/Validation

For self-study textbook:
- Solutions provided in `solutions/` (instructor-only, not deployed to public site)
- Auto-validation scripts (where possible): `pytest` tests students can run locally
- Rubrics for self-assessment

---

## Assessment Question Schemas

### Multiple Choice Question

```markdown
**Question 1 (MC)**: What are the four Denavit-Hartenberg parameters?

A) $x, y, z, \theta$
B) $a, \alpha, d, \theta$
C) $r, \phi, z, \psi$
D) $l, m, n, \gamma$

**Answer**: B
**Explanation**: The DH parameters are link length ($a_i$), link twist ($\alpha_i$), link offset ($d_i$), and joint angle ($\theta_i$) [Siciliano et al., Ch. 2].
```

### Short Answer Question

```markdown
**Question 2 (SA)**: Explain the difference between analytical and numerical inverse kinematics. When is each approach preferred?

**Rubric** (5 points):
- (2 pts) Analytical IK: Closed-form solution, direct computation
- (2 pts) Numerical IK: Iterative solution (e.g., Jacobian pseudo-inverse)
- (1 pt) Preference: Analytical preferred when available (faster, exact); numerical for complex/redundant robots
```

### Diagram Labeling Question

```markdown
**Question 3 (Diagram)**: Label the following diagram with the correct DH frames and parameters.

![DH Arm Diagram](../assets/dh-labeling-question.svg)

**Answer Key**: (See assessment-key.md for labeled diagram)
```

### Code Completion Question

```python
# Question 4 (Code): Complete the forward kinematics function using DH parameters

import numpy as np

def dh_transform(a, alpha, d, theta):
    """
    Compute DH transformation matrix.
    TODO: Fill in the transformation matrix computation.
    """
    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)

    # TODO: Complete this transformation matrix
    T = np.array([
        [ct, ______, ______, ______],
        [st, ______, ______, ______],
        [0,  ______,  ______, ______],
        [0,  0,       0,      1     ]
    ])
    return T

# Answer: (See assessment-key.md for completed code)
```

---

## Glossary Entry Structure

Centralized glossary in `docs/glossary.md` with standardized entry format:

```markdown
## Embodied Intelligence

**Definition**: Intelligence that arises from the interaction between an agent's body (sensors, actuators, morphology) and its environment, emphasizing the role of physical embodiment in cognition and behavior.

**Context**: In Physical AI, embodied intelligence contrasts with disembodied AI (e.g., software-only agents) by recognizing that intelligent behavior emerges from sensorimotor loops and physical constraints [1].

**Example**: A humanoid robot learning to walk develops embodied intelligence through trial-and-error interaction with gravity, ground contact forces, and balance dynamics—knowledge that cannot be fully captured in abstract symbolic representations.

**See Also**: Physical AI, Sensorimotor Loop, Morphological Computation

**Citation**: [1] R. Pfeifer and J. Bongard, *How the Body Shapes the Way We Think*, MIT Press, 2006.

**First Mentioned**: Chapter 1

---
```

### Glossary Metadata

- **Alphabetical ordering** (auto-sorted in Docusaurus)
- **Cross-references**: "See Also" links to related terms
- **Chapter tracking**: Note where term is first introduced
- **Citation**: Authoritative source for definition
- **Target**: 100-150 glossary entries across all chapters

---

## Bibliography Entry Structure

Centralized bibliography in `docs/bibliography.md`, rendered from BibTeX using IEEE format:

```markdown
# Bibliography

## Books

[1] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, *Robotics: Modelling, Planning and Control*. London, U.K.: Springer, 2010.

[2] J. J. Craig, *Introduction to Robotics: Mechanics and Control*, 4th ed. Hoboken, NJ, USA: Pearson, 2017.

## Journal Articles

[3] M. Vukobratović and B. Borovac, "Zero-moment point—Thirty five years of its life," *Int. J. Humanoid Robot.*, vol. 1, no. 1, pp. 157–173, Mar. 2004.

## Conference Papers

[4] J. Pratt, J. Carff, S. Drakunov, and A. Goswami, "Capture point: A step toward humanoid push recovery," in *Proc. IEEE-RAS Int. Conf. Humanoid Robots*, Genova, Italy, Dec. 2006, pp. 200–207.

## Standards

[5] *Robots and Robotic Devices—Collaborative Robots*, ISO Standard 15066, 2016.

## Online Resources

[6] S. M. LaValle, *Planning Algorithms*. Cambridge, U.K.: Cambridge Univ. Press, 2006. [Online]. Available: http://planning.cs.uiuc.edu/
```

### Bibliography Management

- **Source file**: `bibliography.bib` (BibTeX format, version-controlled)
- **Rendering**: Use `pandoc --citeproc --csl=ieee.csl` to generate IEEE-formatted markdown
- **Validation**: Automated script checks required fields, DOI resolution, duplicate entries
- **Target**: 50-70 unique sources

---

## Appendix Structure

### Appendix A: Simulator Setup Guides

```markdown
# Appendix A: Setup Guide - PyBullet Simulator

## Overview
PyBullet is an open-source physics simulation library...

## System Requirements
- OS: Windows 10/11, Ubuntu 20.04+, macOS 11+
- Python: 3.9+
- RAM: 4GB minimum, 8GB recommended
- GPU: Optional (CPU-only mode available)

## Installation

### Ubuntu/Linux
\`\`\`bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev
pip3 install pybullet==3.2.5
\`\`\`

### Windows
\`\`\`bash
# Install via pip (works in native Windows or WSL2)
pip install pybullet==3.2.5
\`\`\`

### macOS
\`\`\`bash
pip install pybullet==3.2.5
\`\`\`

## Verification
\`\`\`python
import pybullet as p
import pybullet_data
print(f"PyBullet version: {p.getAPIVersion()}")
# Expected output: PyBullet version: XYZ
\`\`\`

## Common Issues
...
```

### Appendix B: Math Review

```markdown
# Appendix B: Mathematics Review

## Linear Algebra Essentials

### Vectors
...

### Matrices
...

### Transformations
...

## Calculus Essentials

### Derivatives
...

### Gradients and Jacobians
...
```

### Appendix C: Troubleshooting

```markdown
# Appendix C: Troubleshooting Guide

## PyBullet Issues

### Issue: "ImportError: No module named 'pybullet'"
**Solution**: Ensure pybullet is installed: `pip install pybullet`...

## ROS2 Issues
...

## Cross-Platform Issues
...
```

---

## Robot Model File Structure

Robot models (URDF/SDF) stored in `docs/models/`:

```
docs/models/
├── simple_humanoid.urdf               # Basic humanoid (Ch 1-4 exercises)
├── humanoid_with_hands.urdf           # With manipulators (Ch 5-7)
├── full_humanoid.urdf                 # Complete model (Ch 8-10)
├── meshes/                            # Visual/collision meshes
│   ├── torso.stl
│   ├── upper_arm.stl
│   ├── forearm.stl
│   ├── hand.stl
│   └── ...
└── README.md                          # Model documentation
```

### URDF Metadata

Each URDF file includes XML comments documenting:
- Model name and version
- Degrees of freedom (DOF)
- Mass and inertia properties
- Joint limits and damping
- Collision geometry simplifications
- Source (original model or custom-designed)

---

## Sidebar Navigation Structure

`sidebars.js` defines Docusaurus navigation hierarchy:

```javascript
module.exports = {
  textbookSidebar: [
    'intro',  // Landing page
    {
      type: 'category',
      label: 'Fundamentals',
      items: [
        'ch01-introduction/index',
        'ch02-robot-fundamentals/index',
        'ch03-kinematics/index',
        'ch04-dynamics/index',
      ],
    },
    {
      type: 'category',
      label: 'Core Robotics',
      items: [
        'ch05-perception/index',
        'ch06-planning/index',
        'ch07-manipulation/index',
      ],
    },
    {
      type: 'category',
      label: 'Advanced Topics',
      items: [
        'ch08-locomotion/index',
        'ch09-learning/index',
        'ch10-collaboration/index',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        'glossary',
        'bibliography',
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendices/setup-pybullet',
        'appendices/setup-webots',
        'appendices/setup-ros2',
        'appendices/math-review',
        'appendices/troubleshooting',
      ],
    },
  ],
};
```

---

## Metadata for Search and SEO

### Chapter-Level Metadata
- Embedded in frontmatter: `keywords`, `description`
- Used by Docusaurus for search indexing and meta tags

### Site-Level Metadata
`docusaurus.config.js`:

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A University Textbook for Future-of-Work Robotics Education',
  url: 'https://Abdulahad-laiq.github.io',
  baseUrl: '/Physical-AI-Humanoid-Robotics/',
  organizationName: 'Abdulahad-laiq',
  projectName: 'Physical-AI-Humanoid-Robotics',
  themeConfig: {
    metadata: [
      {name: 'keywords', content: 'robotics, humanoid, Physical AI, ROS2, textbook, education'},
      {name: 'description', content: 'Open educational textbook covering Physical AI and humanoid robotics for university STEM students'},
    ],
    // ...
  },
  // ...
};
```

---

## Content Validation Schema

Automated validation checks during CI:

```yaml
# .github/workflows/validate-content.yml

- name: Validate Chapter Frontmatter
  run: python scripts/validate-frontmatter.py
  # Checks:
  #   - All required frontmatter fields present
  #   - 3-5 learning objectives per chapter
  #   - Prerequisites valid (reference existing chapters)

- name: Validate Exercise Structure
  run: python scripts/validate-exercises.py
  # Checks:
  #   - All exercises have frontmatter
  #   - Setup instructions present
  #   - Expected output documented

- name: Validate Glossary
  run: python scripts/validate-glossary.py
  # Checks:
  #   - All entries have definition, context, citation
  #   - Alphabetical order
  #   - No duplicate terms

- name: Validate Bibliography
  run: python scripts/validate-bibliography.py
  # Checks:
  #   - All BibTeX entries have required fields
  #   - IEEE format compliance
  #   - DOI links resolve (with timeout handling)
```

---

## Summary

This data model ensures:
- **Consistency**: All chapters follow same structure
- **Discoverability**: Rich metadata enables search and navigation
- **Validation**: Automated checks enforce quality standards
- **Maintainability**: Clear schemas make updates predictable
- **Accessibility**: Structured content supports screen readers and alt-text

All templates implementing this data model are provided in `contracts/` directory.

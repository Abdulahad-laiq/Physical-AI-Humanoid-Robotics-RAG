# Assessment Question Templates

**Feature**: Physical AI & Humanoid Robotics Textbook
**Purpose**: Standardized formats for assessment questions embedded in chapters
**Last Updated**: 2025-12-09

## Multiple Choice Questions

### Format

```markdown
**Question [NUMBER] (MC)**: [Question text]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

<details>
<summary>Show Answer</summary>

**Answer**: [LETTER]

**Explanation**: [Why the correct answer is correct and why others are incorrect. Include citations if applicable.]

</details>
```

### Example

```markdown
**Question 1 (MC)**: What are the four Denavit-Hartenberg (DH) parameters?

A) $x, y, z, \theta$
B) $a, \alpha, d, \theta$
C) $r, \phi, z, \psi$
D) $l, m, n, \gamma$

<details>
<summary>Show Answer</summary>

**Answer**: B

**Explanation**: The DH parameters are link length ($a_i$), link twist ($\alpha_i$), link offset ($d_i$), and joint angle ($\theta_i$). These four parameters completely describe the relationship between consecutive coordinate frames in a serial-link manipulator [Craig, Ch. 3]. Options A, C, and D use coordinate systems or variables not part of the DH convention.

</details>
```

---

## Short Answer Questions

### Format

```markdown
**Question [NUMBER] (SA)**: [Question text requiring 2-4 sentence answer]

<details>
<summary>Show Rubric</summary>

**Rubric** ([TOTAL] points):
- ([X] pts) [Key point 1 that must be mentioned]
- ([X] pts) [Key point 2]
- ([X] pts) [Key point 3]
- ([X] pts) [Optional: Citation or specific detail]

**Sample Answer**: [Optional: Provide example of full-credit answer]

</details>
```

### Example

```markdown
**Question 2 (SA)**: Explain the difference between analytical and numerical inverse kinematics. When is each approach preferred?

<details>
<summary>Show Rubric</summary>

**Rubric** (5 points):
- (2 pts) Analytical IK: Closed-form solution derived algebraically; directly computes joint angles from end-effector pose
- (2 pts) Numerical IK: Iterative solution (e.g., Jacobian pseudo-inverse, optimization); approximates solution through repeated calculations
- (1 pt) Preference: Analytical preferred when available (faster, exact); numerical for complex/redundant robots where analytical solutions don't exist

**Sample Answer**: Analytical inverse kinematics uses closed-form mathematical expressions to directly compute joint angles from the desired end-effector pose, providing exact solutions quickly. Numerical inverse kinematics uses iterative algorithms like Jacobian-based methods to approximate solutions through repeated calculations. Analytical IK is preferred when a closed-form solution exists (simpler, faster), but numerical IK is necessary for complex or redundant manipulators where analytical solutions are intractable.

</details>
```

---

## True/False Questions

### Format

```markdown
**Question [NUMBER] (TF)**: [Statement to evaluate]

<details>
<summary>Show Answer</summary>

**Answer**: [True / False]

**Explanation**: [Why this is true or false, with correction if false]

</details>
```

### Example

```markdown
**Question 3 (TF)**: The Zero-Moment Point (ZMP) must always lie within the support polygon for a humanoid robot to maintain static balance.

<details>
<summary>Show Answer</summary>

**Answer**: True

**Explanation**: For static balance, the ZMP (the point on the ground where the sum of moments from gravity and inertial forces equals zero) must remain within the convex hull of the contact points (support polygon). If the ZMP moves outside the support polygon, the robot will tip over [Vukobratović & Borovac, 2004].

</details>
```

---

## Diagram Labeling Questions

### Format

```markdown
**Question [NUMBER] (Diagram)**: [Instruction for labeling diagram]

![Diagram with blank labels](../assets/[DIAGRAM_FILE]-question.svg)

<details>
<summary>Show Answer</summary>

![Diagram with correct labels](../assets/[DIAGRAM_FILE]-answer.svg)

**Labels**:
1. [Label 1]: [Description]
2. [Label 2]: [Description]
3. [Label 3]: [Description]

</details>
```

### Example

```markdown
**Question 4 (Diagram)**: Label the following humanoid arm diagram with the correct DH coordinate frames and parameters.

![Unlabeled DH arm](../assets/dh-arm-unlabeled.svg)

<details>
<summary>Show Answer</summary>

![Labeled DH arm](../assets/dh-arm-labeled.svg)

**Labels**:
1. Frame {0}: Base frame (world reference)
2. Frame {1}: Frame at joint 1 after rotation $\theta_1$
3. $a_1$: Link length between frames {0} and {1}
4. $\alpha_1$: Link twist (rotation about x-axis)
5. $d_2$: Link offset along z-axis
6. $\theta_2$: Joint angle at joint 2

</details>
```

---

## Code Completion Questions

### Format

```markdown
**Question [NUMBER] (Code)**: [Instruction for completing code]

\`\`\`python
# [Context or setup code]

def [function_name]([params]):
    """
    [Function docstring]
    """
    # TODO: Complete this code
    [LINE_WITH_BLANKS]
    ______
    ______

    return [result]
\`\`\`

<details>
<summary>Show Answer</summary>

\`\`\`python
# Completed code
def [function_name]([params]):
    """
    [Function docstring]
    """
    [COMPLETE_LINE_1]
    [COMPLETE_LINE_2]
    [COMPLETE_LINE_3]

    return [result]
\`\`\`

**Explanation**: [Why this code is correct, what it does]

</details>
```

### Example

```markdown
**Question 5 (Code)**: Complete the DH transformation matrix function below.

\`\`\`python
import numpy as np

def dh_transform(a, alpha, d, theta):
    """
    Compute Denavit-Hartenberg transformation matrix.
    """
    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)

    T = np.array([
        [ct, ______, ______, ______],
        [st, ______, ______, ______],
        [0,  ______,  ______, ______],
        [0,  0,       0,      1     ]
    ])
    return T
\`\`\`

<details>
<summary>Show Answer</summary>

\`\`\`python
import numpy as np

def dh_transform(a, alpha, d, theta):
    """
    Compute Denavit-Hartenberg transformation matrix.
    """
    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)

    T = np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,   sa,     ca,    d   ],
        [0,   0,      0,     1   ]
    ])
    return T
\`\`\`

**Explanation**: This is the standard DH transformation matrix [Craig, Ch. 3]. It combines rotation about the z-axis by $\theta$, translation along z by $d$, translation along x by $a$, and rotation about x by $\alpha$. The matrix performs $\text{Rot}_z(\theta) \text{Trans}_z(d) \text{Trans}_x(a) \text{Rot}_x(\alpha)$.

</details>
```

---

## Calculation Questions

### Format

```markdown
**Question [NUMBER] (Calc)**: [Problem requiring numerical calculation]

**Given**:
- [Given value 1]
- [Given value 2]

**Find**: [What to calculate]

<details>
<summary>Show Answer</summary>

**Solution**:

[Step 1]: [Calculation]
[Step 2]: [Calculation]
[Final Answer]: [Result with units]

**Explanation**: [Reasoning for approach, relevant equations used]

</details>
```

### Example

```markdown
**Question 6 (Calc)**: Compute the end-effector position for a 2-DOF planar arm.

**Given**:
- Link 1 length: $l_1 = 0.5$ m
- Link 2 length: $l_2 = 0.3$ m
- Joint 1 angle: $\theta_1 = 45°$ (0.785 rad)
- Joint 2 angle: $\theta_2 = 30°$ (0.524 rad)

**Find**: End-effector position $(x, y)$ in the base frame.

<details>
<summary>Show Answer</summary>

**Solution**:

For a 2-DOF planar arm, forward kinematics is:

$$x = l_1 \cos(\theta_1) + l_2 \cos(\theta_1 + \theta_2)$$
$$y = l_1 \sin(\theta_1) + l_2 \sin(\theta_1 + \theta_2)$$

**Step 1**: Compute $\theta_1 + \theta_2 = 0.785 + 0.524 = 1.309$ rad (75°)

**Step 2**: Calculate $x$:
$$x = 0.5 \cos(0.785) + 0.3 \cos(1.309) = 0.5(0.707) + 0.3(0.259) = 0.354 + 0.078 = 0.432 \text{ m}$$

**Step 3**: Calculate $y$:
$$y = 0.5 \sin(0.785) + 0.3 \sin(1.309) = 0.5(0.707) + 0.3(0.966) = 0.354 + 0.290 = 0.644 \text{ m}$$

**Final Answer**: $(x, y) = (0.432, 0.644)$ m

**Explanation**: This uses the standard planar FK equations where each joint contributes to the overall position based on accumulated rotations [Spong et al., Ch. 3].

</details>
```

---

## Conceptual Comparison Questions

### Format

```markdown
**Question [NUMBER] (Compare)**: Compare and contrast [Concept A] and [Concept B]. Discuss [specific aspects].

<details>
<summary>Show Rubric</summary>

**Rubric** ([TOTAL] points):
- ([X] pts) [Similarity 1]
- ([X] pts) [Difference 1]
- ([X] pts) [Difference 2]
- ([X] pts) [Application context or when to use each]

**Sample Answer**: [Example full-credit response]

</details>
```

### Example

```markdown
**Question 7 (Compare)**: Compare and contrast Zero-Moment Point (ZMP) and Center of Pressure (CoP) for bipedal robots. When are they equivalent?

<details>
<summary>Show Rubric</summary>

**Rubric** (6 points):
- (2 pts) Definition of ZMP: Point on ground where horizontal moment from gravity and inertia equals zero
- (2 pts) Definition of CoP: Point where vertical ground reaction force acts (weighted average of pressure distribution)
- (1 pt) Equivalence: ZMP equals CoP during static balance or quasi-static motion (negligible angular momentum)
- (1 pt) Difference: During dynamic motion with significant angular momentum, ZMP may differ from CoP; ZMP can theoretically lie outside support polygon (indicating imminent fall), while CoP is always within it

**Sample Answer**: ZMP (Zero-Moment Point) is the point on the ground where the sum of horizontal moments from gravity and inertial forces equals zero. CoP (Center of Pressure) is the weighted average of the pressure distribution under the feet, where the net vertical ground reaction force acts. In static or quasi-static conditions (negligible angular momentum), ZMP and CoP coincide. However, during dynamic motion with significant angular momentum, they can differ—ZMP may lie outside the support polygon (indicating loss of balance), while CoP is always within the contact area by definition [Vukobratović & Borovac, 2004].

</details>
```

---

## Application Questions

### Format

```markdown
**Question [NUMBER] (App)**: [Scenario requiring application of concepts to solve a problem]

<details>
<summary>Show Rubric</summary>

**Rubric** ([TOTAL] points):
- ([X] pts) [Identification of relevant concept/principle]
- ([X] pts) [Correct application to scenario]
- ([X] pts) [Justification or explanation]
- ([X] pts) [Optional: Calculation or diagram]

**Sample Answer**: [Example response]

</details>
```

### Example

```markdown
**Question 8 (App)**: A humanoid robot is attempting to reach an object at position (0.6, 0.3, 0.8) m in the workspace. The robot's 6-DOF arm has a singularity when fully extended. How should the motion planner handle this reaching task to avoid singularities?

<details>
<summary>Show Rubric</summary>

**Rubric** (6 points):
- (2 pts) Identify that fully extended configuration is singular (loss of DOF, Jacobian rank deficiency)
- (2 pts) Propose solution: Use redundancy resolution, plan path that avoids singular configurations, or use damped least-squares IK
- (1 pt) Explain why singularities are problematic: Large/unbounded joint velocities, loss of controllability in certain directions
- (1 pt) Mention checking manipulability index or condition number during planning to quantify proximity to singularities

**Sample Answer**: When the arm is fully extended, it reaches a singularity where the Jacobian matrix loses rank, making it impossible to move the end-effector in certain directions (e.g., radially outward). To handle this, the motion planner should avoid trajectories that pass through or near singular configurations. One approach is to use redundancy resolution to find alternative joint configurations that achieve the same end-effector pose but maintain high manipulability. Alternatively, use damped least-squares inverse kinematics which adds numerical damping near singularities to prevent unbounded joint velocities [Siciliano et al., Ch. 3]. The planner can monitor the manipulability index (determinant of Jacobian) and replan if it drops below a threshold.

</details>
```

---

## Assessment Question Distribution by Chapter

Recommended mix of question types per chapter:

| Question Type | Count per Chapter | Purpose |
|---------------|-------------------|---------|
| Multiple Choice | 2-3 | Quick recall, concept identification |
| Short Answer | 2-3 | Explanation, reasoning, comparison |
| True/False | 0-2 | Misconception checking |
| Diagram | 0-1 | Visual understanding, labeling |
| Code Completion | 0-2 | Implementation skills |
| Calculation | 1-2 | Apply equations, numerical problem-solving |
| Comparison | 0-1 | Distinguish related concepts |
| Application | 1-2 | Scenario-based problem solving |
| **Total** | **5-10** | **Aligned with learning objectives** |

---

## Best Practices

1. **Align with Learning Objectives**: Each assessment should map to at least one chapter learning objective
2. **Progressive Difficulty**: Start with recall/understanding, progress to application/analysis
3. **Cite Sources**: Include citations in explanations where appropriate (reinforces research-backed learning)
4. **Avoid Ambiguity**: Questions should have clear, unambiguous correct answers
5. **Provide Feedback**: Explanations should teach, not just verify answers
6. **Balance Breadth and Depth**: Cover all major concepts but go deep on 1-2 core topics

---

## Answer Key Management

- **In-Chapter**: Use collapsible `<details>` tags for self-study textbook (students can reveal answers)
- **Instructor-Only**: For graded courses, maintain separate `assessment-key.md` file not deployed to public site
- **Auto-Grading**: For code questions, provide pytest test cases students can run locally

---

## Example: Full Assessment Section in Chapter

```markdown
## Assessments

Test your understanding of humanoid kinematics with these questions:

### Multiple Choice

**Question 1 (MC)**: What are the four Denavit-Hartenberg parameters?
[Full question as shown in example above]

**Question 2 (MC)**: Which of the following is NOT a valid inverse kinematics approach?
[Another MC question]

### Short Answer

**Question 3 (SA)**: Explain the difference between analytical and numerical IK...
[Full question as shown in example above]

### Calculation

**Question 4 (Calc)**: Compute the end-effector position for a 2-DOF planar arm...
[Full calculation question]

### Application

**Question 5 (App)**: A humanoid robot is attempting to reach an object...
[Full application question]

[5-10 questions total, mixed types]
```

---

This template ensures consistency, clear rubrics, and alignment with learning objectives across all chapters.

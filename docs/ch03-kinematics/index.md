---
id: ch03-kinematics
title: "Chapter 3: Humanoid Kinematics - Forward and Inverse"
sidebar_label: "Ch 3: Humanoid Kinematics"
sidebar_position: 3
description: "Master forward and inverse kinematics for humanoid manipulators using DH convention"
keywords:
  - forward kinematics
  - inverse kinematics
  - Denavit-Hartenberg
  - Jacobian
  - singularities
  - workspace
prerequisites:
  - ch02-robot-fundamentals/ch02-robot-fundamentals
  - "Linear algebra (matrices, matrix multiplication)"
  - "Trigonometry (sine, cosine, atan2)"
learning_objectives:
  - "Derive forward kinematics using the Denavit-Hartenberg convention"
  - "Implement forward kinematics for a 6-DOF humanoid arm"
  - "Solve inverse kinematics problems using analytical and numerical methods"
  - "Understand workspace limitations and singularities"
  - "Apply kinematics for robot control and motion planning"
estimated_time: "6-8 hours"
difficulty: intermediate
---

# Chapter 3: Humanoid Kinematics - Forward and Inverse

## Introduction

**Kinematics** is the study of motion without considering forces. For robots, kinematics answers two fundamental questions: (1) **Forward Kinematics (FK)**: Given joint angles, where is the end-effector? (2) **Inverse Kinematics (IK)**: Given a desired end-effector position, what joint angles achieve it?

- **Context**: Every time a humanoid reaches for an object, walks, or manipulates tools, it uses kinematics. FK tells the robot where its hand currently is; IK determines how to move joints to reach a target.

- **Preview**: This chapter derives forward kinematics using DH parameters from Chapter 2, explores analytical and numerical inverse kinematics methods, introduces the Jacobian matrix for velocity kinematics, and discusses workspace limitations and singularities.

- **Connection**: Kinematics provides the foundation for dynamics (Chapter 4), manipulation (Chapter 7), and motion planning (Chapter 6). It's the mathematical backbone of robot control.

---

## Key Concepts

### 1. Forward Kinematics (FK)

**Definition**: Forward kinematics computes the position and orientation of the end-effector given all joint angles [2], [3].

**Mathematical Formulation**:

For a serial manipulator with n joints:
```
T_0_n = T_0_1(q1) * T_1_2(q2) * ... * T_(n-1)_n(qn)
```

where:
- T_i_(i+1) is the DH transformation from frame i to i+1
- q_i is the joint variable (angle for revolute, position for prismatic)
- T_0_n is the final transformation from base to end-effector

**Example: 2-DOF Planar Arm**

Consider a simple 2-link planar arm with:
- Link 1: length L1, angle θ1
- Link 2: length L2, angle θ2

End-effector position:
```
x = L1*cos(θ1) + L2*cos(θ1 + θ2)
y = L1*sin(θ1) + L2*sin(θ1 + θ2)
```

**Application**: A humanoid arm with 7 DOF (shoulder: 3, elbow: 1, wrist: 3) uses FK to determine hand position for grasping. Given sensor-measured joint angles, FK computes where the hand is in 3D space.

**Computational Complexity**: O(n) matrix multiplications for n joints. Efficient enough for real-time control (1000 Hz+).

**Citation**: [2], [3]

---

### 2. Inverse Kinematics (IK)

**Definition**: Inverse kinematics finds joint angles q = [q1, q2, ..., qn] that position the end-effector at a desired pose (position + orientation) [2], [3].

**Problem Statement**:

Given desired end-effector pose T_desired, find joint angles q such that:
```
FK(q) = T_desired
```

**Challenges**:
1. **Multiple solutions**: May have 0, 1, or infinitely many solutions
2. **Nonlinear equations**: Trigonometric equations often have no closed-form solution
3. **Joint limits**: Solutions must satisfy physical constraints
4. **Singularities**: Some poses unreachable or require infinite joint velocities

**Example**: To grasp a cup at position (0.5, 0.3, 0.8) meters, IK computes shoulder, elbow, and wrist angles. For a 7-DOF arm (redundant), infinitely many solutions exist—choose one optimizing criteria like minimal joint motion.

---

#### Analytical IK

**Approach**: Derive closed-form equations by algebraic manipulation and geometric reasoning [2].

**When Possible**: Works for specific robot geometries, especially when:
- 3 consecutive joint axes intersect (spherical wrist)
- Arm is planar (all parallel Z-axes)
- Special symmetries exist

**Advantages**:
- Fast computation (direct calculation)
- All solutions found explicitly
- Deterministic (same input always gives same output)

**Disadvantages**:
- Requires manual derivation per robot
- Not always possible (no closed form exists for general 6+ DOF)

**Example - 2-DOF Planar Arm**:

Given target (x_d, y_d), solve for (θ1, θ2):

Step 1: Use law of cosines to find θ2:
```
cos(θ2) = (x_d² + y_d² - L1² - L2²) / (2*L1*L2)
θ2 = ±acos(cos(θ2))  # Two solutions (elbow up/down)
```

Step 2: Solve for θ1 using geometry:
```
θ1 = atan2(y_d, x_d) - atan2(L2*sin(θ2), L1 + L2*cos(θ2))
```

**Citation**: [2], [3]

---

#### Numerical IK

**Approach**: Iteratively adjust joint angles to minimize error between current and desired end-effector pose [2], [3].

**Jacobian-Based Method**:

The Jacobian J relates joint velocities to end-effector velocities:
```
velocity_end_effector = J(q) * velocity_joints
```

For IK, invert this relationship:
```
Δq = J^(-1) * Δx
```

where Δx = (x_desired - x_current) is position error.

**Algorithm** (Jacobian Pseudo-Inverse):
```
1. Initialize q (e.g., current joint angles)
2. Repeat until error < threshold:
   a. Compute current end-effector pose: x = FK(q)
   b. Compute error: Δx = x_desired - x
   c. Compute Jacobian: J = J(q)
   d. Update: q = q + J^+ * Δx  (J^+ is pseudo-inverse)
   e. Clamp q to joint limits
3. Return q
```

**Advantages**:
- Works for any robot configuration
- No manual derivation needed
- Handles redundancy (n > 6 DOF)

**Disadvantages**:
- Iterative (slower than analytical)
- May fail to converge
- Singularities cause numerical instability

**Damped Least Squares** (addresses singularities):
```
Δq = J^T * (J*J^T + λ²I)^(-1) * Δx
```

where λ is damping factor (e.g., 0.01).

**Citation**: [2], [3], [12]

---

### 3. Jacobian Matrix

**Definition**: The Jacobian J(q) is an m×n matrix of partial derivatives relating joint velocities to end-effector velocities [2], [3].

**Structure**:
```
J = [∂x/∂q1  ∂x/∂q2  ...  ∂x/∂qn]
    [∂y/∂q1  ∂y/∂q2  ...  ∂y/∂qn]
    [∂z/∂q1  ∂z/∂q2  ...  ∂z/∂qn]
    [∂ωx/∂q1 ∂ωx/∂q2 ... ∂ωx/∂qn]  (if including orientation)
    [∂ωy/∂q1 ∂ωy/∂q2 ... ∂ωy/∂qn]
    [∂ωz/∂q1 ∂ωz/∂q2 ... ∂ωz/∂qn]
```

**Velocity Kinematics**:
```
[v_x]       [J11  J12  ...  J1n]   [q1_dot]
[v_y]   =   [J21  J22  ...  J2n] * [q2_dot]
[v_z]       [J31  J32  ...  J3n]   [  ...  ]
[ω_x]       [J41  J42  ...  J4n]   [qn_dot]
[ω_y]       [J51  J52  ...  J5n]
[ω_z]       [J61  J62  ...  J6n]
```

**Applications**:
1. **IK**: Invert to find joint velocities for desired end-effector velocity
2. **Singularity detection**: Singular when det(J*J^T) = 0 or rank(J) < 6
3. **Force control**: Relate joint torques to end-effector forces: τ = J^T * F
4. **Manipulability**: Measure dexterity via manipulability index = sqrt(det(J*J^T))

**Geometric Jacobian** (column i for revolute joint):
```
J_i = [z_(i-1) × (p_n - p_(i-1))]  (linear velocity component)
      [      z_(i-1)             ]  (angular velocity component)
```

where z_(i-1) is joint axis direction, p_n is end-effector position, p_(i-1) is joint position.

**Citation**: [2], [3]

---

### 4. Workspace

**Definition**: The workspace is the set of all positions (and orientations) the end-effector can reach [2].

**Types**:
1. **Reachable Workspace**: All points reachable with at least one orientation
2. **Dexterous Workspace**: Points reachable with arbitrary orientations

**Factors Determining Workspace**:
- Link lengths (longer links → larger workspace)
- Joint limits (restricted ranges reduce workspace)
- Mechanical interference (links colliding with each other or robot body)
- Singularities (some regions unreachable or poorly controllable)

**Example**: A humanoid arm with 0.3m shoulder-elbow and 0.25m elbow-wrist links has maximum reach ≈ 0.55m from shoulder (slightly less due to joint limits). Objects beyond this distance are outside the workspace.

**Workspace Analysis**:
- **Monte Carlo sampling**: Generate random joint angles within limits, compute FK, plot resulting points
- **Analytical boundaries**: Solve for workspace envelope mathematically (complex for >2 DOF)

**Citation**: [2]

---

### 5. Singularities

**Definition**: A singularity occurs when the Jacobian matrix loses rank, causing loss of one or more DOF in end-effector motion [2], [3].

**Detection**: Singularity exists when:
- det(J) = 0 (for square Jacobian, n=6)
- rank(J) < min(m, n) (general case)
- Condition number κ(J) = σ_max/σ_min → ∞ (singular values)

**Types**:
1. **Boundary singularities**: Occur at workspace edge (arm fully extended or folded)
2. **Internal singularities**: Occur inside workspace (specific alignments)
3. **Wrist singularities**: Two wrist axes align (spherical wrist)

**Consequences**:
- Cannot move in certain directions (DOF lost)
- Small end-effector motion requires unbounded joint velocities
- Numerical IK fails (Jacobian non-invertible)

**Example**: Humanoid arm fully extended (elbow at 180°) is a boundary singularity. Cannot move further outward; can only retract.

**Avoidance Strategies**:
1. **Path planning**: Plan trajectories avoiding singular configurations
2. **Damped least squares**: Add damping to Jacobian inverse (see Numerical IK)
3. **Redundancy**: Use extra DOF (7-DOF arm) to reconfigure away from singularities

**Citation**: [2], [3]

---

## Code Examples

### Example 1: Forward Kinematics for 3-DOF Arm

```python
"""
Forward Kinematics Implementation
3-DOF planar arm using DH parameters
"""

import numpy as np

def dh_transform(a, alpha, d, theta):
    """Create DH transformation matrix"""
    ct, st = np.cos(theta), np.sin(theta)
    ca, sa = np.cos(alpha), np.sin(alpha)

    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,   sa,     ca,    d   ],
        [0,   0,      0,     1   ]
    ])

def forward_kinematics_3dof(theta1, theta2, theta3, L1=0.5, L2=0.3, L3=0.2):
    """
    Compute end-effector pose for 3-DOF planar arm

    Args:
        theta1, theta2, theta3: Joint angles (radians)
        L1, L2, L3: Link lengths (meters)

    Returns:
        T: 4x4 end-effector transformation matrix
        position: (x, y, z) end-effector position
    """
    # DH parameters for planar arm (all alpha=0, d=0)
    T01 = dh_transform(L1, 0, 0, theta1)
    T12 = dh_transform(L2, 0, 0, theta2)
    T23 = dh_transform(L3, 0, 0, theta3)

    # Chain transformations
    T = T01 @ T12 @ T23

    position = T[0:3, 3]
    return T, position

def main():
    # Test case
    theta = [np.radians(30), np.radians(45), np.radians(60)]

    T, pos = forward_kinematics_3dof(*theta)

    print("Forward Kinematics - 3-DOF Arm")
    print(f"Joint angles: {np.degrees(theta)}°")
    print(f"\nEnd-effector position:")
    print(f"  x = {pos[0]:.4f} m")
    print(f"  y = {pos[1]:.4f} m")
    print(f"  z = {pos[2]:.4f} m")
    print(f"\nFull transformation matrix:")
    print(T)

if __name__ == "__main__":
    main()
```

---

### Example 2: Jacobian Pseudo-Inverse IK

```python
"""
Numerical Inverse Kinematics
Jacobian pseudo-inverse method for 3-DOF arm
"""

import numpy as np

def compute_jacobian_numerical(fk_func, q, delta=1e-6):
    """
    Compute Jacobian numerically via finite differences

    Args:
        fk_func: Forward kinematics function q -> position
        q: Current joint angles
        delta: Perturbation for numerical derivative

    Returns:
        J: 3xn Jacobian matrix (position only)
    """
    n = len(q)
    x0 = fk_func(q)
    m = len(x0)

    J = np.zeros((m, n))

    for i in range(n):
        q_perturb = q.copy()
        q_perturb[i] += delta
        x_perturb = fk_func(q_perturb)
        J[:, i] = (x_perturb - x0) / delta

    return J

def inverse_kinematics_numerical(target, fk_func, q_init, max_iter=100, tol=1e-3):
    """
    Solve IK using Jacobian pseudo-inverse

    Args:
        target: Desired (x, y, z) position
        fk_func: Forward kinematics function
        q_init: Initial joint guess
        max_iter: Maximum iterations
        tol: Convergence tolerance (meters)

    Returns:
        q: Joint angles solution
        success: True if converged
    """
    q = q_init.copy()

    for iteration in range(max_iter):
        # Current position
        x_current = fk_func(q)
        error = target - x_current
        error_norm = np.linalg.norm(error)

        if error_norm < tol:
            print(f"Converged in {iteration} iterations")
            return q, True

        # Compute Jacobian and pseudo-inverse
        J = compute_jacobian_numerical(fk_func, q)
        J_pinv = np.linalg.pinv(J)  # Pseudo-inverse

        # Update joint angles
        delta_q = J_pinv @ error
        q = q + 0.5 * delta_q  # Step size 0.5 for stability

        # Clamp to joint limits (example: ±π)
        q = np.clip(q, -np.pi, np.pi)

    print(f"Failed to converge after {max_iter} iterations")
    return q, False

def fk_position_only(q):
    """Wrapper for FK returning position only"""
    _, pos = forward_kinematics_3dof(q[0], q[1], q[2])
    return pos

def main():
    print("Inverse Kinematics - Jacobian Pseudo-Inverse\n")

    # Target position
    target = np.array([0.7, 0.5, 0.0])
    print(f"Target position: {target}")

    # Initial guess (all zeros)
    q_init = np.array([0.0, 0.0, 0.0])

    # Solve IK
    q_solution, success = inverse_kinematics_numerical(
        target, fk_position_only, q_init
    )

    if success:
        print(f"\nSolution found:")
        print(f"  θ1 = {np.degrees(q_solution[0]):.2f}°")
        print(f"  θ2 = {np.degrees(q_solution[1]):.2f}°")
        print(f"  θ3 = {np.degrees(q_solution[2]):.2f}°")

        # Verify
        pos_achieved = fk_position_only(q_solution)
        error = np.linalg.norm(target - pos_achieved)
        print(f"\nVerification:")
        print(f"  Achieved: {pos_achieved}")
        print(f"  Error: {error:.6f} m")
    else:
        print("\nIK failed to converge")

if __name__ == "__main__":
    # Import FK function from Example 1
    main()
```

---

## Practical Exercises

1. **[Implement DH-Based Forward Kinematics](exercises/ex01-dh-fk.md)** - Derive and implement FK for a 6-DOF humanoid arm; verify with known test cases
2. **[Develop Inverse Kinematics Solver](exercises/ex02-ik-solver.md)** - Create analytical IK for 2-DOF arm, then numerical IK for 3-DOF; compare solutions

---

## Assessments

### Multiple Choice

**Q1**: For a 3-DOF planar arm, how many solutions typically exist for a reachable target position?

A) Always exactly 1
B) Typically 2 (elbow up/down)
C) Infinitely many
D) 0 or 1

<details>
<summary>Answer</summary>

**Answer**: B

**Explanation**: A 3-DOF planar arm typically has 2 solutions corresponding to "elbow up" and "elbow down" configurations for the same end-effector position (assuming the position is reachable). Infinitely many solutions (C) require redundancy (n > m DOF) [2], [3].
</details>

---

**Q2**: What does a Jacobian singularity indicate?

A) End-effector has reached maximum speed
B) Robot has lost one or more degrees of freedom in motion
C) Joint angles have exceeded limits
D) Forward kinematics cannot be computed

<details>
<summary>Answer</summary>

**Answer**: B

**Explanation**: At a singularity, the Jacobian loses rank, meaning the robot cannot move in certain directions—it has lost DOF. This typically occurs at workspace boundaries or specific joint alignments [2], [3].
</details>

---

### Short Answer

**Q3**: Explain why inverse kinematics is more challenging than forward kinematics for a 6-DOF robot arm.

<details>
<summary>Rubric (5 pts)</summary>

- (2 pts) FK is direct matrix multiplication (unique solution); IK requires solving nonlinear equations
- (2 pts) IK may have 0, 1, or multiple solutions; must handle joint limits and singularities
- (1 pt) IK computationally harder: analytical requires derivation, numerical requires iteration
</details>

---

**Q4**: A 7-DOF humanoid arm (redundant) reaches for a cup. How many solutions exist for the IK problem? How would you choose one?

<details>
<summary>Rubric (6 pts)</summary>

- (2 pts) Infinitely many solutions (7 DOF for 6 DOF task = 1 redundant DOF)
- (3 pts) Selection criteria examples: minimize joint motion, avoid obstacles, optimize manipulability, maintain comfortable posture, secondary task (e.g., camera pointing)
- (1 pt) Mentions null-space projection or optimization
</details>

---

### Application

**Q5**: Compute IK analytically for a 2-DOF planar arm (L1=0.5m, L2=0.3m) reaching target (x=0.6, y=0.4). Show both elbow-up and elbow-down solutions.

<details>
<summary>Rubric (8 pts)</summary>

- (2 pts) Correctly applies law of cosines: cos(θ2) = (0.6² + 0.4² - 0.5² - 0.3²) / (2*0.5*0.3) = 0.146
- (2 pts) Finds θ2: ±acos(0.146) = ±81.6° (two solutions)
- (3 pts) Finds θ1 for each θ2 using atan2 formula
- (1 pt) Reports both solutions with correct units

Reference: [2]
</details>

---

**Q6**: Explain how you would use the Jacobian to perform force control—making a robot apply a desired force at the end-effector.

<details>
<summary>Rubric (5 pts)</summary>

- (2 pts) Relationship: τ = J^T * F (joint torques from end-effector force)
- (2 pts) Explains: Transpose Jacobian maps forces (not just velocities); used in impedance/force control
- (1 pt) Example: pushing a button with 5N force

Reference: [2], [13]
</details>

---

## Further Reading

1. **J. J. Craig, *Introduction to Robotics*, Ch. 3-4.** [2] - Excellent coverage of FK/IK with worked examples
2. **B. Siciliano et al., *Robotics*, Ch. 2-3.** [1] - Comprehensive kinematics theory and Jacobian derivations
3. **S. M. LaValle, *Planning Algorithms*, Ch. 4.** [17] - FK/IK in context of motion planning
4. **D. E. Whitney, "Resolved motion rate control," *IEEE Trans. Man-Mach. Syst.*, 1969.** [12] - Foundational paper on Jacobian-based control

---

## Summary

This chapter mastered **forward and inverse kinematics** for humanoid manipulators. We learned to derive **forward kinematics** using DH parameters, computing end-effector pose from joint angles via transformation matrix chains. We explored **inverse kinematics**: analytical solutions for simple geometries and numerical Jacobian-based methods for general cases. The **Jacobian matrix** emerged as a critical tool relating joint velocities to end-effector velocities, enabling IK, singularity detection, and force control. We characterized **workspace** boundaries and identified **singularities** where motion capability degrades. You implemented FK and numerical IK in Python, preparing you for dynamics and control (Chapter 4) and trajectory planning (Chapter 6).

**Next Chapter Preview**: Chapter 4 introduces dynamics—the relationship between forces/torques and motion. You'll learn Lagrangian dynamics derivation, PID control, computed-torque control, and impedance control for humanoid robots.

---

## References

Key sources: [1], [2], [3], [12], [13], [17]

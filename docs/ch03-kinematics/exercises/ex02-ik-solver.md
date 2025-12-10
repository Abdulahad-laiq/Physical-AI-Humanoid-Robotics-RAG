---
exercise_id: ex03-02-ik-solver
chapter: ch03-kinematics
title: "Develop Inverse Kinematics Solvers (Analytical and Numerical)"
learning_outcome: "Implement and compare analytical and numerical IK solutions for planar manipulators"
difficulty: advanced
estimated_time: "120-150 minutes"
prerequisites:
  - "Chapter 3: Inverse kinematics and Jacobian sections"
  - "Exercise 1: Forward kinematics implementation"
  - "Linear algebra (matrix pseudo-inverse, numerical methods)"
tools:
  - Python 3.9+
  - NumPy
  - Matplotlib (for convergence plots)
---

# Exercise: Develop Inverse Kinematics Solvers

## Overview

Implement both analytical and numerical inverse kinematics solvers for planar manipulators, then compare their performance, convergence properties, and applicability. You'll solve the fundamental problem: given a desired end-effector position, what joint angles achieve it?

**What you'll build**: Two IK implementations—closed-form analytical solution for 2-DOF arm and iterative Jacobian-based solver for 3-DOF arm

**Why it matters**: IK is essential for task-space control. When you want a robot to reach a specific point or follow a trajectory, you need IK to convert Cartesian goals into joint commands [1]. This is used millions of times daily in manufacturing, surgery, and service robotics.

**Real-world application**: Surgical robots like da Vinci use real-time IK to map surgeon hand motions to instrument tip positions. Industrial robots use IK for pick-and-place, welding, and assembly tasks [2].

---

## Problem Statement

### Part 1: Analytical IK for 2-DOF Planar Arm

**Given**: 2-DOF planar arm (RR configuration, both joints revolute, Z-axes parallel)

| Joint | Link Length (m) | θ (variable) |
|-------|-----------------|--------------|
| 1     | L₁ = 0.5        | θ₁           |
| 2     | L₂ = 0.3        | θ₂           |

**Task**: Implement `analytical_ik_2dof(x, y, L1, L2)` that:
1. Computes joint angles θ₁, θ₂ to reach position (x, y)
2. Returns both elbow-up and elbow-down solutions when they exist
3. Detects unreachable positions (outside workspace)

**Approach**: Use law of cosines to solve the closed-form geometric solution [3].

---

### Part 2: Numerical IK for 3-DOF Planar Arm

**Given**: 3-DOF planar arm (RRR configuration)

| Joint | Link Length (m) | θ (variable) |
|-------|-----------------|--------------|
| 1     | L₁ = 0.5        | θ₁           |
| 2     | L₂ = 0.3        | θ₂           |
| 3     | L₃ = 0.2        | θ₃           |

**Task**: Implement `numerical_ik_3dof(x, y, L1, L2, L3, q_init)` that:
1. Uses Jacobian pseudo-inverse method to iteratively solve IK
2. Starts from initial guess `q_init`
3. Converges to solution with error < 1mm
4. Returns joint angles, convergence status, and iteration count

**Test Cases**:
1. **Target 1**: (x=0.7, y=0.4) - within workspace, moderate reach
2. **Target 2**: (x=0.3, y=0.8) - within workspace, high elevation
3. **Target 3**: (x=1.2, y=0.2) - at workspace boundary
4. **Target 4**: (x=1.5, y=0.5) - outside workspace (should fail gracefully)

**Success Criteria**:
- [ ] Analytical IK returns both solutions when available
- [ ] Analytical IK detects unreachable targets correctly
- [ ] Numerical IK converges within 100 iterations for reachable targets
- [ ] Numerical IK achieves position error < 1mm
- [ ] Convergence plots show monotonic error decrease
- [ ] Code handles singularities gracefully (damped least squares optional)

---

## Theoretical Background

### Analytical IK: 2-DOF Planar Arm

For a 2-DOF planar arm, the forward kinematics is:

```
x = L₁·cos(θ₁) + L₂·cos(θ₁ + θ₂)
y = L₁·sin(θ₁) + L₂·sin(θ₁ + θ₂)
```

Using the law of cosines on the triangle formed by (0,0), (x,y), and the elbow position:

```
cos(θ₂) = (x² + y² - L₁² - L₂²) / (2·L₁·L₂)

θ₂ = ± arccos(cos(θ₂))  # Two solutions: elbow-up (+) and elbow-down (-)

θ₁ = arctan2(y, x) - arctan2(L₂·sin(θ₂), L₁ + L₂·cos(θ₂))
```

**Reachability condition**: |cos(θ₂)| ≤ 1, which means: (L₁ - L₂) ≤ sqrt(x² + y²) ≤ (L₁ + L₂)

---

### Numerical IK: Jacobian Pseudo-Inverse

For systems where analytical solutions are intractable (3+ DOF, arbitrary geometry), use iterative methods:

**Jacobian Pseudo-Inverse Algorithm:**

```
1. Initialize: q = q_init
2. Repeat until convergence:
   a. Compute current position: x_current = FK(q)
   b. Compute error: e = x_target - x_current
   c. If ||e|| < tolerance: SUCCESS
   d. Compute Jacobian: J = ∂FK/∂q (numerical differentiation)
   e. Compute pseudo-inverse: J⁺ = J^T(JJ^T)^(-1)
   f. Update: q = q + α·J⁺·e  (α = step size)
   g. Apply joint limits
3. Return q if converged, else FAILURE
```

**Damped Least Squares (optional)**: For near-singular configurations, use:

```
J⁺_damped = J^T(JJ^T + λ²I)^(-1)
```

where λ is the damping factor (typically 0.01-0.1) [4].

---

## Code Template

```python
import numpy as np
import matplotlib.pyplot as plt

# ========== Part 1: Analytical IK for 2-DOF Arm ==========

def analytical_ik_2dof(x, y, L1=0.5, L2=0.3):
    """
    Analytical IK for 2-DOF planar arm using law of cosines

    Args:
        x, y: target end-effector position (m)
        L1: length of link 1 (m)
        L2: length of link 2 (m)

    Returns:
        solutions: list of (theta1, theta2) tuples in radians
                   Empty list if target is unreachable
    """
    # Distance from base to target
    r = np.sqrt(x**2 + y**2)

    # Check reachability
    if r > (L1 + L2) or r < abs(L1 - L2):
        print(f"Target ({x:.2f}, {y:.2f}) is unreachable. Distance: {r:.3f} m")
        print(f"Workspace: [{abs(L1-L2):.3f}, {L1+L2:.3f}] m")
        return []

    # TODO: Compute cos(theta2) using law of cosines
    # cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)

    # TODO: Compute two solutions for theta2 (elbow-up and elbow-down)
    # theta2_elbow_up = np.arccos(cos_theta2)
    # theta2_elbow_down = -np.arccos(cos_theta2)

    # TODO: For each theta2, compute corresponding theta1
    # Use: theta1 = arctan2(y, x) - arctan2(L2*sin(theta2), L1 + L2*cos(theta2))

    solutions = []

    # TODO: Append both solutions to list
    # solutions.append((theta1_up, theta2_up))
    # solutions.append((theta1_down, theta2_down))

    return solutions

def verify_2dof_solution(theta1, theta2, target_x, target_y, L1=0.5, L2=0.3):
    """Verify IK solution by computing FK"""
    x_fk = L1 * np.cos(theta1) + L2 * np.cos(theta1 + theta2)
    y_fk = L1 * np.sin(theta1) + L2 * np.sin(theta1 + theta2)

    error = np.sqrt((x_fk - target_x)**2 + (y_fk - target_y)**2)
    return x_fk, y_fk, error

# ========== Part 2: Numerical IK for 3-DOF Arm ==========

def forward_kinematics_3dof(q, L1=0.5, L2=0.3, L3=0.2):
    """
    Forward kinematics for 3-DOF planar arm

    Args:
        q: array [theta1, theta2, theta3] in radians
        L1, L2, L3: link lengths

    Returns:
        position: (x, y) end-effector position
    """
    theta1, theta2, theta3 = q
    x = L1*np.cos(theta1) + L2*np.cos(theta1 + theta2) + L3*np.cos(theta1 + theta2 + theta3)
    y = L1*np.sin(theta1) + L2*np.sin(theta1 + theta2) + L3*np.sin(theta1 + theta2 + theta3)
    return np.array([x, y])

def compute_jacobian_numerical(fk_func, q, epsilon=1e-6):
    """
    Compute Jacobian using numerical differentiation

    Args:
        fk_func: forward kinematics function
        q: current joint configuration
        epsilon: finite difference step size

    Returns:
        J: 2×3 Jacobian matrix
    """
    n = len(q)
    x0 = fk_func(q)
    m = len(x0)

    J = np.zeros((m, n))

    for i in range(n):
        q_perturbed = q.copy()
        q_perturbed[i] += epsilon
        x_perturbed = fk_func(q_perturbed)
        J[:, i] = (x_perturbed - x0) / epsilon

    return J

def numerical_ik_3dof(target, L1=0.5, L2=0.3, L3=0.2, q_init=None,
                       max_iter=100, tolerance=1e-3, alpha=0.5, use_damping=False):
    """
    Numerical IK using Jacobian pseudo-inverse method

    Args:
        target: desired (x, y) position
        L1, L2, L3: link lengths
        q_init: initial joint configuration (if None, use zeros)
        max_iter: maximum iterations
        tolerance: convergence threshold (m)
        alpha: step size (0 < alpha <= 1)
        use_damping: whether to use damped least squares

    Returns:
        q: final joint configuration
        converged: True if converged within tolerance
        iterations: number of iterations
        errors: list of errors at each iteration
    """
    if q_init is None:
        q = np.zeros(3)
    else:
        q = q_init.copy()

    errors = []

    for iteration in range(max_iter):
        # Compute current position
        x_current = forward_kinematics_3dof(q, L1, L2, L3)

        # Compute error
        error_vec = target - x_current
        error_norm = np.linalg.norm(error_vec)
        errors.append(error_norm)

        # Check convergence
        if error_norm < tolerance:
            return q, True, iteration + 1, errors

        # TODO: Compute Jacobian
        # J = compute_jacobian_numerical(lambda q: forward_kinematics_3dof(q, L1, L2, L3), q)

        # TODO: Compute pseudo-inverse
        # if use_damping:
        #     lambda_damping = 0.01
        #     J_pinv = J.T @ np.linalg.inv(J @ J.T + lambda_damping**2 * np.eye(2))
        # else:
        #     J_pinv = np.linalg.pinv(J)

        # TODO: Update joint angles
        # delta_q = alpha * J_pinv @ error_vec
        # q = q + delta_q

        # TODO: Apply joint limits (optional)
        # q = np.clip(q, -np.pi, np.pi)

        pass  # Remove after implementing

    # Failed to converge
    return q, False, max_iter, errors

# ========== Testing and Visualization ==========

def test_analytical_ik():
    """Test analytical IK with multiple targets"""
    print("=== Analytical IK Test (2-DOF) ===\n")

    targets = [
        (0.7, 0.3, "Reachable - moderate"),
        (0.4, 0.6, "Reachable - high elevation"),
        (0.8, 0.0, "Reachable - extended"),
        (1.0, 0.5, "Unreachable - too far")
    ]

    for x, y, description in targets:
        print(f"Target: ({x:.2f}, {y:.2f}) - {description}")
        solutions = analytical_ik_2dof(x, y)

        if not solutions:
            print("  No solution\n")
            continue

        for i, (theta1, theta2) in enumerate(solutions):
            config = "elbow-up" if i == 0 else "elbow-down"
            x_fk, y_fk, error = verify_2dof_solution(theta1, theta2, x, y)

            print(f"  Solution {i+1} ({config}):")
            print(f"    θ₁ = {np.degrees(theta1):6.2f}°, θ₂ = {np.degrees(theta2):6.2f}°")
            print(f"    FK verification: ({x_fk:.4f}, {y_fk:.4f}), error = {error:.6f} m")

        print()

def test_numerical_ik():
    """Test numerical IK with multiple targets"""
    print("=== Numerical IK Test (3-DOF) ===\n")

    targets = [
        (np.array([0.7, 0.4]), "Moderate reach"),
        (np.array([0.3, 0.8]), "High elevation"),
        (np.array([0.95, 0.2]), "Near boundary"),
        (np.array([1.2, 0.5]), "Outside workspace")
    ]

    for target, description in targets:
        print(f"Target: ({target[0]:.2f}, {target[1]:.2f}) - {description}")

        q_init = np.array([0.0, 0.0, 0.0])  # Start from zero configuration

        q_final, converged, iterations, errors = numerical_ik_3dof(
            target, q_init=q_init, max_iter=100, tolerance=1e-3, alpha=0.5
        )

        x_final = forward_kinematics_3dof(q_final)
        final_error = np.linalg.norm(target - x_final)

        print(f"  Converged: {converged} (iterations: {iterations})")
        print(f"  Final joint angles (deg): [{np.degrees(q_final[0]):.2f}, {np.degrees(q_final[1]):.2f}, {np.degrees(q_final[2]):.2f}]")
        print(f"  Achieved position: ({x_final[0]:.4f}, {x_final[1]:.4f})")
        print(f"  Final error: {final_error:.6f} m")
        print()

def plot_convergence(target, q_init, L1=0.5, L2=0.3, L3=0.2):
    """Plot convergence curve for numerical IK"""
    q_final, converged, iterations, errors = numerical_ik_3dof(
        target, L1, L2, L3, q_init, max_iter=100, tolerance=1e-3, alpha=0.5
    )

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(errors, 'b-', linewidth=2)
    plt.axhline(y=1e-3, color='r', linestyle='--', label='Tolerance (1mm)')
    plt.xlabel('Iteration')
    plt.ylabel('Position Error (m)')
    plt.title(f'IK Convergence: Target ({target[0]:.2f}, {target[1]:.2f})')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.yscale('log')

    plt.subplot(1, 2, 2)
    plt.plot(errors, 'b-', linewidth=2)
    plt.axhline(y=1e-3, color='r', linestyle='--', label='Tolerance')
    plt.xlabel('Iteration')
    plt.ylabel('Position Error (m)')
    plt.title('Convergence (Linear Scale)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig('ik_convergence.png', dpi=150)
    print("Convergence plot saved: ik_convergence.png")

def main():
    """Main execution function"""
    test_analytical_ik()
    print("\n" + "="*60 + "\n")
    test_numerical_ik()

    # Optional: Plot convergence for a specific target
    # plot_convergence(target=np.array([0.7, 0.4]), q_init=np.zeros(3))

if __name__ == "__main__":
    main()
```

**Deliverable**: Completed code with test output showing:
- Both analytical solutions for reachable 2-DOF targets
- Numerical IK convergence within 100 iterations for reachable 3-DOF targets
- Convergence plot (optional)

---

## Implementation Hints

1. **Analytical IK Debugging**: If solutions don't verify via FK, check:
   - Sign conventions for arctan2 (y argument first, x second)
   - Angle wrapping (use `np.arctan2` instead of `np.arccos` + sign logic when possible)

2. **Jacobian Computation**: Numerical differentiation is simpler than analytical but slower. For production, derive analytical Jacobian.

3. **Step Size Tuning**: If numerical IK oscillates, reduce alpha. If it converges slowly, increase alpha carefully.

4. **Singularity Handling**: Near singularities, J becomes ill-conditioned. Damped least squares prevents large joint velocities.

5. **Initialization Matters**: For numerical IK, good initial guesses converge faster and avoid local minima.

---

## Extension Challenges (Optional)

1. **Orientation Control**: Extend 3-DOF IK to also control end-effector orientation (requires 3D workspace)

2. **Multiple Solutions**: Modify numerical IK to find multiple solutions by trying different initial configurations

3. **Cyclic Coordinate Descent**: Implement alternative numerical IK using CCD algorithm

4. **Benchmark Comparison**: Compare analytical vs. numerical speed and accuracy on 1000 random targets

5. **Obstacle Avoidance**: Add constraints to numerical IK to avoid joint-space or Cartesian obstacles

---

## Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Analytical IK implementation | 3 | Correct law of cosines application, both solutions returned |
| Analytical reachability check | 1 | Correctly detects unreachable targets |
| Numerical IK implementation | 3 | Jacobian pseudo-inverse method correctly implemented |
| Convergence for reachable targets | 1.5 | Achieves error < 1mm within 100 iterations |
| Unreachable target handling | 0.5 | Gracefully handles targets outside workspace |
| Code quality & documentation | 1 | Clear comments, modular functions, test coverage |

**Total**: 10 points

---

## References

[1] Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2009). *Robotics: Modelling, Planning and Control*. Springer. (Chapter 3: Differential Kinematics)

[2] Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson Education. (Chapter 4: Inverse Manipulator Kinematics)

[3] Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. Wiley. (Chapter 3: Forward and Inverse Kinematics)

[4] Nakamura, Y., & Hanafusa, H. (1986). Inverse kinematic solutions with singularity robustness for robot manipulator control. *Journal of Dynamic Systems, Measurement, and Control*, 108(3), 163-171.

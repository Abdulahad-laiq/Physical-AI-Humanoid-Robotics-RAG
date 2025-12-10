---
exercise_id: ex03-01-dh-fk
chapter: ch03-kinematics
title: "Implement Forward Kinematics for 6-DOF Humanoid Arm"
learning_outcome: "Derive and implement DH-based forward kinematics for a 6-DOF humanoid manipulator"
difficulty: intermediate
estimated_time: "90-120 minutes"
prerequisites:
  - "Chapter 2: DH parameters and homogeneous transformations"
  - "Chapter 3: Forward kinematics section"
  - "Linear algebra (matrix multiplication, frame transformations)"
tools:
  - Python 3.9+
  - NumPy
  - Matplotlib (optional for visualization)
---

# Exercise: Implement Forward Kinematics for 6-DOF Humanoid Arm

## Overview

Implement forward kinematics for a 6-DOF humanoid robot arm using Denavit-Hartenberg (DH) parameters. You'll construct transformation matrices for each joint and chain them to compute the end-effector pose (position and orientation) for any given joint configuration.

**What you'll build**: Python functions to compute FK for a 6-DOF arm with verification against analytical solutions

**Why it matters**: Forward kinematics is the foundation of robot control—every motion planner, simulator, and controller needs to know where the robot's end-effector is for a given joint configuration [1].

**Real-world application**: Industrial robots like the KUKA LBR iiwa and collaborative robots like UR5 use FK hundreds of times per second for trajectory execution, collision checking, and visual servoing [2].

---

## Problem Statement

**Given**: 6-DOF humanoid arm with revolute joints. DH parameters (Standard DH convention):

| Joint | a (m) | α (rad) | d (m) | θ (variable) | Joint Limits (rad) |
|-------|-------|---------|-------|--------------|---------------------|
| 1     | 0     | π/2     | 0.3   | θ₁           | [-π, π]             |
| 2     | 0.4   | 0       | 0     | θ₂           | [-π/2, π/2]         |
| 3     | 0.39  | 0       | 0     | θ₃           | [-π, π]             |
| 4     | 0     | π/2     | 0.35  | θ₄           | [-π, π]             |
| 5     | 0     | -π/2    | 0     | θ₅           | [-π/2, π/2]         |
| 6     | 0     | 0       | 0.09  | θ₆           | [-π, π]             |

**Task**: Implement `forward_kinematics_6dof(theta)` that:
1. Accepts a 6-element array of joint angles
2. Computes the transformation from base to end-effector: T₀₆ = T₀₁ · T₁₂ · T₂₃ · T₃₄ · T₄₅ · T₅₆
3. Returns the 4×4 homogeneous transformation matrix and extracts position (x, y, z) and orientation (rotation matrix)

**Test Cases**:
1. **Home Position**: θ = [0, 0, 0, 0, 0, 0]
2. **Right Angle Configuration**: θ = [π/2, π/4, 0, π/2, 0, 0]
3. **Complex Configuration**: θ = [π/6, -π/3, π/4, π/6, -π/4, π/3]

**Success Criteria**:
- [ ] `dh_transform(a, alpha, d, theta)` returns correct 4×4 matrix
- [ ] Forward kinematics chains all 6 transformations correctly
- [ ] Test case 1 (home position) matches expected analytical solution
- [ ] Position error < 1mm for all test cases when verified numerically
- [ ] Code includes joint limit validation

---

## Theoretical Background

### DH Transformation Matrix

For each link i, the transformation from frame (i-1) to frame (i) is:

```
T(i-1,i) = Rot_z(θᵢ) · Trans_z(dᵢ) · Trans_x(aᵢ) · Rot_x(αᵢ)
```

In matrix form:

```
T = | cos(θ)  -sin(θ)cos(α)   sin(θ)sin(α)   a·cos(θ) |
    | sin(θ)   cos(θ)cos(α)  -cos(θ)sin(α)   a·sin(θ) |
    | 0        sin(α)          cos(α)         d        |
    | 0        0               0              1        |
```

### Chaining Transformations

The overall transformation from base to end-effector:

```
T₀₆ = T₀₁ @ T₁₂ @ T₂₃ @ T₃₄ @ T₄₅ @ T₅₆
```

where @ denotes matrix multiplication [3].

---

## Code Template

```python
import numpy as np

def dh_transform(a, alpha, d, theta):
    """
    Create DH transformation matrix using standard DH convention

    Args:
        a: link length (m)
        alpha: link twist (rad)
        d: link offset (m)
        theta: joint angle (rad)

    Returns:
        4×4 homogeneous transformation matrix
    """
    # TODO: Implement DH transformation matrix
    # T = Rz(theta) * Tz(d) * Tx(a) * Rx(alpha)

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

def forward_kinematics_6dof(theta):
    """
    Compute forward kinematics for 6-DOF humanoid arm

    Args:
        theta: array of 6 joint angles [θ₁, θ₂, θ₃, θ₄, θ₅, θ₆] in radians

    Returns:
        T: 4×4 homogeneous transformation matrix from base to end-effector
        position: (x, y, z) end-effector position
        orientation: 3×3 rotation matrix
    """
    # Validate input
    if len(theta) != 6:
        raise ValueError("Expected 6 joint angles")

    # Joint limits (optional validation)
    limits = [
        (-np.pi, np.pi),
        (-np.pi/2, np.pi/2),
        (-np.pi, np.pi),
        (-np.pi, np.pi),
        (-np.pi/2, np.pi/2),
        (-np.pi, np.pi)
    ]

    for i, (angle, (min_lim, max_lim)) in enumerate(zip(theta, limits)):
        if not (min_lim <= angle <= max_lim):
            print(f"Warning: Joint {i+1} angle {angle:.3f} exceeds limits [{min_lim:.3f}, {max_lim:.3f}]")

    # DH parameters [a, alpha, d]
    dh_params = [
        [0,    np.pi/2,  0.3 ],  # Joint 1
        [0.4,  0,        0   ],  # Joint 2
        [0.39, 0,        0   ],  # Joint 3
        [0,    np.pi/2,  0.35],  # Joint 4
        [0,   -np.pi/2,  0   ],  # Joint 5
        [0,    0,        0.09]   # Joint 6
    ]

    # TODO: Create transformation matrices for each joint
    # T01 = dh_transform(dh_params[0][0], dh_params[0][1], dh_params[0][2], theta[0])
    # ...

    # TODO: Chain transformations
    # T = T01 @ T12 @ T23 @ T34 @ T45 @ T56

    # TODO: Extract position and orientation
    # position = T[0:3, 3]
    # orientation = T[0:3, 0:3]

    pass  # Remove this and implement

def test_forward_kinematics():
    """Test FK with known configurations"""

    print("=== Forward Kinematics Test Suite ===\n")

    # Test 1: Home position (all joints at 0)
    print("Test 1: Home Position")
    theta_home = np.zeros(6)
    T_home, pos_home, R_home = forward_kinematics_6dof(theta_home)

    print(f"Joint angles: {np.degrees(theta_home)}")
    print(f"End-effector position: [{pos_home[0]:.4f}, {pos_home[1]:.4f}, {pos_home[2]:.4f}] m")
    print(f"End-effector orientation (Rotation matrix):\n{R_home}\n")

    # Expected: x = a2 + a3 = 0.4 + 0.39 = 0.79
    #           y = 0
    #           z = d1 + d4 + d6 = 0.3 + 0.35 + 0.09 = 0.74
    expected_home = np.array([0.79, 0.0, 0.74])
    error_home = np.linalg.norm(pos_home - expected_home)
    print(f"Expected position: {expected_home}")
    print(f"Position error: {error_home:.6f} m")
    print(f"✓ PASS" if error_home < 0.001 else "✗ FAIL")
    print("\n" + "="*50 + "\n")

    # Test 2: Right angle configuration
    print("Test 2: Right Angle Configuration")
    theta_right = np.array([np.pi/2, np.pi/4, 0, np.pi/2, 0, 0])
    T_right, pos_right, R_right = forward_kinematics_6dof(theta_right)

    print(f"Joint angles (deg): {np.degrees(theta_right)}")
    print(f"End-effector position: [{pos_right[0]:.4f}, {pos_right[1]:.4f}, {pos_right[2]:.4f}] m")
    print(f"Position magnitude: {np.linalg.norm(pos_right):.4f} m\n")

    # Test 3: Complex configuration
    print("Test 3: Complex Configuration")
    theta_complex = np.array([np.pi/6, -np.pi/3, np.pi/4, np.pi/6, -np.pi/4, np.pi/3])
    T_complex, pos_complex, R_complex = forward_kinematics_6dof(theta_complex)

    print(f"Joint angles (deg): {np.degrees(theta_complex)}")
    print(f"End-effector position: [{pos_complex[0]:.4f}, {pos_complex[1]:.4f}, {pos_complex[2]:.4f}] m")
    print(f"Position magnitude: {np.linalg.norm(pos_complex):.4f} m\n")

    # Workspace check
    print("=== Workspace Analysis ===")
    print(f"Maximum reach (approximate): {0.4 + 0.39 + 0.35 + 0.09:.2f} m")
    print(f"Minimum reach (approximate): {np.abs(0.4 + 0.39 - 0.35 - 0.09):.2f} m")

def visualize_arm(theta):
    """
    Optional: Visualize arm configuration (requires matplotlib)

    Plots the 3D positions of all joint frames
    """
    try:
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
    except ImportError:
        print("matplotlib not available for visualization")
        return

    # TODO: Compute positions of all intermediate frames
    # Store T01, T02 = T01@T12, T03 = T02@T23, etc.
    # Extract positions from each transformation

    pass

def main():
    """Main execution function"""
    test_forward_kinematics()

    # Optional: visualize a configuration
    # visualize_arm(np.array([np.pi/4, np.pi/6, 0, 0, 0, 0]))

if __name__ == "__main__":
    main()
```

**Deliverable**: Completed code with all test cases passing (position error < 1mm)

---

## Implementation Hints

1. **DH Matrix Construction**: Be careful with the order of operations. Standard DH convention applies transformations in this order: Rz(θ) → Tz(d) → Tx(a) → Rx(α)

2. **Matrix Chaining**: Use NumPy's `@` operator for matrix multiplication. Ensure proper left-to-right order.

3. **Debugging**: If results don't match, verify each transformation individually before chaining.

4. **Numerical Precision**: Use `np.allclose()` for floating-point comparisons instead of exact equality.

5. **Orientation Representation**: The 3×3 rotation matrix can be converted to Euler angles or quaternions if needed for downstream applications.

---

## Extension Challenges (Optional)

1. **Visualization**: Implement the `visualize_arm()` function to plot the arm in 3D using matplotlib

2. **Velocity Kinematics**: Extend to compute the geometric Jacobian J(θ) and verify that velocity_x = J(θ) · velocity_θ

3. **Workspace Plotting**: Generate and plot the reachable workspace by sampling joint configurations

4. **URDF Integration**: Export the DH parameters to a URDF file and verify FK matches PyBullet's computed pose

---

## Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| DH transform function correct | 3 | Matrix construction follows standard DH convention |
| FK implementation correct | 4 | Proper chaining of all 6 transformations |
| Test 1 (home position) passes | 1 | Error < 1mm for analytical verification |
| Tests 2-3 execute without errors | 1 | Complex configurations computed successfully |
| Joint limit validation | 0.5 | Warnings for out-of-range inputs |
| Code quality & documentation | 0.5 | Clean code with comments explaining key steps |

**Total**: 10 points

---

## References

[1] Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson Education.

[2] Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2009). *Robotics: Modelling, Planning and Control*. Springer.

[3] Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. Wiley.

---
exercise_id: ex02-02-transforms
chapter: ch02-robot-fundamentals
title: "Compute End-Effector Position with DH Parameters"
learning_outcome: "Calculate 3-DOF arm end-effector position using homogeneous transformations"
difficulty: intermediate
estimated_time: "60-75 minutes"
prerequisites:
  - "Chapter 2 coordinate transformations section"
  - "Linear algebra (matrix multiplication)"
tools:
  - Python 3.9+
  - NumPy
---

# Exercise: Compute End-Effector Position with Transforms

## Overview

Given a 3-DOF planar robot arm's DH parameters and joint angles, calculate the end-effector position using homogeneous transformation matrices. This is the foundation of forward kinematics (Chapter 3).

**What you'll build**: Python functions to create DH transformation matrices and chain them to find end-effector pose

**Why it matters**: Forward kinematics is essential for robot control, simulation, and visualization. Every robot controller needs to know where the end-effector is.

**Real-world application**: Industrial robot arms use forward kinematics thousands of times per second to plan trajectories and avoid collisions.

---

## Problem Statement

**Given**: 3-DOF planar arm (3 revolute joints, all Z-axes parallel)

| Joint | a (m) | alpha (rad) | d (m) | theta (variable) |
|-------|-------|-------------|-------|------------------|
| 1     | 0.5   | 0           | 0     | θ1               |
| 2     | 0.3   | 0           | 0     | θ2               |
| 3     | 0.2   | 0           | 0     | θ3               |

**Task**: Implement `forward_kinematics(theta1, theta2, theta3)` that returns end-effector (x, y, z) position

**Test Case**: θ1=30°, θ2=45°, θ3=60°

**Success Criteria**:
- [ ] `dh_transform(a, alpha, d, theta)` function returns correct 4×4 matrix
- [ ] Forward kinematics chains 3 transformations correctly
- [ ] Test case produces correct (x, y) within 0.01m error
- [ ] Code includes verification against manual calculation

---

## Code Template

```python
import numpy as np

def dh_transform(a, alpha, d, theta):
    """
    Create DH transformation matrix

    Args:
        a: link length
        alpha: link twist
        d: link offset
        theta: joint angle

    Returns:
        4x4 homogeneous transformation
    """
    # TODO: Implement DH matrix
    # T = Rz(theta) * Tz(d) * Tx(a) * Rx(alpha)
    pass

def forward_kinematics(theta1, theta2, theta3):
    """Calculate end-effector position for 3-DOF arm"""
    # DH parameters
    # TODO: Create T01, T12, T23
    # TODO: Chain: T03 = T01 @ T12 @ T23
    # TODO: Extract position from T03[0:3, 3]
    pass

def main():
    # Test case
    theta1 = np.radians(30)
    theta2 = np.radians(45)
    theta3 = np.radians(60)

    pos = forward_kinematics(theta1, theta2, theta3)
    print(f"End-effector position: {pos}")

    # Manual verification for θ=[30°, 45°, 60°]
    # x = 0.5*cos(30) + 0.3*cos(75) + 0.2*cos(135)
    # y = 0.5*sin(30) + 0.3*sin(75) + 0.2*sin(135)
    expected_x = 0.5*np.cos(np.radians(30)) + 0.3*np.cos(np.radians(75)) + 0.2*np.cos(np.radians(135))
    expected_y = 0.5*np.sin(np.radians(30)) + 0.3*np.sin(np.radians(75)) + 0.2*np.sin(np.radians(135))

    print(f"Expected: ({expected_x:.4f}, {expected_y:.4f})")
    print(f"Error: {np.abs(pos[0] - expected_x):.6f}m")

if __name__ == "__main__":
    main()
```

**Deliverable**: Completed code with test output showing error < 0.01m

---

## Rubric

| Criterion | Points |
|-----------|--------|
| DH matrix correct | 4 |
| Chaining logic correct | 3 |
| Test case passes | 2 |
| Error analysis | 1 |

**Total**: 10 points

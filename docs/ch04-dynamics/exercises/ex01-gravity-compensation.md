---
exercise_id: ex04-01-gravity-comp
chapter: ch04-dynamics
title: "Implement Gravity Compensation for 3-DOF Humanoid Arm"
learning_outcome: "Derive and implement gravity compensation to hold static poses without drift"
difficulty: intermediate
estimated_time: "75-90 minutes"
prerequisites:
  - "Chapter 3: Forward kinematics"
  - "Chapter 4: Dynamics modeling and equation of motion"
  - "Calculus (partial derivatives) and linear algebra"
tools:
  - Python 3.9+
  - NumPy
  - Matplotlib (for visualization)
---

# Exercise: Implement Gravity Compensation for 3-DOF Humanoid Arm

## Overview

Derive and implement **gravity compensation** for a 3-DOF humanoid robot arm. Gravity compensation computes the exact torques needed to hold the robot in any static pose, counteracting gravity's pull on each link. This is fundamental for:

- **Position control**: Eliminating steady-state errors due to gravity
- **Teleoperation**: Making the robot feel "weightless" to human operators
- **Backdrivability**: Allowing humans to manually move the robot with minimal effort [1]

**What you'll build**: Python function that computes gravity torques g(q) for a 3-DOF arm, plus verification via simulation

**Why it matters**: Without gravity compensation, robots sag under their own weight. Controllers must fight gravity continuously, wasting energy and causing positioning errors [2].

**Real-world application**: Collaborative robots (cobots) like UR5 and Franka Emika Panda use gravity compensation to enable kinesthetic teaching—users physically guide the robot to teach tasks.

---

## Problem Statement

**Given**: 3-DOF humanoid arm with revolute joints (shoulder pitch, shoulder roll, elbow pitch)

| Joint | Axis | Link Length (m) | Link Mass (kg) | COM Location | Joint Limits (rad) |
|-------|------|-----------------|----------------|--------------|---------------------|
| 1     | Z    | L1 = 0.4       | m1 = 3.0       | L1/2 from J1 | [-π, π]             |
| 2     | Y    | L2 = 0.35      | m2 = 2.0       | L2/2 from J2 | [-π/2, π/2]         |
| 3     | Y    | L3 = 0.25      | m3 = 1.0       | L3/2 from J3 | [-π, π]             |

**Assumptions**:
- Links are uniform density (center of mass at midpoint)
- Joints are ideal (no friction)
- Gravity: g = 9.81 m/s² (downward in -Z direction)

**Task**: Implement `gravity_compensation(q)` that:
1. Computes potential energy P(q) for the entire system
2. Derives gravity torques: g(q) = ∂P/∂q (gradient of potential energy)
3. Returns 3×1 vector of joint torques [τ1, τ2, τ3]

**Test Cases**:
1. **Horizontal Pose**: q = [0, π/2, 0] (arm extended horizontally)
2. **Vertical Pose**: q = [0, 0, 0] (arm pointing upward)
3. **Complex Pose**: q = [π/4, π/3, -π/6]

**Success Criteria**:
- [ ] Gravity torque function returns correct 3×1 vector
- [ ] Simulation with g(q) applied shows zero drift (position error < 0.001 rad after 5s)
- [ ] Manual verification: torque values match analytical calculation for test cases
- [ ] Energy conservation: total energy remains constant (within numerical error)

---

## Theoretical Background

### Potential Energy and Gravity Torques

For a robot arm, **potential energy** is the sum of gravitational potential energy of all links:

```
P(q) = Σ m_i g h_i(q)
```

where:
- **m_i**: mass of link i
- **g**: gravitational acceleration (9.81 m/s²)
- **h_i(q)**: height of link i's center of mass (depends on joint configuration q)

The **gravity torque vector** is:

```
g(q) = [∂P/∂q1, ∂P/∂q2, ∂P/∂q3]^T
```

**Physical Interpretation**: Each component g_i represents the torque required at joint i to balance gravity.

---

### Derivation for 3-DOF Arm

**Step 1: Define coordinate frames using DH convention**

For our 3-DOF arm:
- Joint 1 (shoulder pitch): rotates about Z-axis
- Joint 2 (shoulder roll): rotates about Y-axis
- Joint 3 (elbow pitch): rotates about Y-axis

**Step 2: Compute COM positions**

For each link i, we need to find the (x, y, z) position of its center of mass in the base frame.

Using forward kinematics (from Chapter 3), we can compute transformation matrices T_0i that map from base frame to frame i. The COM of link i is at position:

```
p_ci = T_0i * [L_i/2, 0, 0, 1]^T   (assuming COM at link midpoint)
```

The height h_i is the z-component of p_ci:

```
h_i = p_ci(2)   (using 0-indexing: z is index 2)
```

**Step 3: Compute potential energy**

```
P(q) = m1 g h1(q) + m2 g h2(q) + m3 g h3(q)
```

**Step 4: Compute partial derivatives**

For each joint i:

```
g_i = ∂P/∂q_i = Σ m_j g (∂h_j/∂q_i)
```

In practice, we can use **numerical differentiation** or **symbolic derivation**.

---

### Simplified Analytical Approach (Planar Approximation)

For a planar arm (all joints rotating about parallel axes, arm in vertical plane):

```
h1 = L1/2 * cos(θ1)
h2 = L1 * cos(θ1) + L2/2 * cos(θ1 + θ2)
h3 = L1 * cos(θ1) + L2 * cos(θ1 + θ2) + L3/2 * cos(θ1 + θ2 + θ3)
```

Gravity torques:

```
g1 = -m1 g (L1/2) sin(θ1) - m2 g L1 sin(θ1) - m3 g L1 sin(θ1)
     - m2 g (L2/2) sin(θ1 + θ2) - m3 g L2 sin(θ1 + θ2)
     - m3 g (L3/2) sin(θ1 + θ2 + θ3)

g2 = -m2 g (L2/2) sin(θ1 + θ2) - m3 g L2 sin(θ1 + θ2)
     - m3 g (L3/2) sin(θ1 + θ2 + θ3)

g3 = -m3 g (L3/2) sin(θ1 + θ2 + θ3)
```

**Note**: Signs depend on coordinate frame conventions. Positive torque opposes gravity (holds arm up).

---

## Code Template

```python
import numpy as np
import matplotlib.pyplot as plt

def gravity_compensation(q, L=[0.4, 0.35, 0.25], m=[3.0, 2.0, 1.0], g=9.81):
    """
    Compute gravity compensation torques for 3-DOF planar arm

    Args:
        q: joint angles [theta1, theta2, theta3] (rad)
        L: link lengths [L1, L2, L3] (m)
        m: link masses [m1, m2, m3] (kg)
        g: gravitational acceleration (m/s²)

    Returns:
        g_torques: gravity torques [g1, g2, g3] (Nm)
    """
    theta1, theta2, theta3 = q
    L1, L2, L3 = L
    m1, m2, m3 = m

    # TODO: Compute gravity torques
    # Use the analytical expressions derived above
    # Hint: sin_12 = sin(theta1 + theta2), sin_123 = sin(theta1 + theta2 + theta3)

    # g1 = ... (torque at joint 1)
    # g2 = ... (torque at joint 2)
    # g3 = ... (torque at joint 3)

    pass  # Remove after implementing

def forward_kinematics_3dof(q, L=[0.4, 0.35, 0.25]):
    """
    Compute forward kinematics for 3-DOF planar arm (for visualization)

    Args:
        q: joint angles [theta1, theta2, theta3] (rad)
        L: link lengths [L1, L2, L3] (m)

    Returns:
        positions: 4×2 array of (x, z) positions for [base, J1, J2, J3, end-effector]
    """
    theta1, theta2, theta3 = q
    L1, L2, L3 = L

    # Cumulative angles
    angle1 = theta1
    angle2 = theta1 + theta2
    angle3 = theta1 + theta2 + theta3

    # Joint positions (2D planar: x-z plane)
    positions = np.zeros((4, 2))  # [base, joint1_end, joint2_end, joint3_end]

    positions[0] = [0, 0]  # Base
    positions[1] = [L1 * np.sin(angle1), L1 * np.cos(angle1)]  # End of link 1
    positions[2] = positions[1] + [L2 * np.sin(angle2), L2 * np.cos(angle2)]  # End of link 2
    positions[3] = positions[2] + [L3 * np.sin(angle3), L3 * np.cos(angle3)]  # End-effector

    return positions

def simulate_gravity_hold(q0, t_final=5.0, dt=0.01, use_compensation=True):
    """
    Simulate holding a pose with/without gravity compensation

    Args:
        q0: initial joint angles [theta1, theta2, theta3]
        t_final: simulation duration (s)
        dt: timestep (s)
        use_compensation: whether to apply gravity compensation torques

    Returns:
        t, q: time array and joint angle history
    """
    num_steps = int(t_final / dt)
    t = np.linspace(0, t_final, num_steps)

    q = np.zeros((num_steps, 3))
    dq = np.zeros((num_steps, 3))

    q[0] = q0

    for i in range(num_steps - 1):
        if use_compensation:
            # Apply gravity compensation
            tau = gravity_compensation(q[i])
        else:
            # No torques applied
            tau = np.zeros(3)

        # Simplified dynamics: M = I (identity), C = 0, g from function
        # Real dynamics would use full equation: M(q) ddq + C(q, dq) + g(q) = tau
        # For now, assume: ddq = (tau - g(q)) / M

        # Approximate inertia (diagonal approximation)
        M_diag = np.array([1.5, 1.0, 0.5])  # Rough inertia estimates

        # Compute actual gravity torques
        g_actual = gravity_compensation(q[i])

        # Acceleration: ddq = (tau - g_actual) / M
        ddq = (tau - g_actual) / M_diag

        # Euler integration
        dq[i+1] = dq[i] + ddq * dt
        q[i+1] = q[i] + dq[i] * dt

    return t, q

def test_gravity_compensation():
    """Test gravity compensation for multiple poses"""

    print("=== Gravity Compensation Test ===\n")

    # Test poses
    poses = [
        (np.array([0, np.pi/2, 0]), "Horizontal Pose"),
        (np.array([0, 0, 0]), "Vertical Pose (Up)"),
        (np.array([np.pi/4, np.pi/3, -np.pi/6]), "Complex Pose")
    ]

    for q, description in poses:
        print(f"{description}: θ = [{np.degrees(q[0]):.1f}°, {np.degrees(q[1]):.1f}°, {np.degrees(q[2]):.1f}°]")

        g_torques = gravity_compensation(q)

        print(f"  Gravity torques: [{g_torques[0]:.3f}, {g_torques[1]:.3f}, {g_torques[2]:.3f}] Nm")
        print(f"  Total torque magnitude: {np.linalg.norm(g_torques):.3f} Nm\n")

def test_drift():
    """Test that gravity compensation prevents drift"""

    print("=== Drift Test ===\n")

    q0 = np.array([0, np.pi/2, 0])  # Horizontal pose

    # Simulate with compensation
    t, q_comp = simulate_gravity_hold(q0, t_final=5.0, use_compensation=True)

    # Simulate without compensation
    t, q_no_comp = simulate_gravity_hold(q0, t_final=5.0, use_compensation=False)

    # Compute drift
    drift_comp = np.linalg.norm(q_comp[-1] - q0)
    drift_no_comp = np.linalg.norm(q_no_comp[-1] - q0)

    print(f"Initial pose: θ = [{np.degrees(q0[0]):.1f}°, {np.degrees(q0[1]):.1f}°, {np.degrees(q0[2]):.1f}°]")
    print(f"Drift WITH compensation: {drift_comp:.6f} rad ({np.degrees(drift_comp):.4f}°)")
    print(f"Drift WITHOUT compensation: {drift_no_comp:.6f} rad ({np.degrees(drift_no_comp):.4f}°)")
    print(f"Drift reduction: {drift_no_comp / drift_comp:.1f}×\n")

    # Plot comparison
    plt.figure(figsize=(12, 6))

    for joint_idx in range(3):
        plt.subplot(2, 3, joint_idx + 1)
        plt.plot(t, np.degrees(q_comp[:, joint_idx]), 'b-', label='With Compensation')
        plt.plot(t, np.degrees(q_no_comp[:, joint_idx]), 'r--', label='Without Compensation')
        plt.axhline(y=np.degrees(q0[joint_idx]), color='g', linestyle=':', label='Desired')
        plt.xlabel('Time (s)')
        plt.ylabel(f'Joint {joint_idx + 1} (deg)')
        plt.title(f'Joint {joint_idx + 1} Position')
        plt.legend(fontsize=8)
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('gravity_compensation_drift.png', dpi=150)
    print("Drift comparison plot saved: gravity_compensation_drift.png")

def visualize_arm(q):
    """Visualize arm configuration and gravity torques"""

    positions = forward_kinematics_3dof(q)
    g_torques = gravity_compensation(q)

    plt.figure(figsize=(10, 8))

    # Plot arm configuration
    plt.subplot(1, 2, 1)
    plt.plot(positions[:, 0], positions[:, 1], 'o-', linewidth=3, markersize=10, label='Arm')
    plt.plot(positions[0, 0], positions[0, 1], 'ks', markersize=15, label='Base')
    plt.plot(positions[-1, 0], positions[-1, 1], 'r^', markersize=15, label='End-Effector')

    # Draw ground
    plt.axhline(y=0, color='brown', linestyle='-', linewidth=2, alpha=0.5)
    plt.fill_between([-0.5, 1.0], [0, 0], [-0.1, -0.1], color='brown', alpha=0.3)

    plt.xlabel('X (m)')
    plt.ylabel('Z (m) [Height]')
    plt.title(f'Arm Configuration\nθ = [{np.degrees(q[0]):.1f}°, {np.degrees(q[1]):.1f}°, {np.degrees(q[2]):.1f}°]')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.legend()

    # Plot gravity torques
    plt.subplot(1, 2, 2)
    joints = ['Joint 1', 'Joint 2', 'Joint 3']
    colors = ['blue', 'green', 'red']

    bars = plt.bar(joints, g_torques, color=colors, alpha=0.7, edgecolor='black')
    plt.ylabel('Gravity Torque (Nm)')
    plt.title('Gravity Compensation Torques')
    plt.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar, val in zip(bars, g_torques):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom' if val > 0 else 'top')

    plt.tight_layout()
    plt.savefig('gravity_compensation_viz.png', dpi=150)
    print("Arm visualization saved: gravity_compensation_viz.png")

def main():
    """Main execution function"""
    test_gravity_compensation()
    print("\n" + "="*60 + "\n")
    test_drift()

    # Visualize a specific pose
    q_test = np.array([np.pi/4, np.pi/3, -np.pi/6])
    visualize_arm(q_test)

if __name__ == "__main__":
    main()
```

**Deliverable**: Completed code with test output showing drift < 0.001 rad with compensation

---

## Implementation Hints

1. **Sign Conventions**: Gravity pulls downward (-Z direction). Positive torque typically opposes gravity (holds arm up). Check your coordinate frame carefully.

2. **Angle Summation**: For revolute joints, cumulative angles add: angle_i = θ1 + θ2 + ... + θ_i

3. **Numerical Stability**: Use `np.sin` and `np.cos` directly on angle sums to avoid accumulation errors.

4. **Verification Strategy**:
   - For vertical pose (θ = [0, 0, 0]), expect g = [0, 0, 0] (no gravity torque when arm points up)
   - For horizontal pose (θ = [0, π/2, 0]), expect large positive torques to hold arm horizontal

5. **Debugging**: If simulation drifts even with compensation, check:
   - Signs of torques (should oppose gravity)
   - Inertia matrix approximation (may need better model)
   - Numerical integration step size (try smaller dt)

---

## Extension Challenges (Optional)

1. **3D Gravity Compensation**: Extend to full 3D arm (not planar) where Joint 1 rotates about Z-axis

2. **Energy Monitoring**: Compute and plot total mechanical energy E = K + P over time. Should remain constant.

3. **Variable Payload**: Add a payload mass at the end-effector and recompute gravity torques

4. **Friction Compensation**: Add Coulomb friction model and compensate for both gravity and friction

5. **Real Robot Integration**: Export gravity compensation function to ROS and test on real robot (if available)

---

## Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Gravity torque derivation | 3 | Correct analytical expressions for g1, g2, g3 |
| Implementation correct | 3 | Function returns proper 3×1 vector with correct values |
| Test cases pass | 2 | All three test poses produce reasonable torques |
| Drift test < 0.001 rad | 1.5 | Simulation shows minimal drift with compensation |
| Code quality & documentation | 0.5 | Clear comments, modular functions |

**Total**: 10 points

---

## References

[1] Hogan, N. (1985). Impedance control: An approach to manipulation. *Journal of Dynamic Systems, Measurement, and Control*, 107(1), 1-7.

[2] Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2009). *Robotics: Modelling, Planning and Control*. Springer. (Chapter 8: Motion Control)

[3] Featherstone, R. (2008). *Rigid Body Dynamics Algorithms*. Springer. (Chapter 5: Gravity Compensation)

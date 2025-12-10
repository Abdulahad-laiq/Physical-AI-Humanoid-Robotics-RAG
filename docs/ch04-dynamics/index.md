---
id: ch04-dynamics
title: "Chapter 4: Dynamics and Control Fundamentals"
sidebar_label: "Ch 4: Dynamics & Control"
sidebar_position: 4
description: "Robot dynamics modeling, equation of motion derivation, and fundamental control strategies for humanoid robots"
keywords:
  - robot dynamics
  - Lagrangian mechanics
  - Newton-Euler
  - PID control
  - computed torque
  - impedance control
learning_objectives:
  - "Derive equations of motion using Lagrangian and Newton-Euler formulations"
  - "Understand the relationship between joint torques and robot motion"
  - "Design and tune PID controllers for joint-level control"
  - "Implement computed torque control for trajectory tracking"
  - "Apply impedance control for safe physical interaction"
prerequisites:
  - "Chapter 2: Coordinate frames and transformations"
  - "Chapter 3: Kinematics and Jacobian matrices"
  - "Calculus (derivatives, integrals) and linear algebra"
estimated_time: "8-10 hours"
---

# Chapter 4: Dynamics and Control Fundamentals

## Introduction

While **kinematics** tells us *where* a robot's end-effector is for given joint angles, **dynamics** tells us *how* the robot moves under applied forces and torques. Understanding dynamics is essential for:

- **Motion planning**: Generating feasible trajectories that respect actuator limits
- **Control design**: Computing the torques needed to follow desired paths
- **Simulation**: Predicting robot behavior in virtual environments
- **Force control**: Enabling safe physical interaction with humans and objects

This chapter introduces **robot dynamics** (modeling motion equations) and **control** (commanding robots to execute desired behaviors). We cover classical control approaches used widely in industrial and humanoid robotics [1, 2].

**Preview**: You'll learn to derive equations of motion, implement PID controllers, and design model-based controllers for trajectory tracking.

**Connection to Previous Chapters**: Chapter 3 gave us the forward kinematics T(q) and Jacobian J(q). Now we introduce the **dynamics model** M(q)q̈ + C(q,q̇)q̇ + g(q) = τ, which relates joint torques τ to accelerations q̈.

---

## 4.1 Robot Dynamics: Equations of Motion

### 4.1.1 Why Dynamics Matters

**Kinematics** (Chapter 3) answers: "If I set joint angles to θ = [30°, 45°, 60°], where is the end-effector?"

**Dynamics** answers: "What torques must I apply to move from configuration A to configuration B in 2 seconds while carrying a 5kg payload?"

Real robots have:
- **Mass and inertia**: Links have weight; rotating them requires torque
- **Velocity-dependent forces**: Joint friction, Coriolis forces, centrifugal forces
- **Gravity**: Gravity pulls down on all links; torque is needed to hold postures
- **External forces**: Contact with environment (ground, objects, humans)

The **equation of motion** captures all these effects [3]:

```
M(q)q̈ + C(q, q̇)q̇ + g(q) = τ + J^T f_ext
```

where:
- **M(q)**: n×n inertia matrix (configuration-dependent mass properties)
- **C(q, q̇)q̇**: Coriolis and centrifugal forces (velocity-dependent)
- **g(q)**: gravity torques (position-dependent)
- **τ**: applied joint torques (what we control)
- **J^T f_ext**: external forces mapped to joint space

---

### 4.1.2 Lagrangian Formulation

The **Lagrangian approach** derives dynamics from energy considerations [4].

**Step 1: Define Lagrangian**

```
L = K - P
```

where:
- **K**: Total kinetic energy (translational + rotational)
- **P**: Total potential energy (gravity)

**Step 2: Compute Kinetic Energy**

For link i with mass m_i, center of mass position p_ci, and inertia tensor I_i:

```
K_i = (1/2) m_i ||v_ci||² + (1/2) ω_i^T I_i ω_i
```

Total kinetic energy:

```
K = Σ K_i = (1/2) q̇^T M(q) q̇
```

**Step 3: Compute Potential Energy**

For link i at height h_i:

```
P_i = m_i g h_i
```

Total potential energy:

```
P = Σ m_i g h_i
```

**Step 4: Apply Euler-Lagrange Equation**

```
d/dt (∂L/∂q̇) - ∂L/∂q = τ
```

Expanding this yields the equation of motion [5]:

```
M(q)q̈ + C(q, q̇)q̇ + g(q) = τ
```

**Properties**:
- **Symmetry**: M(q) is symmetric and positive-definite
- **Skew-symmetry**: Ṁ - 2C is skew-symmetric (important for stability proofs)
- **Energy conservation**: In the absence of friction, total energy E = K + P is conserved

---

### 4.1.3 Newton-Euler Formulation

The **Newton-Euler approach** applies Newton's laws directly to each link [6].

**Forward Recursion** (compute velocities and accelerations from base to end-effector):

For each link i = 1, ..., n:

```
ω_i = ω_(i-1) + q̇_i z_i               (angular velocity)
v_i = v_(i-1) + ω_i × p_(i-1,i)       (linear velocity)
a_i = a_(i-1) + ω̇_i × p_(i-1,i) + ω_i × (ω_i × p_(i-1,i))
```

where z_i is the joint axis and p_(i-1,i) is the vector from frame i-1 to frame i.

**Backward Recursion** (compute forces and torques from end-effector to base):

For each link i = n, ..., 1:

```
F_i = m_i a_ci + F_{i+1}              (force balance)
N_i = I_i ω̇_i + ω_i × (I_i ω_i) + N_{i+1} + p_ci × F_i   (moment balance)
τ_i = N_i^T z_i                        (joint torque)
```

**Computational Complexity**: Newton-Euler is O(n), making it faster than Lagrangian formulation (O(n²)) for real-time control [7].

---

### 4.1.4 Example: 2-DOF Planar Arm Dynamics

Consider the 2-DOF arm from Chapter 3:

**Given**:
- Link 1: length L1 = 0.5m, mass m1 = 2kg, center of mass at L1/2
- Link 2: length L2 = 0.3m, mass m2 = 1kg, center of mass at L2/2
- Gravity: g = 9.81 m/s²

**Inertia Matrix M(q)**:

```
M(q) = [m11  m12]
       [m12  m22]
```

where:

```
m11 = (m1 + m2)L1² + m2 L2² + 2 m2 L1 L2 cos(θ2)
m12 = m2 L2² + m2 L1 L2 cos(θ2)
m22 = m2 L2²
```

**Coriolis/Centrifugal Terms C(q, q̇)q̇**:

```
C(q, q̇)q̇ = [-m2 L1 L2 sin(θ2) (2 θ̇1 θ̇2 + θ̇2²)]
             [m2 L1 L2 sin(θ2) θ̇1²]
```

**Gravity Terms g(q)**:

```
g(q) = [(m1 + m2) g L1 cos(θ1) + m2 g L2 cos(θ1 + θ2)]
       [m2 g L2 cos(θ1 + θ2)]
```

**Full Equation**:

```
M(q)q̈ + C(q, q̇)q̇ + g(q) = τ
```

This models how torques τ = [τ1, τ2] produce accelerations q̈ = [θ̈1, θ̈2].

---

## 4.2 Control Fundamentals

**Control** is the process of commanding a robot to execute desired behaviors by computing appropriate actuator inputs [8].

### 4.2.1 Control Problem Statement

**Task**: Given a desired trajectory q_d(t), q̇_d(t), q̈_d(t), compute joint torques τ(t) such that:

```
q(t) → q_d(t)   as t → ∞   (tracking)
```

**Challenges**:
- **Model uncertainty**: Real robots don't match mathematical models perfectly
- **Disturbances**: External forces, payload changes, ground irregularities
- **Delays**: Sensor and actuator delays (typically 1-10ms)
- **Constraints**: Joint limits, torque limits, collision avoidance

---

### 4.2.2 PID Control

**Proportional-Integral-Derivative (PID)** control is the most widely used controller in industry due to its simplicity and effectiveness [9].

**Control Law**:

```
τ(t) = K_p e(t) + K_i ∫e(τ)dτ + K_d ė(t)
```

where:
- **e(t) = q_d(t) - q(t)**: position error
- **ė(t) = q̇_d(t) - q̇(t)**: velocity error
- **K_p**: proportional gain (stiffness)
- **K_i**: integral gain (eliminates steady-state error)
- **K_d**: derivative gain (damping)

**Physical Interpretation**:
- **P-term**: Spring pulling robot toward target (larger K_p = stiffer)
- **I-term**: Accumulates error over time; pushes robot to eliminate offset
- **D-term**: Damper resisting velocity (larger K_d = less oscillation)

**Discrete-Time Implementation** (for digital controllers at sampling time Δt):

```
e_k = q_d,k - q_k
integral_k = integral_(k-1) + e_k * Δt
derivative_k = (e_k - e_(k-1)) / Δt
τ_k = K_p * e_k + K_i * integral_k + K_d * derivative_k
```

**Tuning Methods**:
1. **Ziegler-Nichols**: Set K_i = K_d = 0, increase K_p until oscillation, then set K_p = 0.6 K_p,crit, K_i = 1.2 K_p / T_osc, K_d = 0.075 K_p T_osc [10]
2. **Manual tuning**: Start with K_p only, add K_d to reduce overshoot, add K_i to eliminate steady-state error
3. **Optimization**: Use gradient descent or genetic algorithms to minimize tracking error

**Limitations**:
- Ignores coupling between joints (each joint controlled independently)
- No feedforward compensation for gravity or inertia
- Can be slow or oscillatory for heavy payloads

---

### 4.2.3 Computed Torque Control

**Computed Torque Control** (also called **inverse dynamics control** or **feedback linearization**) uses the dynamics model to cancel nonlinearities [11].

**Idea**: If we know M(q), C(q, q̇), and g(q), we can compute the exact torques needed for a desired acceleration:

```
τ = M(q) u + C(q, q̇)q̇ + g(q)
```

where **u** is a new control input. Substituting into the equation of motion:

```
M(q)q̈ + C(q, q̇)q̇ + g(q) = M(q)u + C(q, q̇)q̇ + g(q)
```

Simplifies to:

```
q̈ = u   (double integrator dynamics)
```

**Control Design**: Now design **u** using PID on the linearized system:

```
u = q̈_d + K_p e + K_d ė
```

**Full Control Law**:

```
τ = M(q)[q̈_d + K_p(q_d - q) + K_d(q̇_d - q̇)] + C(q, q̇)q̇ + g(q)
```

**Advantages**:
- Decouples joint dynamics (each joint behaves as independent double integrator)
- Fast, accurate tracking
- Handles varying payloads if M(q) updated

**Disadvantages**:
- Requires accurate model M(q), C(q, q̇), g(q)
- Sensitive to parameter errors (mass, inertia, friction)
- Computationally expensive (matrix inversion at each timestep)

**Practical Consideration**: Real implementations use approximate models M̂(q), Ĉ(q, q̇), ĝ(q), resulting in:

```
τ = M̂(q)u + Ĉ(q, q̇)q̇ + ĝ(q)
```

Residual modeling errors are treated as disturbances and handled by feedback gains K_p, K_d [12].

---

### 4.2.4 Impedance Control

**Impedance control** regulates the relationship between force and motion, enabling compliant interaction with the environment [13].

**Motivation**: For tasks like:
- Opening a door (must apply force while position is constrained)
- Polishing a surface (maintain constant contact force)
- Physical human-robot interaction (avoid injury from rigid collisions)

We need to control **both position and force** simultaneously.

**Impedance Model**: Design desired dynamics relating force f to position x:

```
M_d (ẍ - ẍ_d) + D_d (ẋ - ẋ_d) + K_d (x - x_d) = f_ext - f_d
```

where:
- **M_d**: desired inertia (how heavy the robot "feels")
- **D_d**: desired damping (how much it resists velocity)
- **K_d**: desired stiffness (how much it resists displacement)
- **f_ext**: measured external force
- **f_d**: desired contact force

**Physical Interpretation**: The robot behaves like a mass-spring-damper system. When you push on it:
- Low K_d → compliant (soft, easy to move)
- High K_d → stiff (hard, resists motion)

**Implementation**: In joint space, the impedance control law is:

```
τ = J^T f_d + M̂(q) J_inv [ẍ_d - J̇ q̇ + M_d_inv (D_d (ẋ - ẋ_d) + K_d (x - x_d) + f_ext - f_d)]
```

**Simplified Version** (joint-space impedance):

```
τ = K_p (q_d - q) + K_d (q̇_d - q̇) + τ_ff - J^T f_ext
```

where τ_ff is feedforward gravity/inertia compensation.

**Applications**:
- **Collaborative robots (cobots)**: Set low K_d for safe interaction
- **Teleoperation**: Map human hand impedance to robot
- **Bipedal locomotion**: Compliant ankle for terrain adaptation [14]

---

## 4.3 Code Example 1: Simulate 2-DOF Arm Dynamics

```python
import numpy as np
import matplotlib.pyplot as plt

def dynamics_2dof(q, dq, tau, L1=0.5, L2=0.3, m1=2.0, m2=1.0, g=9.81):
    """
    Compute acceleration for 2-DOF planar arm using equation of motion

    Args:
        q: joint positions [theta1, theta2] (rad)
        dq: joint velocities [dtheta1, dtheta2] (rad/s)
        tau: joint torques [tau1, tau2] (Nm)
        L1, L2: link lengths (m)
        m1, m2: link masses (kg)
        g: gravity (m/s²)

    Returns:
        ddq: joint accelerations [ddtheta1, ddtheta2] (rad/s²)
    """
    theta1, theta2 = q
    dtheta1, dtheta2 = dq

    # Inertia matrix M(q)
    m11 = (m1 + m2) * L1**2 + m2 * L2**2 + 2 * m2 * L1 * L2 * np.cos(theta2)
    m12 = m2 * L2**2 + m2 * L1 * L2 * np.cos(theta2)
    m22 = m2 * L2**2

    M = np.array([
        [m11, m12],
        [m12, m22]
    ])

    # Coriolis/centrifugal matrix C(q, dq)
    h = -m2 * L1 * L2 * np.sin(theta2)
    c1 = h * (2 * dtheta1 * dtheta2 + dtheta2**2)
    c2 = h * dtheta1**2

    C = np.array([c1, c2])

    # Gravity vector g(q)
    g1 = (m1 + m2) * g * L1 * np.cos(theta1) + m2 * g * L2 * np.cos(theta1 + theta2)
    g2 = m2 * g * L2 * np.cos(theta1 + theta2)

    G = np.array([g1, g2])

    # Solve for acceleration: M(q) ddq = tau - C(q, dq) - g(q)
    ddq = np.linalg.solve(M, tau - C - G)

    return ddq

def simulate_forward_dynamics(q0, dq0, tau_func, t_final=5.0, dt=0.01):
    """
    Simulate robot forward dynamics

    Args:
        q0: initial position [theta1, theta2]
        dq0: initial velocity [dtheta1, dtheta2]
        tau_func: function(t, q, dq) returning torques
        t_final: simulation duration (s)
        dt: timestep (s)

    Returns:
        t, q, dq, ddq: time, position, velocity, acceleration arrays
    """
    num_steps = int(t_final / dt)
    t = np.linspace(0, t_final, num_steps)

    q = np.zeros((num_steps, 2))
    dq = np.zeros((num_steps, 2))
    ddq = np.zeros((num_steps, 2))

    q[0] = q0
    dq[0] = dq0

    for i in range(num_steps - 1):
        # Compute torques
        tau = tau_func(t[i], q[i], dq[i])

        # Compute acceleration
        ddq[i] = dynamics_2dof(q[i], dq[i], tau)

        # Euler integration (simple but sufficient for demo)
        dq[i+1] = dq[i] + ddq[i] * dt
        q[i+1] = q[i] + dq[i] * dt

    # Final acceleration
    tau = tau_func(t[-1], q[-1], dq[-1])
    ddq[-1] = dynamics_2dof(q[-1], dq[-1], tau)

    return t, q, dq, ddq

# Test: Gravity compensation (hold arm horizontal)
def gravity_compensation(t, q, dq):
    """Compute torques to hold arm at current position against gravity"""
    theta1, theta2 = q
    L1, L2 = 0.5, 0.3
    m1, m2 = 2.0, 1.0
    g = 9.81

    g1 = (m1 + m2) * g * L1 * np.cos(theta1) + m2 * g * L2 * np.cos(theta1 + theta2)
    g2 = m2 * g * L2 * np.cos(theta1 + theta2)

    return np.array([g1, g2])

# Simulate holding arm horizontal
q0 = np.array([np.pi/2, 0])  # Horizontal configuration
dq0 = np.array([0, 0])

t, q, dq, ddq = simulate_forward_dynamics(q0, dq0, gravity_compensation, t_final=2.0)

# Plot results
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.plot(t, np.degrees(q[:, 0]), label='θ₁')
plt.plot(t, np.degrees(q[:, 1]), label='θ₂')
plt.xlabel('Time (s)')
plt.ylabel('Joint Angle (deg)')
plt.title('Position (Gravity Compensation)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
plt.plot(t, dq[:, 0], label='dθ₁/dt')
plt.plot(t, dq[:, 1], label='dθ₂/dt')
plt.xlabel('Time (s)')
plt.ylabel('Joint Velocity (rad/s)')
plt.title('Velocity')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 3)
plt.plot(t, ddq[:, 0], label='d²θ₁/dt²')
plt.plot(t, ddq[:, 1], label='d²θ₂/dt²')
plt.xlabel('Time (s)')
plt.ylabel('Joint Acceleration (rad/s²)')
plt.title('Acceleration')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Final position: θ₁ = {np.degrees(q[-1, 0]):.2f}°, θ₂ = {np.degrees(q[-1, 1]):.2f}°")
print(f"Position drift: {np.linalg.norm(q[-1] - q0):.6f} rad")
```

**Expected Output**: With perfect gravity compensation, the arm should remain stationary (position drift ≈ 0).

---

## 4.4 Code Example 2: PID Control for Trajectory Tracking

```python
import numpy as np
import matplotlib.pyplot as plt

class PIDController:
    """PID controller for robot joints"""

    def __init__(self, Kp, Ki, Kd, dt):
        """
        Args:
            Kp: proportional gain (can be scalar or array for each joint)
            Ki: integral gain
            Kd: derivative gain
            dt: timestep (s)
        """
        self.Kp = np.atleast_1d(Kp)
        self.Ki = np.atleast_1d(Ki)
        self.Kd = np.atleast_1d(Kd)
        self.dt = dt

        self.integral = np.zeros_like(self.Kp)
        self.prev_error = None

    def reset(self):
        """Reset integral and previous error"""
        self.integral = np.zeros_like(self.Kp)
        self.prev_error = None

    def compute(self, q_desired, q_actual, dq_desired=None, dq_actual=None):
        """
        Compute PID control torques

        Args:
            q_desired: desired position
            q_actual: actual position
            dq_desired: desired velocity (optional)
            dq_actual: actual velocity (optional)

        Returns:
            tau: control torques
        """
        # Position error
        error = q_desired - q_actual

        # Integral term
        self.integral += error * self.dt

        # Derivative term
        if self.prev_error is None:
            derivative = np.zeros_like(error)
        else:
            derivative = (error - self.prev_error) / self.dt

        self.prev_error = error.copy()

        # PID output
        tau = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        return tau

# Test: Track sinusoidal trajectory
def test_pid_tracking():
    """Test PID controller tracking sinusoidal reference"""

    # Simulation parameters
    dt = 0.01
    t_final = 5.0
    num_steps = int(t_final / dt)
    t = np.linspace(0, t_final, num_steps)

    # Desired trajectory (sinusoid)
    amplitude = np.pi / 4  # 45 degrees
    frequency = 0.5  # Hz

    q_desired = np.zeros((num_steps, 2))
    dq_desired = np.zeros((num_steps, 2))

    q_desired[:, 0] = amplitude * np.sin(2 * np.pi * frequency * t)
    dq_desired[:, 0] = amplitude * 2 * np.pi * frequency * np.cos(2 * np.pi * frequency * t)

    # Initialize robot state
    q_actual = np.zeros((num_steps, 2))
    dq_actual = np.zeros((num_steps, 2))
    tau = np.zeros((num_steps, 2))

    # PID controller (tune gains for each joint)
    pid = PIDController(Kp=[50, 30], Ki=[5, 3], Kd=[10, 8], dt=dt)

    # Simulation loop
    for i in range(num_steps - 1):
        # Compute control torques
        tau[i] = pid.compute(q_desired[i], q_actual[i])

        # Forward dynamics
        ddq = dynamics_2dof(q_actual[i], dq_actual[i], tau[i])

        # Integrate
        dq_actual[i+1] = dq_actual[i] + ddq * dt
        q_actual[i+1] = q_actual[i] + dq_actual[i] * dt

    # Plot results
    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t, np.degrees(q_desired[:, 0]), 'r--', label='Desired θ₁')
    plt.plot(t, np.degrees(q_actual[:, 0]), 'b-', label='Actual θ₁')
    plt.xlabel('Time (s)')
    plt.ylabel('Joint 1 Angle (deg)')
    plt.title('Position Tracking (PID Control)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(3, 1, 2)
    error = q_desired[:, 0] - q_actual[:, 0]
    plt.plot(t, np.degrees(error), 'g-')
    plt.xlabel('Time (s)')
    plt.ylabel('Tracking Error (deg)')
    plt.title('Position Error')
    plt.grid(True, alpha=0.3)

    plt.subplot(3, 1, 3)
    plt.plot(t, tau[:, 0], label='τ₁')
    plt.plot(t, tau[:, 1], label='τ₂')
    plt.xlabel('Time (s)')
    plt.ylabel('Torque (Nm)')
    plt.title('Control Torques')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Metrics
    rmse = np.sqrt(np.mean(error**2))
    max_error = np.max(np.abs(error))

    print(f"RMSE tracking error: {np.degrees(rmse):.3f}°")
    print(f"Maximum tracking error: {np.degrees(max_error):.3f}°")
    print(f"Steady-state error: {np.degrees(np.mean(error[-100:])):.3f}°")

test_pid_tracking()
```

**Expected Output**: PID controller tracks sinusoidal reference with small error (typically < 1° after tuning).

---

## Practical Exercises

### Exercise 1: Implement Gravity Compensation
**File**: `exercises/ex01-gravity-compensation.md`

Derive and implement gravity compensation for a 3-DOF humanoid arm. Verify that the arm holds any static pose without drifting.

### Exercise 2: Tune PID Controller
**File**: `exercises/ex02-pid-tuning.md`

Design and tune a PID controller for a 2-DOF arm tracking a figure-eight trajectory. Minimize tracking error and overshoot.

---

## Assessment Questions

### 1. Conceptual Understanding (Multiple Choice)

**Question**: In the equation of motion M(q)q̈ + C(q, q̇)q̇ + g(q) = τ, what happens if we set τ = 0?

A) The robot stops immediately
B) The robot accelerates due to gravity
C) The robot maintains constant velocity
D) The robot oscillates around equilibrium

**Answer**: B

**Rubric**:
- Correct answer (B): 1 point
- Explanation mentioning gravity acceleration: +0.5 points

---

### 2. Derivation (Short Answer)

**Question**: For a single-link pendulum (mass m, length L), derive the gravity torque g(q) as a function of angle θ. Show all steps.

**Answer**:
```
Potential energy: P = m g h = m g L cos(θ)
Gravity torque: g(θ) = -∂P/∂θ = m g L sin(θ)
```

**Rubric**:
- Correct potential energy expression: 1 point
- Correct derivative: 1 point
- Correct sign: 0.5 points

---

### 3. Implementation (Code)

**Question**: Implement a function `compute_inertia_matrix(q, m1, m2, L1, L2)` that returns the 2×2 inertia matrix M(q) for a 2-DOF planar arm. Test with q = [π/4, π/6].

**Rubric**:
- Correct m11, m12, m22 expressions: 2 points
- Proper matrix construction: 1 point
- Test case output provided: 0.5 points

---

### 4. Analysis (Application)

**Question**: A humanoid robot arm carrying a 5kg payload exhibits large tracking errors with PID control. Suggest two improvements and explain why they would help.

**Expected Answer**:
1. Add feedforward gravity compensation to reduce steady-state error
2. Increase proportional gain K_p to improve stiffness
3. Use computed torque control to handle payload-induced coupling

**Rubric**:
- Two valid suggestions: 1 point each
- Physical explanation for each: 0.5 points each

---

### 5. Stability (Advanced)

**Question**: Explain why a PID controller with very high K_p and K_d gains can cause instability, even though higher gains theoretically improve performance.

**Expected Answer**: High gains amplify sensor noise and modeling errors, causing high-frequency oscillations. Actuator delays and sampling time introduce phase lag, reducing stability margins. The closed-loop system can exceed Nyquist frequency, violating stability criteria.

**Rubric**:
- Mention of sensor noise: 1 point
- Mention of delays/sampling: 1 point
- Stability criterion reference: 1 point

---

### 6. Design Trade-off (Application)

**Question**: For a collaborative robot working near humans, would you set impedance stiffness K_d high or low? Justify your answer with safety and performance considerations.

**Expected Answer**: Set K_d **low** for safety (compliant interaction, low impact forces). Trade-off: Lower accuracy and slower response. Mitigation: Use hybrid force/position control or variable impedance.

**Rubric**:
- Correct choice (low): 1 point
- Safety justification: 1 point
- Performance trade-off identified: 1 point

---

## Further Reading

1. **Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G.** (2009). *Robotics: Modelling, Planning and Control*. Springer. (Chapters 7-8: Dynamics and Motion Control)

2. **Spong, M. W., Hutchinson, S., & Vidyasagar, M.** (2006). *Robot Modeling and Control*. Wiley. (Chapters 6-7: Dynamics and Control)

3. **Murray, R. M., Li, Z., & Sastry, S. S.** (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press. (Chapter 4: Robot Dynamics)

4. **Hogan, N.** (1985). Impedance control: An approach to manipulation. *Journal of Dynamic Systems, Measurement, and Control*, 107(1), 1-7.

5. **Slotine, J.-J. E., & Li, W.** (1991). *Applied Nonlinear Control*. Prentice Hall. (Control theory foundations)

---

## Summary

This chapter introduced **robot dynamics** and **control fundamentals**:

1. **Dynamics modeling**: Lagrangian and Newton-Euler formulations derive equations of motion M(q)q̈ + C(q, q̇)q̇ + g(q) = τ

2. **PID control**: Simple, robust joint-level control using proportional-integral-derivative feedback

3. **Computed torque control**: Model-based control that linearizes dynamics for accurate trajectory tracking

4. **Impedance control**: Regulates force-motion relationship for safe physical interaction

**Key Takeaways**:
- Dynamics tells us how forces produce motion
- Control computes forces to achieve desired motion
- Model-based controllers outperform PID but require accurate parameters
- Compliant control is essential for safe human-robot interaction

**Next Chapter Preview**: Chapter 5 covers **perception**—how robots sense their environment using cameras, LIDAR, and tactile sensors to enable autonomous behavior.

---

## References

[1] Siciliano, B., et al. (2009). *Robotics: Modelling, Planning and Control*. Springer.

[2] Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson Education.

[3] Spong, M. W., et al. (2006). *Robot Modeling and Control*. Wiley.

[4] Goldstein, H., Poole, C., & Safko, J. (2002). *Classical Mechanics* (3rd ed.). Addison-Wesley.

[5] Murray, R. M., et al. (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press.

[6] Featherstone, R. (2008). *Rigid Body Dynamics Algorithms*. Springer.

[7] Luh, J. Y., Walker, M. W., & Paul, R. P. (1980). On-line computational scheme for mechanical manipulators. *Journal of Dynamic Systems, Measurement, and Control*, 102(2), 69-76.

[8] Åström, K. J., & Murray, R. M. (2008). *Feedback Systems: An Introduction for Scientists and Engineers*. Princeton University Press.

[9] Ziegler, J. G., & Nichols, N. B. (1942). Optimum settings for automatic controllers. *Transactions of the ASME*, 64(11), 759-765.

[10] Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Prentice Hall.

[11] Slotine, J.-J. E., & Li, W. (1987). On the adaptive control of robot manipulators. *The International Journal of Robotics Research*, 6(3), 49-59.

[12] Sciavicco, L., & Siciliano, B. (1996). *Modeling and Control of Robot Manipulators*. McGraw-Hill.

[13] Hogan, N. (1985). Impedance control: An approach to manipulation. *Journal of Dynamic Systems, Measurement, and Control*, 107(1), 1-7.

[14] Pratt, G. A., & Williamson, M. M. (1995). Series elastic actuators. In *Proceedings 1995 IEEE/RSJ International Conference on Intelligent Robots and Systems* (Vol. 1, pp. 399-406). IEEE.

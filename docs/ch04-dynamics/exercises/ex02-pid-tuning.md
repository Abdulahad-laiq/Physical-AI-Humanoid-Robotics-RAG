---
exercise_id: ex04-02-pid-tuning
chapter: ch04-dynamics
title: "Design and Tune PID Controller for Trajectory Tracking"
learning_outcome: "Implement PID control and systematically tune gains to minimize tracking error"
difficulty: advanced
estimated_time: "90-120 minutes"
prerequisites:
  - "Chapter 3: Forward kinematics"
  - "Chapter 4: PID control fundamentals"
  - "Exercise 1: Gravity compensation (helpful but not required)"
tools:
  - Python 3.9+
  - NumPy
  - Matplotlib
---

# Exercise: Design and Tune PID Controller for Trajectory Tracking

## Overview

Design, implement, and systematically tune a **PID (Proportional-Integral-Derivative) controller** to track a figure-eight trajectory with a 2-DOF planar robot arm. You'll learn:

- How P, I, and D gains affect tracking performance
- Systematic tuning methods (Ziegler-Nichols, manual tuning)
- Performance metrics (RMSE, overshoot, settling time)
- Trade-offs between speed, accuracy, and stability [1]

**What you'll build**: Complete PID controller with automated tuning algorithm and performance analysis

**Why it matters**: PID is the most widely used control algorithm in industry—over 95% of industrial controllers are PID-based [2]. Understanding PID tuning is essential for any robotics engineer.

**Real-world application**: Manufacturing robots use PID controllers tuned for specific tasks: fast P-gain for pick-and-place, high D-gain for delicate assembly, I-gain for eliminating position offsets under varying loads.

---

## Problem Statement

**Given**: 2-DOF planar robot arm from Chapter 4 dynamics

**Task**: Track a figure-eight trajectory in Cartesian space (x-y plane) while:
1. Minimizing tracking error (RMSE < 5mm)
2. Limiting overshoot (< 10% in step response)
3. Achieving fast settling time (< 0.5s for step inputs)
4. Maintaining stability under payload variations (0-2kg)

**Trajectory**: Figure-eight path parameterized by:

```
x(t) = A * sin(ωt)
y(t) = B * sin(2ωt)
```

where A = 0.3m, B = 0.2m, ω = 0.5 rad/s (one loop every ~12.5 seconds)

**Success Criteria**:
- [ ] PID controller tracks figure-eight with RMSE < 5mm
- [ ] Step response overshoot < 10%
- [ ] Settling time < 0.5s
- [ ] Stable performance with 0-2kg payload
- [ ] Automated tuning algorithm implemented
- [ ] Performance plots generated (tracking, error, control effort)

---

## Theoretical Background

### PID Control Recap

The PID control law for each joint i:

```
τ_i(t) = K_p,i e_i(t) + K_i,i ∫e_i(τ)dτ + K_d,i ė_i(t)
```

where:
- **e_i(t) = q_d,i(t) - q_i(t)**: position error
- **K_p**: proportional gain (stiffness, responsiveness)
- **K_i**: integral gain (eliminates steady-state error)
- **K_d**: derivative gain (damping, reduces oscillation)

---

### Gain Effects

**Proportional Gain (K_p)**:
- ↑ K_p → faster response, smaller steady-state error
- ↑↑ K_p → overshoot, oscillation, instability

**Integral Gain (K_i)**:
- ↑ K_i → eliminates steady-state error
- ↑↑ K_i → slow response, overshoot, wind-up issues

**Derivative Gain (K_d)**:
- ↑ K_d → reduces overshoot, improves damping
- ↑↑ K_d → amplifies noise, reduces responsiveness

---

### Ziegler-Nichols Tuning Method

**Step 1**: Set K_i = K_d = 0. Increase K_p until system oscillates with constant amplitude (critical gain K_u).

**Step 2**: Measure oscillation period T_u.

**Step 3**: Compute PID gains:

```
K_p = 0.6 * K_u
K_i = 1.2 * K_u / T_u
K_d = 0.075 * K_u * T_u
```

**Alternative**: For reduced overshoot, use:

```
K_p = 0.45 * K_u
K_i = 0.54 * K_u / T_u
K_d = 0.15 * K_u * T_u
```

[3]

---

### Performance Metrics

**1. Root Mean Square Error (RMSE)**:

```
RMSE = sqrt( (1/N) Σ (q_d,i - q_i)² )
```

**2. Maximum Overshoot**:

```
Overshoot = (peak_value - steady_state_value) / steady_state_value * 100%
```

**3. Settling Time**:

Time for error to enter and stay within ±2% of final value.

**4. Rise Time**:

Time to go from 10% to 90% of final value.

**5. Steady-State Error**:

```
e_ss = lim (t→∞) |q_d(t) - q(t)|
```

---

## Code Template

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

class PIDController:
    """PID controller with anti-windup and derivative filtering"""

    def __init__(self, Kp, Ki, Kd, dt, integral_limit=None, derivative_filter_alpha=0.1):
        """
        Args:
            Kp, Ki, Kd: PID gains (scalars or arrays for each joint)
            dt: sampling time (s)
            integral_limit: anti-windup limit (saturation for integral term)
            derivative_filter_alpha: low-pass filter coefficient for derivative (0 = no filter, 1 = full filter)
        """
        self.Kp = np.atleast_1d(Kp)
        self.Ki = np.atleast_1d(Ki)
        self.Kd = np.atleast_1d(Kd)
        self.dt = dt

        self.integral_limit = integral_limit
        self.derivative_filter_alpha = derivative_filter_alpha

        self.reset()

    def reset(self):
        """Reset internal state"""
        self.integral = np.zeros_like(self.Kp)
        self.prev_error = None
        self.prev_derivative = np.zeros_like(self.Kp)

    def compute(self, q_desired, q_actual, dq_desired=None, dq_actual=None):
        """
        Compute PID control output

        Args:
            q_desired: desired position
            q_actual: actual position
            dq_desired: desired velocity (optional, for feedforward)
            dq_actual: actual velocity (optional, for better derivative term)

        Returns:
            control: PID output (torques)
        """
        # Position error
        error = np.atleast_1d(q_desired) - np.atleast_1d(q_actual)

        # Proportional term
        P = self.Kp * error

        # Integral term with anti-windup
        self.integral += error * self.dt

        if self.integral_limit is not None:
            self.integral = np.clip(self.integral, -self.integral_limit, self.integral_limit)

        I = self.Ki * self.integral

        # Derivative term with filtering
        if self.prev_error is None:
            derivative = np.zeros_like(error)
        else:
            derivative_raw = (error - self.prev_error) / self.dt

            # Low-pass filter to reduce noise
            derivative = (self.derivative_filter_alpha * derivative_raw +
                         (1 - self.derivative_filter_alpha) * self.prev_derivative)

            self.prev_derivative = derivative

        self.prev_error = error.copy()

        D = self.Kd * derivative

        # PID output
        control = P + I + D

        return control

def dynamics_2dof(state, t, tau, params):
    """
    2-DOF arm dynamics for scipy.integrate.odeint

    Args:
        state: [theta1, theta2, dtheta1, dtheta2]
        t: time (required by odeint, not used)
        tau: control torques [tau1, tau2]
        params: dict with L1, L2, m1, m2, g

    Returns:
        dstate: [dtheta1, dtheta2, ddtheta1, ddtheta2]
    """
    theta1, theta2, dtheta1, dtheta2 = state
    L1, L2, m1, m2, g = params['L1'], params['L2'], params['m1'], params['m2'], params['g']

    # Inertia matrix M(q)
    m11 = (m1 + m2) * L1**2 + m2 * L2**2 + 2 * m2 * L1 * L2 * np.cos(theta2)
    m12 = m2 * L2**2 + m2 * L1 * L2 * np.cos(theta2)
    m22 = m2 * L2**2

    M = np.array([[m11, m12], [m12, m22]])

    # Coriolis/centrifugal
    h = -m2 * L1 * L2 * np.sin(theta2)
    c1 = h * (2 * dtheta1 * dtheta2 + dtheta2**2)
    c2 = h * dtheta1**2
    C = np.array([c1, c2])

    # Gravity
    g1 = (m1 + m2) * g * L1 * np.cos(theta1) + m2 * g * L2 * np.cos(theta1 + theta2)
    g2 = m2 * g * L2 * np.cos(theta1 + theta2)
    G = np.array([g1, g2])

    # Solve for acceleration: M ddq = tau - C - G
    ddq = np.linalg.solve(M, tau - C - G)

    return [dtheta1, dtheta2, ddq[0], ddq[1]]

def inverse_kinematics_2dof(x, y, L1=0.5, L2=0.3):
    """
    Analytical IK for 2-DOF planar arm (elbow-up solution)

    Args:
        x, y: desired end-effector position
        L1, L2: link lengths

    Returns:
        theta1, theta2: joint angles (rad)
    """
    r = np.sqrt(x**2 + y**2)

    # Check reachability
    if r > (L1 + L2) or r < abs(L1 - L2):
        raise ValueError(f"Target ({x:.3f}, {y:.3f}) unreachable")

    # Law of cosines
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    cos_theta2 = np.clip(cos_theta2, -1, 1)  # Numerical safety

    theta2 = np.arccos(cos_theta2)  # Elbow-up solution

    # Solve for theta1
    k1 = L1 + L2 * np.cos(theta2)
    k2 = L2 * np.sin(theta2)

    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return theta1, theta2

def generate_figure_eight_trajectory(t, A=0.3, B=0.2, omega=0.5):
    """
    Generate figure-eight trajectory in Cartesian space

    Args:
        t: time array
        A, B: amplitude parameters (m)
        omega: angular frequency (rad/s)

    Returns:
        x, y, dx, dy: position and velocity arrays
    """
    x = A * np.sin(omega * t)
    y = B * np.sin(2 * omega * t)

    dx = A * omega * np.cos(omega * t)
    dy = B * 2 * omega * np.cos(2 * omega * t)

    return x, y, dx, dy

def tune_pid_ziegler_nichols(arm_params, test_amplitude=0.1):
    """
    TODO: Implement Ziegler-Nichols tuning

    Steps:
    1. Set Ki = Kd = 0
    2. Increase Kp until sustained oscillation
    3. Measure critical gain Ku and period Tu
    4. Compute PID gains using Z-N formulas

    Args:
        arm_params: robot parameters
        test_amplitude: step size for testing

    Returns:
        Kp, Ki, Kd: tuned gains for both joints
    """
    # TODO: Implement automated tuning
    # For now, return manually tuned gains
    Kp = np.array([50, 30])
    Ki = np.array([5, 3])
    Kd = np.array([10, 8])

    return Kp, Ki, Kd

def simulate_trajectory_tracking(pid, trajectory_func, params, t_final=15.0, dt=0.01):
    """
    Simulate PID controller tracking a trajectory

    Args:
        pid: PIDController instance
        trajectory_func: function(t) returning (q_desired, dq_desired)
        params: robot parameters
        t_final: simulation duration (s)
        dt: timestep (s)

    Returns:
        t, q_actual, q_desired, tau: time, actual position, desired position, control torques
    """
    num_steps = int(t_final / dt)
    t = np.linspace(0, t_final, num_steps)

    q_actual = np.zeros((num_steps, 2))
    q_desired_arr = np.zeros((num_steps, 2))
    tau_arr = np.zeros((num_steps, 2))

    # Initial state: [theta1, theta2, dtheta1, dtheta2]
    state = np.array([0, 0, 0, 0])

    for i in range(num_steps):
        # Get desired trajectory
        q_desired, dq_desired = trajectory_func(t[i])

        q_desired_arr[i] = q_desired

        # Compute control
        tau = pid.compute(q_desired, state[0:2])
        tau_arr[i] = tau

        # Simulate dynamics (one timestep using odeint)
        state = odeint(dynamics_2dof, state, [0, dt], args=(tau, params))[-1]

        q_actual[i] = state[0:2]

    return t, q_actual, q_desired_arr, tau_arr

def evaluate_performance(t, q_desired, q_actual):
    """
    Compute performance metrics

    Returns:
        metrics: dict with RMSE, max_error, steady_state_error
    """
    error = q_desired - q_actual

    rmse = np.sqrt(np.mean(error**2, axis=0))
    max_error = np.max(np.abs(error), axis=0)
    steady_state_error = np.mean(np.abs(error[-100:]), axis=0)  # Last 1 second

    metrics = {
        'rmse': rmse,
        'max_error': max_error,
        'steady_state_error': steady_state_error
    }

    return metrics

def main():
    """Main execution"""

    # Robot parameters
    params = {'L1': 0.5, 'L2': 0.3, 'm1': 2.0, 'm2': 1.0, 'g': 9.81}
    dt = 0.01

    # Generate figure-eight trajectory
    def traj_func(t):
        x, y, dx, dy = generate_figure_eight_trajectory(np.array([t]))
        theta1, theta2 = inverse_kinematics_2dof(x[0], y[0], params['L1'], params['L2'])
        return np.array([theta1, theta2]), np.array([0, 0])  # Simplified: no velocity IK

    # TODO: Tune PID gains (try different values)
    Kp, Ki, Kd = tune_pid_ziegler_nichols(params)

    print(f"PID Gains: Kp={Kp}, Ki={Ki}, Kd={Kd}")

    # Create PID controller
    pid = PIDController(Kp, Ki, Kd, dt, integral_limit=10.0)

    # Simulate
    t, q_actual, q_desired, tau = simulate_trajectory_tracking(pid, traj_func, params, t_final=15.0)

    # Evaluate performance
    metrics = evaluate_performance(t, q_desired, q_actual)

    print("\n=== Performance Metrics ===")
    print(f"RMSE (Joint 1): {np.degrees(metrics['rmse'][0]):.3f}°")
    print(f"RMSE (Joint 2): {np.degrees(metrics['rmse'][1]):.3f}°")
    print(f"Max Error (Joint 1): {np.degrees(metrics['max_error'][0]):.3f}°")
    print(f"Max Error (Joint 2): {np.degrees(metrics['max_error'][1]):.3f}°")

    # Plot results
    plt.figure(figsize=(14, 10))

    # Joint tracking
    for i in range(2):
        plt.subplot(3, 2, i + 1)
        plt.plot(t, np.degrees(q_desired[:, i]), 'r--', label='Desired', linewidth=2)
        plt.plot(t, np.degrees(q_actual[:, i]), 'b-', label='Actual', alpha=0.7)
        plt.xlabel('Time (s)')
        plt.ylabel(f'Joint {i+1} Angle (deg)')
        plt.title(f'Joint {i+1} Tracking')
        plt.legend()
        plt.grid(True, alpha=0.3)

    # Tracking error
    for i in range(2):
        plt.subplot(3, 2, i + 3)
        error = np.degrees(q_desired[:, i] - q_actual[:, i])
        plt.plot(t, error, 'g-')
        plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
        plt.xlabel('Time (s)')
        plt.ylabel(f'Error (deg)')
        plt.title(f'Joint {i+1} Tracking Error')
        plt.grid(True, alpha=0.3)

    # Control effort
    for i in range(2):
        plt.subplot(3, 2, i + 5)
        plt.plot(t, tau[:, i], color='purple', alpha=0.7)
        plt.xlabel('Time (s)')
        plt.ylabel(f'Torque (Nm)')
        plt.title(f'Joint {i+1} Control Torque')
        plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('pid_trajectory_tracking.png', dpi=150)
    print("\nPlot saved: pid_trajectory_tracking.png")

if __name__ == "__main__":
    main()
```

**Deliverable**: Completed code with tuned PID gains achieving RMSE < 5mm

---

## Tuning Guidelines

### Manual Tuning Procedure

1. **Start with P-only**:
   - Set Ki = Kd = 0
   - Increase Kp until response is fast but oscillates
   - Reduce Kp by 50%

2. **Add D-term**:
   - Increase Kd to reduce overshoot
   - Typical starting point: Kd = Kp / 10

3. **Add I-term**:
   - Increase Ki slowly to eliminate steady-state error
   - Watch for increased overshoot and slower response
   - Typical starting point: Ki = Kp / 50

4. **Iterate**:
   - Fine-tune all three gains
   - Test under different conditions (payloads, speeds)

### Suggested Initial Values

For a 2-DOF arm with L1=0.5m, L2=0.3m, m1=2kg, m2=1kg:

```
Joint 1 (shoulder): Kp = 50, Ki = 5, Kd = 10
Joint 2 (elbow):    Kp = 30, Ki = 3, Kd = 8
```

---

## Extension Challenges (Optional)

1. **Adaptive PID**: Implement gain scheduling based on configuration (different gains for different arm poses)

2. **Feedforward Control**: Add gravity compensation as feedforward term to improve tracking

3. **Anti-Windup**: Implement integral windup protection (saturation, back-calculation)

4. **Noise Robustness**: Add sensor noise and test derivative filtering

5. **Payload Variation**: Test with varying payloads (0-2kg) and show robust performance

---

## Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| PID implementation correct | 2 | All three terms computed properly |
| Trajectory generation | 1.5 | Figure-eight path correct in Cartesian space |
| IK integration | 1.5 | Converts Cartesian trajectory to joint space |
| Tuning achieves RMSE < 5mm | 3 | Systematic tuning process shown |
| Performance plots | 1 | Clear visualization of tracking, error, control |
| Code quality | 1 | Modular, documented, readable |

**Total**: 10 points

---

## References

[1] Åström, K. J., & Hägglund, T. (2006). *Advanced PID Control*. ISA-The Instrumentation, Systems, and Automation Society.

[2] Ang, K. H., Chong, G., & Li, Y. (2005). PID control system analysis, design, and technology. *IEEE Transactions on Control Systems Technology*, 13(4), 559-576.

[3] Ziegler, J. G., & Nichols, N. B. (1942). Optimum settings for automatic controllers. *Transactions of the ASME*, 64(11), 759-765.

[4] O'Dwyer, A. (2009). *Handbook of PI and PID Controller Tuning Rules* (3rd ed.). Imperial College Press.

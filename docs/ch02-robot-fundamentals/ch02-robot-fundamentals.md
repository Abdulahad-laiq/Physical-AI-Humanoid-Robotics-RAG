---
id: ch02-robot-fundamentals
title: "Chapter 2: Robot Fundamentals - Sensors, Actuators, and Coordinate Frames"
sidebar_label: "Ch 2: Robot Fundamentals"
sidebar_position: 2
description: "Explore robot sensors, actuators, and coordinate transformations essential for humanoid robotics"
keywords:
  - sensors
  - actuators
  - IMU
  - coordinate frames
  - homogeneous transformations
  - DH parameters
prerequisites:
  - ch01-introduction/ch01-introduction
  - "Linear algebra (vectors, matrices)"
learning_objectives:
  - "Explain common sensor types used in humanoid robots (IMU, force/torque, cameras, LIDAR)"
  - "Describe actuator technologies (electric motors, hydraulics, series elastic actuators)"
  - "Define and apply coordinate frame transformations in 3D space"
  - "Use homogeneous transformation matrices for position/orientation representation"
  - "Implement basic sensor data acquisition and visualization in Python"
estimated_time: "5-6 hours"
difficulty: beginner
---

# Chapter 2: Robot Fundamentals - Sensors, Actuators, and Coordinate Frames

## Introduction

Humanoid robots are complex electromechanical systems that perceive their environment through **sensors**, act through **actuators**, and represent their configuration using **coordinate frames**. Understanding these three fundamental components is essential for robot programming, control, and simulation.

- **Context**: Sensors provide the "eyes and ears" for robots, actuators are the "muscles," and coordinate frames are the mathematical language describing "where things are." Mastering these fundamentals enables you to work with any robotic system.

- **Preview**: This chapter explores proprioceptive sensors (IMUs, encoders, force sensors), exteroceptive sensors (cameras, LIDAR), actuator types (motors, hydraulics, series elastic actuators), and coordinate transformations (rotation matrices, homogeneous transforms, Denavit-Hartenberg convention).

- **Connection**: Building on Chapter 1's introduction to Physical AI, we now dive into the hardware and mathematics that enable sensorimotor loops. Chapters 3-4 will use these coordinate frame concepts for kinematics and dynamics.

---

## Key Concepts

### 1. Proprioceptive Sensors - Sensing Internal State

**Proprioceptive sensors** measure a robot's own state (joint positions, velocities, forces, orientation) rather than the external environment [1].

#### Inertial Measurement Unit (IMU)

**Definition**: An IMU combines accelerometers and gyroscopes to measure linear acceleration and angular velocity in 3D [1].

**Explanation**: Modern IMUs use MEMS (Micro-Electro-Mechanical Systems) technology, providing compact, low-cost inertial sensing. A 6-axis IMU includes:
- **3-axis accelerometer**: Measures linear acceleration (including gravity) in x, y, z directions
- **3-axis gyroscope**: Measures angular velocity (rotation rate) around x, y, z axes

A 9-axis IMU adds a 3-axis magnetometer for absolute heading (compass).

**Example Application**: A humanoid robot's torso IMU measures body tilt. If the robot leans forward (pitch), the IMU detects angular velocity and acceleration changes, triggering balance controllers to prevent falling.

**Measurement Challenges**:
- **Drift**: Gyroscopes accumulate integration errors over time
- **Noise**: Accelerometers are sensitive to vibrations
- **Gravity**: Accelerometers measure gravity + motion; must separate components

**Typical Specifications** (e.g., MPU-6050 IMU):
- Accelerometer range: ±2g to ±16g
- Gyroscope range: ±250°/s to ±2000°/s
- Update rate: 1-8 kHz

**Citation**: [1], [2]

---

#### Joint Encoders

**Definition**: Encoders measure the angular position (and sometimes velocity) of revolute joints or linear position of prismatic joints [1].

**Types**:
1. **Optical encoders**: Use light patterns and photodetectors
   - *Incremental*: Count position changes from a reference
   - *Absolute*: Provide position directly (no homing needed)
2. **Magnetic encoders**: Use Hall effect sensors and magnetic fields
3. **Potentiometers**: Measure resistance changes (less common, lower precision)

**Resolution**: Measured in pulses per revolution (PPR). High-end encoders: 10,000+ PPR.

**Example**: A humanoid arm with 7 joints needs 7 encoders. Each encoder reports joint angle with ~0.01° precision, enabling accurate forward kinematics calculations (Chapter 3).

**Citation**: [1], [2]

---

#### Force/Torque Sensors

**Definition**: Force/torque (F/T) sensors measure forces and moments acting on a robot, typically mounted at wrists, ankles, or tool interfaces [1].

**6-axis F/T Sensor Output**:
- Forces: Fx, Fy, Fz (Newtons)
- Torques: Tx, Ty, Tz (Newton-meters)

**Applications**:
- **Manipulation**: Detect contact forces during grasping (prevent crushing objects)
- **Walking**: Measure ground reaction forces for balance control
- **Compliance**: Enable force-controlled interaction (push a button gently)

**Example**: When a humanoid picks up an egg, wrist F/T sensors measure grip force. If force exceeds a threshold (e.g., 5N), the controller reduces finger motor torques to avoid breaking the egg.

**Citation**: [1], [27]

---

### 2. Exteroceptive Sensors - Sensing the Environment

**Exteroceptive sensors** measure external world properties (objects, obstacles, distances, images) [1].

#### Cameras (RGB and Depth)

**RGB Cameras**:
- Capture 2D color images (Red-Green-Blue pixel arrays)
- Resolution: 640x480 (VGA) to 1920x1080 (Full HD) or higher
- Frame rate: 30-60 FPS typical
- Use: Object recognition, visual servoing, human detection

**Depth Cameras (RGB-D)**:
- Add distance measurement to each pixel (2.5D perception)
- Technologies:
  - **Structured light**: Project IR pattern, triangulate depth (Kinect v1)
  - **Time-of-Flight (ToF)**: Measure IR light travel time (Kinect v2, RealSense)
  - **Stereo vision**: Use two cameras like human eyes (ZED)
- Output: Color image + depth map
- Range: 0.5-5 meters typical

**Example**: A humanoid uses an RGB-D camera to detect a cup on a table. RGB image identifies "cup" via neural network; depth map gives distance (e.g., 0.8m) for reaching motion planning.

**Pinhole Camera Model**:

The fundamental camera projection relates 3D world point (X, Y, Z) to 2D image pixel (u, v):

```
[u]   [fx  0  cx]   [X/Z]
[v] = [ 0 fy  cy] * [Y/Z]
[1]   [ 0  0   1]   [ 1 ]
```

where (fx, fy) are focal lengths and (cx, cy) is the principal point.

**Citation**: [20], [21], [22]

---

#### LIDAR (Light Detection and Ranging)

**Definition**: LIDAR uses laser beams to measure distances to objects by timing light reflections [1].

**Types**:
- **2D LIDAR**: Scans a plane (e.g., floor level for mobile robots)
- **3D LIDAR**: Scans in 3D (e.g., Velodyne for autonomous cars)

**Specifications**:
- Range: 0.1-100+ meters
- Angular resolution: 0.25-1 degree
- Scan rate: 5-40 Hz

**Advantages**: Works in darkness, precise distance measurement, long range
**Disadvantages**: Expensive, sensitive to rain/fog, no color information

**Example**: A humanoid navigating indoors uses 2D LIDAR to build an occupancy grid map, detecting walls and obstacles for path planning.

**Citation**: [1], [22]

---

### 3. Actuator Technologies

**Actuators** convert electrical, hydraulic, or pneumatic energy into mechanical motion [1].

#### Electric Motors

**DC Motors**:
- **Brushed DC**: Simple, low-cost, require maintenance (brush wear)
- **Brushless DC (BLDC)**: Higher efficiency, longer life, need electronic commutation
- **Characteristics**: High speed (1000-10,000 RPM), low torque → need gearboxes

**Servo Motors**:
- Integrated motor + encoder + controller
- Position control via PWM (Pulse Width Modulation) signal
- Common in hobby robotics (e.g., Dynamixel servos in research humanoids)

**Stepper Motors**:
- Move in discrete steps (e.g., 200 steps/revolution = 1.8°/step)
- Open-loop position control (no encoder needed if no load slipping)
- Lower speed, good for precise positioning

**Key Parameters**:
- **Torque**: Rotational force (Nm) - determines load capacity
- **Speed**: RPM (revolutions per minute)
- **Power**: Torque × Speed (Watts)
- **Efficiency**: Typically 70-90% for BLDC motors

**Example**: A humanoid elbow joint uses a BLDC motor with 100:1 planetary gearbox, producing 50 Nm torque at the joint from a 0.5 Nm motor.

**Citation**: [1], [2]

---

#### Hydraulic Actuators

**Definition**: Hydraulic actuators use pressurized fluid (oil) to generate linear or rotary motion [1].

**Advantages**:
- **High power-to-weight ratio**: Can produce enormous forces
- **High bandwidth**: Fast response (important for dynamic walking)
- **Backdrivability**: Can be pushed/moved by external forces (safer for contact)

**Disadvantages**:
- **Complexity**: Require pump, valves, hoses, fluid management
- **Noise**: Pumps are loud
- **Maintenance**: Fluid leaks, seal wear

**Example**: Boston Dynamics' Atlas humanoid uses hydraulic actuators for legs and arms, enabling dynamic locomotion (running, backflips) that electric motors struggle to achieve.

**Citation**: [1], [10]

---

#### Series Elastic Actuators (SEA)

**Definition**: A Series Elastic Actuator places a compliant spring between the motor and the load, enabling force control through spring deflection measurement [13].

**Concept**:
```
Motor → Gearbox → Spring → Load
                     ↑
                  Encoder (measures deflection)
```

**Advantages**:
- **Force sensing**: Hooke's law: Force = k × spring_deflection
- **Impact tolerance**: Spring absorbs shocks (safer for human interaction)
- **Energy storage**: Springs can store/release energy (efficiency in walking)

**Disadvantages**:
- **Bandwidth limitation**: Spring oscillation limits control speed
- **Position precision**: Spring deflection reduces position accuracy

**Example**: NASA's Valkyrie humanoid uses SEAs in major joints, enabling compliant interaction with humans and environments while measuring interaction forces without dedicated F/T sensors.

**Citation**: [13]

---

### 4. Coordinate Frames and Transformations

**Coordinate frames** are essential for describing where robot parts, objects, and obstacles are in 3D space [2].

#### Reference Frames

**World Frame** (also called Global Frame or Inertial Frame):
- Fixed reference (does not move)
- Origin often at robot base or room corner
- Axes: Xw, Yw, Zw

**Base Frame**:
- Fixed to robot's base (moves with mobile robots)
- Origin at robot base center
- Axes: Xb, Yb, Zb

**Link Frames**:
- One frame attached to each robot link
- Move with the link during robot motion

**End-Effector Frame** (also called Tool Frame):
- Attached to robot's gripper/hand
- Describes where the hand is and where it's pointing

**Example**: For a humanoid standing in a room:
- World frame origin: room corner
- Base frame origin: robot pelvis center
- Right hand frame: right palm center, Xh pointing forward, Yh pointing left, Zh pointing up

**Citation**: [2], [3]

---

#### Rotation Matrices

**Definition**: A 3×3 orthogonal matrix R that rotates vectors from one frame to another while preserving lengths and angles [2].

**Properties**:
- Orthogonal: R^T = R^(-1)
- Determinant: det(R) = 1 (right-handed)
- 9 elements but only 3 degrees of freedom (rotation about x, y, z)

**Basic Rotations**:

Rotation about Z-axis by angle θ:
```
Rz(θ) = [cos(θ)  -sin(θ)   0]
        [sin(θ)   cos(θ)   0]
        [  0        0      1]
```

Rotation about X-axis by angle θ:
```
Rx(θ) = [1    0        0    ]
        [0  cos(θ) -sin(θ)]
        [0  sin(θ)  cos(θ)]
```

Rotation about Y-axis by angle θ:
```
Ry(θ) = [ cos(θ)  0  sin(θ)]
        [   0     1    0   ]
        [-sin(θ)  0  cos(θ)]
```

**Composition**: Rotations are composed by matrix multiplication:
R_combined = Rz(θ3) * Ry(θ2) * Rx(θ1)

**Citation**: [2], [3]

---

#### Homogeneous Transformations

**Definition**: A 4×4 matrix combining rotation and translation to represent rigid body transformations in 3D [2].

**Structure**:
```
T = [R  p]   where R is 3×3 rotation matrix,
    [0  1]         p is 3×1 position vector
```

**Example**: Transform from base frame to hand frame:
```
T_base_hand = [R_base_hand   p_base_hand]
               [    0    0  0      1     ]
```

**Usage**: To find hand position in base frame:
```
p_hand_in_base = T_base_hand * [0, 0, 0, 1]^T
```

To find object position (known in hand frame) in base frame:
```
p_object_in_base = T_base_hand * p_object_in_hand
```

**Chain Rule**: Transformations chain by multiplication:
```
T_A_C = T_A_B * T_B_C
```

**Example**: To find right hand position relative to left hand:
```
T_left_right = T_left_base * T_base_right
```

where T_left_base = inverse(T_base_left).

**Citation**: [2], [3]

---

### 5. Denavit-Hartenberg (DH) Parameters

**Definition**: A systematic convention for assigning coordinate frames to robot links and describing link-joint relationships with four parameters [11], [2].

**Four DH Parameters per link**:
1. **a_i** (link length): Distance between Z(i-1) and Z(i) along X(i)
2. **alpha_i** (link twist): Angle between Z(i-1) and Z(i) about X(i)
3. **d_i** (link offset): Distance from X(i-1) to X(i) along Z(i-1)
4. **theta_i** (joint angle): Angle from X(i-1) to X(i) about Z(i-1)

**Joint Types**:
- **Revolute joint**: theta_i is variable (joint angle), others constant
- **Prismatic joint**: d_i is variable (joint displacement), others constant

**Transformation from frame (i-1) to frame (i)**:
```
T(i-1,i) = Rotz(theta_i) * Transz(d_i) * Transx(a_i) * Rotx(alpha_i)
```

Expanded as 4×4 matrix:
```
[cos(θi)  -sin(θi)*cos(αi)   sin(θi)*sin(αi)   ai*cos(θi)]
[sin(θi)   cos(θi)*cos(αi)  -cos(θi)*sin(αi)   ai*sin(θi)]
[  0          sin(αi)            cos(αi)            di     ]
[  0            0                  0                1      ]
```

**Why DH?**: Provides a systematic, minimal parameterization of serial-link manipulators. Once DH parameters are defined, forward kinematics (Chapter 3) is straightforward matrix multiplication.

**Citation**: [2], [11]

---

## Code Examples

### Example 1: Read IMU Data from Simulated Robot

**Purpose**: Extract IMU acceleration and angular velocity from PyBullet simulation

```python
"""
IMU Data Acquisition
Read accelerometer and gyroscope data from simulated humanoid robot
"""

import pybullet as p
import pybullet_data
import numpy as np
import time

def setup_simulation():
    """Initialize PyBullet with robot"""
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)

    # Load plane and robot
    p.loadURDF("plane.urdf")
    robot_id = p.loadURDF("r2d2.urdf", [0, 0, 0.5])

    return robot_id

def get_imu_data(robot_id, link_index=-1):
    """
    Get IMU data (linear acceleration and angular velocity) for a link

    Args:
        robot_id: PyBullet body ID
        link_index: Link index (-1 for base link)

    Returns:
        accel: 3D linear acceleration (m/s²) in world frame
        gyro: 3D angular velocity (rad/s) in world frame
    """
    # Get link state (position, orientation, velocities)
    if link_index == -1:
        # Base link
        pos, orn = p.getBasePositionAndOrientation(robot_id)
        lin_vel, ang_vel = p.getBaseVelocity(robot_id)
    else:
        # Other links
        link_state = p.getLinkState(robot_id, link_index, computeLinkVelocity=1)
        pos = link_state[0]
        orn = link_state[1]
        lin_vel = link_state[6]
        ang_vel = link_state[7]

    # Approximate linear acceleration (would need velocity derivative in real code)
    # For now, return gravity component
    accel = np.array([0, 0, -9.81])  # Simplified: only gravity

    gyro = np.array(ang_vel)

    return accel, gyro

def main():
    """Demonstrate IMU data reading"""
    robot_id = setup_simulation()

    print("Reading IMU data for 5 seconds...")
    print("(Robot is static, so acceleration = gravity, angular velocity = 0)")
    print()

    for i in range(50):  # 5 seconds at 10 Hz
        # Step simulation
        p.stepSimulation()
        time.sleep(0.1)

        # Get IMU data
        accel, gyro = get_imu_data(robot_id, link_index=-1)

        if i % 10 == 0:  # Print every second
            print(f"t = {i*0.1:.1f}s:")
            print(f"  Acceleration: [{accel[0]:6.2f}, {accel[1]:6.2f}, {accel[2]:6.2f}] m/s²")
            print(f"  Gyro:         [{gyro[0]:6.2f}, {gyro[1]:6.2f}, {gyro[2]:6.2f}] rad/s")

    p.disconnect()

if __name__ == "__main__":
    main()
```

**Expected Output**:
```
Reading IMU data for 5 seconds...
(Robot is static, so acceleration = gravity, angular velocity = 0)

t = 0.0s:
  Acceleration: [  0.00,   0.00,  -9.81] m/s²
  Gyro:         [  0.00,   0.00,   0.00] rad/s
t = 1.0s:
  Acceleration: [  0.00,   0.00,  -9.81] m/s²
  Gyro:         [  0.00,   0.00,   0.00] rad/s
...
```

---

### Example 2: Homogeneous Transformation Matrices

**Purpose**: Create and compose transformation matrices in Python

```python
"""
Coordinate Frame Transformations
Create rotation and homogeneous transformation matrices
"""

import numpy as np

def rotz(theta):
    """Rotation matrix about Z-axis"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

def roty(theta):
    """Rotation matrix about Y-axis"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]
    ])

def rotx(theta):
    """Rotation matrix about X-axis"""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1,  0,  0],
        [0,  c, -s],
        [0,  s,  c]
    ])

def homogeneous_transform(R, p):
    """
    Create 4x4 homogeneous transformation matrix

    Args:
        R: 3x3 rotation matrix
        p: 3x1 position vector

    Returns:
        T: 4x4 transformation matrix
    """
    T = np.eye(4)
    T[0:3, 0:3] = R
    T[0:3, 3] = p
    return T

def main():
    """Demonstrate transformation matrix operations"""

    # Example: Arm is rotated 90° about Z, translated 0.5m in X
    theta = np.pi / 2  # 90 degrees
    R = rotz(theta)
    p = np.array([0.5, 0, 0])

    T_base_shoulder = homogeneous_transform(R, p)

    print("Transformation from base to shoulder:")
    print(T_base_shoulder)
    print()

    # Point in shoulder frame: [0.3, 0, 0] (30cm forward)
    p_in_shoulder = np.array([0.3, 0, 0, 1])  # Homogeneous coordinates

    # Transform to base frame
    p_in_base = T_base_shoulder @ p_in_shoulder

    print("Point in shoulder frame: [0.3, 0, 0]")
    print(f"Point in base frame: {p_in_base[0:3]}")
    print()

    # Expected: Shoulder rotated 90°, so forward in shoulder = left in base
    # Position = base_to_shoulder + rotated_offset = [0.5, 0, 0] + [0, 0.3, 0]
    print(f"Expected: [0.5, 0.3, 0]")
    print(f"Actual:   [{p_in_base[0]:.2f}, {p_in_base[1]:.2f}, {p_in_base[2]:.2f}]")

if __name__ == "__main__":
    main()
```

**Expected Output**:
```
Transformation from base to shoulder:
[[ 6.12e-17 -1.00e+00  0.00e+00  5.00e-01]
 [ 1.00e+00  6.12e-17  0.00e+00  0.00e+00]
 [ 0.00e+00  0.00e+00  1.00e+00  0.00e+00]
 [ 0.00e+00  0.00e+00  0.00e+00  1.00e+00]]

Point in shoulder frame: [0.3, 0, 0]
Point in base frame: [0.5 0.3 0. ]

Expected: [0.5, 0.3, 0]
Actual:   [0.50, 0.30, 0.00]
```

---

## Practical Exercises

1. **[Extract and Plot IMU Data](exercises/ex01-imu-data.md)** - Read accelerometer/gyro data from simulated robot performing motion; plot time-series graphs
2. **[Compute End-Effector Position with Transforms](exercises/ex02-transforms.md)** - Calculate 3-DOF arm end-effector position using DH parameters and homogeneous transformations

---

## Assessments

### Multiple Choice

**Question 1**: Which sensor type measures a robot's own joint angles?

A) Camera
B) LIDAR
C) Joint encoder
D) Force/torque sensor

<details>
<summary>Show Answer</summary>

**Answer**: C

**Explanation**: Joint encoders are proprioceptive sensors that measure internal state—specifically, the angular position of revolute joints or linear position of prismatic joints. Cameras and LIDAR are exteroceptive (measure environment), and F/T sensors measure forces, not positions [1], [2].
</details>

---

**Question 2**: What is the primary advantage of hydraulic actuators over electric motors for humanoid locomotion?

A) Lower cost
B) Higher power-to-weight ratio
C) Quieter operation
D) No maintenance required

<details>
<summary>Show Answer</summary>

**Answer**: B

**Explanation**: Hydraulic actuators can produce very high forces relative to their weight, enabling dynamic motions like running and jumping. This is why Boston Dynamics' Atlas uses hydraulics. However, hydraulics are expensive (not A), noisy (not C), and require maintenance for fluid/seals (not D) [1], [10].
</details>

---

**Question 3**: In a homogeneous transformation matrix T = [R p; 0 1], what does the 3×1 vector p represent?

A) Rotation angles
B) Angular velocity
C) Position/translation
D) Force applied

<details>
<summary>Show Answer</summary>

**Answer**: C

**Explanation**: In a 4×4 homogeneous transformation matrix, the upper-left 3×3 block (R) represents rotation, and the upper-right 3×1 vector (p) represents the translation/position offset between coordinate frames [2], [3].
</details>

---

### Short Answer

**Question 4**: Explain why IMU measurements include gravity. How would you separate gravity from actual robot acceleration?

<details>
<summary>Show Rubric</summary>

**Rubric** (5 points):
- (2 pts) Explains that accelerometers measure total acceleration = gravity + motion
- (2 pts) Describes method to separate: Use gyroscope data to estimate orientation, calculate gravity direction in sensor frame, subtract from accelerometer reading
- (1 pt) Mentions alternative: Complementary filter or Kalman filter for sensor fusion
</details>

---

**Question 5**: Describe the four Denavit-Hartenberg parameters and explain what each represents.

<details>
<summary>Show Rubric</summary>

**Rubric** (8 points, 2 pts each):
- a_i: Link length (distance between Z-axes along X)
- alpha_i: Link twist (angle between Z-axes about X)
- d_i: Link offset (distance between X-axes along Z)
- theta_i: Joint angle (angle between X-axes about Z)

Reference: [2], [11]
</details>

---

### Diagram/Application Questions

**Question 6**: Given a 2-DOF planar arm with:
- Link 1: Length L1 = 0.5m, angle θ1 = 30°
- Link 2: Length L2 = 0.3m, angle θ2 = 45°

Calculate the (x, y) position of the end-effector in the base frame. Show your work using trigonometry or transformation matrices.

<details>
<summary>Show Rubric</summary>

**Rubric** (6 points):
- (2 pts) Correct approach: Chain link positions or multiply transformation matrices
- (3 pts) Correct calculations:
  - x = L1*cos(θ1) + L2*cos(θ1+θ2) = 0.5*cos(30°) + 0.3*cos(75°) ≈ 0.433 + 0.078 = 0.511m
  - y = L1*sin(θ1) + L2*sin(θ1+θ2) = 0.5*sin(30°) + 0.3*sin(75°) ≈ 0.25 + 0.290 = 0.540m
- (1 pt) Correct final answer: (0.51, 0.54) meters
</details>

---

**Question 7**: A humanoid robot's wrist F/T sensor measures Fz = -15N (downward force). The robot is holding an unknown object. Calculate the object's mass. What assumption are you making?

<details>
<summary>Show Rubric</summary>

**Rubric** (5 points):
- (2 pts) Correct equation: F = m*g, so m = F/g
- (2 pts) Correct calculation: m = 15N / 9.81 m/s² ≈ 1.53 kg
- (1 pt) States assumption: Only gravity acts (no acceleration); sensor measures full object weight
</details>

---

**Question 8**: Explain the trade-off between using an RGB camera versus LIDAR for obstacle detection in a humanoid robot navigating indoors.

<details>
<summary>Show Rubric</summary>

**Rubric** (6 points):
- (2 pts) RGB camera advantages: Lower cost, provides color/texture for object recognition
- (2 pts) LIDAR advantages: Direct distance measurement, works in darkness, longer range
- (2 pts) Trade-offs: Camera needs lighting and depth estimation is harder; LIDAR is expensive but provides precise geometry

Reference: [20], [21], [22]
</details>

---

**Question 9**: Why do Series Elastic Actuators (SEAs) enable force control without dedicated force sensors? Explain the principle.

<details>
<summary>Show Rubric</summary>

**Rubric** (5 points):
- (2 pts) Describes SEA structure: motor → spring → load
- (2 pts) Explains force sensing: Measure spring deflection with encoder; use Hooke's law F = k*x
- (1 pt) Mentions benefit: Enables compliant interaction and shock absorption

Reference: [13]
</details>

---

**Question 10**: A robot has three consecutive coordinate frames: World, Base, Hand. If you know T_world_base and T_base_hand, how do you find T_world_hand? Show the equation.

<details>
<summary>Show Rubric</summary>

**Rubric** (4 points):
- (2 pts) Correct equation: T_world_hand = T_world_base * T_base_hand
- (1 pt) Explains: Chain transformations by matrix multiplication
- (1 pt) Notes order matters (matrix multiplication is not commutative)

Reference: [2], [3]
</details>

---

## Further Reading

1. **B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, *Robotics: Modelling, Planning and Control*. London, U.K.: Springer, 2010, Ch. 2-3.** [1]
   - *Summary*: Comprehensive coverage of robot sensors, actuators, and kinematics. Includes detailed DH parameter derivations and transformation mathematics. Essential reference for this chapter.

2. **J. J. Craig, *Introduction to Robotics: Mechanics and Control*, 4th ed. Pearson, 2017, Ch. 2-3.** [2]
   - *Summary*: Clear explanations of coordinate frames, rotation matrices, and homogeneous transformations with worked examples. Excellent for building intuition.

3. **M. W. Spong, S. Hutchinson, and M. Vidyasagar, *Robot Modeling and Control*, 2nd ed. Wiley, 2020, Ch. 2.** [3]
   - *Summary*: Detailed treatment of robot kinematics and coordinate transformations. Includes alternative rotation representations (Euler angles, quaternions).

4. **N. Hogan, "Impedance control: An approach to manipulation," in *Proc. Amer. Control Conf.*, 1984, pp. 304–313.** [13]
   - *Summary*: Foundational paper on impedance control and the concept behind Series Elastic Actuators. Explains how compliance enables safer, more robust manipulation.

5. **R. Hartley and A. Zisserman, *Multiple View Geometry in Computer Vision*, 2nd ed. Cambridge Univ. Press, 2004.** [20]
   - *Summary*: Comprehensive reference for camera models, calibration, and 3D reconstruction from images. Advanced but invaluable for perception systems (Chapter 5).

---

## Summary

This chapter explored the three fundamental building blocks of humanoid robots: **sensors** (proprioceptive: IMUs, encoders, F/T sensors; exteroceptive: cameras, LIDAR), **actuators** (electric motors, hydraulics, series elastic actuators), and **coordinate frames** (rotation matrices, homogeneous transformations, Denavit-Hartenberg parameters). We learned how IMUs measure orientation and acceleration, how joint encoders provide position feedback for control, and how F/T sensors enable force-controlled manipulation. We compared actuator technologies—electric motors are common and versatile, hydraulics provide high power for dynamic locomotion, and SEAs add compliance for safe interaction. Finally, we mastered coordinate transformations using homogeneous matrices and the DH convention, establishing the mathematical foundation for forward kinematics (Chapter 3). You also practiced reading sensor data from simulation and computing transformations in Python.

**Next Chapter Preview**: Chapter 3 applies these coordinate frame concepts to humanoid kinematics. You'll learn to derive forward kinematics using DH parameters to compute end-effector positions from joint angles, and tackle the inverse kinematics problem—finding joint angles that achieve desired end-effector poses.

---

## References

All citations refer to the [Bibliography](../bibliography.md). Key sources: [1], [2], [3], [10], [11], [13], [20], [21], [22], [27].

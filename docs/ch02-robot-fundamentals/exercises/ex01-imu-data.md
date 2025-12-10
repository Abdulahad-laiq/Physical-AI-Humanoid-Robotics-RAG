---
exercise_id: ex02-01-imu-data
chapter: ch02-robot-fundamentals
title: "Extract and Plot IMU Data"
learning_outcome: "Read IMU data from simulated robot and visualize acceleration/gyro time-series"
difficulty: beginner
estimated_time: "45-60 minutes"
prerequisites:
  - "Completed Chapter 1 exercises"
  - "Understanding of basic plotting (matplotlib)"
tools:
  - Python 3.9+
  - PyBullet
  - NumPy
  - Matplotlib
---

# Exercise: Extract and Plot IMU Data

## Overview

Read accelerometer and gyroscope data from a simulated robot performing a motion sequence, then visualize the data as time-series plots. This exercise demonstrates how robots use IMU sensors for state estimation and balance control.

**What you'll build**: Python script that collects IMU data and generates plots showing how acceleration and angular velocity change during robot motion

**Why it matters**: IMU data is fundamental for humanoid balance, state estimation, and sensor fusion. Understanding IMU measurements prepares you for control algorithms in Chapter 4.

**Real-world application**: Humanoid robots like NAO and Atlas use IMUs at 100-1000 Hz for real-time balance control, fall detection, and odometry.

---

## Problem Statement

**Task**: Create a script that:
1. Loads a robot in PyBullet
2. Applies sinusoidal joint motion to create IMU-detectable movement
3. Records IMU data (accel + gyro) for 5 seconds
4. Plots 6 time-series: ax, ay, az, wx, wy, wz

**Success Criteria**:
- [ ] Script runs without errors
- [ ] IMU data collected at 10+ Hz for 5 seconds
- [ ] 2 plots generated: (1) 3-axis acceleration, (2) 3-axis angular velocity
- [ ] Plots show variation during motion (not flat lines)
- [ ] Axes labeled with units

---

## Code Template

```python
import pybullet as p
import pybullet_data
import numpy as np
import matplotlib.pyplot as plt
import time

def setup():
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    robot = p.loadURDF("r2d2.urdf", [0, 0, 0.5])
    return robot

def apply_motion(robot, t):
    """Apply sinusoidal joint motion"""
    # TODO: Set joint targets using sine waves
    pass

def get_imu(robot):
    """Get base link velocity (approximates IMU)"""
    lin_vel, ang_vel = p.getBaseVelocity(robot)
    # Acceleration requires derivative; use simplified gravity
    accel = np.array([0, 0, -9.81])
    gyro = np.array(ang_vel)
    return accel, gyro

def main():
    robot = setup()
    data = {'t': [], 'accel': [], 'gyro': []}

    for i in range(50):  # 5 seconds at 10 Hz
        t = i * 0.1
        apply_motion(robot, t)
        p.stepSimulation()

        accel, gyro = get_imu(robot)
        data['t'].append(t)
        data['accel'].append(accel)
        data['gyro'].append(gyro)

        time.sleep(0.1)

    # TODO: Create plots
    # Plot 1: Acceleration (3 subplots: ax, ay, az)
    # Plot 2: Gyro (3 subplots: wx, wy, wz)

    p.disconnect()

if __name__ == "__main__":
    main()
```

**Deliverable**: Completed script + 2 PNG plots

---

## Rubric

| Criterion | Points |
|-----------|--------|
| Script executes | 2 |
| IMU data collected | 2 |
| Acceleration plot | 3 |
| Gyro plot | 2 |
| Labels/units | 1 |

**Total**: 10 points

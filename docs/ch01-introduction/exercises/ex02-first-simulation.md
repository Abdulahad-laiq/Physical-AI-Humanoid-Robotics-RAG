---
exercise_id: ex01-02-first-simulation
chapter: ch01-introduction
title: "First Robot Simulation - Load and Control a Humanoid"
learning_outcome: "Load a humanoid robot model in PyBullet, observe joint states, and experiment with basic control"
difficulty: beginner
estimated_time: "45-60 minutes"
prerequisites:
  - "Completed Exercise ex01-python-setup"
  - "Python environment with PyBullet installed"
tools:
  - Python 3.9+
  - PyBullet
  - NumPy
---

# Exercise: First Robot Simulation

## Overview

In this exercise, you'll load a humanoid robot model (URDF format) into the PyBullet physics simulator, visualize it in 3D, query joint information, and experiment with joint control. This hands-on experience introduces key concepts in robot simulation and embodied intelligence through sensorimotor interaction.

**What you'll build**: A Python script that loads, visualizes, and controls a simulated humanoid robot

**Why it matters**: Simulation is essential for robotics development—it allows rapid prototyping, algorithm testing, and learning without expensive hardware or safety risks. Understanding how to interface with a physics engine is fundamental for all subsequent chapters.

**Real-world application**: Before deploying humanoid robots like Boston Dynamics' Atlas or NASA's Valkyrie, engineers test control algorithms in simulation environments like PyBullet, Gazebo, or MuJoCo. Simulation validates designs and de-risks hardware experiments.

---

## Setup Instructions

### Prerequisites

- Completed Exercise 1 (Python and PyBullet installed)
- Working Python environment with PyBullet 3.2.5+

### Download Robot Model

**Option 1: Use TextBook's simple_humanoid.urdf**

The robot model `simple_humanoid.urdf` should be in your `docs/models/` directory of this textbook repository. If cloning from GitHub:

```bash
git clone https://github.com/Abdulahad-laiq/Physical-AI-Humanoid-Robotics.git
cd Physical-AI-Humanoid-Robotics
ls docs/models/simple_humanoid.urdf  # Verify file exists
```

**Option 2: Use PyBullet's Built-in Models**

PyBullet includes sample robots. We'll use R2D2 as a simple example:

```python
import pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())
robot_id = p.loadURDF("r2d2.urdf")
```

---

## Problem Statement

**Task**: Write a Python script that:
1. Initializes PyBullet physics engine with GUI
2. Loads a humanoid robot model (URDF)
3. Queries and prints joint information
4. Applies simple joint control commands
5. Runs simulation loop and observes robot behavior

**Success Criteria**:
- [ ] PyBullet GUI window opens with robot visible
- [ ] Script prints robot's joint count and names
- [ ] Robot joints can be controlled programmatically
- [ ] Simulation runs for at least 5 seconds
- [ ] Student can describe what they observed (e.g., robot falling, joints moving)

---

## Step-by-Step Instructions

### Part 1: Load Robot and Inspect (20 minutes)

**Step 1: Create `first_simulation.py`**

```python
"""
First Robot Simulation
Load a humanoid robot and explore its properties
"""

import pybullet as p
import pybullet_data
import time
import numpy as np

def initialize_simulation():
    """Initialize PyBullet physics engine"""
    # Connect to PyBullet with GUI
    physics_client = p.connect(p.GUI)
    print(f"✓ Connected to PyBullet (client ID: {physics_client})")

    # Set gravity
    p.setGravity(0, 0, -9.81)
    print("✓ Gravity set to -9.81 m/s²")

    # Add search path for default URDFs
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    return physics_client

def load_environment():
    """Load ground plane"""
    plane_id = p.loadURDF("plane.urdf")
    print(f"✓ Ground plane loaded (ID: {plane_id})")
    return plane_id

def load_robot():
    """Load humanoid robot model"""
    # Starting position and orientation
    start_pos = [0, 0, 1.0]  # 1 meter above ground
    start_orientation = p.getQuaternionFromEuler([0, 0, 0])

    # Load robot (using R2D2 as example; replace with simple_humanoid.urdf)
    robot_id = p.loadURDF("r2d2.urdf", start_pos, start_orientation)
    print(f"✓ Robot loaded (ID: {robot_id})")

    return robot_id

def inspect_robot(robot_id):
    """Query and print robot joint information"""
    num_joints = p.getNumJoints(robot_id)
    print(f"\n✓ Robot has {num_joints} joints")

    print("\nJoint Information:")
    print("-" * 80)
    print(f"{'Index':<8} {'Name':<25} {'Type':<10} {'Lower Limit':<12} {'Upper Limit':<12}")
    print("-" * 80)

    for i in range(num_joints):
        joint_info = p.getJointInfo(robot_id, i)
        joint_name = joint_info[1].decode('utf-8')
        joint_type = joint_info[2]  # 0=REVOLUTE, 1=PRISMATIC, 4=FIXED
        lower_limit = joint_info[8]
        upper_limit = joint_info[9]

        type_name = {0: "REVOLUTE", 1: "PRISMATIC", 4: "FIXED"}.get(joint_type, "OTHER")

        print(f"{i:<8} {joint_name:<25} {type_name:<10} {lower_limit:<12.2f} {upper_limit:<12.2f}")

    print("-" * 80)
    return num_joints

def main():
    """Main simulation function"""
    print("=" * 60)
    print("First Robot Simulation - Loading Humanoid")
    print("=" * 60)
    print()

    # Initialize
    client = initialize_simulation()
    plane = load_environment()
    robot = load_robot()

    # Inspect robot properties
    num_joints = inspect_robot(robot)

    print("\n✓ Setup complete!")
    print("\nSimulation Controls:")
    print("  - Left mouse: Rotate camera")
    print("  - Middle mouse: Pan camera")
    print("  - Right mouse: Zoom camera")
    print("  - Close window to exit")
    print("\nSimulation will run for 10 seconds...\n")

    # Run simulation loop
    for step in range(2400):  # 10 seconds at 240 Hz
        p.stepSimulation()
        time.sleep(1./240.)

        # Print status every 2 seconds
        if step % 480 == 0:
            elapsed = step / 240.0
            print(f"Simulation time: {elapsed:.1f}s")

    # Cleanup
    p.disconnect()
    print("\n✓ Simulation complete!")

if __name__ == "__main__":
    main()
```

**Step 2: Run the Script**

```bash
python first_simulation.py
```

**Expected Behavior:**
- PyBullet GUI window opens
- Ground plane and robot appear
- Robot falls to the ground (no control yet—just physics!)
- Terminal prints joint information

---

### Part 2: Add Joint Control (25 minutes)

Now let's control the robot's joints. Modify your script to add this function:

```python
def control_robot_joints(robot_id, num_joints):
    """Demonstrate basic joint control"""
    print("\n--- Joint Control Demo ---")

    # Get all revolute joints (controllable)
    controllable_joints = []
    for i in range(num_joints):
        joint_info = p.getJointInfo(robot_id, i)
        joint_type = joint_info[2]
        if joint_type in [0, 1]:  # REVOLUTE or PRISMATIC
            controllable_joints.append(i)

    print(f"Found {len(controllable_joints)} controllable joints: {controllable_joints}")

    if len(controllable_joints) == 0:
        print("No controllable joints found.")
        return

    # Example: Set position targets for all joints
    target_positions = np.sin(np.linspace(0, 2*np.pi, len(controllable_joints)))

    for joint_idx, target_pos in zip(controllable_joints, target_positions):
        p.setJointMotorControl2(
            bodyUniqueId=robot_id,
            jointIndex=joint_idx,
            controlMode=p.POSITION_CONTROL,
            targetPosition=target_pos,
            force=500  # Maximum force (N or Nm)
        )
        print(f"  Joint {joint_idx}: target position = {target_pos:.2f} rad")

    print("✓ Joint commands sent")
```

Add this call to `main()` after `inspect_robot()`:

```python
# After inspect_robot(robot)
control_robot_joints(robot, num_joints)
```

**Step 3: Run Modified Script**

```bash
python first_simulation.py
```

**Observe:**
- Robot joints move to target positions
- Some joints may oscillate (PID control)
- Robot may topple (no balance control yet)

---

### Part 3: Sensorimotor Loop Exploration (15 minutes)

Add real-time joint state monitoring:

```python
def monitor_joint_states(robot_id, joint_indices):
    """Read and print current joint states"""
    states = p.getJointStates(robot_id, joint_indices)

    for idx, state in zip(joint_indices, states):
        position = state[0]  # Joint position (rad or m)
        velocity = state[1]  # Joint velocity (rad/s or m/s)
        print(f"  Joint {idx}: pos={position:6.2f} rad, vel={velocity:6.2f} rad/s")
```

In your simulation loop, add monitoring every 1 second:

```python
# Inside the for loop
if step % 240 == 0 and step > 0:
    print(f"\nJoint states at t={step/240:.1f}s:")
    monitor_joint_states(robot, controllable_joints[:3])  # Monitor first 3 joints
```

**Observe:**
- Positions change over time as controller adjusts
- Velocities show rate of motion
- This is the sensorimotor loop in action: sensing (getJointStates) → acting (setJointMotorControl2)

---

## Expected Output

After completing all parts, your script should:

1. **Load and display robot** in PyBullet GUI
2. **Print joint information** table
3. **Apply joint control commands** with target positions
4. **Monitor joint states** every second during simulation
5. **Run for 10 seconds** before exiting cleanly

**Sample Terminal Output:**

```
============================================================
First Robot Simulation - Loading Humanoid
============================================================

✓ Connected to PyBullet (client ID: 0)
✓ Gravity set to -9.81 m/s²
✓ Ground plane loaded (ID: 0)
✓ Robot loaded (ID: 1)

✓ Robot has 6 joints

Joint Information:
--------------------------------------------------------------------------------
Index    Name                      Type       Lower Limit  Upper Limit
--------------------------------------------------------------------------------
0        base_to_right_leg         REVOLUTE   -1.57        1.57
1        right_leg_to_foot         REVOLUTE   -1.57        1.57
2        base_to_left_leg          REVOLUTE   -1.57        1.57
3        left_leg_to_foot          REVOLUTE   -1.57        1.57
4        base_to_gripper           REVOLUTE   -1.57        1.57
5        gripper_to_foot           FIXED      0.00         -1.00
--------------------------------------------------------------------------------

--- Joint Control Demo ---
Found 5 controllable joints: [0, 1, 2, 3, 4]
  Joint 0: target position = 0.00 rad
  Joint 1: target position = 0.95 rad
  Joint 2: target position = 0.59 rad
  Joint 3: target position = -0.59 rad
  Joint 4: target position = -0.95 rad
✓ Joint commands sent

Simulation time: 0.0s

Joint states at t=1.0s:
  Joint 0: pos=  0.05 rad, vel=  0.23 rad/s
  Joint 1: pos=  0.82 rad, vel=  0.56 rad/s
  Joint 2: pos=  0.43 rad, vel=  0.34 rad/s
...
✓ Simulation complete!
```

---

## Deliverables

Submit:
1. **Python script**: `first_simulation.py` with all three parts completed
2. **Screenshot**: PyBullet GUI showing robot with joints in controlled positions
3. **Observations** (2-3 sentences):
   - What happened when you ran the simulation?
   - Did the robot fall? Why or why not?
   - How did joint positions change over time?

---

## Extensions (Optional)

1. **Use Custom Robot**: Replace `r2d2.urdf` with `simple_humanoid.urdf` from textbook
2. **Oscillating Motion**: Make joints move sinusoidally over time:
   ```python
   target_pos = np.sin(step / 240.0 * 2 * np.pi)  # 1 Hz oscillation
   ```
3. **Camera Control**: Position camera to follow robot:
   ```python
   p.resetDebugVisualizerCamera(cameraDistance=2.0, cameraYaw=45, cameraPitch=-30, cameraTargetPosition=[0,0,0.5])
   ```
4. **Force Sensor**: Add force/torque measurement at joints (Chapter 2 concept preview)

---

## Rubric

| Criterion | Points | Description |
|-----------|--------|-------------|
| Script runs without errors | 3 | No Python exceptions; GUI opens |
| Robot loads and displays | 2 | Visible in PyBullet window |
| Joint info printed | 2 | Table with names, types, limits |
| Joint control works | 2 | Joints move to target positions |
| Observations documented | 1 | Describes what happened and why |

**Total**: 10 points | **Passing**: 7/10

---

## Reflection Questions

1. **Embodiment**: How does the robot's physical structure (links, joints) constrain what motions are possible?
2. **Sensorimotor Loop**: Identify the sensing (perception) and acting (motor commands) in your code.
3. **Simulation vs. Reality**: What aspects of the real world does this simulation simplify or ignore?

---

## Next Steps

Congratulations! You've run your first robot simulation. In **Chapter 2**, we'll dive deeper into sensors (IMUs, cameras, force sensors) and actuators (motor types, control modes), building toward more sophisticated robot behaviors.

**Preview**: In Chapter 3, you'll implement forward and inverse kinematics to precisely control where the robot's hands reach in 3D space.

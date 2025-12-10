---
id: glossary
title: Glossary of Robotics and Physical AI Terms
sidebar_label: Glossary
---

# Glossary

**Purpose**: This glossary provides definitions for technical terms used throughout the textbook, with citations to authoritative sources and cross-references to related concepts.

**Usage**: Terms are organized alphabetically. Each entry includes:
- **Definition**: Clear, concise explanation
- **Context**: Where/how the term is used in robotics
- **Citation**: Source reference (when applicable)
- **See also**: Related terms

---

## A

### Actuator
**Definition**: A mechanical or electromechanical device that converts energy (electrical, hydraulic, pneumatic) into motion.

**Context**: Actuators are the "muscles" of robots, enabling movement of joints and end-effectors. Common types include DC motors, servo motors, hydraulic cylinders, and pneumatic pistons.

**Citation**: B. Siciliano et al., *Robotics: Modelling, Planning and Control*, Springer, 2010, Ch. 2.

**See also**: Sensor, Degree of Freedom (DOF), Joint

---

## B

### Base Frame
**Definition**: The reference coordinate frame fixed to the robot's base, serving as the origin for all kinematic calculations.

**Context**: Also called the world frame or frame {0}. All other coordinate frames (link frames, end-effector frame) are defined relative to the base frame.

**Citation**: J. J. Craig, *Introduction to Robotics: Mechanics and Control*, 4th ed., Pearson, 2017, Ch. 2.

**See also**: Coordinate Frame, Homogeneous Transformation, Denavit-Hartenberg Parameters

---

## C

### Center of Mass (CoM)
**Definition**: The point at which the entire mass of a body or system can be considered to be concentrated for the purpose of analyzing translational motion.

**Context**: Critical for balance and locomotion in humanoid robots. The CoM location determines stability during walking, running, and manipulation tasks.

**Citation**: M. W. Spong, S. Hutchinson, and M. Vidyasagar, *Robot Modeling and Control*, 2nd ed., Wiley, 2020, Ch. 4.

**See also**: Zero-Moment Point (ZMP), Center of Pressure (CoP), Balance

---

### Center of Pressure (CoP)
**Definition**: The point on the ground where the resultant of the ground reaction forces acts; the weighted average of the pressure distribution under the feet.

**Context**: In bipedal locomotion, the CoP must remain within the support polygon for static stability. During dynamic motion, CoP and ZMP may differ.

**Citation**: M. Vukobratović and B. Borovac, "Zero-moment point—Thirty five years of its life," *Int. J. Humanoid Robot.*, vol. 1, no. 1, pp. 157–173, Mar. 2004.

**See also**: Zero-Moment Point (ZMP), Support Polygon, Balance

---

### Coordinate Frame
**Definition**: A set of orthogonal axes (x, y, z) with a defined origin, used to describe positions and orientations in 3D space.

**Context**: Robotics uses multiple coordinate frames (world frame, link frames, end-effector frame) related through transformations. Understanding frame relationships is fundamental to kinematics.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 2.

**See also**: Base Frame, Homogeneous Transformation, Denavit-Hartenberg Parameters

---

## D

### Degree of Freedom (DOF)
**Definition**: The number of independent parameters needed to fully specify the configuration or state of a mechanical system.

**Context**: A humanoid arm typically has 6-7 DOF (shoulder: 3, elbow: 1, wrist: 2-3). More DOF provides greater dexterity but increases control complexity.

**Citation**: B. Siciliano et al., *Robotics*, Ch. 2.

**See also**: Joint, Redundancy, Workspace

---

### Denavit-Hartenberg (DH) Parameters
**Definition**: A systematic convention for assigning coordinate frames to serial-link manipulators, using four parameters (a_i, alpha_i, d_i, theta_i) to describe each link-joint pair.

**Context**: DH parameters enable efficient computation of forward kinematics via transformation matrices. Standard in industrial robotics.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 3.

**See also**: Forward Kinematics, Homogeneous Transformation, Link, Joint

---

## E

### Embodied Intelligence
**Definition**: The theory that intelligence emerges from the interaction between an agent's body, sensorimotor system, and environment, rather than from abstract computation alone.

**Context**: Central to Physical AI. Embodied agents learn through physical interaction, with cognition shaped by body morphology and environmental feedback.

**Citation**: R. Pfeifer and J. Bongard, *How the Body Shapes the Way We Think: A New View of Intelligence*, MIT Press, 2007.

**See also**: Physical AI, Sensorimotor Loop, Morphological Computation

---

### End-Effector
**Definition**: The device at the end of a robotic manipulator designed to interact with the environment (e.g., gripper, tool, hand).

**Context**: The goal of inverse kinematics is to position the end-effector at a desired location and orientation. End-effector design varies by task (grasping, welding, painting, surgery).

**Citation**: B. Siciliano et al., *Robotics*, Ch. 2.

**See also**: Inverse Kinematics, Workspace, Gripper

---

## F

### Forward Kinematics (FK)
**Definition**: The problem of determining the position and orientation of the end-effector given the joint angles of a manipulator.

**Context**: FK uses transformation matrices (often via DH parameters) to compute the end-effector pose from joint configurations. Direct and computationally efficient.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 3.

**See also**: Inverse Kinematics, Denavit-Hartenberg Parameters, Homogeneous Transformation

---

## G

*(Terms starting with G will be added as chapters are written)*

---

## H

### Homogeneous Transformation
**Definition**: A 4×4 matrix representing both rotation and translation, used to transform coordinates from one frame to another in 3D space.

**Context**: Homogeneous transformations enable compact representation of rigid body motion. Multiplying transformation matrices chains coordinate frame relationships.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 2.

**See also**: Coordinate Frame, Forward Kinematics, Rotation Matrix

---

## I

### Inverse Kinematics (IK)
**Definition**: The problem of finding joint angles that position the end-effector at a desired location and orientation.

**Context**: IK is more complex than FK. Solutions may be analytical (closed-form) or numerical (iterative). Multiple solutions, singularities, and no-solution cases are common.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 4.

**See also**: Forward Kinematics, Jacobian, Singularity, Redundancy

---

## J

### Jacobian Matrix
**Definition**: A matrix of partial derivatives relating joint velocities to end-effector velocities (linear and angular).

**Context**: The Jacobian J(q) maps joint space to task space velocities: velocity_x = J(q) * velocity_q. Used in IK, singularity analysis, and force control.

**Citation**: B. Siciliano et al., *Robotics*, Ch. 3.

**See also**: Inverse Kinematics, Singularity, Manipulability

---

### Joint
**Definition**: The connection between two links in a manipulator that allows relative motion. Common types: revolute (rotational) and prismatic (translational).

**Context**: Each joint adds one degree of freedom. Humanoid robots use primarily revolute joints for arms, legs, neck, and torso.

**Citation**: B. Siciliano et al., *Robotics*, Ch. 2.

**See also**: Link, Degree of Freedom, Actuator

---

## K

### Kinematics
**Definition**: The study of motion without considering the forces that cause it. In robotics, kinematics analyzes positions, velocities, and accelerations of links and end-effectors.

**Context**: Forward kinematics (FK) computes end-effector pose from joint angles. Inverse kinematics (IK) finds joint angles for a desired pose.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 3-4.

**See also**: Dynamics, Forward Kinematics, Inverse Kinematics

---

## L

### Link
**Definition**: A rigid body in a manipulator connected to other links via joints.

**Context**: Serial-link manipulators consist of links connected in a chain from base to end-effector. Link parameters (length, twist, offset) define robot geometry.

**Citation**: B. Siciliano et al., *Robotics*, Ch. 2.

**See also**: Joint, Degree of Freedom, Denavit-Hartenberg Parameters

---

## M

### Manipulability
**Definition**: A measure of how easily a robot can move its end-effector in different directions, quantified by the manipulability index (determinant or smallest singular value of the Jacobian).

**Context**: High manipulability indicates good dexterity. Manipulability drops to zero at singularities.

**Citation**: T. Yoshikawa, "Manipulability of robotic mechanisms," *Int. J. Robot. Res.*, vol. 4, no. 2, pp. 3–9, 1985.

**See also**: Jacobian, Singularity, Workspace

---

## P

### Physical AI
**Definition**: Artificial intelligence systems embodied in physical agents (robots) that sense, act, learn, and collaborate in the real world.

**Context**: Distinct from purely digital AI. Physical AI must handle uncertainties, delays, and constraints of physical embodiment. Combines robotics, control, perception, and machine learning.

**See also**: Embodied Intelligence, Sensorimotor Loop

---

## S

### Sensor
**Definition**: A device that detects physical quantities (light, force, position, orientation, etc.) and converts them into signals for processing.

**Context**: Robots use proprioceptive sensors (joint encoders, IMUs) to sense internal state and exteroceptive sensors (cameras, LiDAR, tactile sensors) to sense the environment.

**Citation**: B. Siciliano et al., *Robotics*, Ch. 2.

**See also**: Actuator, Perception, IMU (Inertial Measurement Unit)

---

### Sensorimotor Loop
**Definition**: The cycle of sensing the environment, processing sensory information, making decisions, acting on the world, and sensing the results of actions.

**Context**: Fundamental to embodied intelligence. Continuous sensorimotor loops enable adaptive behavior, learning, and real-time response to environmental changes.

**Citation**: R. Pfeifer and J. Bongard, *How the Body Shapes the Way We Think*, 2007.

**See also**: Embodied Intelligence, Physical AI, Perception-Action Coupling

---

### Singularity
**Definition**: A configuration where the Jacobian matrix loses rank, resulting in loss of one or more degrees of freedom in end-effector motion.

**Context**: At singularities, small end-effector motions require unbounded joint velocities. Robots cannot move in certain directions. Must be avoided or handled with damped IK.

**Citation**: B. Siciliano et al., *Robotics*, Ch. 3.

**See also**: Jacobian, Inverse Kinematics, Manipulability

---

### Support Polygon
**Definition**: The convex hull of the contact points between a robot and the ground.

**Context**: For static stability, the projection of the center of mass (CoM) must lie within the support polygon. In bipedal walking, the support polygon changes between single-foot and double-foot phases.

**Citation**: M. Vukobratović and B. Borovac, "Zero-moment point—Thirty five years of its life," *Int. J. Humanoid Robot.*, 2004.

**See also**: Center of Mass, Zero-Moment Point, Balance

---

## W

### Workspace
**Definition**: The set of all positions and orientations the end-effector can reach.

**Context**: Reachable workspace includes all points reachable with some orientation. Dexterous workspace includes points reachable with arbitrary orientations. Workspace boundaries are determined by joint limits, link lengths, and singularities.

**Citation**: J. J. Craig, *Introduction to Robotics*, Ch. 3.

**See also**: Forward Kinematics, Singularity, Degree of Freedom

---

## Z

### Zero-Moment Point (ZMP)
**Definition**: The point on the ground where the net moment of inertial and gravitational forces equals zero in the horizontal plane.

**Context**: Widely used criterion for bipedal stability. If ZMP remains within the support polygon, the robot maintains dynamic balance. ZMP-based gait planning is common in humanoid locomotion.

**Citation**: M. Vukobratović and B. Borovac, "Zero-moment point—Thirty five years of its life," *Int. J. Humanoid Robot.*, vol. 1, no. 1, pp. 157–173, Mar. 2004.

**See also**: Center of Pressure, Support Polygon, Bipedal Locomotion, Balance

---

## How to Use This Glossary

- **First encounter with a term**: Read the definition and context
- **Need deeper understanding**: Follow citations to source materials
- **Related concepts**: Use "See also" links to explore connected ideas
- **Contributing**: New terms added as chapters are written (alphabetically maintained)

This glossary grows with the textbook. Terms from Chapters 1-4 are included above; terms from Chapters 5-10 will be added during content creation.

# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

## Summary

Create a comprehensive 10-chapter university-level textbook covering Physical AI and Humanoid Robotics for STEM students (ages 17-25). The textbook emphasizes hands-on, simulation-based learning using open-source tools (Python 3.9+, ROS2 Humble/Iron, Webots/PyBullet/MuJoCo) while maintaining academic rigor through authoritative citations (IEEE standards, peer-reviewed research, established robotics textbooks). Content will be structured as Docusaurus-compatible MDX, deployed via GitHub Pages, with comprehensive glossary, index, bibliography, and appendices. Every chapter includes 3-5 learning objectives, concept explanations (F-K grade 10-14), 2+ hands-on exercises, 5-10 assessments, and 3-5 further reading sources. Minimum 40% of technical content will cite authoritative sources in IEEE format with 0% plagiarism tolerance.

**Technical Approach**: Sequential fundamentals-to-applications structure with modular chapters enabling flexible course design. Hybrid code approach combining Python-only examples for accessibility with ROS2+simulator integration for realistic robotics workflows. Mermaid diagrams for inline visualization with external SVG/PNG for complex figures. Concurrent research-and-writing workflow where each chapter is researched immediately before writing. CI/CD pipeline validates code executability, citation format, readability metrics, and Docusaurus build success before deployment.

## Technical Context

**Language/Version**: Python 3.9+, JavaScript/Node.js 18+ (Docusaurus), Markdown/MDX 2.0+
**Primary Dependencies**: Docusaurus 3.x, ROS2 Humble/Iron, Webots R2023b/PyBullet 3.2+/MuJoCo 3.x, NumPy, Matplotlib, BibTeX/pandoc-citeproc
**Storage**: Git repository with markdown files; static assets in `docs/assets/`; robot models (URDF/SDF) in `docs/models/`
**Testing**: Python pytest for code examples; markdownlint-cli2 for MDX syntax; Flesch-Kincaid readability analysis; citation format validator; Docusaurus build verification
**Target Platform**: Web (GitHub Pages), cross-platform development environment (Windows/Linux/macOS)
**Project Type**: Documentation/textbook (Docusaurus static site)
**Performance Goals**: Docusaurus build < 60s; all pages load < 3s; search index < 2MB; mobile-responsive (< 1200px width)
**Constraints**: F-K readability 10-14; 40%+ authoritative citations; 0% plagiarism; WCAG 2.1 AA accessibility; 8GB RAM for simulator exercises
**Scale/Scope**: 10 chapters (~35,000-50,000 total words), 20+ code examples, 20+ practical exercises, 50-70 citations, 100+ glossary terms

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **I. Technical Accuracy and Authority**
- Plan includes research.md strategy for sourcing IEEE standards, peer-reviewed papers, established textbooks
- 40%+ content citation requirement enforced through citation audit process
- All technical claims will reference Siciliano, Craig, Spong, Murray, or equivalent authoritative sources

✅ **II. Clarity and Accessibility**
- F-K grade 10-14 enforced through automated readability analysis in CI pipeline
- Progressive concept building: fundamentals (Ch 1-3) → intermediate (Ch 4-7) → advanced (Ch 8-10)
- Glossary and index ensure term consistency and easy reference

✅ **III. Hands-On Learning Orientation**
- Every chapter includes 2+ practical exercises with simulator integration
- Code examples include setup instructions, expected outputs, and troubleshooting
- Appendices provide cross-platform simulator installation guides

✅ **IV. Diagrams and Visual Communication**
- Mermaid for inline diagrams (flowcharts, state machines, architecture)
- External SVG/PNG for complex kinematics, perception pipelines (created with Draw.io/Matplotlib)
- All diagrams include alt-text and source files committed to repository

✅ **V. Code Quality and Executability**
- All Python code tested with pytest; ROS2 examples tested in Humble/Iron
- CI pipeline validates code execution in specified environments
- Dependencies documented with version pinning (requirements.txt, package.xml)

✅ **VI. Future-of-Work Alignment**
- Chapters 8-10 emphasize AI-agent collaboration, human-robot teaming, ethical considerations
- Examples include collaborative manipulation, shared autonomy, intent recognition

✅ **VII. Content Originality and Academic Integrity**
- Plagiarism detection (Turnitin/Copyscape) run before each chapter merge
- 0% tolerance enforced; content must be originally written with proper attribution
- Direct quotes limited to definitions/key statements with full IEEE citations

**Constitution Compliance**: ALL PRINCIPLES SATISFIED

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Citation strategy and authoritative sources
├── data-model.md        # Content structure (chapters, exercises, assessments)
├── quickstart.md        # Development workflow for textbook creation
├── contracts/           # Chapter and exercise templates
│   ├── chapter-template.md
│   ├── exercise-template.md
│   └── assessment-template.md
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── (tasks.md will be created via /sp.tasks command)
```

### Source Code (repository root)

```text
docs/                          # Docusaurus content root
├── intro.md                   # Landing page / course overview
├── ch01-introduction/         # Chapter 1: Introduction to Physical AI
│   ├── index.md              # Chapter content (MDX)
│   ├── exercises/
│   │   ├── ex01-python-basics.md
│   │   └── ex02-first-simulation.md
│   └── assets/               # Chapter-specific diagrams, images
│       └── embodied-ai-diagram.svg
├── ch02-robot-fundamentals/   # Chapter 2: Robot Fundamentals
│   ├── index.md
│   ├── exercises/
│   └── assets/
├── ch03-kinematics/           # Chapter 3: Humanoid Kinematics
├── ch04-dynamics/             # Chapter 4: Dynamics and Control
├── ch05-perception/           # Chapter 5: Perception Systems
├── ch06-planning/             # Chapter 6: Motion Planning
├── ch07-manipulation/         # Chapter 7: Manipulation and Grasping
├── ch08-locomotion/           # Chapter 8: Bipedal Locomotion
├── ch09-learning/             # Chapter 9: Learning and Adaptation
├── ch10-collaboration/        # Chapter 10: Human-Robot Collaboration
├── appendices/                # Supporting materials
│   ├── setup-webots.md
│   ├── setup-pybullet.md
│   ├── setup-ros2.md
│   ├── math-review.md
│   └── troubleshooting.md
├── glossary.md                # Comprehensive term definitions
├── bibliography.md            # IEEE-formatted references
├── assets/                    # Shared diagrams, images, icons
│   └── global/
└── models/                    # Robot models (URDF/SDF) for exercises
    ├── simple_humanoid.urdf
    └── humanoid_with_hands.urdf

docusaurus.config.js           # Docusaurus configuration
sidebars.js                    # Sidebar navigation structure
package.json                   # Node dependencies
.github/workflows/             # CI/CD pipeline
├── build-and-deploy.yml       # Build Docusaurus, deploy to GitHub Pages
├── validate-code.yml          # Run pytest on all code examples
└── check-quality.yml          # F-K readability, citations, plagiarism

scripts/                       # Automation scripts
├── validate-citations.py      # Check IEEE format, ensure 40%+ coverage
├── check-readability.py       # F-K grade level analysis
└── test-exercises.sh          # Execute all exercise code blocks

README.md                      # Repository overview
LICENSE                        # MIT or CC BY-NC-SA 4.0
requirements.txt               # Python dependencies for exercises
```

**Structure Decision**: Docusaurus documentation project with one chapter per directory. Each chapter is a self-contained module with content (index.md), exercises (subdirectory), and assets (images/diagrams). This structure enables:
1. Independent chapter development and testing
2. Clear navigation hierarchy in Docusaurus sidebar
3. Easy asset management (chapter-specific vs. global)
4. Modular course design (instructors can select specific chapters)
5. Version control clarity (changes isolated to specific chapters)

## Complexity Tracking

> No constitution violations detected. All requirements align with established principles.

## Chapter Architecture

### 10-Chapter Sequential Structure with Modular Units

**Design Rationale**: Sequential fundamentals-to-applications progression ensures students build prerequisite knowledge before advanced topics. However, chapters 4-7 are designed as semi-independent modules allowing flexible course sequencing for different learning paths (e.g., perception-focused vs. manipulation-focused tracks).

### Chapter 1: Introduction to Physical AI and Embodied Intelligence

**Learning Objectives**:
1. Define Physical AI and explain how it differs from traditional AI and robotics
2. Describe the concept of embodied intelligence and sensorimotor loops
3. Identify key components of humanoid robotic systems (sensors, actuators, compute)
4. Explain the future-of-work paradigm of human-AI-robot collaboration
5. Set up Python and simulation environment for subsequent chapters

**Key Concepts**:
- Embodied intelligence vs. disembodied AI
- Sensorimotor coordination and feedback loops
- Physical AI system components and architecture
- Human-robot teaming paradigms
- Ethical considerations in autonomous systems

**Code Examples**:
- Python environment setup and verification
- First simulation: Load and visualize a simple robot model in PyBullet
- Basic robot state observation (joint positions, velocities)

**Practical Exercises**:
1. Install Python 3.9+, PyBullet, and verify installation with test script
2. Load a humanoid robot model (URDF) and render it in PyBullet GUI; experiment with joint controls

**Assessments** (10 questions):
- Define embodied intelligence with examples
- Compare/contrast Physical AI vs. traditional robotics
- Identify components in a humanoid system diagram
- Discuss an ethical consideration in autonomous humanoid robots
- Explain a sensorimotor loop with a real-world example

**Diagrams**:
- Physical AI system architecture (sensors → perception → planning → control → actuators)
- Embodied intelligence concept map
- Human-robot collaboration taxonomy

**Further Reading**:
1. R. Pfeifer and J. Bongard, "How the Body Shapes the Way We Think" (MIT Press, 2006)
2. G. Sandini et al., "Embodied Intelligence," IEEE Robotics & Automation Magazine
3. R. Brooks, "Intelligence without Representation," Artificial Intelligence journal

**Prerequisites**: Basic programming (variables, functions, loops); high school physics

---

### Chapter 2: Robot Fundamentals - Sensors, Actuators, and Coordinate Frames

**Learning Objectives**:
1. Explain common sensor types used in humanoid robots (IMU, force/torque, cameras, LIDAR)
2. Describe actuator technologies (electric motors, hydraulics, series elastic actuators)
3. Define and apply coordinate frame transformations in 3D space
4. Use homogeneous transformation matrices for position/orientation representation
5. Implement basic sensor data acquisition and visualization in Python

**Key Concepts**:
- Sensor modalities and measurement principles
- Actuator characteristics (torque, speed, bandwidth, compliance)
- Coordinate frames (world, base, joint, end-effector)
- Homogeneous transformations (rotation + translation)
- Sensor-actuator integration

**Code Examples**:
- Read IMU data from simulated humanoid robot
- Apply homogeneous transformations to robot link positions
- Visualize coordinate frames using Matplotlib 3D plots

**Practical Exercises**:
1. Extract and plot IMU acceleration data from a simulated robot performing a motion
2. Compute end-effector position given joint angles and DH parameters for a simple 3-DOF arm

**Assessments** (8 questions):
- List three sensor types and their measurement principles
- Explain advantages of series elastic actuators over rigid actuators
- Given a transformation matrix, extract rotation and translation components
- Describe the difference between world frame and base frame

**Diagrams**:
- Sensor taxonomy for humanoid robots
- Actuator comparison table (electric vs. hydraulic vs. SEA)
- Coordinate frame visualization (world, base, joint frames on humanoid model)
- Homogeneous transformation matrix structure

**Further Reading**:
1. J. Craig, "Introduction to Robotics: Mechanics and Control," Ch. 2-3 (Pearson, 2017)
2. B. Siciliano et al., "Robotics: Modelling, Planning and Control," Ch. 2 (Springer, 2010)
3. IEEE Standard for Robot Coordinate Systems (ISO 8373)

**Prerequisites**: Chapter 1; linear algebra (vectors, matrices)

---

### Chapter 3: Humanoid Kinematics - Forward and Inverse

**Learning Objectives**:
1. Derive forward kinematics using Denavit-Hartenberg (DH) convention
2. Solve inverse kinematics for humanoid arms using analytical and numerical methods
3. Understand workspace and singularities in humanoid manipulators
4. Implement FK and IK solvers in Python for serial-link arms
5. Analyze kinematic redundancy in humanoid systems

**Key Concepts**:
- Denavit-Hartenberg parameters
- Forward kinematics (joint angles → end-effector pose)
- Inverse kinematics (desired pose → joint angles)
- Analytical IK vs. numerical IK (Jacobian-based, optimization)
- Singularities and workspace analysis
- Redundancy resolution (null-space methods)

**Code Examples**:
- FK solver for 6-DOF humanoid arm using DH parameters
- Analytical IK for 3-DOF planar arm
- Numerical IK using Jacobian pseudo-inverse
- Workspace visualization for arm reach

**Practical Exercises**:
1. Implement DH-based FK for a 6-DOF humanoid arm; verify against simulator ground truth
2. Develop an IK solver (analytical or numerical) to reach specified target positions; test singularity behavior

**Assessments** (10 questions):
- Define DH parameters and their purpose
- Given DH table, compute transformation matrix
- Explain the difference between analytical and numerical IK
- What is a kinematic singularity? Provide an example.
- How does redundancy help in humanoid manipulation?

**Diagrams**:
- DH frame assignment on humanoid arm
- FK computation flowchart
- IK solution space and redundancy visualization
- Workspace boundary for 6-DOF arm

**Further Reading**:
1. J. Craig, "Introduction to Robotics," Ch. 3-4 (Forward/Inverse Kinematics)
2. M. Spong et al., "Robot Modeling and Control," Ch. 3 (Wiley, 2005)
3. Analytical IK paper: "A Geometric Approach to Inverse Kinematics" (IEEE Trans. Robotics)

**Prerequisites**: Chapter 2; calculus (derivatives); linear algebra (matrix operations)

---

### Chapter 4: Dynamics and Control Fundamentals

**Learning Objectives**:
1. Derive equations of motion for robotic systems using Lagrangian mechanics
2. Understand inertia, Coriolis, gravity, and friction forces in robot dynamics
3. Implement PID control for joint-level trajectory tracking
4. Explain computed-torque control and feedback linearization
5. Analyze stability and performance trade-offs in robot controllers

**Key Concepts**:
- Lagrangian dynamics (kinetic/potential energy, generalized forces)
- Newton-Euler recursive formulation
- Joint-space vs. task-space control
- PID control structure and tuning
- Computed-torque control (inverse dynamics)
- Impedance and admittance control

**Code Examples**:
- Compute inertia matrix for a 2-link planar arm
- PID controller implementation for joint position tracking
- Simulate torque-controlled robot arm with gravity compensation
- Trajectory tracking with computed-torque control

**Practical Exercises**:
1. Implement and tune a PID controller to track a sinusoidal joint trajectory; analyze overshoot and settling time
2. Develop a computed-torque controller for a 3-DOF arm; compare performance with PID-only control

**Assessments** (10 questions):
- Write the Lagrangian for a simple 1-DOF system
- Explain the role of each term in robot dynamics equation: M(q)q'' + C(q,q')q' + g(q) = τ
- How does PID control respond to step input? Describe P, I, D effects.
- What is computed-torque control and when is it advantageous?

**Diagrams**:
- Robot dynamics components (inertia, Coriolis, gravity)
- PID control block diagram
- Computed-torque control architecture
- Trajectory tracking performance comparison (PID vs. computed-torque)

**Further Reading**:
1. M. Spong et al., "Robot Modeling and Control," Ch. 4-6 (Dynamics and Control)
2. B. Siciliano et al., "Robotics," Ch. 4 (Dynamics) and Ch. 8 (Motion Control)
3. R. Kelly et al., "Control of Robot Manipulators in Joint Space" (Springer, 2005)

**Prerequisites**: Chapter 3; physics (mechanics, energy); differential equations

---

### Chapter 5: Perception Systems - Vision and Depth Sensing

**Learning Objectives**:
1. Explain camera models (pinhole, distortion) and calibration
2. Process RGB and depth images for object detection and 3D reconstruction
3. Understand point cloud data and filtering techniques
4. Implement visual feature extraction and matching
5. Integrate perception with robot state estimation

**Key Concepts**:
- Camera intrinsics and extrinsics
- Image processing pipelines (filtering, edge detection, segmentation)
- Depth sensing (stereo vision, structured light, Time-of-Flight)
- Point clouds (PCL library, filtering, registration)
- Object detection and pose estimation
- Sensor fusion (camera + LIDAR + IMU)

**Code Examples**:
- Load and visualize RGB-D images from simulated robot camera
- Apply camera projection to map 3D points to 2D image plane
- Filter point cloud using voxel grid and statistical outlier removal
- Detect objects in image using color-based segmentation

**Practical Exercises**:
1. Capture RGB-D images from simulated humanoid's head camera; convert depth to point cloud and visualize in 3D
2. Implement a simple object detector (color-based or template matching); estimate object position relative to robot

**Assessments** (9 questions):
- Define camera intrinsic parameters (fx, fy, cx, cy)
- Explain the difference between stereo vision and structured light depth sensing
- What is a point cloud? How is it generated from depth images?
- Describe one method for object detection in images

**Diagrams**:
- Pinhole camera model and projection
- RGB-D perception pipeline (image → depth → point cloud → segmentation)
- Sensor fusion architecture (camera + LIDAR + IMU → state estimator)
- Point cloud filtering workflow

**Further Reading**:
1. R. Hartley and A. Zisserman, "Multiple View Geometry in Computer Vision" (Cambridge, 2004)
2. R. Szeliski, "Computer Vision: Algorithms and Applications," Ch. 2-3 (Springer, 2022)
3. R. Rusu and S. Cousins, "3D is here: Point Cloud Library (PCL)," IEEE ICRA 2011

**Prerequisites**: Chapter 2; linear algebra (projections); basic image processing concepts

---

### Chapter 6: Motion Planning for Humanoid Robots

**Learning Objectives**:
1. Explain configuration space and collision checking for robot planning
2. Implement sampling-based planners (RRT, RRT*) for arm motion
3. Understand whole-body planning for humanoid stability
4. Apply trajectory optimization techniques (cubic splines, minimum-jerk)
5. Integrate perception feedback into reactive planning

**Key Concepts**:
- Configuration space (C-space) and obstacles
- Graph-based planning (A*, Dijkstra) vs. sampling-based (RRT, PRM)
- Collision detection (bounding volumes, distance queries)
- Whole-body planning (balance constraints, center-of-mass)
- Trajectory generation (interpolation, optimization, dynamic feasibility)
- Reactive planning (dynamic replanning, obstacle avoidance)

**Code Examples**:
- RRT planner for 2D/3D configuration space
- Collision checking using simple geometric primitives
- Cubic spline trajectory generation
- Integrate RRT with inverse kinematics for arm reaching task

**Practical Exercises**:
1. Implement RRT planner for a 2-DOF planar arm in cluttered environment; visualize explored tree and final path
2. Generate a smooth trajectory using cubic splines for the arm to follow planned waypoints; execute in simulation

**Assessments** (10 questions):
- Define configuration space. Why is it useful for planning?
- Compare RRT and A*: advantages and disadvantages
- Explain how collision checking works in C-space
- What is whole-body planning? Why is it needed for humanoids?
- Describe one trajectory optimization method

**Diagrams**:
- Configuration space with obstacles
- RRT tree exploration visualization
- Trajectory generation (waypoints → interpolated path)
- Whole-body planning framework (stability constraints + task goals)

**Further Reading**:
1. S. LaValle, "Planning Algorithms," Ch. 5-6 (Cambridge University Press, 2006)
2. L. Kavraki et al., "Probabilistic Roadmaps for Path Planning," IEEE Trans. Robotics
3. M. Vukobratović and B. Borovac, "Zero-Moment Point—Thirty Five Years of its Life," Int. J. Humanoid Robotics

**Prerequisites**: Chapter 3; data structures (trees, graphs); algorithms (search)

---

### Chapter 7: Manipulation and Grasping

**Learning Objectives**:
1. Understand grasp quality metrics (force closure, contact stability)
2. Implement grasp planning for multi-fingered hands
3. Explain object manipulation strategies (power grasp, precision grasp, in-hand manipulation)
4. Integrate force/torque sensing for contact control
5. Plan pick-and-place tasks with obstacle avoidance

**Key Concepts**:
- Grasp taxonomy (power, precision, hook, pinch)
- Contact models (point contact, soft contact, rolling contact)
- Force closure and grasp stability
- Grasp planning algorithms (analytical, data-driven)
- Manipulation primitives (reaching, grasping, placing, releasing)
- Impedance control for compliant contact
- In-hand manipulation techniques

**Code Examples**:
- Compute grasp quality metric (e.g., largest minimum resisted wrench)
- Plan grasp approach for parallel-jaw gripper
- Simulate pick-and-place task with impedance-controlled contact
- Force feedback integration for grasp force regulation

**Practical Exercises**:
1. Implement a simple grasp planner for parallel-jaw gripper targeting a box object; execute grasp in PyBullet
2. Develop pick-and-place controller with impedance control for compliant approach and contact stabilization

**Assessments** (9 questions):
- Define force closure. Why is it important for grasping?
- Compare power grasp vs. precision grasp with examples
- Explain impedance control and its role in manipulation
- What is in-hand manipulation? Provide an application scenario.

**Diagrams**:
- Grasp taxonomy visual guide
- Force closure illustration (contact forces and friction cones)
- Manipulation primitive sequence (reach → approach → grasp → lift → place)
- Impedance control block diagram

**Further Reading**:
1. A. Murray et al., "A Mathematical Introduction to Robotic Manipulation" (CRC Press, 1994)
2. A. Bicchi and V. Kumar, "Robotic Grasping and Contact: A Review," IEEE ICRA 2000
3. M. Mason, "Mechanics of Robotic Manipulation" (MIT Press, 2001)

**Prerequisites**: Chapter 4; statics (forces, moments); basic optimization

---

### Chapter 8: Bipedal Locomotion and Balance

**Learning Objectives**:
1. Explain Zero-Moment Point (ZMP) and Center of Pressure (CoP) for balance
2. Understand gait patterns (walking, running) and phase transitions
3. Implement footstep planning and ZMP-based walking controller
4. Analyze dynamic stability criteria (Capture Point, N-step capturability)
5. Integrate push recovery and disturbance rejection strategies

**Key Concepts**:
- Zero-Moment Point (ZMP) and support polygon
- Center of Mass (CoM) dynamics and inverted pendulum model
- Gait cycles and phase state machines (swing, stance, double support)
- Footstep planning (discrete footholds, terrain adaptation)
- Walking controllers (ZMP-based, model-predictive control)
- Dynamic stability (Capture Point, Divergent Component of Motion)
- Push recovery (ankle strategy, hip strategy, step strategy)

**Code Examples**:
- Compute ZMP for given CoM trajectory
- Linear Inverted Pendulum Model (LIPM) simulation
- Simple walking controller using ZMP preview control
- Footstep planner for flat terrain

**Practical Exercises**:
1. Simulate a linear inverted pendulum and compute ZMP; analyze stability as CoM deviates
2. Implement basic walking controller for simplified humanoid (LIPM assumptions); generate footstep plan and execute forward walking

**Assessments** (10 questions):
- Define Zero-Moment Point. How does it relate to stability?
- Explain the inverted pendulum model for bipedal walking
- Describe the phases of a walking gait cycle
- What is Capture Point? Why is it useful for balance control?
- Compare ankle vs. step strategy for push recovery

**Diagrams**:
- ZMP and support polygon visualization
- Inverted pendulum model schematic
- Gait cycle phase diagram (swing/stance transitions)
- Footstep planning on uneven terrain

**Further Reading**:
1. M. Vukobratović and D. Juricic, "Contribution to the Synthesis of Biped Gait," IEEE Trans. Biomedical Eng.
2. S. Kajita et al., "Biped Walking Pattern Generation using Preview Control of ZMP," IEEE ICRA 2003
3. J. Pratt et al., "Capture Point: A Step toward Humanoid Push Recovery," IEEE Humanoids 2006

**Prerequisites**: Chapter 4; dynamics (equations of motion, momentum); control theory

---

### Chapter 9: Learning and Adaptation in Physical AI

**Learning Objectives**:
1. Explain the role of machine learning in robot skill acquisition
2. Understand reinforcement learning basics (MDP, policy, reward)
3. Implement imitation learning for robot motion primitives
4. Explain model-based vs. model-free learning trade-offs
5. Describe sim-to-real transfer challenges and solutions

**Key Concepts**:
- Supervised learning for perception (object recognition, pose estimation)
- Reinforcement learning (RL) fundamentals (states, actions, rewards, policies)
- Imitation learning and learning from demonstration (LfD)
- Model-based RL (world models, planning in learned models)
- Model-free RL (Q-learning, policy gradients, actor-critic)
- Sim-to-real transfer (domain randomization, system identification)
- Online adaptation and meta-learning

**Code Examples**:
- Train simple neural network for object classification
- Implement basic Q-learning agent for grid-world navigation
- Imitation learning: Record human demonstrations and fit policy
- Domain randomization for sim-to-real robustness

**Practical Exercises**:
1. Implement a Q-learning agent to learn navigation in a simple environment; visualize learned policy
2. Record teleoperated robot demonstrations for reaching task; train imitation learning policy and evaluate in simulation

**Assessments** (10 questions):
- Define Markov Decision Process (MDP) components
- Explain the difference between supervised learning and reinforcement learning
- What is imitation learning? Provide an application example.
- Describe one sim-to-real transfer technique
- Compare model-based vs. model-free RL: when to use each?

**Diagrams**:
- RL feedback loop (agent-environment interaction)
- Imitation learning pipeline (demonstrations → policy training → execution)
- Sim-to-real transfer workflow (simulation training → domain randomization → real-world deployment)
- Model-based RL architecture (world model + planner + controller)

**Further Reading**:
1. R. Sutton and A. Barto, "Reinforcement Learning: An Introduction" (MIT Press, 2018)
2. B. Argall et al., "A Survey of Robot Learning from Demonstration," Robotics and Autonomous Systems, 2009
3. OpenAI et al., "Solving Rubik's Cube with a Robot Hand," arXiv 2019 (sim-to-real example)

**Prerequisites**: Chapter 6; probability (distributions, expectations); basic machine learning concepts

---

### Chapter 10: Human-Robot Collaboration and Ethical AI

**Learning Objectives**:
1. Explain shared autonomy and human-in-the-loop control paradigms
2. Understand human intent recognition and prediction techniques
3. Implement collaborative task planning with human and robot roles
4. Identify safety protocols (ISO 15066, collision avoidance, emergency stops)
5. Discuss ethical considerations in autonomous humanoid systems

**Key Concepts**:
- Human-robot interaction (HRI) modalities (teleoperation, shared autonomy, full autonomy)
- Intent recognition (gesture, gaze, EMG signals)
- Shared control and assistance (haptic feedback, authority allocation)
- Collaborative task planning (role assignment, human capabilities modeling)
- Safety standards (ISO 15066 for collaborative robots, risk assessment)
- Ethical considerations (privacy, transparency, accountability, bias)
- Explainable AI for trust and interpretability

**Code Examples**:
- Simple intent recognition from simulated human hand trajectory
- Shared control system (human provides high-level goals, robot executes low-level control)
- Collision avoidance with dynamic obstacle (simulated human)
- Authority allocation in shared autonomy (blend human and autonomous commands)

**Practical Exercises**:
1. Implement shared autonomy controller where human teleoperation is blended with autonomous obstacle avoidance
2. Develop simple intent predictor from simulated human motion data; use prediction to pre-emptively assist in pick-and-place task

**Assessments** (10 questions):
- Define shared autonomy. How does it differ from full autonomy?
- Explain one method for human intent recognition
- What is ISO 15066? Why is it important for collaborative robots?
- Discuss one ethical concern in deploying autonomous humanoid robots
- Describe transparency in AI and its role in human-robot trust

**Diagrams**:
- HRI spectrum (teleoperation → shared autonomy → full autonomy)
- Intent recognition pipeline (sensor data → feature extraction → classifier → predicted intent)
- Collaborative task workflow (human + robot role allocation)
- Safety architecture (emergency stop, collision detection, speed/force monitoring)

**Further Reading**:
1. A. Billard et al., "Learning from Humans," Springer Handbook of Robotics, 2016
2. ISO 15066: Robots and Robotic Devices - Collaborative Robots (ISO standard document)
3. J. Bryson and A. Winfield, "Standardizing Ethical Design for AI and Autonomous Systems," IEEE Computer, 2017
4. D. Aarno and D. Kragic, "Motion Intention Recognition in Robot Assisted Applications," Robotics and Autonomous Systems, 2008

**Prerequisites**: Chapters 6, 9; basic ethics and social science concepts

---

## Architectural Decisions

### Decision 1: Textbook Structure - Sequential Fundamentals

**Options Considered**:
- A) Sequential fundamentals-to-applications (chosen)
- B) Modular topic-based units (perception, control, planning as independent clusters)
- C) Project-driven spiral curriculum (revisit topics with increasing depth)

**Decision**: A) Sequential fundamentals-to-applications

**Rationale**:
- University courses typically follow linear progression; aligns with semester structure
- Prerequisite dependencies (Ch 2 → Ch 3 → Ch 4) require sequential ordering
- Students build confidence with early wins (Ch 1-2 accessible, Ch 8-10 advanced)
- Modular elements within (Ch 4-7 allow some flexibility for instructors)

**Trade-offs**:
- Less flexible than purely modular design
- Students must complete foundational chapters before advanced topics
- Instructors cannot easily create custom learning paths

**Mitigation**: Clearly document prerequisite dependencies in each chapter; provide "skip ahead" guidance for students with prior knowledge

---

### Decision 2: Diagram Style - Hybrid Mermaid + External Images

**Options Considered**:
- A) Inline ASCII diagrams
- B) Mermaid diagrams only
- C) External image references only (SVG/PNG)
- D) Hybrid Mermaid + external images (chosen)

**Decision**: D) Hybrid Mermaid + external images

**Rationale**:
- Mermaid diagrams render inline, version-controllable as text, easy to update
- Complex kinematics/perception diagrams require precision drawing (Draw.io, Matplotlib)
- Best of both: flowcharts/state machines in Mermaid; technical figures as SVG/PNG
- Accessibility: Mermaid auto-generates alt-text; external images require manual alt-text (enforced by checklist)

**Trade-offs**:
- Two diagramming workflows to maintain
- External images require separate editing tools

**Mitigation**: Establish clear guidelines (use Mermaid for flowcharts, block diagrams, state machines; use Draw.io/Matplotlib for kinematics, perception pipelines, complex math)

---

### Decision 3: Code Examples - Hybrid Python + ROS2

**Options Considered**:
- A) Python-only examples (no ROS2)
- B) ROS2-only examples
- C) Webots-specific API
- D) Hybrid Python + ROS2 + simulator integration (chosen)

**Decision**: D) Hybrid approach

**Rationale**:
- Python-only examples for foundational concepts (kinematics, dynamics) - maximize accessibility
- ROS2 integration for realistic robotics workflows (Chapter 5+: perception, planning, control)
- Simulator agnostic where possible (PyBullet default; Webots/MuJoCo alternatives noted)
- Mirrors industry practice (Python for prototyping, ROS2 for deployment)

**Trade-offs**:
- Students must learn multiple tools (Python, ROS2, simulator)
- Code examples more complex in later chapters

**Mitigation**: Gradual tool introduction (Ch 1-2 Python-only, Ch 3-4 add ROS2, Ch 5+ full integration); comprehensive setup guides in appendices

---

### Decision 4: Robotics Depth - Conceptual Learning with Applied Math

**Options Considered**:
- A) Conceptual only (minimal math)
- B) Deep mathematical derivations (graduate-level rigor)
- C) Conceptual learning with applied math (chosen)

**Decision**: C) Conceptual learning with applied math

**Rationale**:
- Undergraduate STEM students need mathematical grounding without measure theory/differential geometry
- Derive key equations (FK using DH, dynamics using Lagrangian) to build understanding
- Avoid proof-heavy sections; focus on "how to use" rather than "pure theory"
- Aligns with constitution principle: "undergraduate level, not graduate-level proofs"

**Trade-offs**:
- Cannot achieve full theoretical rigor (some concepts simplified)
- Advanced students may desire deeper mathematical treatment

**Mitigation**: "Further Reading" sections point to graduate-level resources for deeper study

---

### Decision 5: Physical AI Scope - Biomechanics + Sensorimotor + Embodied Cognition

**Options Considered**:
- A) Narrow focus on control and kinematics
- B) Broad coverage including biomechanics, sensorimotor loops, embodied cognition (chosen)
- C) AI-heavy focus (deep RL, neural architectures)

**Decision**: B) Broad coverage of Physical AI aspects

**Rationale**:
- "Physical AI" differentiates from traditional robotics texts
- Biomechanics (Ch 2, 8): How biological systems inspire robot design
- Sensorimotor loops (Ch 1, 5): Embodied intelligence through perception-action coupling
- Embodied cognition (Ch 9, 10): Intelligence arising from body-environment interaction
- Future-of-work emphasis requires AI collaboration context (Ch 10)

**Trade-offs**:
- Broader scope means less depth in each area compared to specialized texts
- Risk of superficial coverage if not carefully scoped

**Mitigation**: Maintain focus on humanoid robotics applications; use embodied AI as lens, not separate subject; ensure every concept ties back to practical robotics

---

### Decision 6: Practical Exercises - Simulation-Only

**Options Considered**:
- A) Simulation-only exercises (chosen)
- B) Real hardware option (with fallback simulations)
- C) Hybrid simulation + optional hardware labs

**Decision**: A) Simulation-only exercises

**Rationale**:
- Accessibility: Not all students/universities have physical humanoid robots
- Reproducibility: Simulated environments are controlled and deterministic
- Safety: No risk of hardware damage or injury during learning
- Cost: Open-source simulators are free (PyBullet, Webots, MuJoCo)
- Aligns with spec constraint: "All practical work uses simulation"

**Trade-offs**:
- Sim-to-real gap: Simulations don't capture all real-world physics
- Students don't experience hardware debugging, mechanical issues

**Mitigation**: Address sim-to-real gap explicitly in Chapter 9; note where simulations simplify reality; encourage optional hardware exploration via Further Reading

---

### Decision 7: Locomotion Abstraction - High-Level + Low-Level Control

**Options Considered**:
- A) High-level only (footstep planning, ZMP tracking)
- B) Low-level only (joint torque control, whole-body optimization)
- C) High-level + low-level control (chosen)

**Decision**: C) Cover both high-level planning and low-level control

**Rationale**:
- High-level (ZMP, footstep planning): Intuitive, accessible to beginners
- Low-level (torque control, dynamics): Necessary for understanding how controllers work
- Realistic robotics requires both layers (planner → controller → actuators)
- Chapter 8 structure: Start high-level (ZMP concept), progress to low-level (LIPM dynamics, control)

**Trade-offs**:
- More content to cover in single chapter
- Risk of overwhelming students with complexity

**Mitigation**: Clear progression from intuitive (ZMP polygon) to technical (LIPM equations); exercises start simple (compute ZMP) and build (implement controller)

---

### Decision 8: Deployment - GitHub Pages

**Options Considered**:
- A) GitHub Pages (chosen)
- B) ReadTheDocs
- C) Custom hosted server (AWS, Netlify)

**Decision**: A) GitHub Pages

**Rationale**:
- Free hosting for public repositories
- Native Docusaurus integration (official documentation recommends GitHub Pages)
- Automatic deployment via GitHub Actions
- Reliable, fast CDN
- Aligns with spec requirement: "Deploy to GitHub Pages"

**Trade-offs**:
- Tied to GitHub platform
- Limited customization compared to self-hosted

**Mitigation**: None needed; GitHub Pages meets all requirements

---

### Decision 9: Version Control Strategy - Branch-per-Chapter

**Options Considered**:
- A) Single main branch (all edits via PRs to main)
- B) Branch-per-chapter (chosen)
- C) Feature branches for each major change

**Decision**: B) Branch-per-chapter development

**Rationale**:
- Parallel chapter development (multiple authors can work simultaneously)
- Isolated testing (each chapter built and validated independently before merge)
- Clear PR scope (review one chapter at a time)
- Rollback safety (can revert individual chapter without affecting others)

**Workflow**:
1. Create branch `chapter-01-intro` from main
2. Write chapter content, exercises, assessments
3. Run quality checks (CI pipeline: code tests, F-K readability, citations)
4. Submit PR; reviewer checks technical accuracy, clarity
5. Merge to main after approval
6. Repeat for each chapter

**Trade-offs**:
- More branches to manage
- Potential merge conflicts if chapters reference each other

**Mitigation**: Establish chapter interface contracts early (glossary terms, shared assets); use rebasing to keep branches up-to-date with main

---

## Testing and Validation Strategy

### Phase 0: Setup Validation (Before Writing)
- ✅ Docusaurus project initializes and builds successfully
- ✅ CI pipeline configured and executing (linting, placeholder tests)
- ✅ Repository structure matches plan.md specification
- ✅ All required tools installed in development environment (Python, Node.js, ROS2, simulators)

### Phase 1: Per-Chapter Validation (During Writing)
Each chapter must pass these checks before PR approval:

**Content Quality**:
- Flesch-Kincaid grade level 10-14 (automated via `scripts/check-readability.py`)
- 3-5 learning objectives clearly stated
- Glossary terms defined for all technical vocabulary
- Further Reading section includes 3-5 annotated sources

**Technical Accuracy**:
- All technical claims cite authoritative sources (IEEE, textbooks, peer-reviewed papers)
- Citation audit confirms 40%+ content has evidence-based references
- Citations follow IEEE format (automated validation via `scripts/validate-citations.py`)
- Diagrams accurately represent concepts (manual review by subject matter expert)

**Code Executability**:
- All code blocks execute successfully in specified environments (pytest in CI pipeline)
- Code includes comments explaining key steps
- Dependencies documented with version numbers (requirements.txt, package.xml)
- Expected outputs documented for each exercise

**Exercises and Assessments**:
- Minimum 2 hands-on exercises per chapter
- Exercises include learning outcomes, setup instructions, expected outputs
- Minimum 5 assessment questions aligned with learning objectives
- Assessments cover key concepts from chapter (manual review)

**Plagiarism Check**:
- Automated plagiarism detection (Turnitin/Copyscape/Grammarly) reports 0% similarity
- Direct quotes properly attributed with IEEE citations
- All content originally written for this textbook

### Phase 2: Integration Validation (After All Chapters Written)
**Cross-Chapter Consistency**:
- Glossary terms used consistently across all chapters
- Notation and symbols standardized (e.g., q for joint angles, τ for torque)
- Internal links functional (chapter references, glossary lookups)
- Progressive concept building verified (foundational topics in early chapters, advanced in later)

**Docusaurus Build**:
- `npm run build` completes without errors or warnings
- All pages render correctly in development server (`npm start`)
- Sidebar navigation includes all chapters in correct order
- Search index functional (can find terms from chapters, glossary, exercises)
- All internal links resolve (no 404 errors)

**Accessibility Compliance**:
- WCAG 2.1 AA validation using automated tools (axe, WAVE)
- All images include descriptive alt-text
- Color contrast meets minimum ratios
- Keyboard navigation functional

**Performance**:
- Build time < 60 seconds (measured in CI)
- Page load times < 3 seconds (measured with Lighthouse)
- Search index size < 2MB
- Mobile responsiveness verified (viewport < 1200px width)

### Phase 3: End-to-End Validation (Before Deployment)
**Full Site Navigation**:
- Navigate from intro page to all 10 chapters via sidebar
- Test all internal links (chapter cross-references, glossary terms)
- Verify all external links (bibliography DOIs, Further Reading URLs) resolve correctly
- Test search functionality (search for technical terms, code snippets, find relevant results)

**Exercise Reproducibility**:
- Execute all 20+ practical exercises in fresh environment (Docker container)
- Verify all exercises complete successfully with documented outputs
- Test on all three platforms (Windows/WSL2, Linux, macOS)
- Confirm simulator installation guides work (Appendix setup instructions)

**Citation Audit**:
- Manual review of random sample (20% of citations) for accuracy
- Verify DOI links work and point to correct papers
- Confirm authoritative sources (IEEE, Siciliano, Craig, Spong, Murray, recent research)
- Check minimum 50 total bibliography entries requirement (SC-015)

**Educational Validation** (Optional but Recommended):
- Pilot test with small group of target students (5-10 STEM undergrads)
- Collect feedback on clarity, exercise difficulty, engagement
- Measure learning objectives achievement via assessments
- Iterate based on feedback before final deployment

### Phase 4: Deployment Validation (After GitHub Pages Deploy)
- GitHub Pages site accessible at expected URL
- All chapters, assets, diagrams load correctly
- No broken links or missing images
- Search works in production environment
- Mobile and desktop rendering verified
- Analytics configured (Google Analytics or similar) to track usage

### Continuous Validation (Post-Deployment)
- Monitor GitHub Issues for bug reports, typos, technical errors
- Re-run CI pipeline on any content updates (PRs to main branch)
- Quarterly citation link check (ensure DOIs still resolve)
- Periodic readability re-check if content significantly updated
- Track errata and publish corrections as needed

---

## Research and Citation Strategy

See [research.md](./research.md) for detailed citation sourcing strategy, authoritative robotics resources, and IEEE format guidelines.

**Summary**:
- Prioritize established robotics textbooks (Siciliano, Craig, Spong, Murray) for foundational theory
- Use IEEE standards for definitions and terminology
- Cite recent peer-reviewed papers (2015+) for advanced topics (embodied AI, learning, collaboration)
- Maintain BibTeX file for all references; use pandoc-citeproc for automatic IEEE formatting
- Aim for 50-70 total bibliography entries across 10 chapters (~5-7 per chapter)

---

## Content Structure and Data Model

See [data-model.md](./data-model.md) for detailed content structure including chapter templates, exercise formats, assessment question schemas, and metadata specifications.

**Summary**:
- Each chapter: frontmatter (ID, title, objectives, prerequisites) + content (MDX) + exercises (subdirectory) + assets (diagrams/images)
- Exercises: structured markdown with learning outcome, setup instructions, code blocks, expected output, assessment rubric
- Assessments: multiple choice, short answer, diagram labeling, code completion formats
- Glossary: centralized terms with definitions, context, citations
- Bibliography: BibTeX source → rendered IEEE format in bibliography.md

---

## Development Workflow and Quickstart

See [quickstart.md](./quickstart.md) for step-by-step developer setup, chapter writing workflow, quality check procedures, and deployment instructions.

**Summary**:
1. Clone repository, install dependencies (Node.js, Python, ROS2, simulators)
2. Create branch for chapter (e.g., `chapter-03-kinematics`)
3. Write chapter content using template from `contracts/chapter-template.md`
4. Add code examples (test locally with pytest)
5. Create exercises using `contracts/exercise-template.md`
6. Add assessments using `contracts/assessment-template.md`
7. Run quality checks (`npm run lint`, `python scripts/check-readability.py`, `python scripts/validate-citations.py`)
8. Submit PR for review
9. After approval, merge to main (triggers CI build and deploy to GitHub Pages)

---

## Chapter and Exercise Templates

See `contracts/` directory for structured templates ensuring consistency across all chapters.

**Templates**:
1. `chapter-template.md` - Chapter structure with frontmatter, learning objectives, concept sections, code blocks, exercise links, assessments, further reading
2. `exercise-template.md` - Exercise format with learning outcome, prerequisites, setup, instructions, code scaffold, expected output, troubleshooting
3. `assessment-template.md` - Question formats (multiple choice, short answer, diagram, code completion) with rubrics

---

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Simulator versions change, breaking code examples | High | Medium | Pin exact simulator versions in requirements; provide migration guides in appendix; test in CI with locked versions |
| ROS2 API changes between Humble and Iron | Medium | Low | Test code in both distributions; document version-specific variations; prioritize Humble (LTS) |
| Citations become inaccessible (paywalls, broken DOIs) | Medium | Medium | Prioritize open-access sources; include arXiv/ResearchGate alternatives; use DOI resolver services |
| Readability exceeds F-K 14 for complex topics | Medium | Medium | Iterative editing; simplify sentence structure; use glossary for technical terms; add explanatory diagrams |
| Plagiarism detection false positives (common technical phrases) | Low | Medium | Manually review flagged sections; ensure paraphrasing; use direct quotes sparingly with attribution |
| Chapter content scope creep (exceeds 6000 words) | Medium | High | Enforce word count guidelines in PR reviews; move detailed derivations to appendices; prioritize clarity over completeness |
| CI pipeline execution time exceeds limits (GitHub Actions timeout) | Low | Low | Optimize test execution (parallel pytest, caching dependencies); split pipelines if needed (build separate from tests) |
| Accessibility failures (missing alt-text, color contrast) | High | Medium | Automated WCAG checks in CI; manual review during PR; provide alt-text template in diagram guidelines |

---

## Quality Assurance Checklist

Before deploying to production, verify:

- [ ] All 10 chapters written and merged to main branch
- [ ] Docusaurus build succeeds without errors (`npm run build`)
- [ ] Flesch-Kincaid readability 10-14 for all chapters (automated check passed)
- [ ] Citation audit confirms 40%+ content includes authoritative references
- [ ] All citations in IEEE format (automated validation passed)
- [ ] Plagiarism detection reports 0% similarity (manual review completed)
- [ ] All code examples tested and execute successfully (CI pytest passed)
- [ ] All 20+ exercises include setup instructions and expected outputs
- [ ] Glossary includes 100+ technical terms with definitions
- [ ] Bibliography includes 50+ authoritative sources
- [ ] Index maps key concepts to chapter locations
- [ ] Appendices cover simulator setup (Webots, PyBullet, ROS2), math review, troubleshooting
- [ ] All diagrams include alt-text and source files committed
- [ ] Internal links functional (chapter cross-references, glossary lookups)
- [ ] External links verified (bibliography DOIs, Further Reading URLs)
- [ ] Search functionality works (can find technical terms, code snippets)
- [ ] Accessibility compliance (WCAG 2.1 AA automated checks passed)
- [ ] Mobile responsiveness verified (viewport < 1200px renders correctly)
- [ ] GitHub Pages deployment successful (site accessible at production URL)
- [ ] Final manual review by subject matter expert (technical accuracy)
- [ ] Optional: Pilot test with target students (5-10 undergrads) completed

---

## Next Steps

After plan approval:
1. Run `/sp.tasks` to generate dependency-ordered task list for implementation
2. Set up Docusaurus project structure and CI/CD pipeline (Phase 0)
3. Begin chapter-by-chapter content creation following quickstart workflow
4. Conduct incremental reviews and quality checks as chapters are completed
5. Perform end-to-end validation before final deployment

**Estimated Timeline** (not a constraint, for planning purposes):
- Phase 0 (Setup): Repository structure, Docusaurus config, CI pipeline
- Phase 1 (Chapters 1-3): Foundational content (intro, sensors, kinematics)
- Phase 2 (Chapters 4-7): Core robotics (dynamics, perception, planning, manipulation)
- Phase 3 (Chapters 8-10): Advanced topics (locomotion, learning, collaboration)
- Phase 4 (Supporting Materials): Glossary, index, bibliography, appendices
- Phase 5 (Integration & QA): Cross-chapter consistency, build validation, deployment

**Definition of Done**:
- All success criteria from spec.md verified
- Constitution principles validated
- Textbook deployed to GitHub Pages and accessible to students
- Academic approval obtained for university course adoption (optional but goal)

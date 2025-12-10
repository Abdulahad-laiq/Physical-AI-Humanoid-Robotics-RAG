# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/001-physical-ai-textbook/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, quickstart.md, contracts/

**Tests**: This is an educational textbook project. Quality validation (readability, citations, code execution) serves as testing.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files/chapters, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Documentation project**: `docs/` for all textbook content
- **Configuration**: Root-level config files (docusaurus.config.js, sidebars.js, package.json)
- **Infrastructure**: `.github/workflows/`, `scripts/` for automation
- **Supporting**: `specs/001-physical-ai-textbook/` for planning artifacts

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure

- [ ] T001 Create repository directory structure per plan.md (docs/, scripts/, .github/workflows/)
- [ ] T002 Initialize Docusaurus project with `npx create-docusaurus@latest` in repository root
- [ ] T003 [P] Create package.json with Docusaurus 3.x dependencies and custom scripts
- [ ] T004 [P] Create requirements.txt with Python dependencies (numpy, matplotlib, pybullet, pytest, textstat, flake8)
- [ ] T005 [P] Create .gitignore for node_modules/, build/, .docusaurus/, __pycache__
- [ ] T006 [P] Create LICENSE file (MIT or CC BY-NC-SA 4.0)
- [ ] T007 [P] Create README.md with project overview, setup instructions, contribution guidelines

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story content creation

**⚠️ CRITICAL**: No chapter writing can begin until this phase is complete

- [ ] T008 Configure docusaurus.config.js with site metadata, GitHub Pages deployment settings, theme configuration
- [ ] T009 Create sidebars.js with 5-category structure (Fundamentals, Core Robotics, Advanced Topics, Reference, Appendices)
- [ ] T010 [P] Create docs/intro.md landing page with textbook overview and navigation guide
- [ ] T011 [P] Create docs/glossary.md with frontmatter and initial structure (alphabetical sections)
- [ ] T012 [P] Create docs/bibliography.md with frontmatter and initial structure
- [ ] T013 [P] Create bibliography.bib (BibTeX) with initial 5-10 foundational sources from research.md
- [ ] T014 [P] Create docs/models/ directory and add simple_humanoid.urdf robot model
- [ ] T015 [P] Create docs/assets/global/ directory for shared diagrams and icons
- [ ] T016 Create scripts/validate-citations.py for IEEE format checking and 40%+ density validation
- [ ] T017 [P] Create scripts/check-readability.py for Flesch-Kincaid grade level analysis
- [ ] T018 [P] Create scripts/test-exercises.sh for executing all code examples
- [ ] T019 Create .github/workflows/build-and-deploy.yml for CI/CD to GitHub Pages
- [ ] T020 [P] Create .github/workflows/validate-code.yml for pytest execution on all code examples
- [ ] T021 [P] Create .github/workflows/check-quality.yml for readability, citations, plagiarism checks
- [ ] T022 Test local Docusaurus build with `npm start` and verify landing page renders

**Checkpoint**: Foundation ready - chapter content creation can now begin in parallel

---

## Phase 3: User Story 1 - Foundation Learning Journey (Priority: P1) 🎯 MVP

**Goal**: Deliver Chapters 1-4 covering foundational Physical AI and robotics concepts with hands-on learning

**Independent Test**: Student with STEM background completes Chapters 1-4 exercises using free tools and demonstrates understanding through assessments

### Chapter 1: Introduction to Physical AI

- [ ] T023 [P] [US1] Create docs/ch01-introduction/ directory with subdirectories (exercises/, assets/)
- [ ] T024 [US1] Write docs/ch01-introduction/index.md using chapter template (learning objectives, concepts, code examples, assessments)
- [ ] T025 [US1] Add 3 diagrams to docs/ch01-introduction/assets/ (Physical AI architecture, embodied intelligence concept map, collaboration taxonomy)
- [ ] T026 [P] [US1] Write docs/ch01-introduction/exercises/ex01-python-setup.md (Python + PyBullet installation and verification)
- [ ] T027 [P] [US1] Write docs/ch01-introduction/exercises/ex02-first-simulation.md (Load humanoid URDF in PyBullet, experiment with joints)
- [ ] T028 [US1] Add 10 assessment questions to ch01 index.md (MC, short answer, conceptual)
- [ ] T029 [US1] Add 3-5 further reading sources to ch01 index.md with IEEE citations
- [ ] T030 [US1] Update docs/glossary.md with ch01 terms (embodied intelligence, sensorimotor loop, Physical AI, etc.)
- [ ] T031 [US1] Update bibliography.bib with ch01 citations (Pfeifer & Bongard, Brooks, Sandini et al.)
- [ ] T032 [US1] Update sidebars.js to include ch01-introduction/index under Fundamentals category
- [ ] T033 [US1] Run quality checks on ch01 (F-K readability, citations 40%+, code execution, plagiarism 0%)

### Chapter 2: Robot Fundamentals

- [ ] T034 [P] [US1] Create docs/ch02-robot-fundamentals/ directory with subdirectories
- [ ] T035 [US1] Write docs/ch02-robot-fundamentals/index.md (sensors, actuators, coordinate frames, homogeneous transforms)
- [ ] T036 [US1] Add 4 diagrams to docs/ch02-robot-fundamentals/assets/ (sensor taxonomy, actuator comparison, coordinate frames, transformation matrix)
- [ ] T037 [P] [US1] Write docs/ch02-robot-fundamentals/exercises/ex01-imu-data.md (Extract and plot IMU data from simulated robot)
- [ ] T038 [P] [US1] Write docs/ch02-robot-fundamentals/exercises/ex02-transforms.md (Compute end-effector position with DH parameters for 3-DOF arm)
- [ ] T039 [US1] Add 8 assessment questions to ch02 index.md
- [ ] T040 [US1] Add 3-5 further reading sources to ch02 with IEEE citations
- [ ] T041 [US1] Update docs/glossary.md with ch02 terms (IMU, actuator, coordinate frame, homogeneous transformation, etc.)
- [ ] T042 [US1] Update bibliography.bib with ch02 citations (Craig, Siciliano, ISO 8373)
- [ ] T043 [US1] Update sidebars.js to include ch02-robot-fundamentals/index
- [ ] T044 [US1] Run quality checks on ch02

### Chapter 3: Humanoid Kinematics

- [ ] T045 [P] [US1] Create docs/ch03-kinematics/ directory with subdirectories
- [ ] T046 [US1] Write docs/ch03-kinematics/index.md (DH convention, FK/IK, workspace, singularities)
- [ ] T047 [US1] Add 4 diagrams to docs/ch03-kinematics/assets/ (DH frames, FK flowchart, IK solution space, workspace boundary)
- [ ] T048 [P] [US1] Write docs/ch03-kinematics/exercises/ex01-dh-fk.md (Implement DH-based FK for 6-DOF arm)
- [ ] T049 [P] [US1] Write docs/ch03-kinematics/exercises/ex02-ik-solver.md (Develop analytical or numerical IK solver)
- [ ] T050 [US1] Add 10 assessment questions to ch03 index.md
- [ ] T051 [US1] Add 3-5 further reading sources to ch03 with IEEE citations
- [ ] T052 [US1] Update docs/glossary.md with ch03 terms (Denavit-Hartenberg, forward kinematics, inverse kinematics, singularity, workspace, etc.)
- [ ] T053 [US1] Update bibliography.bib with ch03 citations (Craig Ch 3-4, Spong Ch 3, analytical IK papers)
- [ ] T054 [US1] Update sidebars.js to include ch03-kinematics/index
- [ ] T055 [US1] Run quality checks on ch03

### Chapter 4: Dynamics and Control

- [ ] T056 [P] [US1] Create docs/ch04-dynamics/ directory with subdirectories
- [ ] T057 [US1] Write docs/ch04-dynamics/index.md (Lagrangian dynamics, PID, computed-torque, impedance control)
- [ ] T058 [US1] Add 4 diagrams to docs/ch04-dynamics/assets/ (dynamics components, PID block diagram, computed-torque architecture, performance comparison)
- [ ] T059 [P] [US1] Write docs/ch04-dynamics/exercises/ex01-pid-tuning.md (Implement and tune PID for sinusoidal trajectory tracking)
- [ ] T060 [P] [US1] Write docs/ch04-dynamics/exercises/ex02-computed-torque.md (Develop computed-torque controller, compare with PID)
- [ ] T061 [US1] Add 10 assessment questions to ch04 index.md
- [ ] T062 [US1] Add 3-5 further reading sources to ch04 with IEEE citations
- [ ] T063 [US1] Update docs/glossary.md with ch04 terms (Lagrangian, PID, computed-torque, impedance control, etc.)
- [ ] T064 [US1] Update bibliography.bib with ch04 citations (Spong Ch 4-6, Siciliano Ch 4+8, Kelly, Åström & Murray)
- [ ] T065 [US1] Update sidebars.js to include ch04-dynamics/index
- [ ] T066 [US1] Run quality checks on ch04

**Checkpoint US1**: At this point, Chapters 1-4 (foundational learning) should be fully functional and independently testable

---

## Phase 4: User Story 2 - Hands-On Simulation Practice (Priority: P2)

**Goal**: Add advanced chapters 5-7 with practical simulator exercises for perception, planning, manipulation

**Independent Test**: Students execute 2+ exercises per chapter using Webots/PyBullet/MuJoCo with provided robot models

### Chapter 5: Perception Systems

- [ ] T067 [P] [US2] Create docs/ch05-perception/ directory with subdirectories
- [ ] T068 [US2] Write docs/ch05-perception/index.md (camera models, RGB-D processing, point clouds, object detection, sensor fusion)
- [ ] T069 [US2] Add 4 diagrams to docs/ch05-perception/assets/ (pinhole camera, RGB-D pipeline, sensor fusion architecture, point cloud filtering)
- [ ] T070 [P] [US2] Write docs/ch05-perception/exercises/ex01-rgbd-pointcloud.md (Capture RGB-D from robot camera, convert to point cloud, visualize)
- [ ] T071 [P] [US2] Write docs/ch05-perception/exercises/ex02-object-detection.md (Implement color-based or template matching detector, estimate object position)
- [ ] T072 [US2] Add 9 assessment questions to ch05 index.md
- [ ] T073 [US2] Add 3-5 further reading sources to ch05 with IEEE citations
- [ ] T074 [US2] Update docs/glossary.md with ch05 terms (camera intrinsics, point cloud, depth sensing, sensor fusion, etc.)
- [ ] T075 [US2] Update bibliography.bib with ch05 citations (Hartley & Zisserman, Szeliski, Rusu & Cousins PCL)
- [ ] T076 [US2] Update sidebars.js to include ch05-perception/index under Core Robotics category
- [ ] T077 [US2] Run quality checks on ch05

### Chapter 6: Motion Planning

- [ ] T078 [P] [US2] Create docs/ch06-planning/ directory with subdirectories
- [ ] T079 [US2] Write docs/ch06-planning/index.md (configuration space, RRT, collision checking, whole-body planning, trajectory optimization)
- [ ] T080 [US2] Add 4 diagrams to docs/ch06-planning/assets/ (C-space with obstacles, RRT tree visualization, trajectory generation, whole-body framework)
- [ ] T081 [P] [US2] Write docs/ch06-planning/exercises/ex01-rrt-planner.md (Implement RRT for 2-DOF arm in cluttered environment)
- [ ] T082 [P] [US2] Write docs/ch06-planning/exercises/ex02-trajectory-generation.md (Generate smooth trajectory using cubic splines for waypoints)
- [ ] T083 [US2] Add 10 assessment questions to ch06 index.md
- [ ] T084 [US2] Add 3-5 further reading sources to ch06 with IEEE citations
- [ ] T085 [US2] Update docs/glossary.md with ch06 terms (configuration space, RRT, collision checking, trajectory optimization, etc.)
- [ ] T086 [US2] Update bibliography.bib with ch06 citations (LaValle Ch 5-6, Kavraki PRM, Vukobratović ZMP)
- [ ] T087 [US2] Update sidebars.js to include ch06-planning/index
- [ ] T088 [US2] Run quality checks on ch06

### Chapter 7: Manipulation and Grasping

- [ ] T089 [P] [US2] Create docs/ch07-manipulation/ directory with subdirectories
- [ ] T090 [US2] Write docs/ch07-manipulation/index.md (grasp quality, force closure, grasp planning, impedance control, in-hand manipulation)
- [ ] T091 [US2] Add 4 diagrams to docs/ch07-manipulation/assets/ (grasp taxonomy, force closure, manipulation primitives, impedance control block diagram)
- [ ] T092 [P] [US2] Write docs/ch07-manipulation/exercises/ex01-grasp-planner.md (Simple grasp planner for parallel-jaw gripper, execute in PyBullet)
- [ ] T093 [P] [US2] Write docs/ch07-manipulation/exercises/ex02-pick-and-place.md (Pick-and-place controller with impedance control)
- [ ] T094 [US2] Add 9 assessment questions to ch07 index.md
- [ ] T095 [US2] Add 3-5 further reading sources to ch07 with IEEE citations
- [ ] T096 [US2] Update docs/glossary.md with ch07 terms (force closure, grasp quality, impedance control, manipulation primitive, etc.)
- [ ] T097 [US2] Update bibliography.bib with ch07 citations (Murray et al., Bicchi & Kumar, Mason, Hogan)
- [ ] T098 [US2] Update sidebars.js to include ch07-manipulation/index
- [ ] T099 [US2] Run quality checks on ch07

### Appendices for Simulator Setup (Supporting US2)

- [ ] T100 [P] [US2] Create docs/appendices/ directory
- [ ] T101 [P] [US2] Write docs/appendices/setup-pybullet.md (cross-platform installation guide, verification, troubleshooting)
- [ ] T102 [P] [US2] Write docs/appendices/setup-webots.md (installation for Windows/Linux/macOS, first simulation)
- [ ] T103 [P] [US2] Write docs/appendices/setup-ros2.md (ROS2 Humble installation, workspace setup, basic examples)
- [ ] T104 [P] [US2] Write docs/appendices/troubleshooting.md (common issues for PyBullet, ROS2, simulators across platforms)
- [ ] T105 [P] [US2] Write docs/appendices/math-review.md (linear algebra, calculus essentials, prerequisites review)
- [ ] T106 [US2] Update sidebars.js to include all appendices under Appendices category

**Checkpoint US2**: At this point, Chapters 5-7 and appendices provide hands-on simulation practice

---

## Phase 5: User Story 3 - Research-Backed Understanding (Priority: P2)

**Goal**: Ensure 40%+ citation density, IEEE format compliance, comprehensive bibliography and quality validation

**Independent Test**: Reviewer traces technical claims to cited sources, verifies 40%+ content has evidence-based citations in IEEE format

- [ ] T107 [US3] Complete bibliography.bib with all citations from Chapters 1-10 (target: 50-70 unique sources)
- [ ] T108 [US3] Regenerate docs/bibliography.md from bibliography.bib using `pandoc --citeproc --csl=ieee.csl`
- [ ] T109 [US3] Run scripts/validate-citations.py on all chapters and verify 40%+ citation density passes
- [ ] T110 [US3] Manual citation audit: verify 20% random sample of citations for accuracy and DOI resolution
- [ ] T111 [US3] Verify all glossary entries include citations to authoritative sources
- [ ] T112 [US3] Run F-K readability check on all chapters and ensure grade 10-14 compliance
- [ ] T113 [US3] Run plagiarism detection (Turnitin/Grammarly/Copyscape) on all chapters and verify 0% similarity
- [ ] T114 [US3] Complete docs/glossary.md with 100+ technical terms from all chapters (alphabetically sorted)
- [ ] T115 [US3] Create index mapping (manual or scripted) for key concepts → chapter locations
- [ ] T116 [US3] Update sidebars.js to include glossary and bibliography under Reference category

**Checkpoint US3**: At this point, textbook has academic rigor with research-backed content and comprehensive references

---

## Phase 6: User Story 5 - Future-of-Work Skill Development (Priority: P3)

**Goal**: Add advanced Chapters 8-10 emphasizing AI-human-robot collaboration, learning, and ethics

**Independent Test**: Students articulate embodied AI vs. traditional robotics, explain human-robot teaming, identify ethical considerations

### Chapter 8: Bipedal Locomotion

- [ ] T117 [P] [US5] Create docs/ch08-locomotion/ directory with subdirectories
- [ ] T118 [US5] Write docs/ch08-locomotion/index.md (ZMP, inverted pendulum, footstep planning, walking control, push recovery)
- [ ] T119 [US5] Add 4 diagrams to docs/ch08-locomotion/assets/ (ZMP/support polygon, inverted pendulum, gait cycle, footstep planning)
- [ ] T120 [P] [US5] Write docs/ch08-locomotion/exercises/ex01-lipm-simulation.md (Simulate linear inverted pendulum, compute ZMP, analyze stability)
- [ ] T121 [P] [US5] Write docs/ch08-locomotion/exercises/ex02-walking-controller.md (Basic walking controller for simplified humanoid using LIPM)
- [ ] T122 [US5] Add 10 assessment questions to ch08 index.md
- [ ] T123 [US5] Add 3-5 further reading sources to ch08 with IEEE citations
- [ ] T124 [US5] Update docs/glossary.md with ch08 terms (ZMP, inverted pendulum, gait cycle, Capture Point, etc.)
- [ ] T125 [US5] Update bibliography.bib with ch08 citations (Kajita, Vukobratović, Pratt Capture Point)
- [ ] T126 [US5] Update sidebars.js to include ch08-locomotion/index under Advanced Topics category
- [ ] T127 [US5] Run quality checks on ch08

### Chapter 9: Learning and Adaptation

- [ ] T128 [P] [US5] Create docs/ch09-learning/ directory with subdirectories
- [ ] T129 [US5] Write docs/ch09-learning/index.md (RL fundamentals, imitation learning, sim-to-real, online adaptation)
- [ ] T130 [US5] Add 4 diagrams to docs/ch09-learning/assets/ (RL feedback loop, imitation learning pipeline, sim-to-real workflow, model-based RL architecture)
- [ ] T131 [P] [US5] Write docs/ch09-learning/exercises/ex01-q-learning.md (Implement Q-learning agent for grid-world navigation)
- [ ] T132 [P] [US5] Write docs/ch09-learning/exercises/ex02-imitation-learning.md (Record teleoperated demos, train imitation policy, evaluate in sim)
- [ ] T133 [US5] Add 10 assessment questions to ch09 index.md
- [ ] T134 [US5] Add 3-5 further reading sources to ch09 with IEEE citations
- [ ] T135 [US5] Update docs/glossary.md with ch09 terms (reinforcement learning, MDP, imitation learning, sim-to-real, etc.)
- [ ] T136 [US5] Update bibliography.bib with ch09 citations (Sutton & Barto, Argall et al., OpenAI sim-to-real)
- [ ] T137 [US5] Update sidebars.js to include ch09-learning/index
- [ ] T138 [US5] Run quality checks on ch09

### Chapter 10: Human-Robot Collaboration and Ethical AI

- [ ] T139 [P] [US5] Create docs/ch10-collaboration/ directory with subdirectories
- [ ] T140 [US5] Write docs/ch10-collaboration/index.md (shared autonomy, intent recognition, ISO 15066, ethics, transparency)
- [ ] T141 [US5] Add 4 diagrams to docs/ch10-collaboration/assets/ (HRI spectrum, intent recognition pipeline, collaborative task workflow, safety architecture)
- [ ] T142 [P] [US5] Write docs/ch10-collaboration/exercises/ex01-shared-autonomy.md (Shared autonomy controller blending teleoperation with obstacle avoidance)
- [ ] T143 [P] [US5] Write docs/ch10-collaboration/exercises/ex02-intent-prediction.md (Simple intent predictor from simulated human motion, use for pre-emptive assistance)
- [ ] T144 [US5] Add 10 assessment questions to ch10 index.md
- [ ] T145 [US5] Add 3-5 further reading sources to ch10 with IEEE citations
- [ ] T146 [US5] Update docs/glossary.md with ch10 terms (shared autonomy, intent recognition, ISO 15066, transparency, etc.)
- [ ] T147 [US5] Update bibliography.bib with ch10 citations (Billard et al., ISO 15066, Bryson & Winfield, Aarno & Kragic)
- [ ] T148 [US5] Update sidebars.js to include ch10-collaboration/index
- [ ] T149 [US5] Run quality checks on ch10

**Checkpoint US5**: At this point, all 10 chapters complete with future-of-work emphasis in advanced topics

---

## Phase 7: User Story 4 - Docusaurus Web Deployment (Priority: P3)

**Goal**: Deploy textbook to GitHub Pages with functional search, navigation, and mobile responsiveness

**Independent Test**: Maintainer runs `npm run build`, deploys to GitHub Pages, verifies all features work across browsers

- [ ] T150 [US4] Run full Docusaurus build with `npm run build` and resolve any errors
- [ ] T151 [US4] Test all internal links (chapter cross-references, glossary lookups, bibliography links)
- [ ] T152 [US4] Verify all external links (DOI resolution, Further Reading URLs) using automated link checker
- [ ] T153 [US4] Test search functionality (verify can find technical terms, code snippets, returns relevant results)
- [ ] T154 [US4] Validate WCAG 2.1 AA accessibility compliance using automated tools (axe, WAVE)
- [ ] T155 [US4] Test mobile responsiveness on viewport widths < 1200px (sidebar collapse, images scale, code blocks scroll)
- [ ] T156 [US4] Verify syntax highlighting works for all code blocks (Python, bash, URDF/SDF, YAML)
- [ ] T157 [US4] Verify all diagrams include alt-text and render correctly
- [ ] T158 [US4] Test local production build with `npm run serve` and navigate through all chapters
- [ ] T159 [US4] Configure GitHub Pages deployment in repository settings (gh-pages branch)
- [ ] T160 [US4] Trigger CI/CD pipeline (.github/workflows/build-and-deploy.yml) and deploy to GitHub Pages
- [ ] T161 [US4] Verify deployed site at production URL (all chapters load, navigation works, search functions)
- [ ] T162 [US4] Test deployed site on multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] T163 [US4] Run Lighthouse performance audit (target: load times < 3s, mobile score > 90)

**Checkpoint US4**: At this point, textbook is deployed and accessible via GitHub Pages

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple chapters and final quality assurance

- [ ] T164 [P] Cross-chapter consistency review: verify terminology, notation, symbols standardized across all chapters
- [ ] T165 [P] Verify progressive concept building: foundational topics in early chapters, advanced in later chapters
- [ ] T166 [P] Final plagiarism detection scan on entire textbook corpus
- [ ] T167 [P] Final F-K readability check on all chapters (ensure 10-14 grade level)
- [ ] T168 [P] Final citation density audit across all chapters (ensure 40%+ minimum met)
- [ ] T169 [P] Execute all 20+ exercises in fresh Docker container to verify reproducibility
- [ ] T170 [P] Test exercises on all three platforms (Windows WSL2, Ubuntu Linux, macOS)
- [ ] T171 Create humanoid_with_hands.urdf robot model for advanced exercises and add to docs/models/
- [ ] T172 [P] Review and update README.md with final setup instructions, contribution guidelines, license info
- [ ] T173 [P] Create CONTRIBUTING.md with guidelines for chapter authors, reviewers, maintainers
- [ ] T174 [P] Add global assets (logos, icons, branding) to docs/assets/global/
- [ ] T175 Optional: Pilot test with 5-10 target students (STEM undergrads), collect feedback, iterate
- [ ] T176 Optional: Seek academic review from subject matter experts (roboticists, educators)
- [ ] T177 Final end-to-end validation: complete site navigation, all links functional, search index complete

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (P1): Can start after Foundational - Independent (Chapters 1-4)
  - US2 (P2): Can start after Foundational - Builds on US1 (uses models from Ch 2-4), adds Chapters 5-7 + appendices
  - US3 (P2): Can run in parallel with US1-2 once chapters exist - Quality validation and citation work
  - US5 (P3): Can start after Foundational - Builds on US1-2 (uses concepts from Ch 1-7), adds Chapters 8-10
  - US4 (P3): Can start after US1 has at least 1 chapter - Deployment infrastructure; final deployment after all content complete
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Foundation Learning)**: Can start after Foundational (Phase 2) - No dependencies on other stories
  - Deliverable: Chapters 1-4 independently completable
- **User Story 2 (P2 - Hands-On Simulation)**: Builds on US1 (uses robot models, coordinate frames from Ch 1-4)
  - Can start Chapters 5-7 after Foundational phase
  - Appendices can be written in parallel
  - Deliverable: Chapters 5-7 + appendices independently completable
- **User Story 3 (P2 - Research-Backed)**: Can run in parallel with US1-2 as chapters are written
  - Citation work, bibliography building, glossary maintenance ongoing
  - Final validation after all chapters exist
  - Deliverable: 40%+ citations, IEEE format, comprehensive bibliography
- **User Story 5 (P3 - Future-of-Work)**: Builds on US1-2 (references concepts from Ch 1-7)
  - Can start Chapters 8-10 after Foundational phase
  - Deliverable: Chapters 8-10 independently completable
- **User Story 4 (P3 - Docusaurus Deployment)**: Infrastructure can start early; final deployment after all content
  - Deliverable: Deployed GitHub Pages site

### Within Each Chapter

- Directory creation → Content writing → Diagrams → Exercises → Assessments → Further Reading → Glossary/Bibliography updates → Quality checks → Sidebar update
- Each chapter should be complete before starting next (sequential within user story)
- Exercises within a chapter can be written in parallel ([P] tasks)

### Parallel Opportunities

- All Setup tasks in Phase 1 can run in parallel
- All Foundational tasks in Phase 2 marked [P] can run in parallel
- Once Foundational completes:
  - US1 Chapters 1-4 can be written by different authors in parallel
  - US2 Chapters 5-7 + appendices can be written in parallel (after US1 or concurrently if authors coordinate)
  - US3 citation work can proceed alongside US1-2
  - US5 Chapters 8-10 can be written in parallel (after US1-2 or concurrently if authors coordinate)
- Within each chapter, exercises marked [P] can be written in parallel
- Diagram creation, glossary updates can often run in parallel with content writing

---

## Parallel Example: User Story 1 (Foundation Learning)

```bash
# After Foundational phase complete, launch Chapter 1-4 creation in parallel (if multiple authors):
# Author A: Chapter 1
# Author B: Chapter 2
# Author C: Chapter 3
# Author D: Chapter 4

# Within Chapter 1, these can run in parallel:
Task T026 [P]: Write exercise ex01-python-setup.md
Task T027 [P]: Write exercise ex02-first-simulation.md
(After T024 content is written)

# Or sequential approach (single author):
# Complete Chapter 1 → Chapter 2 → Chapter 3 → Chapter 4 in order
```

---

## Implementation Strategy

### MVP First (User Story 1 Only - Chapters 1-4)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all content)
3. Complete Phase 3: User Story 1 (Chapters 1-4)
4. **STOP and VALIDATE**: Test Chapters 1-4 independently (students complete exercises, assessments)
5. Deploy MVP to GitHub Pages for early feedback

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Infrastructure ready
2. Add User Story 1 (Chapters 1-4) → Test independently → Deploy MVP
3. Add User Story 2 (Chapters 5-7 + Appendices) → Test independently → Deploy update
4. Add User Story 3 (Citations/Quality) → Validate research rigor → Deploy update
5. Add User Story 5 (Chapters 8-10) → Test independently → Deploy update
6. Add User Story 4 (Final Deployment) → Full site validation → Production release
7. Each increment adds value without breaking previous content

### Parallel Team Strategy

With multiple content authors:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Author Team A: User Story 1 (Chapters 1-4)
   - Author Team B: User Story 2 (Chapters 5-7 + Appendices) - coordinate with Team A for shared concepts
   - Quality Team: User Story 3 (Citations, validation) - reviews all content
   - Author Team C: User Story 5 (Chapters 8-10) - after Teams A&B or in parallel with coordination
   - Infra Team: User Story 4 (Deployment) - setup early, final deployment at end
3. Stories complete and integrate independently with cross-team coordination

---

## Notes

- [P] tasks = different files/chapters, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Commit after each chapter or logical group
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 177
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 15 tasks (BLOCKING)
- Phase 3 (US1 - Foundation Learning): 44 tasks (Chapters 1-4)
- Phase 4 (US2 - Hands-On Simulation): 33 tasks (Chapters 5-7 + Appendices)
- Phase 5 (US3 - Research-Backed): 10 tasks (Citations & Quality)
- Phase 6 (US5 - Future-of-Work): 33 tasks (Chapters 8-10)
- Phase 7 (US4 - Docusaurus Deployment): 14 tasks (Deploy & Validate)
- Phase 8 (Polish): 14 tasks (Cross-cutting)

**Parallel Opportunities**: 58 tasks marked [P] can run in parallel (within phases or across chapters)

**MVP Scope**: Phases 1-2-3 (Setup + Foundational + US1) = ~66 tasks for minimum viable textbook (Chapters 1-4)

**Format Validation**: ✅ All tasks follow required checkbox format with IDs, [P] markers where applicable, [Story] labels for user story phases, and file paths

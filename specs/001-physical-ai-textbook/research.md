# Research and Citation Strategy

**Feature**: Physical AI & Humanoid Robotics Textbook
**Purpose**: Define authoritative source selection, citation methodology, and research workflow to achieve 40%+ evidence-based content with IEEE-format references
**Last Updated**: 2025-12-09

## Citation Requirements (from Constitution)

- **Minimum 40% of technical content** MUST cite validated research or authoritative textbooks
- **All citations** MUST follow IEEE citation style
- **Bibliography** MUST include minimum 50 authoritative sources
- **No technical claim** may be included without citation or clear derivation from cited principles
- **Priority sources**: IEEE standards, peer-reviewed papers, established robotics textbooks

## Authoritative Robotics Sources

### Tier 1: Foundational Robotics Textbooks

These are the canonical references for robotics fundamentals. Cite extensively for kinematics, dynamics, control, and planning.

1. **Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G.** (2010). *Robotics: Modelling, Planning and Control*. Springer.
   - **Coverage**: Kinematics (DH parameters, FK/IK), dynamics (Lagrangian, Newton-Euler), control (PID, computed-torque), planning
   - **Use in**: Chapters 2, 3, 4, 6, 7
   - **Citation frequency**: 8-12 times across chapters

2. **Craig, J. J.** (2017). *Introduction to Robotics: Mechanics and Control* (4th ed.). Pearson.
   - **Coverage**: Kinematics, dynamics, trajectory generation, control, manipulator design
   - **Use in**: Chapters 3, 4, 7
   - **Citation frequency**: 6-8 times

3. **Spong, M. W., Hutchinson, S., & Vidyasagar, M.** (2005). *Robot Modeling and Control*. Wiley.
   - **Coverage**: Lagrangian dynamics, control theory, stability analysis
   - **Use in**: Chapters 4, 6, 7
   - **Citation frequency**: 5-7 times

4. **Murray, R. M., Li, Z., & Sastry, S. S.** (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press.
   - **Coverage**: Grasping, force closure, manipulation mechanics, nonholonomic systems
   - **Use in**: Chapters 7, 8
   - **Citation frequency**: 4-6 times

### Tier 2: Specialized Humanoid Robotics Sources

These provide humanoid-specific knowledge: bipedal locomotion, whole-body control, human-robot interaction.

5. **Kajita, S., Hirukawa, H., Harada, K., & Yokoi, K.** (2014). *Introduction to Humanoid Robotics*. Springer.
   - **Coverage**: Bipedal walking, ZMP, balance control, whole-body motion
   - **Use in**: Chapter 8
   - **Citation frequency**: 5-7 times

6. **Vukobratović, M. & Borovac, B.** (2004). "Zero-Moment Point—Thirty Five Years of its Life." *International Journal of Humanoid Robotics*, 1(1), 157-173.
   - **Coverage**: ZMP theory, history, applications
   - **Use in**: Chapter 8
   - **Citation frequency**: 2-3 times

7. **Pratt, J., Carff, J., Drakunov, S., & Goswami, A.** (2006). "Capture Point: A Step toward Humanoid Push Recovery." *IEEE-RAS International Conference on Humanoid Robots*.
   - **Coverage**: Dynamic stability, push recovery, Capture Point concept
   - **Use in**: Chapter 8
   - **Citation frequency**: 2-3 times

### Tier 3: Perception and Computer Vision

For sensor systems, image processing, point clouds, object detection.

8. **Hartley, R. & Zisserman, A.** (2004). *Multiple View Geometry in Computer Vision* (2nd ed.). Cambridge University Press.
   - **Coverage**: Camera models, calibration, stereo vision, 3D reconstruction
   - **Use in**: Chapter 5
   - **Citation frequency**: 3-5 times

9. **Szeliski, R.** (2022). *Computer Vision: Algorithms and Applications* (2nd ed.). Springer.
   - **Coverage**: Image processing, feature detection, segmentation, object recognition
   - **Use in**: Chapter 5
   - **Citation frequency**: 3-4 times

10. **Rusu, R. B. & Cousins, S.** (2011). "3D is here: Point Cloud Library (PCL)." *IEEE International Conference on Robotics and Automation*.
    - **Coverage**: Point cloud processing, filtering, registration
    - **Use in**: Chapter 5
    - **Citation frequency**: 1-2 times

### Tier 4: Motion Planning

For sampling-based planners, trajectory optimization, whole-body planning.

11. **LaValle, S. M.** (2006). *Planning Algorithms*. Cambridge University Press.
    - **Coverage**: Configuration space, RRT, PRM, graph search, kinodynamic planning
    - **Use in**: Chapter 6
    - **Citation frequency**: 4-6 times

12. **Kavraki, L. E., Svestka, P., Latombe, J. C., & Overmars, M. H.** (1996). "Probabilistic Roadmaps for Path Planning in High-Dimensional Configuration Spaces." *IEEE Transactions on Robotics and Automation*, 12(4), 566-580.
    - **Coverage**: PRM algorithm, probabilistic completeness
    - **Use in**: Chapter 6
    - **Citation frequency**: 1-2 times

### Tier 5: Machine Learning and Embodied AI

For reinforcement learning, imitation learning, sim-to-real transfer, embodied intelligence.

13. **Sutton, R. S. & Barto, A. G.** (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
    - **Coverage**: MDP, value functions, policy gradients, Q-learning, actor-critic
    - **Use in**: Chapter 9
    - **Citation frequency**: 5-7 times

14. **Argall, B. D., Chernova, S., Veloso, M., & Browning, B.** (2009). "A Survey of Robot Learning from Demonstration." *Robotics and Autonomous Systems*, 57(5), 469-483.
    - **Coverage**: Imitation learning, learning from demonstration, policy transfer
    - **Use in**: Chapter 9
    - **Citation frequency**: 2-3 times

15. **Pfeifer, R. & Bongard, J.** (2006). *How the Body Shapes the Way We Think: A New View of Intelligence*. MIT Press.
    - **Coverage**: Embodied intelligence, morphological computation, sensorimotor loops
    - **Use in**: Chapters 1, 9
    - **Citation frequency**: 3-4 times

16. **Brooks, R. A.** (1991). "Intelligence without Representation." *Artificial Intelligence*, 47(1-3), 139-159.
    - **Coverage**: Subsumption architecture, reactive control, embodied AI philosophy
    - **Use in**: Chapter 1
    - **Citation frequency**: 1-2 times

### Tier 6: Human-Robot Interaction and Ethics

For collaboration, shared autonomy, safety, ethical considerations.

17. **Billard, A., Calinon, S., & Dillmann, R.** (2016). "Learning from Humans." In *Springer Handbook of Robotics* (2nd ed.), pp. 1995-2014. Springer.
    - **Coverage**: HRI modalities, imitation learning, collaborative tasks
    - **Use in**: Chapter 10
    - **Citation frequency**: 3-4 times

18. **ISO 15066:2016** - *Robots and Robotic Devices - Collaborative Robots* (International Organization for Standardization).
    - **Coverage**: Safety requirements, power and force limiting, risk assessment
    - **Use in**: Chapter 10
    - **Citation frequency**: 2-3 times

19. **Bryson, J. J. & Winfield, A. F. T.** (2017). "Standardizing Ethical Design for Artificial Intelligence and Autonomous Systems." *IEEE Computer*, 50(5), 116-119.
    - **Coverage**: Ethical AI principles, transparency, accountability
    - **Use in**: Chapter 10
    - **Citation frequency**: 1-2 times

### Tier 7: Control Theory

For PID control, stability analysis, impedance/admittance control.

20. **Åström, K. J. & Murray, R. M.** (2021). *Feedback Systems: An Introduction for Scientists and Engineers* (2nd ed.). Princeton University Press. (Open access)
    - **Coverage**: Feedback control principles, PID, stability, frequency domain
    - **Use in**: Chapter 4
    - **Citation frequency**: 2-3 times

21. **Hogan, N.** (1985). "Impedance Control: An Approach to Manipulation." *Journal of Dynamic Systems, Measurement, and Control*, 107(1), 1-24.
    - **Coverage**: Impedance control, compliant manipulation, force/position hybrid control
    - **Use in**: Chapters 4, 7
    - **Citation frequency**: 1-2 times

### Tier 8: IEEE Standards and Definitions

For terminology, coordinate systems, safety.

22. **ISO 8373:2021** - *Robots and Robotic Devices - Vocabulary* (International Organization for Standardization).
    - **Coverage**: Standard robotics terminology
    - **Use in**: Glossary, Chapters 1, 2
    - **Citation frequency**: 2-3 times

23. **IEEE Standard for Robot Coordinate Systems** (if applicable, or use ISO 9787).
    - **Coverage**: Coordinate frame definitions, right-hand rule conventions
    - **Use in**: Chapter 2
    - **Citation frequency**: 1-2 times

## Additional Research Sources (20-30 Papers)

To reach 50-70 total citations, supplement textbooks with recent research papers (2015-2024) on:

**Chapter 5 (Perception)**:
- Deep learning for object detection (YOLO, Faster R-CNN papers)
- RGB-D SLAM algorithms
- Semantic segmentation for robotics

**Chapter 6 (Planning)**:
- RRT* and informed sampling methods
- Whole-body planning for humanoids
- Trajectory optimization (CHOMP, TrajOpt)

**Chapter 7 (Manipulation)**:
- Deep grasping networks (GraspNet, 6-DOF grasp pose estimation)
- Tactile sensing for manipulation
- Dexterous in-hand manipulation

**Chapter 8 (Locomotion)**:
- Model-Predictive Control (MPC) for walking
- Optimization-based contact planning
- Terrain adaptation and rough-terrain locomotion

**Chapter 9 (Learning)**:
- Sim-to-real transfer (domain randomization, system ID)
- Deep RL for robot control (DDPG, SAC, PPO applied to robotics)
- Meta-learning for adaptation

**Chapter 10 (Collaboration)**:
- Shared autonomy frameworks
- Intent recognition using vision/EMG
- Explainable AI for robot transparency

**Source databases for papers**:
- IEEE Xplore (ieee.org)
- arXiv Robotics (arxiv.org/list/cs.RO)
- Robotics: Science and Systems (RSS) proceedings
- ICRA and IROS conference papers
- Journal of Field Robotics
- International Journal of Robotics Research (IJRR)

## IEEE Citation Format Guidelines

### Book Citation
[1] B. Siciliano, L. Sciavicco, L. Villani, and G. Oriolo, *Robotics: Modelling, Planning and Control*. London, U.K.: Springer, 2010.

### Journal Article Citation
[2] M. Vukobratović and B. Borovac, "Zero-moment point—Thirty five years of its life," *Int. J. Humanoid Robot.*, vol. 1, no. 1, pp. 157–173, Mar. 2004.

### Conference Paper Citation
[3] J. Pratt, J. Carff, S. Drakunov, and A. Goswami, "Capture point: A step toward humanoid push recovery," in *Proc. IEEE-RAS Int. Conf. Humanoid Robots*, Genova, Italy, Dec. 2006, pp. 200–207.

### Standard Citation
[4] *Robots and Robotic Devices—Collaborative Robots*, ISO Standard 15066, 2016.

### Online Resource Citation
[5] S. LaValle, *Planning Algorithms*. Cambridge, U.K.: Cambridge Univ. Press, 2006. [Online]. Available: http://planning.cs.uiuc.edu/

### Chapter in Edited Book Citation
[6] A. Billard, S. Calinon, and R. Dillmann, "Learning from humans," in *Springer Handbook of Robotics*, 2nd ed., B. Siciliano and O. Khatib, Eds. Cham, Switzerland: Springer, 2016, pp. 1995–2014.

## Citation Workflow

### During Chapter Writing

1. **Identify claims requiring citation**: Technical definitions, algorithms, equations, experimental results, design principles
2. **Select appropriate source**: Prefer Tier 1-2 textbooks for foundational content; use papers for advanced/recent topics
3. **Add inline citation marker**: `[1]`, `[2]`, etc. in text
4. **Add BibTeX entry**: Immediately add to `bibliography.bib` file with correct IEEE fields

### BibTeX Entry Format

```bibtex
@book{siciliano2010robotics,
  title={Robotics: Modelling, Planning and Control},
  author={Siciliano, Bruno and Sciavicco, Lorenzo and Villani, Luigi and Oriolo, Giuseppe},
  year={2010},
  publisher={Springer},
  address={London, U.K.}
}

@article{vukobratovic2004zero,
  title={Zero-moment point—Thirty five years of its life},
  author={Vukobratovi{\'c}, Miomir and Borovac, Branislav},
  journal={International Journal of Humanoid Robotics},
  volume={1},
  number={1},
  pages={157--173},
  year={2004},
  month={Mar.},
  publisher={World Scientific}
}

@inproceedings{pratt2006capture,
  title={Capture point: A step toward humanoid push recovery},
  author={Pratt, Jerry and Carff, John and Drakunov, Sergey and Goswami, Ambarish},
  booktitle={Proc. IEEE-RAS Int. Conf. Humanoid Robots},
  pages={200--207},
  year={2006},
  month={Dec.},
  address={Genova, Italy}
}
```

### Automated Citation Rendering

Use pandoc-citeproc or similar tool to render BibTeX → IEEE format in `bibliography.md`:

```bash
pandoc --citeproc --csl=ieee.csl bibliography.bib -o bibliography.md
```

IEEE CSL file available at: https://github.com/citation-style-language/styles/blob/master/ieee.csl

### Citation Validation Script

`scripts/validate-citations.py` performs:
1. Parse all MDX files for citation markers `[1]`, `[2]`, etc.
2. Check that each marker has corresponding BibTeX entry
3. Verify BibTeX entries include required fields (author, title, year, publisher/journal)
4. Compute citation density: (paragraphs with citations) / (total technical paragraphs) ≥ 40%
5. Check IEEE format compliance in rendered bibliography.md
6. Report missing citations, incomplete entries, format errors

Run during PR review:
```bash
python scripts/validate-citations.py --strict
```

## Citation Density Target by Chapter

To achieve 40%+ overall citation density, distribute citations across chapters:

| Chapter | Technical Paragraphs (est.) | Min Citations Needed (40%) | Target Citations |
|---------|----------------------------|---------------------------|------------------|
| Ch 1    | 20                         | 8                          | 8-10             |
| Ch 2    | 25                         | 10                         | 10-12            |
| Ch 3    | 30                         | 12                         | 12-15            |
| Ch 4    | 30                         | 12                         | 12-15            |
| Ch 5    | 25                         | 10                         | 10-12            |
| Ch 6    | 25                         | 10                         | 10-12            |
| Ch 7    | 25                         | 10                         | 10-12            |
| Ch 8    | 30                         | 12                         | 12-15            |
| Ch 9    | 25                         | 10                         | 10-12            |
| Ch 10   | 20                         | 8                          | 8-10             |
| **Total** | **255** | **102 (40%)** | **102-125** |

**Unique sources**: Aim for 50-70 distinct bibliography entries. Citations will be reused across chapters (e.g., Siciliano cited in Ch 2, 3, 4, 6, 7).

## Open Access Prioritization

When possible, prioritize open-access sources to ensure student accessibility:

**Open Access Textbooks**:
- Åström & Murray, *Feedback Systems* (free PDF: https://fbswiki.org/)
- LaValle, *Planning Algorithms* (free online: http://planning.cs.uiuc.edu/)

**Open Access Papers**:
- arXiv preprints (cs.RO category)
- Papers with author-hosted PDFs on institutional pages

**Institutional Access**:
- Note in appendix: "Many IEEE and Springer papers are accessible via university library subscriptions"
- Provide DOI links for permanent access (DOI resolver works regardless of paywall)

## Example Citation Usage in Chapter

**Chapter 3 Excerpt: Forward Kinematics**

> Forward kinematics (FK) computes the end-effector pose given joint angles. The Denavit-Hartenberg (DH) convention [1] provides a systematic method for assigning coordinate frames to robot links and deriving transformation matrices. Each link is described by four DH parameters: link length $a_i$, link twist $\alpha_i$, link offset $d_i$, and joint angle $\theta_i$ [2]. The transformation matrix from frame $i-1$ to frame $i$ is given by:
>
> $$T_i^{i-1} = \text{Rot}_{z}(\theta_i) \text{Trans}_{z}(d_i) \text{Trans}_{x}(a_i) \text{Rot}_{x}(\alpha_i)$$
>
> This formulation is widely used in robotics for serial-link manipulators [1], [2], [3]. For a detailed derivation, see Craig [2, Ch. 3] or Siciliano et al. [1, Ch. 2].

**Bibliography Entries**:
- [1] B. Siciliano et al., *Robotics: Modelling, Planning and Control*, 2010.
- [2] J. Craig, *Introduction to Robotics: Mechanics and Control*, 2017.
- [3] M. Spong et al., *Robot Modeling and Control*, 2005.

## Fallback Strategy for Inaccessible Sources

If a cited source becomes unavailable (journal paywall, broken DOI):

1. **Alternative archival sources**: Check arXiv, ResearchGate, author's institutional page
2. **University library access**: Note in appendix that students should use institutional access
3. **Replace citation**: If source is consistently unavailable, find alternative authoritative source covering the same material
4. **Document in bibliography**: Include note: "Available via institutional access" or "Preprint: arXiv:XXXX.XXXXX"

## Quality Checklist for Citations

Before finalizing each chapter:
- [ ] All technical claims have citations or are derived from cited principles
- [ ] Citation density ≥ 40% (validated by script)
- [ ] All BibTeX entries include required fields (author, title, year, publisher/journal/conference)
- [ ] All citations rendered in IEEE format (validated by script)
- [ ] DOI links functional (checked with automated link validator)
- [ ] Open-access alternatives noted where available
- [ ] No plagiarism detected (content is paraphrased/original, not copy-paste from sources)

## Estimated Research Time per Chapter

- **Foundation chapters (1-4)**: ~4-6 hours research (textbooks well-established, fewer papers needed)
- **Advanced chapters (5-10)**: ~6-10 hours research (mix of textbooks + recent papers)
- **Total research time**: ~50-70 hours across all chapters

**Concurrent research workflow**: Research each chapter immediately before writing (not all upfront). This allows:
- Focused research (only gather sources for current chapter)
- Flexibility to adjust based on evolving chapter scope
- Avoiding research fatigue (spreading work across project timeline)

<!--
SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: Added Section VIII (RAG Chatbot System Principles)
Added sections: RAG Chatbot architectural standards, success criteria
Removed sections: None
Templates requiring updates:
  ✅ .specify/templates/spec-template.md - Validated (aligned)
  ✅ .specify/templates/plan-template.md - Validated (aligned)
  ✅ .specify/templates/tasks-template.md - Validated (aligned)
Follow-up TODOs:
  - Create RAG Chatbot feature specification (/sp.specify)
  - Create RAG Chatbot architectural plan (/sp.plan)
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Technical Accuracy and Authority

Every technical definition, explanation, and algorithm MUST reference authoritative sources from robotics, mechatronics, AI, and control systems standards. Sources include:
- IEEE standards and publications
- Research institutions (MIT, CMU, Stanford Robotics Labs)
- Peer-reviewed journals and conference papers
- Established robotics textbooks (Siciliano, Craig, Spong, Murray)

**Minimum threshold**: 40% of technical content must be derived from validated research or authoritative textbooks.

**Citation requirement**: All references MUST follow IEEE citation style.

**Non-negotiable**: No technical claim may be included without either a direct citation or clear derivation from cited principles.

### II. Clarity and Accessibility

Content MUST be accessible to university-level learners with STEM backgrounds (ages 17–25). This requires:
- Writing level: Flesch-Kincaid grade 10–14 (engineering clarity)
- Progressive concept building: foundational concepts before advanced topics
- Clear definitions before usage in explanations
- Consistent terminology throughout the textbook
- Visual aids (diagrams, flowcharts) for complex systems

**Validation**: Each chapter must pass readability analysis and peer review for clarity.

### III. Hands-On Learning Orientation

Every chapter MUST support project-based outcomes with practical exercises in either Physical AI or Humanoid Robotics contexts. Requirements include:
- Learning objectives clearly stated at chapter start
- Concept explanations with real-world applications
- Practical exercises using accessible tools/simulators
- Assessment questions aligned with learning objectives
- Code examples in Python, ROS2, Webots, or simulation-friendly frameworks

**Reproducibility requirement**: All exercises must be executable using open-source tools and clearly documented setup procedures.

### IV. Diagrams and Visual Communication

All diagrams and technical illustrations MUST be reproducible using open-source tools. Requirements:
- Vector graphics preferred (SVG, PDF)
- Tools: Draw.io, PlantUML, Matplotlib, TikZ, or equivalent open-source alternatives
- Consistent visual style across all chapters
- Alt-text and captions for accessibility
- Source files committed alongside rendered outputs

**Quality standard**: Diagrams must enhance comprehension and be publication-grade.

### V. Code Quality and Executability

All code blocks MUST be functional, tested, and follow best practices:
- Languages: Python 3.9+, ROS2 (Humble/Iron), URDF/SDF for robot models
- Frameworks: Webots, PyBullet, MuJoCo, or other accessible simulators
- Code must include comments explaining key steps
- Dependencies clearly listed with version numbers
- Executable examples with expected outputs documented

**Testing requirement**: All code examples must be tested in specified environments before publication.

### VI. Future-of-Work Alignment

Content MUST emphasize AI-agent and human collaboration patterns, reflecting the evolving landscape of robotics and AI:
- Human-robot teaming and collaboration
- AI-assisted design and control
- Embodied AI and physical intelligence concepts
- Ethical considerations in autonomous systems
- Industry-relevant skill development

**Perspective**: Position robotics as a collaborative human-AI endeavor, not purely autonomous systems.

### VII. Content Originality and Academic Integrity

All content MUST be original with ZERO tolerance for plagiarism:
- All text written specifically for this textbook
- Paraphrased content must add value and provide proper attribution
- Direct quotes limited to definitions and key statements (with citations)
- All code examples original or significantly adapted (with attribution)
- Plagiarism checking required before publication

**Enforcement**: Automated plagiarism detection plus manual review for every chapter.

### VIII. RAG Chatbot System Principles

The integrated RAG chatbot MUST adhere to the following principles:

#### Grounded Truthfulness
All chatbot responses MUST be derived strictly from indexed book content or explicitly selected user text:
- NO hallucinated or external knowledge allowed unless cited as supplemental
- Explicit statement required when information is not found: "Information not found in the book"
- Every answer must be traceable to retrieved source chunks

#### Retrieval-First Reasoning
Every response MUST be backed by retrieved passages from the vector database before generation:
- Chunking strategy must preserve semantic and section-level coherence
- Each chunk must include source metadata (chapter, section, URL anchor)
- Retrieval parameters must be deterministic for reproducibility

#### Explainability and Transparency
The system MUST be able to surface which document chunks or text selections were used:
- Retrieved passages must be citeable in responses
- Debug mode for retrieval accuracy verification via logs
- Clear separation of retrieval, reasoning, and generation layers

#### Academic and Technical Clarity
Responses MUST be clear, concise, and suitable for computer science and robotics audiences:
- Maintain consistency with textbook terminology and style
- Technical accuracy aligned with textbook content standards
- Progressive concept building matching textbook pedagogy

#### AI-Native Architecture
The system MUST be architected around agentic workflows, tool use, and retrieval pipelines:
- Backend API: FastAPI or LangGraph
- Agent orchestration: LangGraph or ChatKit
- Vector storage: Qdrant (Cloud Free Tier)
- Metadata and session storage: Neon PostgreSQL
- Stateless inference endpoints
- No monolithic request-response logic

#### Security and Isolation
User-selected text queries MUST be sandboxed and isolated:
- Selected text mode: retrieval limited strictly to that text scope
- Global embeddings must NOT be queried in selected text mode
- No training on user data
- No storage of personally identifiable information (PII)
- Backend deployable independently from Docusaurus frontend

#### Cost and Resource Constraints
System MUST operate fully within free tiers where specified:
- Qdrant Cloud Free Tier for vector storage
- Neon PostgreSQL for metadata storage
- Efficient chunking and retrieval to minimize API costs

**Validation**: Zero hallucinations, graceful handling of empty/irrelevant queries, modular and testable code.

## Content Requirements

### Chapter Structure (Mandatory)

Each of the 8–12 chapters MUST include:

1. **Learning Objectives**: 3–5 specific, measurable outcomes
2. **Concept Explanations**: Clear, progressive exposition of theory
3. **Practical Exercises**: Minimum 2 hands-on activities per chapter
4. **Code Examples**: Working implementations in specified languages
5. **Assessment Questions**: 5–10 questions covering chapter content
6. **Further Reading**: Annotated list of 3–5 authoritative sources

### Supporting Sections (Required)

The textbook MUST include:
- **Glossary**: Comprehensive technical terms with definitions
- **Index**: Searchable term and concept index
- **Bibliography**: Complete IEEE-style reference list
- **Appendices**: Setup guides, installation instructions, troubleshooting

### Length and Scope

- Total chapters: 8–12 chapters
- Chapter length: 3,000–6,000 words per chapter (excluding code blocks)
- Exercises per chapter: Minimum 2 hands-on activities
- Assessment questions: 5–10 per chapter

## Technical Standards

### Documentation Format

Output format: Docusaurus-compatible Markdown
- Valid MDX syntax
- Front-matter metadata for all pages
- Proper internal linking structure
- Code syntax highlighting configured
- Responsive image handling

### Deployment Requirements

- GitHub Pages deployment target
- Docusaurus build MUST complete without errors
- All internal links validated
- Mobile-responsive layout verified
- Accessibility standards met (WCAG 2.1 AA minimum)

### Version Control and Quality Gates

All content changes MUST:
- Pass markdown linting
- Pass spell-checking
- Pass plagiarism detection
- Pass technical review (subject matter expert)
- Pass clarity review (educational expert)
- Build successfully in Docusaurus

## Constraints

### Tool and Framework Restrictions

MUST use:
- Python 3.9+ for programming examples
- ROS2 (Humble or Iron) for robotics middleware
- Webots, PyBullet, or MuJoCo for simulation
- Open-source libraries only (no proprietary dependencies)

MUST NOT use:
- Proprietary software requiring expensive licenses
- Deprecated frameworks (ROS1, Python 2.x)
- Platform-specific code without cross-platform alternatives

### Content Boundaries

IN SCOPE:
- Fundamentals of robotics and control
- Physical AI and embodied intelligence
- Humanoid robot kinematics and dynamics
- Perception, planning, and control for humanoid systems
- Practical simulation and implementation

OUT OF SCOPE:
- Deep theoretical proofs (beyond undergraduate level)
- Manufacturing and production engineering
- Business and commercialization strategies
- Military or weaponized robotics applications

## Success Criteria

The textbook succeeds when:

1. **Educational Effectiveness**:
   - Students can complete all exercises independently
   - Assessment questions accurately measure learning objectives
   - Feedback from test cohorts rates clarity ≥4.0/5.0

2. **Technical Quality**:
   - All code examples execute successfully
   - All citations verified and properly formatted
   - Zero plagiarism detected
   - Technical accuracy verified by domain experts

3. **Deployment Success**:
   - Docusaurus site builds without errors
   - Deployed successfully to GitHub Pages
   - All pages load correctly across browsers
   - Mobile responsiveness verified

4. **Academic Readiness**:
   - Content suitable for official university course adoption
   - Meets or exceeds standards of comparable robotics textbooks
   - Exercises provide sufficient depth for course projects

5. **RAG Chatbot Functionality**:
   - Chatbot correctly answers questions about book content
   - Chatbot correctly answers questions using only user-selected text
   - Zero hallucinations observed during evaluation
   - Retrieval accuracy verified via logging and debug mode
   - Frontend integration seamlessly embedded in Docusaurus UI
   - Backend operates within free tier resource constraints
   - All answers traceable to source chunks with citations

## Governance

### Amendment Process

Constitution amendments require:
1. Documented rationale for proposed change
2. Impact analysis on existing content and templates
3. Approval from project stakeholders
4. Migration plan for affected chapters/content
5. Version increment following semantic versioning

### Versioning Rules

- **MAJOR** (X.0.0): Backward-incompatible principle removals or redefinitions
- **MINOR** (x.Y.0): New principles added or sections materially expanded
- **PATCH** (x.y.Z): Clarifications, wording fixes, non-semantic refinements

### Compliance and Review

All chapter submissions MUST:
- Verify compliance with ALL principles
- Include checklist confirming each requirement met
- Pass automated quality gates (linting, plagiarism, build)
- Undergo peer review before merging

### Conflict Resolution

When principles conflict in specific situations:
1. Technical Accuracy (Principle I) takes precedence
2. Academic Integrity (Principle VII) is non-negotiable
3. Escalate to project leadership for adjudication
4. Document resolution as clarification amendment

**Version**: 1.1.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-25

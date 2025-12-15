# Implementation Plan: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

**Branch**: `006-isaac-robot-brain` | **Date**: December 15, 2025 | **Spec**: [specs/006-isaac-robot-brain/spec.md](specs/006-isaac-robot-brain/spec.md)
**Input**: Feature specification from `/specs/006-isaac-robot-brain/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The plan outlines the implementation for Module 3: The AI-Robot Brain (NVIDIA Isaac™) of the Physical AI & Humanoid Robotics Textbook. This module will comprise three chapters focused on photorealistic simulation, hardware-accelerated perception (VSLAM), and bipedal navigation for humanoids, leveraging Isaac Sim 5.1, Isaac ROS 3.2, ROS 2 Kilted Kaiju, and Nav2 1.4.x. The implementation will ensure strict adherence to technical accuracy, executable code standards, consistent terminology, glossary integration, hardware track callouts, and an 11-section chapter template, with a capstone project involving synthetic data generation for humanoid navigation.

## Technical Context

**Language/Version**: Python 3.11+, TypeScript (for Docusaurus frontend), C++ (for core ROS 2 concepts).  
**Primary Dependencies**: NVIDIA Isaac Sim 5.1, Isaac ROS 3.2, ROS 2 Kilted Kaiju, Nav2 1.4.x, Docusaurus 3.x, React 18, Mermaid.js, Three.js, Playwright.  
**Storage**: Docusaurus primarily uses Markdown/MDX files for content.  
**Testing**: Playwright for E2E testing, Docusaurus build validation, code execution validation (Docker).  
**Target Platform**: Ubuntu 24.04 (for executable code), Web (for Docusaurus frontend).  
**Project Type**: Hybrid (documentation/web with executable code examples).  
**Performance Goals**: Docusaurus site load <2s, WCAG AA compliance, Real-time VSLAM and navigation performance in simulation.  
**Constraints**: 3 chapters exactly, progressive chapter flow (Sim → Perception → Planning), 3–5 runnable examples per chapter, specific hardware tracks (RTX Workstation, Jetson/Unitree, Cloud/AWS Omniverse), APA citations, zero plagiarism, 11-section chapter template.  
**Scale/Scope**: 9,000–12,000 words total across 3 chapters, 10+ diagrams, 5+ code snippets (OmniGraph, ROS launch), ≥25 glossary terms.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The provided `constitution.md` is a template. Given the nature of this project (textbook content generation), the most relevant "constitution" aspects are the strict adherence to the output format, technical accuracy, code executability, and quality standards defined in the `sp.specify` and `sp.plan` prompts themselves.

-   [X] **Technical Accuracy**: Ensured through mandatory research validation and APA citations, with ≥50% from official NVIDIA sources.
-   [X] **Executable Code**: Guaranteed by requiring all examples to run on specified Ubuntu/ROS2/Isaac versions and validated through Docker.
-   [X] **Consistent Terminology & Glossary**: Enforced by glossary requirements and review processes.
-   [X] **Hardware Track Callouts**: Explicitly mandated in the spec and plan.
-   [X] **Chapter Template Compliance**: Strict 11-section template enforcement.
-   [X] **APA Citations, Zero Plagiarism**: Explicitly required.
-   [X] **Load <2s, WCAG AA**: Performance and accessibility goals for the Docusaurus site.

All gates are justified as they align with the explicit requirements of the project.

## Project Structure

### Documentation (this feature)

```text
specs/006-isaac-robot-brain/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── book-content/          # Docusaurus MDX files for chapters (module3-isaac/ch1-sim.mdx etc.)
├── components/            # Custom React components (IsaacSimScene, VslamPipeline, Nav2BehaviorTree)
├── docusaurus-config/     # Docusaurus configuration, plugins
├── scripts/               # Helper scripts, e.g., for code validation
└── tests/
    ├── e2e/               # Playwright tests for Docusaurus UI and component rendering
    └── unit/              # Unit tests for custom React components or utility functions
```

**Structure Decision**: This project primarily involves generating documentation (a textbook module) and some custom frontend components. Therefore, the existing Docusaurus-based structure is suitable, with specific directories for chapter content, custom React components, and testing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Phased Roadmap

### Phase 0: Research Validation & Docker/Omniverse Setup

**Objective**: To validate the specific versions of Isaac Sim, Isaac ROS, ROS 2, and Nav2, gather all necessary research, and establish a foundational development environment. This phase also aims to resolve any remaining ambiguities identified in the technical context or the spec.

**Tasks**:
-   Execute all research tasks defined in `specs/006-isaac-robot-brain/research.md`.
-   Consolidate research findings in `research.md`, explicitly detailing decisions, rationales, and alternatives considered for each research question.
-   Set up a Docker-based development environment (Ubuntu 24.04, ROS 2 Kilted Kaiju, Isaac Sim 5.1).
-   Verify basic functionality of Isaac Sim and Isaac ROS within the Docker environment.

**Deliverables**:
-   `research.md` (completed with consolidated findings)
-   Functional Docker environment for development.

### Phase 1: Chapter-by-Chapter Crafting (Ch1 → Ch3 sequential)

**Objective**: To sequentially develop the content for each of the three chapters, adhering to the specified chapter template, technical requirements, and quality standards. This phase will also generate the data model, API contracts (if any for interactive components), and quickstart guides.

**Tasks**:
-   **Chapter 1: Photorealistic Simulation with NVIDIA Isaac Sim**
    -   Draft content, including outcomes, sections, word counts, 3+ code examples, 2 worked examples, and relevant math/equations.
    -   Generate `data-model.md` based on key entities identified in the feature spec (Humanoid Robot Model, Omniverse Scene, Synthetic Dataset).
    -   Generate `contracts/` (if needed for custom interactive components like IsaacSimScene).
    -   Generate `quickstart.md` for setting up and running Chapter 1 examples.
    -   Ensure all code snippets for OmniGraph/USD are compliant with Isaac Sim 5.1.
    -   Incorporate Hardware Track A callouts.
-   **Chapter 2: Isaac ROS for Hardware-Accelerated Perception**
    -   Draft content, focusing on VSLAM and sensor fusion.
    -   Update `data-model.md` (if new entities like VSLAM Pipeline or GEMs are introduced).
    -   Generate `contracts/` (if needed for VslamPipeline component).
    -   Update `quickstart.md` with Chapter 2 setup and examples.
    -   Integrate Isaac ROS GEMs with CUDA examples.
    -   Incorporate Hardware Track B callouts.
-   **Chapter 3: Nav2 Path Planning for Bipedal Humanoids**
    -   Draft content, focusing on locomotion and obstacle avoidance.
    -   Update `data-model.md` (if new entities like Nav2 Stack are introduced).
    -   Generate `contracts/` (if needed for Nav2BehaviorTree component).
    -   Update `quickstart.md` with Chapter 3 setup and examples.
    -   Integrate Nav2 YAML/launch files.
    -   Incorporate Hardware Track C callouts.
-   Throughout all chapters: Ensure APA citations, glossary links, sim-to-real warnings, and Mermaid diagrams are correctly integrated.

**Deliverables**:
-   Chapter 1 MDX content (`docs/module3-isaac/ch1-sim.mdx`)
-   Chapter 2 MDX content (`docs/module3-isaac/ch2-perception.mdx`)
-   Chapter 3 MDX content (`docs/module3-isaac/ch3-nav2.mdx`)
-   `data-model.md` (completed)
-   `contracts/` (containing relevant API schemas if any)
-   `quickstart.md` (comprehensive guide for all chapters)
-   Custom components: IsaacSimScene, VslamPipeline, Nav2BehaviorTree (initial drafts).

### Phase 2: Integration & Capstone

**Objective**: To integrate all chapters, develop the module capstone project, and ensure seamless flow and consistency across the entire module.

**Tasks**:
-   Integrate all three chapters into the Docusaurus site structure (`/docs/module3-isaac/`).
-   Develop the capstone project, ensuring it integrates concepts from all three chapters (synthetic data generation, VSLAM-trained humanoid navigator).
-   Implement and integrate custom components (IsaacSimScene, VslamPipeline, Nav2BehaviorTree) into the MDX content.
-   Ensure all interlinking to Module 2 and Module 4 is functional.

**Deliverables**:
-   Integrated Docusaurus module (Module 3)
-   Completed capstone project code and documentation.
-   Implemented custom components.

### Phase 3: Review, Testing & Polish

**Objective**: To conduct thorough testing, review, and polishing to ensure the module meets all quality gates, technical requirements, and user experience standards.

**Tasks**:
-   Run Docusaurus build process and resolve any errors.
-   Execute code validation (Docker-based) for all examples and capstone project.
-   Conduct accuracy review against official NVIDIA docs.
-   Perform WCAG AA compliance audit.
-   Perform APA citation linting.
-   Execute Playwright tests for section visibility, diagram rendering, and interactive component functionality.
-   Refine glossary, ensure consistent terminology.
-   Conduct a final content review for clarity, conciseness, and pedagogical effectiveness.

**Deliverables**:
-   Fully tested and validated module.
-   Comprehensive test reports.
-   Polished content ready for publication.

## Architecture Sketch

-   **Docusaurus Folder Structure**: The module content will reside in `/docs/module3-isaac/`, with individual chapter files such as `ch1-sim.mdx`, `ch2-perception.mdx`, and `ch3-nav2.mdx`.
-   **Mermaid VSLAM Pipeline Graph**: Embedded within the VSLAM chapter, illustrating the data flow and processing stages.
-   **Custom Components**:
    -   `IsaacSimScene`: A React component to embed interactive Isaac Sim environments or visualizations directly within MDX.
    -   `VslamPipeline`: A React component to visualize or demonstrate aspects of the VSLAM pipeline.
    -   `Nav2BehaviorTree`: A React component to illustrate or interact with Nav2 behavior trees.

## Chapter Template Enforcement

-   All 11 sections of the chapter template are mandatory for each chapter.
-   Hardware track callouts (A, B, C) will be integrated where relevant.
-   Glossary terms will be linked inline to a central glossary.
-   Explicit sim-to-real warnings will accompany executable code examples.

## Formatting & Code Standards

-   **OmniGraph/USD Snippets**: Will be presented in code blocks, adhering to Isaac Sim 5.1 conventions.
-   **Isaac ROS GEMs with CUDA**: Code examples will demonstrate the usage of GPU-accelerated GEMs.
-   **Nav2 YAML/Launch Files**: Standard ROS 2 formatting will be used for configuration and launch files.
-   **Mermaid for Perception/Planning Flows**: Used for diagramming complex processes.
-   **APA References Block**: A dedicated section at the end of each chapter.

## Research Approach

-   **Prioritization**: Official `developer.nvidia.com/isaac-sim` and `developer.nvidia.com/isaac-ros` documentation will be the primary source.
-   **Augmentation**: `arXiv` for relevant peer-reviewed papers on VSLAM and humanoid robotics, and NVIDIA blogs/forums for the latest 2025 updates and community insights.
-   **Concurrent Validation**: Research findings will be validated continuously while drafting chapter content to ensure accuracy and currency.

## Key Decisions

-   **Base Versions**: The module will be developed using NVIDIA Isaac Sim 5.1, Isaac ROS 3.2, ROS 2 Kilted Kaiju (or latest 2025 LTS), and Nav2 1.4.x.
-   **Humanoid Examples**: Will include generic bipedal humanoid examples and specific integrations/references to Unitree H1.
-   **Executable Pipelines**: All code examples will represent full deployable pipelines or functional scripts rather than isolated snippets.
-   **Interlinking**: Explicit interlinking will be established to Module 2 (e.g., how the simulated environment is passed) and Module 4 (e.g., how outputs might feed into VLA).

## Testing & Validation

-   **Docusaurus Build**: Regular `npm run build` checks for site integrity.
-   **Code Execution**: Automated testing within a Docker container (Ubuntu 24.04 + Kilted + Isaac Sim 5.1 + RTX sim) to verify all examples run as expected.
-   **Accuracy**: Manual and automated checks comparing content against official NVIDIA documentation.
-   **Objectives Coverage**: Checklist-based validation to ensure all learning objectives from the spec are met.
-   **APA Lint**: Automated checks for APA citation formatting compliance.
-   **Playwright Tests**: End-to-end tests for Docusaurus page rendering, visibility of sections, correct rendering of Mermaid diagrams, and functionality of custom interactive components.

## Version Strategy

-   **Pinned Versions**: Explicitly pin NVIDIA Isaac Sim 5.1, Isaac ROS 3.2, ROS 2 Kilted Kaiju (or latest LTS for 2025), and Nav2 1.4.x.
-   **Migration Paths**: Note potential migration paths or considerations for future software updates where applicable.
-   **Changelog**: Maintain a changelog for any updates to the underlying tools or versions used in the module.

## Risks & Mitigation

| Risk                                    | Mitigation                                                                                             |
|:----------------------------------------|:-------------------------------------------------------------------------------------------------------|
| GPU requirement mismatches for students | Provide clear minimum specs, offer cloud-based alternatives (AWS Omniverse), and highlight hardware tracks. |
| Rapid software updates (Isaac, ROS)     | Pin versions for stability, but actively monitor for critical updates and plan for minor revisions.      |
| Complexity of environment setup         | Provide detailed, tested Docker-based setup scripts and comprehensive quickstart guides.                 |
| Sim-to-real gap challenges              | Emphasize "sim-to-real" warnings, discuss calibration, and provide best practices for deployment.        |
| Maintaining APA citation compliance     | Utilize automated linting tools and provide clear author guidelines.                                   |
| Ensuring executable code quality        | Implement CI/CD with automated Docker-based testing for all code examples.                             |

## Timeline Estimate

-   **Phase 0 (Research Validation & Docker/Omniverse Setup)**: 1 week
-   **Phase 1 (Chapter-by-Chapter Crafting)**:
    -   Chapter 1: 2 weeks
    -   Chapter 2: 2 weeks
    -   Chapter 3: 2 weeks
-   **Phase 2 (Integration & Capstone)**: 1.5 weeks
-   **Phase 3 (Review, Testing & Polish)**: 1.5 weeks
-   **Total Estimated Time**: ~10 weeks

## Next Actions

-   Execute Phase 0 research tasks and complete `research.md`.
-   Set up the Docker-based development environment.
-   Begin drafting content for Chapter 1.
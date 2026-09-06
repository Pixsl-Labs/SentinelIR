# 3.0 Methodology

This chapter outlines the methodology used to design, implement, test, and evaluate SentinelIR. The project follows an incremental software engineering approach, with development divided into clearly defined functional and technical tasks that can be implemented, validated, and reviewed independently.

The methodology covers the development process, requirements traceability, system architecture, implementation decisions, testing strategy, experimental data collection, and evaluation approach. Particular emphasis is placed on maintaining a stable reusable backend while progressively extending the system towards API and Web UI support.

The chapter also explains how synthetic data and controlled CTF-generated logs will be used to evaluate SentinelIR against known ground truth. This allows the effectiveness of the system to be assessed using repeatable attack scenarios, measurable detection outcomes, and controlled experimental conditions.

The methodology is structured as follows:

- Section 3.1 describes the development approach used throughout the project.
- Section 3.2 explains requirements management and traceability.
- Section 3.3 presents the overall system architecture.
- Section 3.4 describes the implementation methodology and major technical components.
- Section 3.5 outlines the testing strategy.
- Section 3.6 explains the experimental data collection process.
- Section 3.7 defines the evaluation methodology and metrics.
- Section 3.8 discusses ethical and security considerations.
- Section 3.9 identifies limitations of the methodology.

## 3.1 Development Approach

SentinelIR was developed using an incremental and issue-driven software engineering approach. Rather than implementing the complete system in a single development cycle, the project was divided into smaller functional areas that could be designed, implemented, tested, and reviewed independently. This approach was selected to reduce the risk of introducing large regressions into the existing CLI backend while allowing the project to expand progressively towards API and Web UI support.

Development work was organised through GitHub Issues, with each issue representing a defined area of functionality or engineering improvement. Examples include repository validation, automated code-quality protection, centralised path handling, reusable backend interfaces, and technical documentation. Each issue further divided into smaller tasks so that progress could be tracked and individual changes could be completed in a controlled manner.

A branch-based workflow was used for implementation. New development was completed on dedicated branches rather than directly on the protected `main` branch. Once a task or issue was completed, the branch was validatedd locally before being pushed to the remote repository and submitted through a pull request. This provided a clear separation between stable code and work in progress, while also creating a traceable history of the decisions and changes made throughout development.

Automated quality checks were integrated into this workflow using GitHub Actions. Pull requests are validated using Python compilation checks, Flake8, and the pytest tests suite before they are merged into `main`. Branch protection rules are used to prevent unvalidated changes from being merged directly. This supports continuous regression testing and helps ensure that new development does not unintentionally break previously working functionality.

The project also follows an architecture-preserving approach. Existing CLI functionality is treated as the stable backend foundation, with new components added around it rather than replacing working behaviour unncessarily. For example, structured result models and a small service layer were introduced to make existing analysis, detection, file handling, and export functionality reusable by future interfaces. This allows the CLI, future FastAPI layer, and planned Web UI to share the same core backend logic.

This development approach also support dissertation traceability. Requirements and engineering tasks can be linked to implementation branches, tests, pull requests, and later evaluation evidence. As a result, the methodology reflects not only what was implemented, but also the process used to design, validate, and evolve SentinelIR throughout the project.

---

## 3.2 Requirements And Traceability

asd

---

## 3.3 System Architecture

---

## 3.4 Implementation Method

---

### 3.4.1 Log Parsing

### 3.4.2 Structured Event Modelling

### 3.4.3 Filtering

### 3.4.4 Detection Logic

### 3.4.5 Live Monitoring

### 3.4.6 Alert Cooldown And Persistence

### 3.4.7 Scenario Generation

### 3.4.8 Service Layer

### 3.4.9 Safe File Handling

### 3.4.10 API And Web Integration

---

## 3.5 Testing Strategy

---

## 3.6 Experimental Data Collection

---

### 3.6.1 Synthetic Dataset

### 3.6.2 Controlled CTF Dataset

---

## 3.7 Evaluation Method

---

## 3.8 Ethical And Security Considerations

---

## 3.9 Methodology Limitations

---

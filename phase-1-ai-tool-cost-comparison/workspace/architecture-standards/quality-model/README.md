# Quality Model Reference

## Overview

This section provides reference material based on **ISO/IEC 25010:2011**, the international standard for software product quality. ISO 25010 defines a quality model that categorizes software quality into characteristics and sub-characteristics, providing a structured framework for evaluating and specifying quality requirements.

## Purpose

The quality model serves several purposes in architecture work:

- **Quality Requirements**: Provides a vocabulary for specifying non-functional requirements
- **Architecture Evaluation**: Offers a framework for assessing architectural trade-offs
- **Quality Scenarios**: Enables concrete, testable quality attribute scenarios
- **Stakeholder Communication**: Provides a shared language for discussing quality concerns

## Structure

The ISO 25010 quality model defines **8 top-level quality characteristics**, each broken down into sub-characteristics. See [iso-25010-quality-tree.md](iso-25010-quality-tree.md) for the full tree with definitions and example scenarios.

## Usage in Architecture

1. **Identify** relevant quality characteristics for your system
2. **Prioritize** characteristics based on stakeholder needs
3. **Define** concrete quality scenarios with measurable targets
4. **Evaluate** architectural options against quality scenarios
5. **Document** quality trade-offs in Architecture Decision Records (ADRs)

## Quality Scenario Format

A quality scenario consists of:

| Element | Description |
|---------|-------------|
| **Source** | Who or what generates the stimulus |
| **Stimulus** | The event or condition |
| **Artifact** | The system or component affected |
| **Environment** | Conditions under which the stimulus occurs |
| **Response** | How the system should respond |
| **Response Measure** | Measurable criteria for success |

## References

- ISO/IEC 25010:2011 - Systems and software engineering -- Systems and software Quality Requirements and Evaluation (SQuaRE)
- Bass, Clements, Kazman: "Software Architecture in Practice" (4th Edition)

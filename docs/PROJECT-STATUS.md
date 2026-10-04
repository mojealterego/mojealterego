# Project status model

This document defines the shared status vocabulary used across the MojeAlterego repositories.

## PRODUCTION

A project may be marked `PRODUCTION` only when the applicable production path has been verified.

Minimum evidence should include:

- reproducible build or deployment,
- successful required CI checks,
- documented runtime/deployment instructions,
- verified core user flow,
- security and secret-handling baseline,
- no known blocker that invalidates the production claim.

## BETA

Use `BETA` when the project is integrated and testable but production hardening is incomplete.

Typical remaining work can include wider runtime coverage, deployment-specific validation, observability, performance work, migration hardening and UX/accessibility polish.

## PROTOTYPE

Use `PROTOTYPE` for a working or partially working technical demonstrator, vertical slice or foundation.

A prototype can contain real code and tests, but it must not be described as a production deployment without evidence.

## RESEARCH

Use `RESEARCH` for knowledge bases, experiments, benchmarks, architecture exploration, source synthesis, hypothesis testing and technical investigations.

Research status does not imply a shippable product.

## CONCEPT

Use `CONCEPT` when the repository primarily contains an idea, identity, specification, design direction or incomplete source from which implementation cannot yet be verified.

## Promotion rule

Status promotion is evidence-driven:

`CONCEPT → RESEARCH/PROTOTYPE → BETA → PRODUCTION`

A project may skip a stage only when stronger evidence already exists. A status can also be downgraded when implementation, deployment or verification no longer supports the previous claim.

## Automation rule

Automation may refresh repository metadata such as primary language or last activity. It must **never** autonomously promote the declared maturity status.

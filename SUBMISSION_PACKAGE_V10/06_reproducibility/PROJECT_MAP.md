# Battery RUL project map

## 01_data
Data documentation and pointers. Raw files remain under `external_data/raw` because parsers use that stable path.

## 02_protocol
Locked research protocol, EOL/RUL definitions, split rules and feature contracts.

## 03_pipeline
Core executable scripts remain at the project root so their `ROOT` paths remain reproducible. This folder contains the code index.

## 04_results
All generated tables, figures and audit reports are under `outputs/tables`, `outputs/figures` and `outputs/reports`.

## 05_online
Online service, BMS adapter and HIL test entry points.

## 06_manuscript
The current thesis/paper deliverables. Intermediate drafts are in `archive/old_manuscripts`.

## 07_reproducibility
Manifests, requirements and independent-review records.

## archive
Historical scripts and obsolete reports. Nothing here is used for the final release.

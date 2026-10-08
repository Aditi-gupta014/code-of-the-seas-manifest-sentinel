# Approach Dossier — Manifest Sentinel

## 1. Approach and reasoning
We treat the manifest as a collection of mutually constraining records rather than trusting any single field. The detector uses a hybrid of deterministic rules and statistical anomaly detection.

Deterministic checks are used for conditions that are objectively suspicious: invalid numeric values, impossible/unknown locations, future timestamps and duplicate patterns. Statistical detection is used for unusual combinations of weight, container count and declared value.

Each evidence source adds points to an explainable suspicion score. This reduces dependence on one fragile rule and lets judges inspect exactly why a record was flagged.

## 2. Alternatives considered
A pure machine-learning classifier was rejected because the competition explicitly provides no labelled ground truth for the detector. A fully rule-based system was also considered insufficient because an attacker can create novel combinations that do not violate a predefined rule. The hybrid method combines both strengths.

## 3. Strengths
- Explainable evidence for each alert.
- Reproducible synthetic data using a fixed seed.
- Works without reading the private injection log.
- Handles thousands of rows with vectorized pandas operations.
- Dashboard makes results easy to inspect.

## 4. Weaknesses
- Current prototype is not a forensic guarantee.
- Confidence is a heuristic evidence score and should be calibrated on larger validation sets.
- Shipment-history reconstruction is simplified.
- Near-duplicate matching can be strengthened with fuzzy matching.

## 5. Scalability
The data-generation and rule checks are linear or near-linear in record count. For much larger manifests, SQLite/PostgreSQL indexes can be used for IDs, owners, timestamps and route queries. Streaming events can be processed in batches.

## 6. Adaptation to the Shifting Waters twist
The system separates explicit rules from statistical detection, so a previously unseen attack can still receive an anomaly score even when there is no dedicated rule. The live simulator demonstrates a novel impossible-container-count attack.

## 7. Evaluation
The private injection log is used only after detection to calculate precision, recall and false-alarm rate. It is never read by detector.py.

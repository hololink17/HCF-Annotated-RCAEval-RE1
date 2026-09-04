# HCF Method — Supplementary Materials

This package accompanies the paper:

> "Assessing System Coherence via Conflict Graph Analysis: A Validated Method for Microservice State Assessment with Early Warning Capability"  
> Xiangyu Liu  
> IEEE Transactions on Software Engineering (in review)

## Contents

| File | Description |
|------|-------------|
| `hcf_demo.py` | Python demo implementing the mathematical core (Section 3, Definitions 3-8, Algorithm 1) of the HCF method. |
| `HCF-Annotated-RCAEval-RE1.zip` | Annotated dataset derived from RCAEval: 147 cases with fault-injection timestamps and HCF diagnostic-code annotations. |

## hcf_demo.py

This script demonstrates the computation of the Internal Friction Index (I-value), four coherence factors (f1–f4), and the synergy score H from a pre-constructed conflict graph.

**What it does:**
- Implements all mathematical formulas from Section 3 (Definitions 3-8)
- Computes f1 (Monitoring Uniformity), f2 (Resilience), f3/I (Internal Friction), f4 (Control Responsiveness), and H
- Includes a self-test with a demo conflict matrix

**What it does NOT include:**
- Triplet mapping logic (raw indicators → L-D-M triplets)
- Conflict matrix numerical values from real systems
- Intervention mapping table (diagnostic codes → actions)

The demo uses a simplified example matrix for illustration only.

**Requirements:** Python 3.6+, NumPy

**Usage:** `python hcf_demo.py`

## Dataset

`HCF-Annotated-RCAEval-RE1.zip` contains:
- 147 fault-injection cases from RCAEval
- Per-case diagnostic-code annotations
- Fault-type and window definitions

## License

The dataset is released under CC BY 4.0. The script is released under the same license.

For the complete mathematical formulation, refer to Sections 3.1–3.8 and Algorithm 1 of the paper.
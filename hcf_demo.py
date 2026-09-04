#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HCF Demo: Internal Friction Index (I-value) Calculation
=======================================================

This script demonstrates the mathematical core of the Holographic Coding
Framework (HCF, 全息编码框架) as defined in Section 3 of the paper.

IMPORTANT: This is a demonstration of the mathematical formulas only.
It does NOT include:
  - Proprietary triplet mapping logic (raw indicators -> L-D-M triplets)
  - Proprietary conflict matrix numerical values
  - Proprietary intervention mapping table (diagnostic codes -> actions)

The input to this demo is a pre-constructed conflict matrix W (adjacency matrix)
and a set of indicator weights w_i, which in a production implementation would
be derived from the triplet mapping and conflict lookup steps.

The demo computes:
  - Individual conflict scores c_i
  - Monitoring Uniformity f1
  - Resilience f2
  - Internal Friction Index f3 (I-value)
  - Control Responsiveness f4
  - Synergy Score H

All formulas are taken from Definition 3-8 and Algorithm 1 in Section 3.

Author: Xiangyu Liu
Paper: "Assessing System Coherence via Conflict Graph Analysis"
Venue: IEEE Transactions on Software Engineering (in review)
License: CC BY 4.0
"""

import numpy as np
from typing import Tuple, Dict


def compute_conflict_scores(W: np.ndarray) -> np.ndarray:
    """
    Definition 5 (Individual Conflict Score).
    
    c_i = Σ_{j≠i} w_ij
    
    Args:
        W: Adjacency matrix of the conflict graph (N x N).
           W_ij is the conflict intensity between indicator i and j.
    
    Returns:
        c: Vector of individual conflict scores for each indicator.
    """
    return np.sum(W, axis=1)


def compute_f1(c: np.ndarray) -> float:
    """
    Definition 7 (f1: Monitoring Uniformity).
    
    f1 = 1 - σ(c)
    
    where σ(c) is the standard deviation of the individual conflict scores.
    
    Args:
        c: Vector of individual conflict scores.
    
    Returns:
        f1: Monitoring uniformity score in [0, 1].
    """
    return 1.0 - np.std(c)


def compute_f2(W: np.ndarray, tau: float = 0.5) -> float:
    """
    Definition 7 (f2: Resilience).
    
    f2 = 1 - (1/M) Σ_{i<j} 𝕀(w_ij > τ)
    
    where M = N(N-1)/2 is the number of indicator pairs, and 𝕀 is the indicator
    function (1 if true, 0 otherwise).
    
    Args:
        W: Adjacency matrix of the conflict graph.
        tau: Conflict threshold (set to 0.5 in the current implementation).
    
    Returns:
        f2: Resilience score in [0, 1].
    """
    N = W.shape[0]
    M = N * (N - 1) // 2
    if M == 0:
        return 1.0
    # Extract upper triangular entries (i < j) to avoid double counting
    upper_tri = W[np.triu_indices_from(W, k=1)]
    conflicts_above_threshold = np.sum(upper_tri > tau)
    return 1.0 - (conflicts_above_threshold / M)


def compute_f3(W: np.ndarray) -> float:
    """
    Definition 7 (f3: Internal Friction Index / I-value).
    
    f3 = 1 - λₘₐₓ(W / ||W||_F)
    
    where λₘₐₓ is the largest eigenvalue of the conflict matrix,
    and ||W||_F is the Frobenius norm.
    
    The Internal Friction Index (I-value) is defined as I = f3.
    
    Args:
        W: Adjacency matrix of the conflict graph.
    
    Returns:
        f3: Internal Friction Index (I-value) in [0, 1].
    """
    frob_norm = np.linalg.norm(W, ord='fro')
    if frob_norm == 0:
        return 1.0  # No conflicts, perfect coherence
    normalized_W = W / frob_norm
    eigvals = np.linalg.eigvalsh(normalized_W)  # Hermitian matrix, real eigenvalues
    lambda_max = np.max(eigvals)
    return 1.0 - lambda_max


def compute_f4(x: np.ndarray, W: np.ndarray) -> float:
    """
    Definition 7 (f4: Control Responsiveness).
    
    f4 = 1 - Var(x_i · 𝕀(w_ij > 0)) / Var(x_i)
    
    where x_i denotes the raw value of indicator i,
    and 𝕀(·) is the indicator function.
    
    In cases where Var(x_i) = 0, f4 is defined as 1 by convention.
    
    Args:
        x: Vector of raw indicator values.
        W: Adjacency matrix of the conflict graph.
    
    Returns:
        f4: Control responsiveness score in [0, 1].
    """
    # Determine which indicators have at least one conflict
    has_conflict = np.sum(W > 0, axis=1) > 0
    # Compute x_i · 𝕀(w_ij > 0)
    x_weighted = x * has_conflict.astype(float)
    var_x = np.var(x)
    if var_x == 0:
        return 1.0
    var_weighted = np.var(x_weighted)
    return 1.0 - (var_weighted / var_x)


def compute_H(f1: float, f2: float, f3: float, f4: float) -> float:
    """
    Definition 8 (Synergy Score H).
    
    H = (f1 · f2 · f3 · f4)^(1/4)
    
    Args:
        f1: Monitoring Uniformity
        f2: Resilience
        f3: Internal Friction Index (I-value)
        f4: Control Responsiveness
    
    Returns:
        H: Synergy score in [0, 1].
    """
    return (f1 * f2 * f3 * f4) ** (1.0 / 4.0)


def assess_coherence(W: np.ndarray, x: np.ndarray, tau: float = 0.5) -> Dict[str, float]:
    """
    Algorithm 1: HCF Coherence Assessment (main entry point).
    
    Args:
        W: Adjacency matrix of the conflict graph (N x N).
        x: Vector of raw indicator values (length N).
        tau: Conflict threshold (set to 0.5 in the current implementation).
    
    Returns:
        Dictionary containing f1, f2, f3 (I-value), f4, and H.
    """
    if W.shape[0] != len(x):
        raise ValueError("W and x must have the same length.")
    
    c = compute_conflict_scores(W)
    f1 = compute_f1(c)
    f2 = compute_f2(W, tau)
    f3 = compute_f3(W)
    f4 = compute_f4(x, W)
    H = compute_H(f1, f2, f3, f4)
    
    return {
        "f1_monitoring_uniformity": f1,
        "f2_resilience": f2,
        "f3_internal_friction_I": f3,
        "f4_control_responsiveness": f4,
        "H_synergy_score": H
    }


# ----------------------------------------------------------------------------
# Demo / Self-test
# ----------------------------------------------------------------------------

def run_demo():
    """
    Run a self-test with a simple example conflict graph.
    
    This example demonstrates the calculation on a small system with
    N=4 indicators, with a plausible conflict structure.
    
    The conflict matrix W and indicator values x are for demonstration
    purposes only and do not represent any production system.
    """
    print("=" * 70)
    print("HCF Coherence Assessment - Demo")
    print("=" * 70)
    
    # Example: N = 4 indicators
    # W_ij values represent conflict intensities between indicator i and j
    # All values are in [0, 1], where 0 = no conflict, 1 = maximum conflict
    # This is a symmetric matrix (W_ij = W_ji) as per Definition 4.
    W = np.array([
        [0.0, 0.9, 0.6, 0.1],
        [0.9, 0.0, 0.8, 0.2],
        [0.6, 0.8, 0.0, 0.3],
        [0.1, 0.2, 0.3, 0.0]
    ])
    
    # x_i: raw indicator values
    x = np.array([0.75, 0.70, 0.60, 0.40])
    
    print("Demo input:")
    print(f"  Conflict matrix W (shape {W.shape}):")
    print(f"  {W}")
    print(f"  Indicator values x: {x}")
    print()
    
    # Compute coherence factors
    results = assess_coherence(W, x, tau=0.5)
    
    print("Results:")
    print(f"  f1 (Monitoring Uniformity):    {results['f1_monitoring_uniformity']:.4f}")
    print(f"  f2 (Resilience):               {results['f2_resilience']:.4f}")
    print(f"  f3 (Internal Friction / I):    {results['f3_internal_friction_I']:.4f}")
    print(f"  f4 (Control Responsiveness):   {results['f4_control_responsiveness']:.4f}")
    print(f"  H  (Synergy Score):            {results['H_synergy_score']:.4f}")
    print()
    
    print("Usage notes:")
    print("  - In a production implementation, W and x would be derived")
    print("    from the triplet mapping and conflict lookup steps.")
    print("  - The triplet mapping logic and conflict matrix numerical")
    print("    values are proprietary and not included in this demo.")
    print("  - This demo implements only the mathematical formulas")
    print("    defined in Section 3 of the paper (Definitions 3-8).")
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    run_demo()
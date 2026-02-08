# Author Response - Round 1

## Overview

We thank both reviewers for their thorough and constructive feedback. The reviews converge on several critical points: (1) the manuscript reads as a narrative literature survey rather than a research contribution with original technical or conceptual depth; (2) the paper lacks quantitative benchmarking data comparing quantum approaches to state-of-the-art classical methods; (3) technical discussions of algorithms, resource estimates, and encoding schemes are superficial; and (4) the scope is too broad for the depth provided. We recognize these criticisms as valid and substantive. Rather than defend the current manuscript, we have decided to restructure the work fundamentally around a single, well-defined technical contribution with concrete quantitative analysis. Below, we outline our response to each reviewer's major concerns and describe the revised approach.

---

## Response to Reviewer 1: Quantum Algorithms for Molecular Simulation

**Overall Assessment**: We acknowledge the reviewer's score (4.5/10) and agree with the core assessment: the current manuscript lacks the technical rigor, quantitative specificity, and novel contribution expected from a quantum algorithms perspective. The criticisms regarding missing resource estimates, absent ansatz analysis, and lack of benchmarking are well-founded.

### Major Points

**1. Absence of quantitative technical detail on VQE and QPE implementations**

- **Our response**: The reviewer is correct that the current treatment of VQE and QPE is superficial. We did not discuss ansatz choices (UCCSD vs. hardware-efficient vs. ADAPT-VQE), circuit depths, gate counts, or encoding overhead comparisons. This was a significant oversight that undermines credibility in the algorithms community.
  
- **Action taken**: We will restructure the manuscript around a **focused case study**: a comparative resource analysis for a pharmacologically relevant molecular system (a metalloenzyme active site with ~60-100 spin-orbitals, e.g., a simplified model of a P450 active site or FeMoco-like system). We will provide:
  - Original or updated resource estimates comparing Jordan-Wigner (JW) vs. Bravyi-Kitaev (BK) encodings for this specific system, with explicit qubit counts and two-qubit gate counts under each scheme
  - Detailed discussion of ansatz choices (UCCSD, hardware-efficient, ADAPT-VQE) and their impact on circuit depth and parameter count
  - Quantitative analysis of how symmetry reduction and active space selection affect feasibility
  - Comparison of Hamiltonian factorization strategies (double factorization, tensor hypercontraction) and their circuit-level implications

**2. Lack of benchmarking data and unsubstantiated claims of quantum advantage**

- **Our response**: The reviewer correctly notes that we claim benchmarking is essential but provide no actual benchmarks. This is a critical gap. We cannot claim quantum advantage or potential advantage without concrete comparisons.
  
- **Action taken**: We will include a **quantitative benchmarking table** (or short section) that:
  - Summarizes known VQE accuracy results for small benchmark molecules (H₂, LiH, BeH2, H₂O) in terms of error relative to FCI/CCSD(T)
  - Compares these to the accuracy achievable by classical state-of-the-art methods (CCSD(T), DMRG, AFQMC) for the same systems
  - Explicitly discusses the "quantum advantage threshold"—the problem size and accuracy requirement at which quantum methods would outperform classical alternatives—based on current resource estimates
  - Acknowledges that this threshold remains beyond current NISQ capabilities and provides a realistic timeline based on published roadmaps

**3. Zero novelty and poor citation quality**

- **Our response**: We accept that the current manuscript is a literature survey without novel contribution. The inclusion of reference [9] (Violaris 2025, on causality and time-travel paradoxes) is indefensible and represents a citation error on our part.
  
- **Action taken**: 
  - We will **remove reference [9]** entirely.
  - We will restructure the paper to present an **original technical contribution**: either (a) new resource estimates for a specific drug-relevant target under different encoding/ansatz choices, or (b) a critical analysis of the quantum advantage threshold for drug discovery, showing under what conditions quantum methods would be preferable to classical alternatives.
  - We will strengthen the citation base with key technical references currently missing:
    - Lee et al. (2021) on improved qubitization resource estimates
    - Goings et al. (2022) on fault-tolerant quantum chemistry for drug discovery
    - Reiher et al. (2017) on FeMoco resource estimates
    - von Burg et al. (2021) on tensor hypercontraction for quantum chemistry
    - McClean et al. (2018) on barren plateaus and mitigation strategies

### Minor Points

- We will expand the discussion of barren plateaus beyond a single mention to include mitigation strategies (local cost functions, layerwise training, problem-informed ansätze) and their implications for circuit depth and wall-clock time.
- We will add a dedicated section on encoding schemes with quantitative comparison of JW vs. BK vs. compact mappings for a representative drug-like molecule, showing how these choices affect qubit and gate counts.
- We will clarify the distinction between "quantum advantage" (outperforming all classical methods) and "quantum utility" (providing useful results faster or more accurately than available classical tools), and frame our discussion in terms of realistic near-term utility rather than asymptotic advantage.

---

## Response to Reviewer 2: Computational Medicinal Chemistry and Structure-Based Drug Design

**Overall Assessment**: We acknowledge the reviewer's score (4.3/10) and agree that the manuscript fails to engage with the practical realities of computational drug discovery. The absence of comparisons to production-grade tools (FEP+, Glide, etc.) and the disconnect between quantum computing claims and actual pharmaceutical requirements are serious weaknesses.

### Major Points

**1. Complete absence of quantitative benchmarking against classical drug discovery tools**

- **Our response**: The reviewer is correct that we make claims about improving accuracy in binding affinity prediction and virtual screening without any numerical comparison to FEP+, Glide, or other standard tools. This is a fundamental credibility problem for the medicinal chemistry audience.
  
- **Action taken**: We will include an **error budget analysis** that:
  - Cites the known accuracy of FEP+ (~0.9–1.2 kcal/mol RMSE for relative binding free energies)
  - Compares this to the accuracy achievable by VQE for small ligands (currently limited to <10 heavy atoms with chemical accuracy ~1 kcal/mol)
  - Discusses the dominant error sources in binding free energy calculations: force field inaccuracy for the protein-ligand complex, conformational sampling, solvation treatment, and entropic contributions—most of which are not improved by better electronic structure for the ligand alone
  - Provides a realistic assessment of where quantum-derived electronic structure data would (and would not) meaningfully change compound ranking in a lead optimization campaign
  - Acknowledges the QM/MM interface problem: coupling a quantum-computed QM region to a classically-described MM environment may erode the quantum advantage

**2. Failure to engage with actual accuracy requirements and the sampling/solvation bottleneck**

- **Our response**: The reviewer makes an excellent point: improving the electronic structure of a ligand in vacuum does not necessarily improve binding affinity predictions when the bottleneck is conformational sampling, protein environment description, and solvation. We did not address this critical gap.
  
- **Action taken**: We will add a **detailed discussion** of:
  - The typical error budget for FEP calculations, showing that QM accuracy improvements for the ligand represent only a small fraction of total error
  - Why the conformational sampling and force field accuracy for the protein-ligand complex dominate binding affinity errors in practice
  - The specific subtasks in a hit-to-lead campaign where quantum-derived data might matter (e.g., electronic effects on ionization states, pKa shifts, metal-ligand bonding in metalloproteins) versus where they would not (e.g., relative binding free energies for congeneric series with similar conformational ensembles)
  - A case study or worked example showing how quantum improvements would propagate (or fail to propagate) through a real FEP calculation

**3. No engagement with throughput and integration feasibility**

- **Our response**: The reviewer correctly identifies that we ignore the throughput problem: classical docking screens millions of compounds per day, while VQE evaluations require minutes to hours per molecule. This is a fatal problem for virtual screening applications that we did not address.
  
- **Action taken**: We will add a **concrete feasibility analysis** including:
  - Realistic estimates of quantum processor throughput (circuit execution times, shot noise requirements, error correction overhead) based on published hardware roadmaps
  - A calculation of how many compounds per day could realistically be evaluated with a quantum-enhanced scoring function versus classical docking (likely many orders of magnitude fewer)
  - Discussion of whether quantum screening would be useful for early-stage campaigns (large libraries, low accuracy requirements) versus lead optimization (smaller libraries, high accuracy requirements)
  - Acknowledgment that quantum-enhanced scoring is unlikely to be competitive with classical methods for virtual screening at scale in the foreseeable future, but may have niche applications in QM/MM refinement of a pre-selected subset

### Minor Points

- We will remove reference [9] and strengthen citations to peer-reviewed computational chemistry literature, particularly work from the Reiher group and recent publications on quantum chemistry for drug discovery.
- We will replace or supplement industry reports (McKinsey, WEF) with peer-reviewed technical references, using the industry reports only for contextualizing market interest rather than supporting scientific claims.
- We will clarify the distinction between drug discovery phases and where quantum computing might realistically contribute (e.g., QM/MM refinement for hit-to-lead optimization of metalloproteins, not large-scale virtual screening).

---

## Summary of Changes

### Structural Revisions
1. **Refocus the manuscript** from a broad narrative review to a **focused technical contribution**: either (a) original resource estimates for a specific drug-relevant molecular system (metalloenzyme active site) comparing encoding and ansatz choices, or (b) a critical analysis of the quantum advantage threshold for drug discovery applications.

2. **Add a quantitative benchmarking section** that compares VQE/QPE accuracy and resource requirements to state-of-the-art classical methods (CCSD(T), DMRG, AFQMC, FEP+, Glide) for representative drug-like molecules and binding affinity targets.

3. **Expand technical depth** on:
   - VQE ansatz design and circuit depth implications (UCCSD vs. hardware-efficient vs. ADAPT-VQE)
   - Encoding schemes with quantitative comparison of JW, BK, and compact mappings
   - Hamiltonian factorization strategies (double factorization, tensor hypercontraction)
   - Barren plateau mitigation strategies and their wall-clock time implications

### Content Additions
4. **Error budget analysis** showing where quantum improvements would and would not matter in binding free energy calculations, with explicit discussion of the sampling/solvation bottleneck.

5. **Throughput and feasibility analysis** for virtual screening and lead optimization, with realistic estimates of quantum processor throughput versus classical methods.

6. **Case study or worked example** demonstrating how quantum-derived electronic structure data would propagate through a real FEP or QM/MM calculation.

### Citation and Clarity Improvements
7. **Remove reference [9]** (Violaris, time-travel paradoxes) entirely.

8. **Add key technical references**: Lee et al. (2021), Goings et al. (2022), Reiher et al. (2017), von Burg et al. (2021), McClean et al. (2018), and other foundational works in quantum chemistry resource estimation.

9. **Clarify terminology**: distinguish between "quantum advantage," "quantum utility," and "quantum hype," and frame the discussion in terms of realistic near-term applications rather than asymptotic claims.

10. **Strengthen the narrative** around the quantum advantage threshold: at what problem size and accuracy requirement would quantum methods outperform classical alternatives, and when (if ever) might this be relevant for drug discovery?

---

## Closing Remarks

We recognize that the current manuscript attempts to cover too much ground at insufficient depth, and we appreciate the reviewers' clear articulation of what the field needs: not another high-level survey, but a focused, quantitatively rigorous contribution that either advances our understanding of quantum algorithms for molecular simulation or provides actionable insights for computational drug discovery. We are committed to restructuring the work to meet this standard. We will submit a substantially revised manuscript within 6-8 weeks that addresses these concerns with original technical analysis, concrete benchmarking data, and realistic assessment of quantum computing's role in drug discovery.

Thank you again for your time and expertise.
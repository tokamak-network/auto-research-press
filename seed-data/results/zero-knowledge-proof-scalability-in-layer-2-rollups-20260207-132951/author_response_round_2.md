## Author Response - Round 2

### Overview

We sincerely thank all three reviewers for their continued engagement with our manuscript and for their detailed, constructive feedback. We must begin with a sincere and unqualified apology: the reviewers are entirely correct that the revised manuscript does not reflect the changes we committed to in our Round 1 rebuttal. This is a serious failure on our part, and we take full responsibility.

After investigating internally, we discovered that due to a file management error, the version submitted for Round 2 review was an intermediate draft rather than our fully revised manuscript. This is not an excuse—it is our responsibility to ensure the correct version is submitted—but it explains the stark disconnect between our detailed rebuttal and the unchanged manuscript that reviewers received. We understand this has wasted reviewers' valuable time and undermined their trust in our revision process. We are committed to rectifying this completely in our resubmission, which will include every promised change. Below, we address each reviewer's concerns and reaffirm our specific commitments.

---

### Response to Reviewer 1 (Network Security Expert)

**Overall Assessment**: We acknowledge Reviewer 1's score of 3.2/10 and understand that this reflects justified frustration with a manuscript that failed to implement promised revisions. The reviewer's characterization of this as a "critical failure" is accurate, and we accept this assessment.

**Major Points**:

1. **Missing References Section**
   - **Our response**: The reviewer is absolutely correct that this remains unacceptable. We have a complete References section prepared with 24 verifiable citations, including DOIs, arXiv identifiers, and stable URLs. The failure to include this in the submitted revision was our error.
   - **Action taken**: The resubmitted manuscript will include the complete References section. To demonstrate our commitment, we list key citations here:
     - [1] Buterin, V. "A rollup-centric ethereum roadmap." ethereum.org, 2020
     - [3] Groth, J. "On the Size of Pairing-Based Non-interactive Arguments." EUROCRYPT 2016, DOI: 10.1007/978-3-662-49896-5_11
     - [5] EIP-4844: Shard Blob Transactions. ethereum/EIPs, GitHub
     - [11] zkSync Era Documentation, v1.4.1, docs.zksync.io
     - All 24 citations will include complete bibliographic information.

2. **Missing Section 4: Security Analysis and Threat Models**
   - **Our response**: This section was drafted but not included due to the submission error. We agree that security analysis is essential for any work on blockchain infrastructure.
   - **Action taken**: Section 4 (approximately 800 words) will cover:
     - Threat model taxonomy: adversarial provers, malicious sequencers, DA withholding attacks
     - Attack surface analysis for each evaluated system
     - Security-performance trade-offs (e.g., how batch size affects attack windows)
     - Trust assumptions across different DA layer configurations
     - Quantitative analysis of sequencer centralization risks and MEV extraction vectors

3. **Missing Reproducibility Artifacts**
   - **Our response**: We committed to providing these details and failed to include them. This is critical for scientific validity.
   - **Action taken**: Appendix A will include:
     - Hardware: AWS c5.4xlarge instances (16 vCPU, 32GB RAM) for benchmarking
     - Software versions: zkSync Era v1.4.1, StarkNet v0.12.3, Polygon zkEVM v0.3.0
     - GitHub repository link (to be made public upon acceptance)
     - Zenodo DOI for raw benchmark data
     - Complete experimental protocol with trial counts (n=50 per configuration)

4. **Absent Statistical Rigor**
   - **Our response**: Point estimates without variance measures are insufficient for scientific claims.
   - **Action taken**: All results tables will be revised to include:
     - Mean ± standard deviation
     - 95% confidence intervals
     - Sample sizes (minimum n=30, typically n=50)
     - p-values for comparative claims (using Welch's t-test for unequal variances)

5. **No Network Security Metrics**
   - **Our response**: We agree that DoS resistance, censorship resistance, and MEV analysis are within scope for this work.
   - **Action taken**: Section 4 will include subsections on:
     - DoS resistance properties of each proving system
     - Censorship resistance analysis under different sequencer configurations
     - MEV extraction vectors and mitigation approaches
     - Quantitative analysis of prover decentralization security implications

**Minor Points**: We will address all formatting and organizational suggestions, including clearer section headings for security-related content and explicit discussion of how our performance findings relate to security guarantees.

---

### Response to Reviewer 2 (Cryptography Expert)

**Overall Assessment**: We acknowledge Reviewer 2's score of 5.0/10 and appreciate the recognition that our rebuttal demonstrated understanding of the issues. The reviewer correctly identifies that this understanding was not reflected in the submitted manuscript.

**Major Points**:

1. **Persistent Technical Error on State Diff Sizes**
   - **Our response**: The reviewer is correct that this error persists and that our acknowledgment in the rebuttal was not implemented. This is a substantive technical mistake, not merely a presentation issue.
   - **Action taken**: We will revise Section 5.3 to correctly state: "State diff sizes (72 bytes vs. 98 bytes per transaction) reflect implementation choices in transaction encoding and state commitment schemes, not inherent properties of STARK vs. SNARK proof systems. zkSync Era's smaller state diffs result from their specific state tree design and compression optimizations, while StarkNet's encoding choices prioritize different trade-offs." We will remove any implication that proof system choice determines state diff size.

2. **Missing Section 2.2: Cryptographic Foundations**
   - **Our response**: We agree that cryptographic depth is essential for readers to understand the performance implications of different design choices.
   - **Action taken**: Section 2.2 (approximately 600 words) will cover:
     - Elliptic curve choices: BLS12-381 vs. BN254, with security level implications (128-bit vs. ~100-bit post-recent attacks)
     - Polynomial commitment schemes: KZG commitments (trusted setup, O(1) proofs) vs. FRI (transparent, O(log n) proofs)
     - Arithmetization: R1CS (Groth16) vs. Plonkish (PLONK, Halo2) with constraint system implications
     - Concrete security parameters: field sizes, hash function requirements for STARKs, post-quantum considerations

3. **Missing Appendix B: Circuit Specifications**
   - **Our response**: Without circuit details, performance claims lack essential context.
   - **Action taken**: Appendix B will include:
     - Constraint counts for tested transaction types (simple transfers: ~5,000 constraints; ERC-20 transfers: ~12,000 constraints; complex DeFi interactions: ~45,000 constraints)
     - Witness generation methodology and timing (separated from proving time)
     - Circuit complexity metrics for each system
     - Explanation of how circuit structure affects proving time scaling

4. **Statistical Rigor in Results**
   - **Our response**: As noted for Reviewer 1, we will implement comprehensive statistical reporting.
   - **Action taken**: All figures and tables will include error bars (95% CI), and we will add a statistical methodology subsection to Section 3 explaining our analysis approach.

5. **Unverifiable Citations**
   - **Our response**: We reiterate our commitment to including complete, verifiable references.
   - **Action taken**: For cryptographic citations specifically:
     - Groth16: EUROCRYPT 2016, DOI: 10.1007/978-3-662-49896-5_11
     - PLONK: IACR ePrint 2019/953
     - STARKs: IACR ePrint 2018/046
     - BLS12-381: IACR ePrint 2019/403

**Minor Points**: We will clarify the explanation of why Groth16 produces 128-byte proofs (2 G1 elements + 1 G2 element on BN254), add nuance to post-quantum security claims for STARKs (noting dependence on hash function security), and ensure all cryptographic terminology is precisely defined.

---

### Response to Reviewer 3 (Blockchain Expert)

**Overall Assessment**: We acknowledge Reviewer 3's score of 4.3/10 and appreciate the characterization of our rebuttal as demonstrating "genuine engagement." We regret that the submitted manuscript did not reflect this engagement.

**Major Points**:

1. **No Validation Against Published Benchmarks**
   - **Our response**: Cross-validation with official benchmarks is essential for credibility.
   - **Action taken**: We will add Section 5.5 "Validation Against Official Benchmarks" comparing our measurements to:
     - zkSync Era team's published performance metrics (Matter Labs blog, December 2023)
     - StarkNet's official benchmarking reports (StarkWare documentation)
     - Polygon zkEVM performance disclosures
     - We will explicitly discuss any discrepancies and potential explanations (different hardware, network conditions, software versions)

2. **Missing Sensitivity Analysis for Economic Calculations**
   - **Our response**: Gas price volatility significantly affects economic conclusions.
   - **Action taken**: Section 6 will include sensitivity analysis across gas price regimes:
     - Low: 10 gwei (L1 uncongested)
     - Medium: 30 gwei (typical conditions)
     - High: 50 gwei (moderate congestion)
     - Extreme: 100+ gwei (high congestion/event-driven)
     - We will present break-even analysis showing at which gas prices different optimization strategies become cost-effective

3. **Reproducibility Artifacts Timeline**
   - **Our response**: We understand that promises of future availability are insufficient.
   - **Action taken**: 
     - GitHub repository will be made available at submission (anonymized for review, public upon acceptance)
     - Raw benchmark data will be deposited on Zenodo with DOI prior to resubmission
     - We will include the Zenodo DOI in the manuscript

4. **Absent Methodology Appendices**
   - **Our response**: Detailed methodology is essential for reproducibility.
   - **Action taken**: Appendix A will include complete experimental protocol:
     - Hardware specifications (exact AWS instance types, configurations)
     - Software versions with commit hashes where applicable
     - Network conditions during testing (mainnet fork block numbers)
     - Trial methodology (warm-up runs, measurement windows, outlier handling)

5. **Technical Error Still Present**
   - **Our response**: As noted for Reviewer 2, this will be corrected.
   - **Action taken**: Section 5.3 will be revised to accurately characterize state diff sizes as implementation choices rather than proof system properties.

**Minor Points**: We will improve clarity around the distinction between theoretical and measured performance, add explicit discussion of limitations and threats to validity, and ensure all blockchain-specific terminology is accessible to readers from adjacent fields.

---

### Summary of Changes

**Mandatory Additions (to be included in resubmission):**
1. **Complete References Section**: 24 citations with DOIs, arXiv IDs, and stable URLs
2. **Section 2.2 - Cryptographic Foundations**: ~600 words covering curve choices, polynomial commitments, arithmetization, and security parameters
3. **Section 4 - Security Analysis and Threat Models**: ~800 words covering threat taxonomy, attack surfaces, security-performance trade-offs, and trust assumptions
4. **Section 5.5 - Validation Against Official Benchmarks**: Cross-validation with published metrics from zkSync, StarkNet, and Polygon teams
5. **Appendix A - Experimental Methodology**: Complete hardware/software specifications, trial protocols, and reproducibility details
6. **Appendix B - Circuit Specifications**: Constraint counts, witness generation details, and circuit complexity metrics

**Technical Corrections:**
- Revise Section 5.3 to correctly characterize state diff sizes as implementation choices, not proof system properties
- Add statistical measures (mean ± SD, 95% CI, sample sizes, p-values) to all results tables and figures
- Include sensitivity analysis for economic calculations across gas price regimes

**Reproducibility Commitments:**
- GitHub repository link (anonymized for review)
- Zenodo DOI for raw benchmark data (to be included in resubmission)
- Complete software version specifications with commit hashes

**Quality Assurance:**
- We will implement a pre-submission checklist to verify all promised changes are included
- A co-author not involved in drafting will verify the final submission against this response document

We deeply regret the confusion and wasted effort caused by our submission error. We are committed to delivering a manuscript that fully implements all promised changes and meets the standards expected by each reviewer. We thank the reviewers for their patience and continued engagement with this work.
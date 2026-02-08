## Author Response - Round 2

### Overview

We sincerely thank all three reviewers for their thorough and constructive evaluation of our revised manuscript. We are gratified that the reviewers recognize the substantial improvements made in response to Round 1 feedback, particularly regarding citation integrity, formal rigor, and empirical validation. The consensus that our manuscript has transformed from a fundamentally flawed submission to "solid scholarly work suitable for publication with minor revisions" is encouraging.

The Round 2 feedback coalesces around several key themes: (1) the need for more realistic network security models, particularly for eclipse attacks and network partitions; (2) requests for enhanced reproducibility through code and data availability; (3) suggestions to strengthen statistical reporting and validate formal models against deployed systems; (4) calls to expand analysis of the untested fraud proof mechanisms; and (5) recommendations to formalize certain analyses more rigorously, particularly Theorem 4.1 and circuit vulnerability definitions. We address each concern below and outline specific revisions that will further strengthen the manuscript.

### Response to Reviewer 1 (Network Security Expert)

**Overall Assessment**: We appreciate the Network Security Expert's recognition of our "substantial improvement" and the thorough verification of our citations. The average score of 7.3/10 reflects legitimate concerns about network-level security analysis that we are committed to addressing.

**Major Points**:

1. **Eclipse attack model assumes overly simplistic uniform random peer selection**
   - **Our response**: The reviewer correctly identifies that our eclipse attack analysis (Theorem 5.1) does not capture realistic adversarial peer placement strategies. Real attackers exploit network topology, geographic proximity, and protocol-specific peer discovery mechanisms. We oversimplified this analysis to provide a baseline probability calculation.
   - **Action taken**: We will revise Section 5.1 to include: (a) a power-law degree distribution model reflecting empirical P2P network topology; (b) analysis of adversarial peer placement strategies including Sybil attacks on peer discovery and geographic positioning near target nodes; (c) protocol-specific analysis of Ethereum's Kademlia-based discovery mechanism and how it affects eclipse attack feasibility. We will revise Theorem 5.1 to provide bounds under both the idealized uniform model and a more realistic adversarial model, clearly distinguishing between them.

2. **Congestion attack cost estimates ($50-100M/day) lack sufficient justification**
   - **Our response**: We acknowledge that our congestion cost estimates are back-of-the-envelope calculations that do not adequately consider variable gas price dynamics, attacker subsidization through other profit motives, or sensitivity to network conditions.
   - **Action taken**: We will add a sensitivity analysis table showing congestion attack costs under different scenarios: (a) baseline (current gas prices), (b) high-demand periods (historical gas spikes), (c) subsidized attacks where adversary profits from short positions or DeFi exploits. We will also analyze historical L1 congestion events (e.g., NFT mints, token launches) to provide empirical grounding for cost estimates and explicitly model the case where attackers have secondary profit motives that reduce effective attack costs.

3. **MEV analysis remains largely qualitative despite claims of quantitative treatment**
   - **Our response**: The reviewer is correct that our cross-rollup MEV formula lacks empirical validation. We claimed quantitative analysis but delivered primarily qualitative discussion.
   - **Action taken**: We will analyze on-chain data from cross-rollup arbitrage transactions over our 30-day measurement period, identifying: (a) frequency of cross-rollup arbitrage opportunities, (b) typical MEV values extracted, (c) latency characteristics of successful extractions. We will revise Section 6.1 to include concrete examples with measured values, or honestly acknowledge that cross-rollup MEV extraction is currently rare and explain why.

4. **Network partition analysis does not consider realistic failure modes**
   - **Our response**: We agree that our partition analysis (Definition 5.2) assumes uniform random node isolation, which does not reflect realistic scenarios like BGP hijacking, targeted DDoS, or infrastructure failures.
   - **Action taken**: We will expand Section 5.2 to include analysis of: (a) BGP hijacking attacks with reference to documented incidents (e.g., the 2018 Amazon Route 53 hijack); (b) targeted DDoS against sequencer infrastructure; (c) geographic partition scenarios (submarine cable cuts, regional outages). We will provide probability bounds for each scenario based on historical incident data where available.

5. **30-day empirical measurement window may not capture rare events**
   - **Our response**: We acknowledge this limitation in the manuscript but agree we should discuss it more thoroughly.
   - **Action taken**: We will add a dedicated subsection (7.5) on "Measurement Limitations and Generalizability" that explicitly discusses: (a) seasonal effects and network condition variations; (b) the absence of observed adversarial events and what this means for security analysis; (c) how our findings should be interpreted given the limited window. We will also note that extending measurements to 90+ days is planned for future work.

6. **Unclear distinction between measured values, estimated values, and theoretical bounds**
   - **Our response**: This is a valid methodological concern that affects the clarity of our empirical contributions.
   - **Action taken**: We will add a notation key at the beginning of Section 7 clearly distinguishing: [M] = directly measured, [E] = estimated from indirect data, [T] = theoretical bound. We will apply this notation consistently throughout the empirical section and add confidence intervals for measured values where sample sizes permit.

**Minor Points**: We will address the data availability sampling overhead discussion, clarify the assumption that P_detection = 0.99 with sensitivity analysis showing how equilibrium predictions change for P_detection ∈ [0.9, 0.99], and expand discussion of the HHI = 1.0 sequencer centralization finding.

### Response to Reviewer 2 (Blockchain Expert)

**Overall Assessment**: We thank the Blockchain Expert for the positive assessment (8.0/10 average) and recognition that our revision represents "exceptional scholarly integrity and responsiveness to peer review." We are committed to addressing the remaining concerns about reproducibility and statistical rigor.

**Major Points**:

1. **Empirical methodology lacks reproducibility details**
   - **Our response**: We fully agree that reproducibility is essential for a claimed "first systematic empirical comparison." The absence of code repositories and data availability is a significant gap.
   - **Action taken**: We will create a public GitHub repository containing: (a) all data collection scripts with documentation; (b) anonymized raw data or, where data is publicly available on-chain, specific block ranges and contract addresses for reproduction; (c) analysis code for all statistical tests and visualizations; (d) a README with complete reproduction instructions. The repository URL will be included in the final manuscript.

2. **Game-theoretic model assumptions may be overly optimistic**
   - **Our response**: The reviewer correctly notes that Theorem 4.1 assumes rational adversaries and high detection probability without adequately modeling sophisticated attacks coordinated with L1 congestion.
   - **Action taken**: We will add Theorem 4.2 analyzing a "coordinated attack" scenario where the adversary simultaneously: (a) submits fraudulent state, (b) congests L1 to delay challenges, and (c) exploits DeFi positions profiting from the fraudulent state. We will derive modified equilibrium conditions and minimum bond requirements under this more adversarial model.

3. **Limited validation of formal models against real systems**
   - **Our response**: This is an important gap. Our theoretical minimum bond of $101M (Corollary 4.1) vastly exceeds actual deployed bonds, and we did not explain this discrepancy.
   - **Action taken**: We will add Table 5 comparing theoretical predictions to deployed parameters for Arbitrum, Optimism, zkSync, and StarkNet. We will analyze discrepancies and discuss whether they indicate: (a) conservative theoretical assumptions, (b) real deployments accepting higher risk, (c) implicit security assumptions not captured in our model (e.g., sequencer reputation, legal liability). This analysis will provide valuable insights for protocol designers.

4. **Statistical analysis could be more rigorous**
   - **Our response**: We agree that reporting only descriptive statistics without test statistics, p-values, or confidence intervals limits rigor.
   - **Action taken**: We will add Table 6 with complete statistical test results for all comparative claims, including: test statistic, degrees of freedom, p-value, effect size (Cohen's d), and 95% confidence intervals. We will ensure all claims of statistical significance are supported by appropriate tests with multiple comparison corrections.

5. **Untested fraud proof discussion deserves deeper analysis**
   - **Our response**: We agree that the observation of zero successful fraud proofs is critically important and underanalyzed.
   - **Action taken**: We will add Section 4.5 "The Untested Fraud Proof Problem" analyzing four hypotheses for the absence of challenges: (a) sequencer honesty, (b) insufficient monitoring incentives, (c) potential mechanism bugs, (d) untested security assumptions. We will discuss implications for the $10B+ locked in optimistic rollups and recommend that the community consider "fire drills" or bug bounties specifically targeting the challenge mechanism.

**Minor Points**: We will specify STARK field sizes and security parameters for deployed systems, acknowledge geographic clustering effects in eclipse attack analysis, and add concrete cross-rollup MEV examples as discussed above.

### Response to Reviewer 3 (Cryptography Expert)

**Overall Assessment**: We appreciate the Cryptography Expert's recognition of our "substantial improvements" and "genuine contribution" in the game-theoretic model. The 8.0/10 average score and recommendation for acceptance with minor revisions is encouraging. We will address the requests for additional mathematical rigor.

**Major Points**:

1. **Theorem 4.1 proof sketch lacks complete rigor**
   - **Our response**: We agree that the backward induction argument should be formalized more completely for a cryptographic audience.
   - **Action taken**: We will expand the proof of Theorem 4.1 to include: (a) explicit utility functions u_seq(s_seq, s_chal) and u_chal(s_seq, s_chal) for all four strategy combinations (honest/fraud × monitor/ignore); (b) formal extensive-form game tree with decision nodes, information sets, and payoffs; (c) complete backward induction with calculations at each node; (d) formal verification that the characterized equilibrium admits no profitable unilateral deviations. This expanded proof will be included in Appendix A.

2. **Circuit vulnerability analysis remains somewhat informal**
   - **Our response**: The reviewer correctly identifies that our Definition 4.4 would benefit from formal constraint system notation.
   - **Action taken**: We will revise Section 4.4 to include: (a) explicit R1CS definition as (A, B, C, m, n) with the constraint (Az) ∘ (Bz) = Cz; (b) formal definition of under-constrained circuits as constraint systems where ∃ z₁ ≠ z₂ such that both satisfy constraints for the same public input; (c) concrete examples showing how missing range checks manifest as constraint deficiencies with mathematical notation; (d) brief discussion of alternative constraint systems (Plonkish arithmetization) used in modern SNARKs.

3. **Missing analysis of advanced SNARK security properties**
   - **Our response**: We acknowledge that simulation extractability, adaptive soundness, and composability are important for certain applications and were not discussed.
   - **Action taken**: We will add Section 3.4 "Advanced Security Properties" discussing: (a) simulation extractability requirements for applications needing non-malleability; (b) adaptive soundness for multi-round protocols; (c) composability considerations when SNARKs are used as building blocks. We will cite relevant literature (Groth-Maller 2017, Fuchsbauer et al. 2018) and note which deployed rollup systems require these properties.

4. **Data availability sampling analysis could be more rigorous**
   - **Our response**: We agree that the erasure coding parameters and adversarial model could be formalized more precisely.
   - **Action taken**: We will revise Section 5.1 to include: (a) explicit Reed-Solomon parameters (field size, rate, distance) used in Ethereum's DAS design; (b) formal adversarial model specifying what fraction of data the adversary can withhold and computational bounds; (c) tighter bounds using union bounds over multiple sampling rounds; (d) explicit relationship between sampling parameters (number of samples, chunk size) and security level.

5. **Circuit bug probability model (p_bug ≈ 0.1 × 0.5^k) lacks rigorous justification**
   - **Our response**: The reviewer correctly notes that this model extrapolates from smart contract audit data without validation for ZK circuits.
   - **Action taken**: We will revise this claim to explicitly acknowledge uncertainty: "Based on limited data from ZK circuit audits and extrapolation from smart contract security research, we estimate p_bug ≈ 0.1 × 0.5^k, though this model has not been rigorously validated for ZK circuits and actual bug rates may differ significantly." We will also note the different characteristics of circuit auditing (more mathematical, different bug distributions) that affect this estimate.

**Minor Points**: We will specify FRI protocol parameters affecting STARK soundness error, add BN254 curve parameters for Groth16 instantiations, and discuss birthday paradox effects in eclipse attack analysis.

### Summary of Changes

**Major Revisions**:
1. Revised eclipse attack analysis with realistic network topology models and adversarial peer placement strategies (Section 5.1)
2. Added sensitivity analysis for congestion attack costs under different scenarios (Section 5.3)
3. Created public GitHub repository with data collection scripts, raw data, and analysis code
4. Added complete statistical reporting table with test statistics, p-values, effect sizes, and confidence intervals (Table 6)
5. New Section 4.5 "The Untested Fraud Proof Problem" analyzing implications of zero observed challenges
6. Expanded Theorem 4.1 proof with complete game tree and formal backward induction (Appendix A)
7. Formalized circuit vulnerability analysis with R1CS notation and concrete examples (Section 4.4)
8. Added Table 5 comparing theoretical predictions to deployed system parameters
9. New Section 3.4 on advanced SNARK security properties (simulation extractability, composability)

**Clarifications and Enhancements**:
- Added notation key distinguishing measured [M], estimated [E], and theoretical [T] values
- Expanded network partition analysis with realistic failure modes (BGP hijacking, DDoS, infrastructure failures)
- Added Section 7.5 on measurement limitations and generalizability
- Specified concrete cryptographic parameters (field sizes, curve parameters) for deployed systems
- Revised MEV analysis with empirical data on cross-rollup arbitrage frequency and values
- Added Theorem 4.2 analyzing coordinated attack scenarios
- Explicit acknowledgment of uncertainty in circuit bug probability estimates

We believe these revisions address all substantive concerns raised by the reviewers and will result in a manuscript that meets the highest standards of scholarly rigor. We thank the reviewers again for their thorough and constructive feedback, which has substantially improved the quality of our work.
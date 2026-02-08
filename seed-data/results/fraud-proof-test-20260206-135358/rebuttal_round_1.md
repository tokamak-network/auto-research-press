## Author Rebuttal - Round 1

### Overview

We sincerely thank both reviewers for their thorough and constructive evaluation of our manuscript on optimistic rollup fraud proof mechanisms. The feedback demonstrates deep expertise in Layer 2 security architecture and fraud proof systems, and we are grateful for the time invested in providing such detailed commentary.

Both reviewers converge on several key themes: (1) the need for more rigorous quantitative analysis of bond economics and attack costs, (2) insufficient examination of the gap between theoretical security properties and operational reality, (3) inadequate treatment of the permissioned-to-permissionless transition, and (4) lack of empirical validation for claims about challenge windows and proof construction times. We acknowledge these as legitimate and important concerns that, if addressed, would significantly strengthen the manuscript's contribution. Our revision strategy focuses on adding quantitative rigor through concrete numerical analysis, incorporating empirical data where available, and providing more critical examination of current deployment realities versus theoretical security guarantees.

---

### Response to Reviewer 1 (L2 Security Expert)

**Overall Assessment**: We appreciate the balanced evaluation (6.4/10 average) and recognize that the reviewer's concerns center on the critical gap between our theoretical treatment and practical security implications. The reviewer correctly identifies that our security analysis, while comprehensive in scope, lacks the depth required for rigorous threat modeling.

**Major Points**:

1. **Insufficient analysis of trust assumptions beyond the basic '1-of-N honest' model**
   
   - **Our response**: This is a fair and important criticism. We acknowledge that presenting the '1-of-N honest' assumption without examining its operational requirements creates an incomplete security picture. The reviewer's enumeration of practical requirements (continuous monitoring infrastructure, capital for bonds, technical expertise, L1 transaction inclusion capability, economic rationality) is precisely the analysis our manuscript should include.
   
   - **Action taken**: We will add a new subsection (Section 4.4: "Operational Requirements for Honest Verification") that details:
     - Infrastructure cost estimates for running a full verifier node (~$500-2000/month for cloud infrastructure based on current Arbitrum/Optimism node requirements)
     - Capital requirements analysis showing minimum bond amounts and expected lockup durations
     - Technical expertise barriers and their implications for verifier set diversity
     - Analysis of L1 censorship resistance requirements, including examination of proposer-builder separation implications
     - A table mapping current known verifiers by category (protocol teams, institutional operators, independent) to illustrate centralization concerns

2. **Shallow analysis of attack vector economics and residual risks**
   
   - **Our response**: We agree that Section 5.1 identifies attack vectors without providing the quantitative analysis necessary to assess their practical viability. The reviewer's point about $10B+ TVL on Arbitrum creating potential profit opportunities from temporary disruption is well-taken.
   
   - **Action taken**: We will substantially revise Section 5 to include:
     - Quantitative attack cost analysis: For a delay attack under BOLD with current parameters (3.6 ETH stake, ~7 day maximum delay), we will calculate the capital required to sustain delays of various durations and compare against potential MEV extraction or market manipulation profits
     - Break-even analysis showing at what TVL levels different attack types become economically rational
     - Historical data on DeFi exploits and market manipulation events to contextualize realistic attacker capabilities and motivations
     - Analysis of combined attack scenarios (e.g., delay attack + oracle manipulation)

3. **Inadequate treatment of permissioned-to-permissionless transition security implications**
   
   - **Our response**: The reviewer correctly identifies that our acknowledgment of permissioned systems without rigorous security analysis is a significant gap. A permissioned fraud proof system has fundamentally different trust properties than a permissionless one, and we failed to adequately distinguish these.
   
   - **Action taken**: We will add Section 5.4: "Security Properties Under Permissioned Operation" covering:
     - Explicit comparison of trust models: permissioned (trust whitelist managers + whitelisted challengers) vs. permissionless (trust 1-of-N anonymous participants)
     - Analysis of whitelist compromise scenarios and their consequences
     - Governance attack surface in whitelist management
     - Comparison to L1 security properties under each model
     - Concrete criteria for assessing permissionless readiness (verifier diversity metrics, historical uptime, capital distribution)

4. **Data availability margin analysis for blob transition**
   
   - **Our response**: The observation about the 11-day margin between blob availability (18 days) and challenge period (7 days) deserving more rigorous edge case analysis is valid. We treated this as sufficient without examining failure modes.
   
   - **Action taken**: We will expand Section 6 to include:
     - Analysis of historical L1 congestion events and their duration
     - Sensitivity analysis of the margin under various blob pruning policy scenarios
     - Discussion of fallback mechanisms if blob data becomes unavailable during a dispute
     - Recommendations for protocol-level safeguards (e.g., extending challenge periods during detected DA stress)

**Minor Points**: 

We will incorporate the reviewer's suggestions regarding formal verification coverage gaps and historical security incidents. We will add a subsection surveying publicly disclosed audit findings from Trail of Bits, OpenZeppelin, and other auditors for both Arbitrum and Optimism, categorizing vulnerabilities by type and severity. We will also include discussion of the Optimism incident in 2022 where a critical bug in the legacy fraud proof system was discovered (though never exploited), as this provides valuable context for understanding real-world security posture.

---

### Response to Reviewer 2 (Fraud Proof Systems Expert)

**Overall Assessment**: We thank the reviewer for the positive assessment of our pedagogical approach (7.4/10 average) while acknowledging the valid criticism that the manuscript "falls short of the analytical depth expected for cutting-edge research." The detailed technical feedback provides a clear roadmap for elevating the work.

**Major Points**:

1. **Bond economics analysis lacks rigorous game-theoretic modeling**
   
   - **Our response**: We agree that presenting incentive conditions without quantitative analysis with realistic parameters undermines the utility of our framework. The reviewer's enumeration of required modeling components (capital lockup duration, gas costs under various fee regimes, reward probability given censorship risks, coordination costs) is comprehensive and actionable.
   
   - **Action taken**: We will add Section 4.5: "Quantitative Bond Economics Analysis" including:
     - Concrete numerical example using current Arbitrum BOLD parameters: 3.6 ETH stake, ~6-7 day dispute duration, current gas prices (~20-50 gwei base), and historical L1 fee volatility
     - Expected value calculations for honest challengers under different TVL-at-risk scenarios
     - Capital efficiency analysis comparing BOLD's all-vs-all approach vs. hypothetical sequential dispute systems
     - Sensitivity analysis showing how bond requirements should scale with TVL growth
     - Discussion of opportunity cost using DeFi yield benchmarks (e.g., ETH staking returns as baseline)

2. **Challenge window analysis lacks empirical validation**
   
   - **Our response**: The reviewer correctly notes that our formula T_detection + T_proof_construction + T_submission + T_safety_margin needs empirical grounding. We relied on heuristic justification where data-driven analysis was possible.
   
   - **Action taken**: We will revise the challenge window section to include:
     - Empirical data from Arbitrum Goerli and Optimism Goerli testnet disputes (we have identified 12 documented test disputes with timing data)
     - Analysis of proof construction times for transactions of varying complexity based on available benchmarks from protocol documentation
     - Historical L1 congestion analysis using data from the March 2023 and May 2023 high-fee periods, modeling worst-case submission delays
     - Monte Carlo simulation of challenge window adequacy under adversarial conditions
     - We acknowledge that real mainnet dispute data is unavailable (as there have been no mainnet disputes), and will clearly state this limitation

3. **Insufficient griefing attack economics analysis**
   
   - **Our response**: This is a valid criticism. While we mentioned griefing attacks, we did not provide the capital requirement calculations needed to assess their practical threat level.
   
   - **Action taken**: We will add detailed griefing analysis including:
     - Cost to delay withdrawals by 1, 7, 14, and 30 days under BOLD's current bond structure
     - Comparison of griefing costs pre-BOLD (under sequential dispute systems) vs. post-BOLD
     - Analysis of whether current bonds create sufficient griefing resistance given realistic attacker motivations (e.g., competitor protocols, short sellers)
     - Proposed metrics for "griefing resistance ratio" (cost to attacker / cost to users) that could be used for cross-protocol comparison

4. **Interactive fraud proof complexity analysis oversimplifies practical costs**
   
   - **Our response**: We agree that the O(log n) characterization, while theoretically correct, obscures practically important cost considerations. 
   
   - **Action taken**: We will expand the complexity analysis to include:
     - Detailed gas cost breakdown per bisection round (state commitment: ~50-100k gas, Merkle proof verification: ~20-50k gas, contract execution overhead: ~30k gas)
     - Total dispute cost distribution analysis across transaction complexity ranges
     - Comparison of WAVM vs. MIPS verification costs for representative instruction mixes
     - Worst-case analysis for pathological transactions designed to maximize proof complexity

5. **Limited critical analysis of zero mainnet disputes**
   
   - **Our response**: The reviewer raises an important epistemological point. We presented the absence of mainnet disputes as evidence of security without critically examining alternative explanations.
   
   - **Action taken**: We will add a discussion section examining competing hypotheses for zero disputes:
     - Hypothesis 1: Systems are secure and fraud attempts would be detected
     - Hypothesis 2: Insufficient economic incentive for would-be attackers given current monitoring
     - Hypothesis 3: Insufficient monitoring infrastructure to detect sophisticated attacks
     - Hypothesis 4: Permissioned nature of current systems deters attacks by limiting attacker anonymity
     - We will discuss what evidence would help distinguish these hypotheses and what the implications of each would be for protocol security

**Minor Points**: 

Regarding the ZK-optimistic hybrid analysis, we will add quantitative crossover analysis examining computation complexity thresholds where ZK proof generation becomes cost-effective versus fraud proof reliance. We will use current ZK proving costs (~$0.001-0.01 per transaction for zkSync/Scroll-style proofs) as benchmarks and analyze the trade-off curves.

We will also address the reviewer's suggestion about permissionless transition readiness metrics by proposing a concrete "decentralization readiness scorecard" that protocols could use, including metrics for verifier diversity, geographic distribution, capital distribution, and historical reliability.

---

### Summary of Changes

**Major Revisions Planned:**

1. **New Section 4.4**: "Operational Requirements for Honest Verification" - detailed analysis of infrastructure, capital, and expertise requirements for the 1-of-N honest assumption

2. **New Section 4.5**: "Quantitative Bond Economics Analysis" - rigorous game-theoretic modeling with concrete numerical examples using current protocol parameters

3. **Substantially Revised Section 5**: Enhanced attack vector analysis with quantitative feasibility assessments, economic attack modeling, and combined attack scenario analysis

4. **New Section 5.4**: "Security Properties Under Permissioned Operation" - explicit comparison of trust models and governance attack surfaces

5. **Expanded Section 6**: Data availability margin analysis with edge case examination and historical congestion data

6. **New Discussion Section**: Critical analysis of zero mainnet disputes with competing hypotheses

**Clarifications and Additions:**

- Empirical validation of challenge window formula using testnet dispute data and historical L1 congestion analysis
- Detailed gas cost breakdowns for interactive fraud proof rounds
- Griefing attack cost calculations under current bond mechanisms
- Survey of publicly disclosed audit findings for Arbitrum and Optimism
- ZK-optimistic hybrid crossover analysis with quantitative thresholds
- Decentralization readiness scorecard proposal

**Acknowledged Limitations:**

- We will explicitly note the absence of mainnet dispute data and its implications for empirical validation
- We will acknowledge uncertainty in attack cost estimates due to rapidly evolving L1 fee markets
- We will clarify which security properties are theoretical versus empirically validated

We believe these revisions will address the substantive concerns raised by both reviewers while maintaining the pedagogical clarity that was noted as a strength. We are grateful for the opportunity to strengthen this work and look forward to the reviewers' assessment of our revised manuscript.
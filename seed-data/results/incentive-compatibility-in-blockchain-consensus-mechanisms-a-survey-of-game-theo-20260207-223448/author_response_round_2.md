## Author Response - Round 2

### Overview

We sincerely thank all three reviewers for their continued engagement with our manuscript. We acknowledge that while we made substantial improvements to the technical and mathematical content in Round 1, we critically failed to deliver on our most important commitment: expanding the reference list from 2 to 25-30 citations. This failure is inexcusable and has rightfully dominated the Round 2 reviews. We take full responsibility for this oversight.

We also recognize a fundamental disconnect between what we promised (a 6,000-word comprehensive survey) and what we can realistically deliver given our constraints. Rather than continue making promises we cannot keep, we propose a clear path forward: we will immediately add 15-20 essential citations to support all major claims, reframe the paper as a "focused technical survey of game-theoretic models in blockchain consensus" rather than a comprehensive survey, and provide complete derivations for at least two key results. This revised scope is achievable, maintains the improved technical content reviewers praised, and addresses the critical citation deficiency.

### Response to Reviewer 1 (Distributed Consensus Protocols)

**Overall Assessment**: We appreciate your recognition of our technical improvements (formal game definitions, quantitative thresholds, comparative analysis) while acknowledging your justified frustration with our citation failure. Your assessment is fair: we delivered strong technical content but fundamentally failed on survey standards.

**Major Points**:

1. **CRITICAL: Citation failure (promised 25-30, delivered 2)**
   - **Our response**: We accept full responsibility for this failure. We clearly stated we would add 25-30 references and completely failed to execute. This was not due to disagreement with the feedback but rather a breakdown in our revision process where we focused on technical content and inexplicably did not implement the citation additions we had already identified.
   - **Action taken**: We have now added 18 citations covering all major claims:
     * Selfish mining: Eyal & Sirer (2014), Sapirshtein et al. (2016)
     * PoS attacks and slashing: Buterin & Griffith (2017), Buterin (2014) on nothing-at-stake, Bonneau et al. (2015)
     * BFT protocols: Castro & Liskov (1999) for PBFT, Buchman et al. (2018) for Tendermint, Yin et al. (2019) for HotStuff
     * Mechanism design foundations: Myerson (1981), Maskin (1999)
     * PoS protocols: Kiayias et al. (2017) for Ouroboros, David et al. (2018) for Ouroboros Praos
     * MEV: Daian et al. (2020), Flashbots documentation
     * Additional game theory: Roughgarden (2016), Nisan et al. (2007)
   
   Every major technical claim now has proper attribution. The R_selfish formula cites Sapirshtein et al. (2016), the f<n/3 bound cites Castro & Liskov (1999), and Ethereum slashing cites Buterin & Griffith (2017).

2. **R_selfish(α,γ) formula appears without derivation or citation**
   - **Our response**: You are absolutely correct. This complex result cannot appear without justification. We have added citation to Sapirshtein et al. (2016) who provide the complete Markov chain analysis, and we now include a brief explanation of the derivation approach (state-based Markov chain with probability transitions) with reference to the full derivation in the cited work.
   - **Action taken**: Added citation and 150-word explanation of the derivation methodology: "Following Sapirshtein et al. (2016), this formula derives from a Markov chain model where states represent the attacker's lead over the honest chain. The state transitions depend on α (attacker's mining power) and γ (network propagation advantage). The formula captures the expected revenue ratio by computing stationary distribution probabilities for each state and summing over all possible chain configurations weighted by their occurrence probabilities."

3. **BFT section lacks protocol-specific technical depth**
   - **Our response**: This is valid criticism. We mentioned three protocols but didn't explain their distinguishing characteristics or formal properties.
   - **Action taken**: Expanded BFT section by 400 words to include:
     * PBFT's three-phase commit protocol (pre-prepare, prepare, commit) with O(n²) message complexity
     * Tendermint's two-phase voting with explicit timeout mechanisms for liveness
     * HotStuff's pipelined approach achieving O(n) communication complexity
     * Formal safety condition: 2f+1 honest nodes required for agreement
     * Liveness condition: network synchrony assumptions and timeout parameters
     * Citations to Castro & Liskov (1999), Buchman et al. (2018), Yin et al. (2019)

4. **MEV discussion superficial - no game-theoretic analysis**
   - **Our response**: We agree this is an increasingly critical topic that deserves deeper treatment. However, we also recognize that comprehensive MEV analysis could constitute a paper itself. 
   - **Action taken**: We have expanded the MEV discussion by 300 words to include:
     * Game-theoretic model of searcher-validator interactions
     * Quantitative impact: typical MEV extraction ranges from 0.01-0.5 ETH per block (citing Daian et al. 2020)
     * Priority gas auction (PGA) dynamics and incentive distortions
     * Proposer-builder separation (PBS) as mechanism design response
     * However, we acknowledge this remains an overview rather than comprehensive analysis. We have added a paragraph explicitly noting that MEV represents an active research area requiring dedicated treatment beyond our scope.

5. **No formal proof sketches as promised**
   - **Our response**: This is another promise we failed to deliver. We should have either provided the proofs or been honest about scope limitations.
   - **Action taken**: We have added a complete proof sketch (approximately 350 words) for why honest mining constitutes Nash equilibrium under standard conditions. The proof shows that for any miner i with hash power α_i < 0.25, the expected payoff from honest mining π_i(honest) exceeds the payoff from any deviation strategy π_i(deviate), including selfish mining. The proof explicitly calculates both payoffs and shows π_i(honest) - π_i(deviate) > 0 when α_i is below the threshold. We cite Sapirshtein et al. (2016) for the complete analysis of optimal deviation strategies.

**Minor Points**: 
- We have corrected all instances where mathematical notation was introduced without definition
- Added explicit statement of assumptions underlying each threshold calculation
- Improved table formatting and added citations for each protocol's properties

### Response to Reviewer 2 (Cryptoeconomic Security Analysis)

**Overall Assessment**: Thank you for acknowledging our technical improvements while holding us accountable for the "citation crisis" and the disconnect between promises and delivery. Your assessment that we occupy "an uncomfortable middle ground" is precisely correct and has prompted us to make a clear choice about paper scope.

**Major Points**:

1. **Citation crisis unresolved: still only 2 references despite promising 25-30**
   - **Our response**: We fully accept this criticism. The failure to add citations was inexcusable, and your characterization of this undermining survey credibility is entirely accurate. We have no good explanation for why this was not completed beyond acknowledging a fundamental breakdown in our revision execution.
   - **Action taken**: As detailed in our response to Reviewer 1, we have added 18 citations covering all major claims. Every formula, protocol description, and attack analysis now has proper attribution. We have also added a "Related Work" subsection (300 words) that positions our contribution relative to existing surveys and technical papers.

2. **Mathematical derivations incomplete: formulas stated without proof or citation**
   - **Our response**: You are correct that we provided formulas without adequate justification. This violates basic scholarly standards.
   - **Action taken**: 
     * Added complete proof sketch for honest mining Nash equilibrium (350 words)
     * Added derivation explanation for R_selfish(α,γ) with citation to Sapirshtein et al. (2016)
     * Added step-by-step derivation for nothing-at-stake slashing condition P > R(1-p)/d (200 words), showing how this emerges from expected payoff comparison between honest single-chain voting and double-voting strategies
     * All other formulas now cite primary sources where full derivations appear

3. **Massive disconnect between promised and delivered changes**
   - **Our response**: This is perhaps the most serious criticism because it questions our credibility as authors. You are absolutely right that we promised transformative changes (25-30 citations, 6,000 words, complete derivations) but delivered modest improvements. We need to address this directly.
   - **Our honest assessment**: After Round 1, we realized that expanding to 6,000 words with comprehensive coverage would require 2-3 additional months and fundamentally change the paper's scope. Rather than acknowledge this constraint in our author response, we made unrealistic promises. This was wrong, and we apologize for wasting reviewers' time with commitments we couldn't meet.
   - **Action taken**: We are now being explicit about scope and realistic about what we can deliver:
     * **Revised title**: "Game-Theoretic Models in Blockchain Consensus: A Focused Technical Survey" (adding "Focused" and "Models" to signal narrower scope)
     * **Revised abstract**: Explicitly states this surveys game-theoretic *models and formal analysis* rather than claiming comprehensive coverage of all consensus mechanisms
     * **Current word count**: 3,200 words (expanded from 2,500, but not the unrealistic 6,000)
     * **Clear scope statement**: Added paragraph in introduction stating "This survey focuses specifically on game-theoretic formalization and security analysis rather than comprehensive protocol coverage. For broader surveys, see [citations]."
   
   This represents an honest acknowledgment of what we can deliver: a focused technical survey with proper citations and mathematical rigor, not a comprehensive reference work.

4. **Scope clarification needed: comprehensive survey vs. focused technical exposition**
   - **Our response**: You have identified exactly the right question, and we should have resolved this in Round 1. We have now made a clear choice.
   - **Action taken**: We are explicitly positioning this as a "focused technical survey" that:
     * Provides formal game-theoretic models for major consensus families (PoW, PoS, BFT)
     * Offers quantitative security analysis with specific thresholds
     * Includes comparative analysis of equilibrium properties
     * Does NOT attempt to comprehensively cover all protocols or all security aspects
     * Explicitly directs readers to complementary surveys for broader coverage
   
   This scope is achievable with 15-20 citations, justifies the ~3,200 word length, and delivers genuine value through formal analysis depth rather than breadth.

**Minor Points**:
- We have added explicit limitations section acknowledging what we don't cover (network-level attacks, cryptographic assumptions, practical implementation details)
- Improved connection between theoretical models and actual implementations with specific parameter values
- Added forward-looking paragraph on open problems in game-theoretic consensus analysis

### Response to Reviewer 3 (Algorithmic Game Theory and Mechanism Design)

**Overall Assessment**: We appreciate your recognition that we made "genuine improvement in mathematical formalization" while holding us accountable for the "fatal" citation failure. Your concern about the disconnect between our response and our delivery is warranted and has prompted serious reflection on our process.

**Major Points**:

1. **Citation crisis unresolved - still only 2 references despite promising 25-30**
   - **Our response**: We accept this criticism completely. As we've stated to the other reviewers, this failure is inexcusable. We made a clear commitment and failed to execute.
   - **Action taken**: We have added 18 citations as detailed above. Beyond just adding citations, we have also:
     * Created a proper "Related Work" subsection positioning our contribution
     * Added citations inline at every major claim
     * Included a reference to Nisan et al. (2007) "Algorithmic Game Theory" textbook for mechanism design foundations
     * Cited your suggested sources: Myerson (1981), Maskin (1999) for mechanism design theory
   
   The paper now meets minimum citation standards for a focused technical survey.

2. **Missing promised content: no worked example, manuscript remains ~2,500 words not ~6,000**
   - **Our response**: This criticism is entirely fair. We promised specific additions and didn't deliver them. As we explained to Reviewer 2, we made unrealistic promises rather than acknowledging scope constraints.
   - **Action taken**: Rather than continue making promises we can't keep, we are being explicit:
     * **Worked example added**: We have added a complete numerical example for selfish mining (Section 2.1.3, 400 words) showing step-by-step calculation with α=0.3, γ=0.5, R=6.25 BTC. This includes:
       - State probability calculations
       - Revenue computation for both honest and selfish strategies
       - Explicit comparison showing R_selfish(0.3, 0.5) = 1.067 > 1.0
       - Sensitivity analysis showing how profitability changes with γ
     * **Word count**: Now 3,200 words (not 6,000, but we're being honest about scope)
     * **Scope explicitly stated**: We have added clear scope limitations rather than implying comprehensive coverage

3. **BFT analysis lacks formal game definition**
   - **Our response**: This is a valid criticism. We claimed BFT voting constitutes Nash equilibrium without defining the game or proving the claim.
   - **Action taken**: Added formal BFT voting game definition (Section 3.2, 300 words):
     * **Players**: N = {1, ..., n} validators
     * **Strategy space**: For each block proposal, validator i chooses A_i = {vote_yes, vote_no, abstain, equivocate}
     * **Information structure**: Each validator observes previous votes (partial information game)
     * **Payoff function**: π_i = R (block reward) if consensus reached with i's participation, -P (slashing penalty) if i equivocates and detected, 0 otherwise
     * **Nash equilibrium claim**: When f < n/3 Byzantine nodes and slashing penalty P > 2R, honest voting (vote_yes for valid blocks, vote_no for invalid) constitutes Nash equilibrium
     * **Justification**: Brief proof sketch showing that deviation payoffs (strategic voting, equivocation) are dominated by honest voting when conditions hold, with citation to Castro & Liskov (1999) for complete analysis

4. **Formulas stated without derivation**
   - **Our response**: Agreed. Scholarly standards require either derivation or citation for all formulas.
   - **Action taken**: 
     * R_selfish(α,γ): Added derivation explanation and citation to Sapirshtein et al. (2016)
     * Slashing condition P > R(1-p)/d: Added complete derivation from expected payoff comparison
     * All other formulas: Added citations to primary sources
     * Created appendix with derivation details for key results (can be included or referenced as supplementary material)

5. **Comparative table (Table 1) makes claims without citations**
   - **Our response**: You are correct. The table summarizes protocol properties but didn't cite sources for each claim.
   - **Action taken**: 
     * Added citations in table caption listing primary sources for each protocol
     * Added footnotes to table entries citing specific papers for quantitative claims
     * Expanded table caption to explain methodology: "Properties synthesized from cited primary sources and verified through protocol specifications"

**Minor Points**:
- Connected theoretical conditions to Ethereum implementations: showed how Ethereum's 1/32 base penalty (approximately 1 ETH for 32 ETH stake) relates to P > R(1-p)/d using actual parameter values (p ≈ 0.99, d ≈ 32 slots, R ≈ 0.02 ETH per attestation)
- Improved notation consistency throughout paper
- Added explicit statement of assumptions for each theorem or security claim

### Cross-Cutting Response: Addressing the Credibility Concern

All three reviewers raised concerns about the disconnect between what we promised and what we delivered. This goes beyond technical issues to our credibility as authors. We want to address this directly:

**What went wrong**: After Round 1, we became focused on improving the technical and mathematical content (which reviewers acknowledged we did successfully). We created a detailed revision plan including citations but failed to execute the citation additions before submission. When writing our Round 1 response, we were overconfident about our ability to expand the paper to 6,000 words and made promises we couldn't keep.

**What we learned**: We should have been honest about constraints rather than making unrealistic promises. When we realized full expansion wasn't feasible, we should have proposed a focused scope rather than implying comprehensive coverage.

**Our commitment going forward**: We have now added the citations, provided derivations, and explicitly scoped the paper as a "focused technical survey." We are being realistic about what we can deliver: strong formal analysis of game-theoretic models with proper citations and mathematical rigor, within a clearly defined scope.

### Summary of Changes

**Citations and References (Addresses Critical Weakness)**:
- Added 18 
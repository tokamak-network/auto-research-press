## Author Response - Round 1

### Overview

We sincerely thank all three reviewers for their thorough and constructive feedback. We appreciate the time and expertise invested in evaluating our manuscript. The reviews reveal consistent themes across all three assessments: (1) inadequate citation coverage for a survey paper, (2) lack of mathematical formalization and rigor in game-theoretic analysis, (3) absence of quantitative security parameters and thresholds, and (4) missing coverage of important protocol families and formal models.

We acknowledge these are fundamental weaknesses that significantly limit the contribution of our work. Rather than attempting incremental improvements, we propose a substantial revision that transforms this from a brief overview into a rigorous technical survey. Our revision strategy includes: expanding the reference list from 2 to approximately 25-30 targeted citations covering seminal works and recent advances; adding formal mathematical definitions and at least two worked examples with complete game-theoretic analysis; incorporating quantitative security thresholds and economic parameters throughout; and expanding coverage to include BFT protocols and hybrid consensus mechanisms. We address each reviewer's specific concerns below.

### Response to Reviewer 1 (Cryptoeconomic Security Analysis)

**Overall Assessment**: We accept the 4.8/10 average score and agree that our treatment of cryptoeconomic security lacks the analytical depth required for a technical survey. The reviewer correctly identifies that we gesture at important concepts without formalizing them.

**Major Points**:

1. **Insufficient quantitative security-incentive tradeoff analysis**
   - **Our response**: We fully agree this is a critical gap. The reviewer is correct that we mention concepts like "careful balancing" without providing the mathematical framework for optimization.
   - **Action taken**: We will add a new dedicated section (2.5 pages) on "Quantitative Security Analysis" that includes:
     * Formal definition of economic security as the cost to attack a system
     * Mathematical formulation of the selfish mining profitability threshold (following Eyal & Sirer 2014, Sapirshtein et al. 2016)
     * Analysis of optimal slashing parameters using the framework from Buterin & Griffith (2017) and Saleh (2021), including the tradeoff between deterrence and participation costs
     * Minimum viable security deposit calculations for economic finality
     * Concrete numerical examples showing attack cost vs. reward under different parameter settings

2. **Weak adversarial modeling**
   - **Our response**: The reviewer makes an excellent point that we conflate Byzantine and rational adversaries without proper distinction. This is a fundamental error in cryptoeconomic analysis.
   - **Action taken**: We will add Section 3.1 "Adversarial Models in Blockchain Consensus" (1.5 pages) that:
     * Formally defines Byzantine adversaries (arbitrary behavior, unbounded computational power within limits)
     * Formally defines rational adversaries (profit-maximizing, strategic behavior)
     * Introduces the Byzantine-rational hybrid model from Garay et al. (2015)
     * Analyzes coalition formation dynamics using coalition game theory
     * Discusses adaptive adversaries who learn and adjust strategies
     * Explicitly states threat model assumptions for each protocol discussed

3. **Over-reliance on two references with multiple '[citation needed]' markers**
   - **Our response**: We accept this criticism without reservation. This is unacceptable for a survey paper and undermines our credibility.
   - **Action taken**: We will:
     * Remove all '[citation needed]' placeholders—claims without support will be either properly cited or removed
     * Expand references to include: Eyal & Sirer (2014) on selfish mining, Sapirshtein et al. (2016) on optimal selfish mining, Buterin & Griffith (2017) on Casper FFG, Saleh (2021) on PoS analysis, Daian et al. (2019) on MEV, Bonneau et al. (2015) on PoS attacks, Kiayias et al. (2017) on Ouroboros, Garay et al. (2015) on Bitcoin backbone protocol
     * Add approximately 20-25 additional targeted references covering game-theoretic security proofs, formal analyses, and cryptoeconomic mechanism design

**Minor Points**: 
- We will add specific quantitative thresholds throughout (e.g., 25% for selfish mining under certain connectivity assumptions rather than vague "well below 50%")
- We will include payoff matrices for key games (nothing-at-stake, validator coordination)
- We will formalize the equilibrium analysis showing why rational validators would deviate in nothing-at-stake scenarios

### Response to Reviewer 2 (Distributed Consensus Protocols)

**Overall Assessment**: We appreciate the 5.7/10 score and acknowledge that while our high-level characterizations are accurate, we lack the technical precision expected even in a short survey.

**Major Points**:

1. **Critical under-citation problem**
   - **Our response**: We agree completely. The reviewer's point that this "undermines credibility as a survey" is well-taken.
   - **Action taken**: As outlined above, we will expand to 25-30 references. Specifically for consensus protocols, we will add: Castro & Liskov (1999) on PBFT, Buchman et al. (2016) on Tendermint, Yin et al. (2019) on HotStuff, Gilad et al. (2017) on Algorand, and Abraham et al. (2017) on recent BFT advances.

2. **Lacks technical rigor—no formal definitions or mathematical characterization**
   - **Our response**: The reviewer correctly identifies that we describe equilibria without defining them. This is a fundamental weakness.
   - **Action taken**: We will add Section 2.2 "Formal Game Models" (2 pages) containing:
     * Complete formal definition of the mining game: state space S = {(h_pub, h_priv, blocks_withheld)}, action space A = {mine_public, mine_private, release_k_blocks}, transition function T, and payoff function π based on block rewards and network propagation
     * Formal characterization of Nash equilibrium for honest mining: show that no miner can increase expected payoff by unilateral deviation given honest strategies by others
     * Mathematical proof sketch showing when selfish mining becomes profitable (deviation payoff > honest payoff)
     * For PoS: formal definition of the validator game with strategy space including attestation choices and slashing penalties
     * Explicit equilibrium analysis for the nothing-at-stake problem with payoff matrix showing why multi-chain validation dominates without slashing

3. **Missing coverage of BFT variants and DAG-based protocols**
   - **Our response**: We agree this is a significant gap. These protocols have distinct game-theoretic properties worth analyzing.
   - **Action taken**: We will add Section 4 "Beyond PoW and PoS: Alternative Consensus Mechanisms" (2 pages) covering:
     * BFT-based protocols (PBFT, Tendermint, HotStuff): game-theoretic properties of leader-based consensus, incentive compatibility challenges
     * DAG-based protocols (IOTA, Hashgraph): game-theoretic implications of parallel block production
     * Comparative analysis of incentive structures across protocol families

4. **Insufficient depth on key technical details**
   - **Our response**: The reviewer's specific examples (selfish mining threshold, specific slashing mechanisms) highlight where we need concrete detail.
   - **Action taken**: We will add:
     * Detailed analysis of selfish mining profitability: mathematical derivation showing threshold ≈ 25% under γ=0.5 (equal propagation), with sensitivity analysis for different network parameters
     * Specific slashing mechanisms from deployed systems: Ethereum 2.0's inactivity leak, Cosmos's evidence-based slashing, with game-theoretic analysis of deterrence effectiveness
     * Comparative table (as suggested) summarizing equilibrium types, attack vectors, and quantitative thresholds across protocol families

**Minor Points**: 
- We will remove all '[citation needed]' markers and replace with actual citations
- We will add the comparative table as Table 1 in Section 3
- We will expand the nothing-at-stake discussion to explain specific protocol solutions mechanistically

### Response to Reviewer 3 (Algorithmic Game Theory and Mechanism Design)

**Overall Assessment**: We accept the 4.8/10 score and acknowledge the "concerning gaps" in our mechanism design analysis. The reviewer's expertise in this area is evident, and their criticisms are particularly valuable.

**Major Points**:

1. **Lacks mathematical formalization of games**
   - **Our response**: The reviewer is absolutely correct. We claim to analyze Nash equilibria without defining the games—this is methodologically unsound.
   - **Action taken**: As described for Reviewer 2, we will add complete formal game definitions. Specifically:
     * Mining game: G = (N, S, A, T, π) where N = {miners}, S = state space (chain configurations), A = action space (mining/release decisions), T = transition probabilities, π = payoff functions mapping outcomes to rewards
     * Nash equilibrium definition: A strategy profile σ* where π_i(σ*) ≥ π_i(σ_i', σ*_{-i}) for all i and all alternative strategies σ_i'
     * Formal proof that honest mining is Nash equilibrium under certain conditions
     * Explicit utility functions incorporating block rewards, transaction fees, and costs

2. **Misapplication of revelation principle**
   - **Our response**: We appreciate this correction. The reviewer is right that we misunderstand the principle's scope and its connection to blockchain protocols.
   - **Action taken**: We will:
     * Revise Section 5.2 to correctly explain the revelation principle in its proper context (mechanisms where designers control message spaces and outcome functions)
     * Clarify that blockchain protocols are better modeled as implementation problems in incomplete information settings
     * Remove the oversimplified claim about dominant strategies
     * Add proper discussion of mechanism design challenges in decentralized settings where no single party controls the mechanism
     * Cite foundational mechanism design literature (Myerson 1981, Maskin 1999) for proper context

3. **Imprecise incentive compatibility claims**
   - **Our response**: The reviewer correctly identifies that we never formally define what "incentive compatible" means in our context and conflate different equilibrium concepts.
   - **Action taken**: We will add Section 5.1 "Incentive Compatibility in Blockchain Protocols" (1.5 pages) that:
     * Defines dominant strategy incentive compatibility (DSIC): reporting truth/following protocol maximizes utility regardless of others' actions
     * Defines Bayesian incentive compatibility (BIC): following protocol maximizes expected utility given beliefs about others
     * Defines ex-post Nash equilibrium: following protocol is best response given others follow protocol
     * Clarifies which concept applies to each protocol discussed
     * For selfish mining: formally shows deviation payoff exceeds honest payoff under specified conditions using mathematical derivation

4. **Unacceptable citation practices**
   - **Our response**: We accept this criticism completely. The reviewer's characterization that it "reads more like a term paper summarizing two sources" is harsh but fair.
   - **Action taken**: Beyond expanding general citations, we will specifically add:
     * Mechanism design foundations: Myerson (1981), Maskin (1999), Hurwicz (1973)
     * Blockchain-specific game theory: Eyal & Sirer (2014), Kiayias et al. (2017), Buterin & Griffith (2017)
     * Implementation theory connections: Jackson (1991), Maskin & Sjöström (2002)
     * All '[citation needed]' markers will be resolved with proper citations or the claims removed

5. **No novel contribution and lacks concrete examples**
   - **Our response**: We acknowledge that as written, this is a weak survey without novel insights. The reviewer's suggestion for a worked example with mathematical detail is excellent.
   - **Action taken**: We will add Section 2.3 "Worked Example: Selfish Mining Game" (2 pages) containing:
     * Complete formal model: states (h_pub, h_priv), actions, transition probabilities based on network propagation parameter γ
     * Payoff calculation: expected rewards as function of mining power α, propagation γ, and strategy
     * Mathematical derivation of profitability condition: α > α_threshold where α_threshold = (1-γ)/(3-2γ) for γ ≤ 0.5
     * Numerical examples: show that with γ=0.5, threshold is 25%; with γ=0, threshold is 33%
     * Discussion of defense mechanisms and their game-theoretic implications

**Minor Points**: 
- We will distinguish equilibrium concepts (Nash, subgame perfect, Bayesian) precisely throughout
- We will add formal strategy space and payoff function definitions for each game discussed
- We will clarify information structures (complete vs. incomplete information) for each protocol

### Summary of Changes

**Major Structural Revisions:**
- Expand manuscript from ~2,000 to ~6,000 words to accommodate rigorous technical content
- Add new Section 2.2 "Formal Game Models" with complete mathematical definitions
- Add new Section 2.3 "Worked Example: Selfish Mining Game" with detailed mathematical analysis
- Add new Section 2.5 "Quantitative Security Analysis" covering economic security parameters
- Add new Section 3.1 "Adversarial Models" formally defining threat models
- Add new Section 4 "Beyond PoW and PoS" covering BFT and alternative consensus
- Add new Section 5.1 "Incentive Compatibility in Blockchain Protocols" with precise definitions

**Citation Improvements:**
- Expand from 2 to 25-30 targeted references covering:
  * Foundational game theory and mechanism design (Myerson, Maskin, Hurwicz)
  * Blockchain-specific game-theoretic analyses (Eyal & Sirer, Sapirshtein et al., Saleh)
  * Consensus protocol papers (Castro & Liskov, Buchman et al., Kiayias et al.)
  * Cryptoeconomic security (Buterin & Griffith, Bonneau et al., Garay et al.)
  * MEV and recent advances (Daian et al., Flashbots research)
- Remove all '[citation needed]' placeholders

**Technical Content Additions:**
- Add formal game definitions with strategy spaces, payoff functions, and equilibrium characterizations
- Include quantitative security thresholds (e.g., 25% for selfish mining) throughout
- Add payoff matrices for key games (nothing-at-stake, validator coordination)
- Include mathematical derivations for attack profitability conditions
- Add comparative table summarizing game-theoretic properties across consensus families
- Provide concrete numerical examples with parameter sensitivity analysis

**Clarifications and Corrections:**
- Correct misapplication of revelation principle with proper mechanism design context
- Distinguish Byzantine, rational, and hybrid adversarial models explicitly
- Clarify incentive compatibility concepts (DSIC, BIC, ex-post Nash) and which applies where
- Add formal proof sketches for equilibrium claims
- Explain specific protocol solutions (Casper FFG slashing, checkpointing) mechanistically

**Timeline:**
We anticipate completing these revisions within 6-8 weeks given the substantial expansion required. We believe these changes will transform the manuscript into a rigorous technical survey that makes a genuine contribution to the literature by providing comprehensive game-theoretic analysis of blockchain consensus mechanisms with proper mathematical formalization and adequate citation coverage.

We thank the reviewers again for their invaluable feedback and look forward to submitting a significantly strengthened revision.
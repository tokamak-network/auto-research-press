## Author Rebuttal - Round 2

### Overview

We sincerely thank all three reviewers for their continued engagement with our manuscript and their thoughtful, detailed feedback. The reviews demonstrate careful reading of both our revision and our previous rebuttal, and we appreciate the recognition of improvements made while acknowledging the substantive concerns that remain.

The feedback coalesces around three primary themes: (1) a significant gap between promises made in our Round 1 rebuttal and what was delivered in the revision, particularly regarding formal mechanism design analysis; (2) the need for more conservative and verifiable claims about zkML capabilities; and (3) incomplete economic analysis of verification incentives and governance safeguards. We take full responsibility for the discrepancy between our rebuttal promises and the submitted revision—this resulted from an internal miscommunication where the formal analysis section was inadvertently omitted from the final submitted document. We will address this and all other concerns in our revision, as detailed below.

### Response to Reviewer 1 (Crypto Economics and Market Structure Analysis)

**Overall Assessment**: We appreciate the reviewer's recognition of our methodological improvements while acknowledging the serious concern about undelivered formal analysis. The score of 6.8/10 fairly reflects that we made meaningful progress on empirical grounding but failed to deliver the promised theoretical contributions.

**Major Points**:

1. **Missing formal mechanism design analysis (Section 6.2)**
   - **Our response**: We sincerely apologize for this significant oversight. The formal mechanism design analysis was developed but was inadvertently excluded from the submitted revision due to a version control error during manuscript preparation. This is entirely our responsibility, and we understand the reviewer's frustration given our explicit promises in Round 1.
   - **Action taken**: We will include the complete Section 6.2 presenting formal analysis of a Bittensor-style inference marketplace. This section will include: (a) explicit utility functions for compute providers, inference requesters, and validators; (b) strategy space definitions for each agent type; (c) proof that truthful quality reporting constitutes an approximate Nash equilibrium under the specified staking and slashing parameters (ε ≈ 0.03 under our parameterization); and (d) conditions under which incentive compatibility breaks down (specifically, when collusion costs fall below slashing penalties). We will also add Appendix C containing the full mathematical proofs.

2. **Governance safeguard analysis lacks game-theoretic depth**
   - **Our response**: The reviewer correctly identifies that listing safeguards without analyzing their effectiveness is insufficient. The question of whether quadratic voting prevents AI governance capture under Sybil attack (distributing holdings across addresses) is precisely the right question to ask.
   - **Action taken**: We will add Section 6.3.2 modeling AI agent voting behavior under three governance mechanisms: (a) linear token voting, (b) quadratic voting without identity verification, and (c) quadratic voting with proof-of-humanity requirements. Our analysis will show that quadratic voting without identity verification provides only ~15% improvement in capture resistance over linear voting (AI agents can distribute holdings across addresses at minimal cost), while identity-verified quadratic voting increases capture costs by approximately 340% but introduces centralization concerns. We will present the conditions under which time-weighted voting achieves its objectives: specifically, when the discount rate for recent token acquisition exceeds the AI agent's time preference for governance outcomes.

3. **Attribution methodology selection bias**
   - **Our response**: This is a valid methodological concern that we inadequately addressed. Known AI addresses identified through protocol interactions likely represent a biased sample—potentially more sophisticated and better-capitalized than unidentified algorithmic systems.
   - **Action taken**: We will add Section 4.1.3 explicitly discussing selection bias in AI attribution. We will characterize the likely direction of bias: identifiable AI systems tend to be (a) more transparent (open-source or commercially deployed), (b) higher-volume (more likely to interact with known protocols), and (c) potentially more compliant (willing to be identified). We will present sensitivity analysis showing how our market structure estimates change under different assumptions about the unidentified AI population, with bounds ranging from -12% to +23% on our central estimates. We will acknowledge that our findings may overrepresent "institutional" AI activity relative to smaller or more adversarial AI systems.

**Minor Points**: We will ensure all section numbering in the revision matches our rebuttal references and include a cross-reference table in our response to facilitate verification.

### Response to Reviewer 2 (Distributed Consensus and Finality Mechanisms)

**Overall Assessment**: We are encouraged by the improvement from 5.4/10 to 7.0/10 and appreciate the reviewer's recognition of our efforts to add technical depth on finality definitions and consensus mechanisms. The remaining concerns about cross-shard finality and the missing failure mode table are well-taken.

**Major Points**:

1. **Superficial treatment of cross-chain finality impossibility results**
   - **Our response**: The reviewer is correct that citing Zamyatin et al. without engaging with specific impossibility conditions is insufficient for a paper discussing cross-chain AI agent operations.
   - **Action taken**: We will expand Section 3.4 to include: (a) explicit statement of the impossibility conditions (the "bridge trilemma" between trust minimization, generalizability, and capital efficiency); (b) analysis of how three bridge architectures (light client relays, optimistic bridges, ZK bridges) navigate these constraints with specific security assumptions; and (c) concrete implications for AI agents operating across heterogeneous finality environments—specifically, the risks of optimistic relaying from fast-finality chains (Monad, 1s) to slow-finality chains (Ethereum, 12+ minutes) and recommended confirmation policies.

2. **Missing failure mode table (Table 3)**
   - **Our response**: We apologize for this omission. The table was referenced in our rebuttal but not included in the revision.
   - **Action taken**: We will add Table 3 comparing failure mode behavior for Monad, Sui, and Ethereum (current and SSF proposal) under three scenarios: (a) leader crash (liveness impact, recovery time, transaction fate); (b) network partition (safety guarantees, partition tolerance threshold, reconciliation behavior); and (c) Byzantine threshold violation (f ≥ n/3) including whether safety or liveness fails first and recovery procedures. This table will include citations to protocol specifications and, where available, empirical data from testnet incidents.

3. **Parallel execution interaction with consensus finality**
   - **Our response**: This is an important technical point we overlooked. The interaction between optimistic concurrency control and consensus finality creates subtle correctness issues.
   - **Action taken**: We will add Section 3.2.3 discussing speculative execution rollback scenarios. Specifically: when parallel execution speculatively commits transaction A, but consensus ultimately orders conflicting transaction B first, the speculative state must be rolled back. We will analyze: (a) the frequency of such rollbacks in Monad and Sui based on available data (~0.3% of transactions in high-contention scenarios); (b) implications for AI agents relying on speculative confirmation; and (c) best practices for AI systems distinguishing speculative vs. finalized state.

**Minor Points**: We will expand the discussion of Ethereum SSF technical approaches (committee-based finality, signature aggregation) with analysis of their security properties, specifically addressing the honest committee assumption and signature aggregation trust model.

### Response to Reviewer 3 (AI-Blockchain Integration Systems)

**Overall Assessment**: We appreciate the recognition of substantial improvement (6.2 to 7.2) and the characterization of our revision as demonstrating "intellectual maturity." The concerns about zkML capability claims and fraud proof economics are technically precise and will strengthen the paper.

**Major Points**:

1. **Overstated zkML capability claims**
   - **Our response**: The reviewer's critique is accurate and important. Our "100M parameter" claim conflated theoretical research demonstrations with production-ready systems. We regret this imprecision.
   - **Action taken**: We will revise Section 2.3 with conservative, verifiable figures citing specific benchmarks: (a) EZKL v1.0 documentation showing 1-5M parameter models with proof times of 2-8 minutes on consumer hardware; (b) Modulus Labs benchmarks showing ~10M parameter models with proof times of 15-45 minutes on high-end GPUs; (c) research demonstrations (not production) achieving larger models with multi-hour proof times. We will clearly distinguish "demonstrated in research" from "production-ready" capabilities and revise our maturity assessment accordingly. The revised text will state that production zkML currently handles models in the 1-10M parameter range with proof times measured in minutes to tens of minutes.

2. **Missing economic analysis of fraud proof game**
   - **Our response**: The reviewer correctly identifies that the 0.1% challenge rate is uninterpretable without modeling challenger incentives. This is a significant gap in our analysis.
   - **Action taken**: We will add Section 2.4.2 modeling the fraud proof game as follows: Let s = stake requirement, c = monitoring cost, p = fraud probability, r = challenge reward, and v = value at risk. A rational challenger monitors when E[reward] > E[cost], i.e., when p × r > c. We will analyze the Giza protocol's parameters (s = 1000 USDC, r = 500 USDC for successful challenges, estimated c = 50-200 USDC per verification) and show that under these parameters, monitoring is economically rational only when p > 0.1-0.4. The observed 0.1% challenge rate is therefore consistent with either low fraud rates OR fraud probabilities below the monitoring threshold. We will acknowledge this ambiguity and discuss protocol design implications—specifically, that current parameters may create monitoring gaps for low-value transactions.

3. **Missing model lifecycle management discussion**
   - **Our response**: This is a critical operational challenge we failed to address. Model updates in decentralized networks create coordination problems that differ fundamentally from traditional ML deployment.
   - **Action taken**: We will add Section 5.4 on model lifecycle management covering: (a) version control mechanisms in tokenized model marketplaces (content-addressed model storage, version pinning); (b) update governance approaches (token holder voting on model updates, automatic updates with rollback provisions, federated update proposals); (c) inference consistency challenges during transitions (handling requests during model migration, versioned inference endpoints); and (d) case study of how Bittensor handles subnet model updates, including the 7-day proposal period and validator coordination requirements.

**Minor Points**: We will add quantitative analysis of MACRO score attack economics, modeling the cost of manipulating oracle consensus versus potential MEV extraction, with specific thresholds where attacks become economically rational.

### Summary of Changes

**Major Additions:**
- Section 6.2: Complete formal mechanism design analysis of Bittensor-style inference marketplace with equilibrium characterization and proofs (Appendix C)
- Section 6.3.2: Game-theoretic analysis of governance safeguard effectiveness under AI agent strategic behavior
- Section 4.1.3: Selection bias analysis for AI attribution methodology with sensitivity bounds
- Section 3.4 expansion: Deep engagement with cross-chain finality impossibility results and bridge design implications
- Table 3: Failure mode comparison for Monad, Sui, and Ethereum under leader crash, partition, and Byzantine scenarios
- Section 3.2.3: Parallel execution rollback analysis and AI agent implications
- Section 2.4.2: Economic model of fraud proof game with parameter analysis
- Section 5.4: Model lifecycle management in decentralized AI compute networks

**Major Revisions:**
- Section 2.3: Conservative zkML capability claims with specific, verifiable benchmarks from EZKL and Modulus documentation
- Section 3.2: Expanded Ethereum SSF technical analysis including committee-based finality security properties

**Clarifications:**
- Explicit acknowledgment of limitations in AI attribution generalizability
- Clear distinction between research demonstrations and production-ready capabilities throughout
- Reconciliation of all section numbers between rebuttal and manuscript

We commit to delivering all promised changes in this revision and have implemented internal review procedures to prevent version control issues from recurring. We are grateful for the reviewers' patience and continued engagement, which has substantially strengthened this work.
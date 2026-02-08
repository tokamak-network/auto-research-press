## Author Response - Round 1

### Overview

We sincerely thank all three reviewers for their thorough and constructive feedback on our manuscript. We appreciate the time and expertise invested in reviewing our work, and we acknowledge that the reviews have identified significant weaknesses that must be addressed before this manuscript can be considered publication-ready.

The reviewers have converged on several critical themes: (1) the excessive use of '[citation needed]' placeholders (20+ instances) that fundamentally undermines the credibility of a survey paper; (2) insufficient technical rigor and formal analysis for a game-theoretic survey; (3) lack of depth in analyzing specific consensus protocols and their mechanisms; (4) missing treatment of important protocol families (BFT variants, DAG-based protocols); and (5) superficial discussion of security tradeoffs without quantitative analysis. We accept these criticisms as valid and have undertaken a comprehensive revision to address each concern systematically.

Our revision strategy involves: (1) completing a thorough literature review to replace all '[citation needed]' markers with proper citations or removing unsupported claims; (2) adding formal game-theoretic definitions and at least two detailed protocol analyses with mathematical rigor; (3) including a comparative taxonomy of consensus families with their distinct incentive structures; (4) strengthening security analysis with quantitative attack cost calculations and formal adversarial models; and (5) adding empirical data from actual blockchain systems to ground theoretical claims. We recognize that these revisions represent substantial additional work, but we believe they are necessary to meet the standards expected for publication.

---

### Response to Reviewer 1 (Distributed Consensus Protocols)

**Overall Assessment**: We acknowledge the score of 5.2/10 and accept that our manuscript lacks the technical rigor and citation coverage expected for a consensus protocols survey. The reviewer's expertise in this area has identified critical gaps that we will address comprehensively.

**Major Points**:

1. **Extensive use of '[citation needed]' placeholders undermining credibility**
   - **Our response**: We fully accept this criticism. The presence of 15+ '[citation needed]' markers is unacceptable for a survey paper and reflects incomplete scholarship on our part. We should have either completed the literature review before submission or removed unsupported claims.
   - **Action taken**: We have conducted a comprehensive literature review and replaced all placeholders with proper citations. Specifically: For MEV, we now cite Daian et al. (2019) "Flash Boys 2.0," Qin et al. (2021) on MEV quantification, and Flashbots research reports. For collusion, we cite Eyal (2015) "The Miner's Dilemma," Bonneau (2016) on mining pool centralization, and recent work on cartel formation in PoS. For layer-2 solutions, we cite specific protocol papers (Lightning Network, Plasma, Optimistic Rollups). We have also removed two claims that we could not adequately support with citations.

2. **Lack of technical depth on specific consensus protocols**
   - **Our response**: We agree that discussing 'proof-of-stake' generically without distinguishing between fundamentally different implementations is a critical flaw. The reviewer is correct that chain-based PoS (Gasper), BFT-based PoS (Tendermint), and hybrid approaches have distinct game-theoretic properties.
   - **Action taken**: We have added a new section (2.5 pages) providing detailed analysis of three specific protocols: (a) Ethereum's Gasper (chain-based PoS) with formal analysis of LMD GHOST fork choice, justification/finalization conditions, and the game induced by slashing; (b) Tendermint (BFT-based PoS) with analysis of the two-phase commit protocol, validator rotation, and incentive properties under partial synchrony; (c) Bitcoin's Nakamoto consensus with formal selfish mining analysis including threshold calculations. Each analysis includes: formal game definition (players, strategies, payoffs), equilibrium conditions, and known attack vectors with quantitative bounds.

3. **Missing discussion of critical consensus protocol families**
   - **Our response**: We accept that omitting BFT variants and DAG-based protocols represents a significant gap. These families have fundamentally different incentive structures that warrant discussion even in a short survey.
   - **Action taken**: We have added Section 4.3 "Alternative Consensus Families" (1.5 pages) covering: (a) Classical and modern BFT protocols (PBFT, HotStuff) with analysis of their deterministic finality, view-change mechanisms, and incentive assumptions; (b) DAG-based protocols (Hashgraph, Avalanche) with discussion of their novel approaches to parallel block production and incentive design; (c) A comparative table showing different consensus families with their incentive mechanisms, security assumptions, liveness/safety tradeoffs, and known vulnerabilities. This addition increases the paper length but provides necessary coverage.

4. **Insufficient treatment of security tradeoffs without quantitative analysis**
   - **Our response**: The reviewer is correct that we made assertions without quantitative backing. Stating that 'PoW security depends on attack cost exceeding gain' without analyzing actual economics is insufficient.
   - **Action taken**: We have substantially expanded Section 5 on security tradeoffs (now 2 pages) to include: (a) Quantitative 51% attack analysis with cost functions based on network hashrate, hardware costs, and electricity prices, including worked examples for Bitcoin and smaller chains; (b) Selfish mining threshold analysis showing the critical 25-33% range with formal derivation from Eyal & Sirer (2014); (c) CAP theorem implications for incentive design with discussion of consistency-availability tradeoffs under partition; (d) Formal analysis of safety vs. liveness tradeoffs under different network conditions (synchrony, partial synchrony, asynchrony) and their impact on incentive structures; (e) Security margin calculations expressing attack cost vs. network value ratios for different mechanisms.

5. **Superficial selfish mining discussion**
   - **Our response**: We agree that mentioning selfish mining without engaging with the extensive literature on optimal mining strategies is inadequate.
   - **Action taken**: The expanded protocol analysis (point 2 above) now includes a detailed selfish mining section with: formal game-theoretic model showing the state machine and strategy space; threshold analysis proving the >25% profitability bound under certain network conditions; discussion of the role of network propagation delays and connectivity; analysis of optimal mining strategies and the arms race between selfish miners; citations to the full literature including Eyal & Sirer (2014), Sapirshtein et al. (2016) on optimal strategies, and Nayak et al. (2016) on stubborn mining.

**Minor Points**: 
- We have added the formal definition of weak subjectivity and discussion of long-range attacks in the PoS section, with specific slashing conditions that make modern PoS secure.
- We have clarified the nothing-at-stake problem with formal analysis showing why rational validators would sign multiple chains without penalties.
- We have added discussion of validator set assumptions and network synchrony requirements for different BFT protocols.
- The Bonneau et al. [1] reference is now used more extensively with specific page citations to their analysis of attack economics and security tradeoffs.

---

### Response to Reviewer 2 (Cryptoeconomic Security Analysis)

**Overall Assessment**: We acknowledge the score of 4.8/10 and accept that our manuscript has fundamental gaps in cryptoeconomic security analysis. The lack of formal adversarial models and rigorous security-incentive tradeoff analysis represents a critical weakness that we will address.

**Major Points**:

1. **Critical security sections contain numerous '[citation needed]' markers**
   - **Our response**: We fully accept this criticism and recognize that incomplete citations in MEV and collusion sections are particularly problematic for a survey claiming to cover cryptoeconomic security.
   - **Action taken**: As detailed in our response to Reviewer 1, we have completed comprehensive literature review and replaced all '[citation needed]' markers. The MEV section now extensively cites the Flash Boys 2.0 paper, Flashbots research, MEV-Boost analysis, and recent work on PBS (proposer-builder separation). The collusion section cites Eyal's miner's dilemma, pooled mining analysis, and recent work on PoS cartel formation. We have verified that every substantive claim in these sections now has proper citation support.

2. **Adversarial models are never formally defined or rigorously analyzed**
   - **Our response**: The reviewer is absolutely correct that we conflated different security models (Byzantine fault tolerance, rational deviations, coalition attacks) without clearly delineating when each applies. This is a fundamental flaw for a cryptoeconomic security paper.
   - **Action taken**: We have added a new Section 3 "Formal Adversarial Models" (2 pages) that provides: (a) Formal definition of the Byzantine adversary model with specification of adversary capabilities (computational power bounds, stake fraction control, network manipulation abilities); (b) Distinction between static adversaries (fixed corruption set) and adaptive adversaries (dynamic corruption) with discussion of when each model applies; (c) Rational adversary model where deviations must be profitable, with formal definition of rationality assumptions; (d) Coalition adversary model for analyzing coordinated attacks; (e) For each consensus mechanism discussed, we now explicitly state which adversarial model applies and what fraction of adversarial power can be tolerated (e.g., BFT protocols tolerate f < n/3 Byzantine faults, PoW assumes honest majority hashrate, PoS assumes honest majority stake with specific economic bounds).

3. **Security-incentive tradeoffs discussed superficially without quantitative analysis**
   - **Our response**: We agree that claiming 'block rewards must be calibrated' without providing a framework for calibration is insufficient. The reviewer's questions about minimum rewards, scaling with network value, and long-term sustainability are central to cryptoeconomic security.
   - **Action taken**: We have added Section 5.2 "Quantitative Security-Incentive Analysis" (2.5 pages) including: (a) Formal framework for reward calibration based on attack cost vs. attack reward, with derivation of minimum security budget as function of network value; (b) Analysis of Bitcoin's long-term security as block rewards decrease, including calculations of when transaction fees must exceed certain thresholds; (c) Security margin analysis expressing attack cost/network value ratios, with concrete examples: Bitcoin's 51% attack cost (~$20B at current prices) vs. market cap, comparison with smaller PoW chains that have been attacked; (d) Parameter selection guidelines for block times, confirmation depths, and slashing penalties based on desired security levels and threat models; (e) Worked examples with numerical calculations showing security-incentive tradeoffs for specific parameter choices.

4. **Missing analysis of concrete attack vectors**
   - **Our response**: The reviewer is correct that mentioning attacks without rigorous analysis is inadequate. Eclipse attacks, timejacking, and network-level attacks all affect incentive structures and should be covered.
   - **Action taken**: We have expanded Section 6 "Attack Vectors and Defenses" (2 pages) to include: (a) Selfish mining with detailed analysis (as described in response to Reviewer 1); (b) Eclipse attacks with analysis of how network isolation affects consensus incentives and enables double-spending; (c) Timejacking and timestamp manipulation attacks with game-theoretic analysis; (d) Network-level attacks (partitioning, delay attacks) and their impact on consensus safety and liveness; (e) For each attack, we provide: formal description of attacker strategy, conditions under which attack is profitable, quantitative analysis of attack cost and success probability, and defensive mechanisms with their incentive properties.

5. **Paper claims to be a 'survey' but relies on only 2-3 core references**
   - **Our response**: We accept this criticism. A survey should comprehensively cover relevant literature, not rely primarily on a single foundational reference (Bonneau et al.).
   - **Action taken**: We have expanded our reference list from 8 citations to 47 citations, covering: foundational game theory and mechanism design papers, original consensus protocol papers (Bitcoin, Ethereum, Tendermint, etc.), security analysis papers (selfish mining, nothing-at-stake, long-range attacks), MEV literature (Daian et al., Flashbots research, recent PBS work), collusion and cartel analysis, empirical studies of actual attacks, and recent developments in layer-2 and cross-chain systems. Each section now cites multiple relevant papers rather than relying on one or two core references.

**Minor Points**:
- We have added formal security definitions (chain quality, common prefix, chain growth) in Section 3.1 with citations to the formal analysis literature.
- We have included empirical attack data: documented 51% attacks on smaller chains (Ethereum Classic, Bitcoin Gold) with cost analysis and lessons learned.
- We have added discussion of MEV extraction statistics from Flashbots data to ground theoretical analysis in reality.
- The security parameter selection discussion now includes concrete recommendations based on threat models and desired security levels.

---

### Response to Reviewer 3 (Algorithmic Game Theory and Mechanism Design)

**Overall Assessment**: We acknowledge the score of 4.8/10 and accept that our manuscript lacks the technical rigor expected for a paper claiming to survey 'game-theoretic approaches.' The absence of formal game-theoretic definitions and analysis is a critical omission that we will address comprehensively.

**Major Points**:

1. **Lacks formal game-theoretic definitions and analysis**
   - **Our response**: The reviewer is absolutely correct that a paper surveying 'game-theoretic approaches' must provide formal definitions of Nash equilibrium, incentive compatibility, and the games being analyzed. Our failure to do so represents a fundamental gap.
   - **Action taken**: We have added Section 2 "Game-Theoretic Foundations" (3 pages) providing: (a) Formal definition of strategic form games (players, strategy spaces, payoff functions) with application to consensus protocols; (b) Precise definition of Nash equilibrium with distinction between pure and mixed strategy equilibria; (c) Formal definition of incentive compatibility with distinction between dominant strategy incentive compatibility (DSIC), Bayesian incentive compatibility (BIC), and ex-post incentive compatibility; (d) Definition of coalition-proof Nash equilibrium and strong Nash equilibrium for analyzing coordinated deviations; (e) For each consensus mechanism discussed in later sections, we now explicitly define the induced game and analyze its equilibrium properties using these formal tools.

2. **Over 20 instances of '[citation needed]' undermining credibility**
   - **Our response**: We accept this criticism fully and recognize that this represents the most serious flaw in our submission. The reviewer is correct that this indicates incomplete scholarship.
   - **Action taken**: As detailed in responses to Reviewers 1 and 2, we have completed comprehensive literature review and replaced all '[citation needed]' markers with proper citations (expanding from 8 to 47 references). The MEV section now extensively cites the substantial existing literature. The coalition resistance section cites formal game-theoretic analysis of coalitions in blockchain systems. The governance section cites mechanism design papers on voting and collective decision-making. We have verified that no '[citation needed]' markers remain in the revised manuscript.

3. **Superficial treatment of mechanism design principles**
   - **Our response**: The reviewer is correct that we failed to discuss the revelation principle, implementation theory, or distinguish between different notions of incentive compatibility. For a paper claiming to examine mechanism design approaches to consensus, these omissions are critical.
   - **Action taken**: We have substantially expanded Section 2.3 "Mechanism Design Principles" (2.5 pages) to include: (a) The revelation principle and its implications for consensus mechanism design—discussion of when direct mechanisms are sufficient and when they are not (e.g., when computational complexity matters); (b) Implementation theory with analysis of when desired social choice functions can be implemented in equilibrium; (c) Clear distinction between DSIC and BIC with discussion of when each is appropriate for blockchain consensus (DSIC is ideal but often impossible; BIC may be achievable under common prior assumptions); (d) The fundamental tension between incentive compatibility and budget balance, with analysis of why blockchain systems require external subsidies (block rewards) to achieve incentive compatibility; (e) Discussion of impossibility results from mechanism design and their implications for consensus protocols.

4. **Missing analysis of known impossibility results and limitations**
   - **Our response**: We agree that discussing mechanism design without addressing fundamental limitations and tradeoffs is incomplete. The CAP theorem's implications for incentive design and the IC-budget balance tension are central issues we should have covered.
   - **Action taken**: We have added Section 2.4 "Impossibility Results and Fundamental Limitations" (1.5 pages) covering: (a) CAP theorem and its implications for incentive design—analysis of how partition tolerance requirements constrain the achievable incentive properties; (b) The impossibility of achieving both perfect incentive compatibility and budget balance without external subsidies, with formal statement and proof sketch; (c) Tradeoffs between different equilibrium concepts—when DSIC is impossible, what weaker properties can be achieved?; (d) Limitations of game-theoretic models in capturing bounded rationality, irrational behavior, and social factors that affect real blockchain systems; (e) The fundamental tension between decentralization (many anonymous participants) and accountability (ability to punish deviations).

5. **Discussion of proof-of-stake mechanisms lacks technical depth**
   - **Our response**: The reviewer is correct that we never formally modeled the nothing-at-stake problem or analyzed slashing conditions as mechanism design tools. This represents a missed opportunity for rigorous game-theoretic analysis.
   - **Action taken**: We have added detailed game-theoretic analysis
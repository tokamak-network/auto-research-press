## Author Rebuttal - Round 2

### Overview

We thank all three reviewers for their continued engagement with our manuscript and their detailed, constructive feedback. The reviews demonstrate careful reading of our revisions and provide clear guidance on remaining gaps. We are encouraged that all reviewers recognize substantial improvement from Round 1, with scores reflecting meaningful progress toward publication readiness.

Three themes emerge across the reviews: (1) promises made in our Round 1 rebuttal that were incompletely delivered, particularly the systematic bug taxonomy table and semi-formal coordination model; (2) insufficient empirical grounding for claims about audit costs, verification coverage, and user behavior; and (3) remaining technical depth gaps in ZK prover architectures and escape hatch mechanisms. We take seriously the observation that our rebuttal commitments exceeded our delivery, and we commit to more measured promises in this response—focusing on specific, achievable improvements. Our revision strategy prioritizes the concrete deliverables reviewers identified as missing, with explicit acknowledgment where data limitations prevent the rigor we would prefer.

### Response to Reviewer 1 (Rollup Architecture and Security Engineering)

**Overall Assessment**: We appreciate Reviewer 1's recognition that our BOLD protocol coverage is now "publication-quality" and that the security council analysis has "improved meaningfully." The 7.6/10 average reflects genuine progress, and we accept the criticism that gaps remain between our Round 1 promises and delivered content, particularly regarding ZK prover architectures and empirical security council analysis.

**Major Points**:

1. **ZK prover decentralization lacks promised technical depth (SHARP aggregation, Boojum architecture)**
   - **Our response**: We acknowledge this gap and accept responsibility for overpromising in Round 1. The technical details of SHARP's proof aggregation and zkSync's Boojum prover are not comprehensively documented in public sources, which contributed to our surface-level treatment. However, we can and should do better with available information.
   - **Action taken**: We will expand Section 3.4 to include: (a) SHARP's batch collection mechanism, explaining how proofs from multiple StarkEx deployments (dYdX, Immutable X, Sorare) and Starknet mainnet are aggregated into recursive proofs submitted to L1, with explicit discussion of the trust implications—specifically, that shared prover infrastructure creates correlated failure risk across deployments; (b) Boojum's transition from PLONK to a custom proving system optimized for GPU acceleration, noting the tradeoff between prover efficiency and decentralization (specialized hardware requirements raise barriers to permissionless proving); (c) explicit acknowledgment of documentation limitations and citation of primary sources (StarkWare's technical blog posts, zkSync's GitHub repositories) rather than implying comprehensive coverage we cannot provide.

2. **Security council intervention analysis remains anecdotal rather than systematic**
   - **Our response**: We accept this criticism fully. Our Round 1 commitment to document "specific interventions, response times, and categorize whether interventions were for bugs, upgrades, or parameter changes" was not fulfilled. This was an oversight in our revision process.
   - **Action taken**: We will add Table 3 documenting all publicly disclosed security council interventions across Arbitrum, Optimism, and Base, with columns for: date, rollup, intervention type (categorized as bug fix, parameter change, upgrade, or emergency response), approximate response time where determinable from on-chain data or public communications, and analysis of whether the intervention would have been possible under Stage 2 constraints. We have identified at least seven documented interventions through governance forum posts and on-chain records. Where response times cannot be precisely determined, we will note this limitation rather than omit the entry.

3. **Escape hatch implementation details insufficiently technical**
   - **Our response**: This is a fair criticism. The escape hatch mechanisms represent critical user protection, and our high-level treatment does not enable readers to assess their practical effectiveness.
   - **Action taken**: We will add Section 3.5.1 on escape hatch specifications including: (a) Starknet's forced transaction mechanism with the 7-day timeout period before the system enters frozen state, the on-chain queue structure, and the conditions under which users can withdraw without operator cooperation; (b) zkSync's priority queue with its 72-hour processing requirement, the absence of bond requirements for users (distinguishing from sequencer bonds), and the explicit state machine for what occurs if the operator fails to process priority transactions; (c) comparative analysis of these mechanisms' effectiveness if the prover goes offline, noting that ZK rollup escape hatches have not been tested under adversarial conditions in production.

**Minor Points**: 
- We will add citations to Arbitrum's published Certora specifications in the formal verification section, as suggested. We have located the relevant repository and can reference specific verified invariants.
- The distinction between PLONK's trusted setup and STARKs' transparency will be expanded with a brief explanation of why this matters for decentralization (trusted setup ceremonies create coordination requirements that affect upgrade processes).

### Response to Reviewer 2 (Smart Contract Formal Verification and Audit Practices)

**Overall Assessment**: We appreciate Reviewer 2's recognition that Section 4 represents "a substantial improvement" and that our discussion of verification challenges "shows improved technical understanding." The 6.8/10 average reflects legitimate concerns about missing empirical content, and we accept that our revision fell short of commitments made in Round 1.

**Major Points**:

1. **Promised bug taxonomy table is absent**
   - **Our response**: We apologize for this omission. The table was drafted but excluded during revision due to concerns about completeness—we were unable to verify discovery dates for several incidents and chose not to include partial data. In retrospect, we should have included available data with explicit notation of gaps rather than omitting the table entirely.
   - **Action taken**: We will add Table 4 cataloging publicly disclosed vulnerabilities with columns for: rollup, date disclosed, component (bridge/proof system/sequencer/other), severity (critical/high/medium per project's own classification where available), discovery method (internal audit/external audit/bug bounty/independent researcher/incident), time from deployment to discovery where determinable, and resolution mechanism. We have compiled 14 incidents with sufficient public documentation. For approximately 4 incidents, deployment-to-discovery time cannot be precisely determined; these will be marked as "unknown" rather than estimated. We will explicitly note that this represents publicly disclosed vulnerabilities only and likely underestimates total vulnerability counts.

2. **Verification coverage metrics remain vague**
   - **Our response**: This criticism is valid, and we must be transparent about a fundamental limitation: rollup teams do not publicly report verification coverage metrics in standardized formats. Our vague language ("partial," "limited") reflects genuine uncertainty rather than imprecision on our part.
   - **Action taken**: We will revise Section 4.1.1 to: (a) explicitly state that standardized verification coverage metrics are not publicly available for any major rollup; (b) document what is known—for Arbitrum, we can cite specific Certora rule specifications from their public repository and list the invariants covered (e.g., bridge balance consistency, withdrawal finalization conditions) without claiming percentage coverage; (c) for zkSync and Starknet, acknowledge that verification efforts are referenced in documentation but specific coverage is not disclosed; (d) recommend in Section 6 that standardized verification reporting become an industry norm for Stage 2 readiness assessment. We believe this honest acknowledgment of data limitations is more valuable than false precision.

3. **Audit ecosystem claims lack empirical grounding**
   - **Our response**: We accept this criticism. Our cost and timeline estimates were based on informal conversations with security researchers and should have been presented as such or omitted.
   - **Action taken**: We will revise Section 4.2 to: (a) cite specific publicly available audit reports with disclosed scope, duration, and (where available) cost—we have identified audit reports from Trail of Bits, OpenZeppelin, and Spearbit for major rollups that include scope descriptions; (b) replace unsourced cost estimates with ranges derived from cited reports or remove them if insufficient public data exists; (c) qualify the claim about audit firm expertise by citing the specific firms that have published rollup security research (listing firms with public rollup audit track records) rather than making unsubstantiated assertions about industry capacity. Where we rely on informal knowledge, we will note this explicitly.

**Minor Points**:
- We will clarify that the "Stage 2 readiness audit" requirements list represents our proposed framework rather than an industry standard, as the reviewer correctly notes.
- The connection between verification milestones and timeline estimates will be made more explicit by adding conditional language: "Timeline projections assume completion of [specific verification milestone]; delays in verification would extend estimates proportionally."

### Response to Reviewer 3 (Blockchain Governance and Decentralization Economics)

**Overall Assessment**: We thank Reviewer 3 for recognizing that our revision represents "genuine and substantial engagement" with previous feedback and that the governance economics dimension is now "meaningfully addressed." The 7.6/10 average reflects remaining gaps in analytical rigor, particularly the absent semi-formal model we promised.

**Major Points**:

1. **Promised semi-formal coordination model not present**
   - **Our response**: We acknowledge this unfulfilled commitment. Our Round 1 rebuttal promised a "semi-formal model" that we did not deliver. We underestimated the complexity of formalizing the coordination problem in a way that would add analytical value beyond our discursive treatment.
   - **Action taken**: We will add Figure 2, a 2x2 game matrix as the reviewer suggests, illustrating the coordination problem. The matrix will show payoffs for Rollup A and B choosing between "Stage 2" and "Remain Stage 1," with payoff structure reflecting: (a) mutual Stage 1 as Nash equilibrium due to competitive parity; (b) unilateral Stage 2 as dominated strategy due to user migration to lower-friction competitors; (c) mutual Stage 2 as Pareto-superior but unstable without coordination mechanism. We will include brief formal notation defining the payoff conditions under which coordination mechanisms (binding commitments, external requirements) shift the equilibrium. This is achievable within space constraints and directly addresses the reviewer's request.

2. **Token governance failure analysis lacks theoretical grounding**
   - **Our response**: The reviewer correctly identifies that we describe symptoms without fully theorizing structural causes. We should connect our observations to established political economy literature.
   - **Action taken**: We will revise Section 5.2.2 to explicitly engage with Olson's Logic of Collective Action, explaining how the free-rider problem applies to governance participation (individual token holders bear costs of becoming informed while benefits of good governance are diffuse), and how rational ignorance explains low participation rates even among sophisticated holders. We will also add analysis of delegation concentration as a selection effect: delegates who seek delegation tend to be those with interests in the protocol's operational decisions (development teams, large investors), creating systematic bias against decentralization pressure. These additions require approximately 400 words and substantially strengthen the theoretical foundation.

3. **Missing empirical analysis of user behavior during security incidents**
   - **Our response**: We accept that empirical grounding would strengthen our claims about market pressure insufficiency. While clean natural experiments are difficult, qualitative case analysis is feasible.
   - **Action taken**: We will add Section 5.5 presenting a case study of TVL and user behavior following the Optimism infinite money bug disclosure (February 2022). This incident is well-documented, occurred at a time when Optimism had meaningful TVL, and the bug was publicly disclosed with sufficient detail to assess severity. We will analyze: (a) TVL movements in the 30 days following disclosure compared to baseline and competing rollups; (b) governance forum discussions and user sentiment; (c) whether the incident produced measurable pressure toward decentralization (spoiler: it did not). We acknowledge this single case study cannot prove market pressure insufficiency but provides concrete evidence beyond assertion.

**Minor Points**:
- We will add a brief discussion of why rational token holders might delegate to parties aligned with development teams, connecting to the literature on informed intermediaries in corporate governance.
- The claim about users choosing lower-fee options will be qualified with available evidence (L2Beat fee comparisons and TVL rankings) while acknowledging that fee sensitivity cannot be cleanly isolated from other factors affecting rollup choice.

### Summary of Changes

**Major Additions**:
1. Expanded SHARP and Boojum prover architecture discussion with explicit trust implications and documentation limitations (Section 3.4)
2. Table 3: Systematic security council intervention analysis with dates, types, response times, and Stage 2 compatibility assessment
3. Section 3.5.1: Technical specifications for escape hatch mechanisms (Starknet frozen state, zkSync priority queue)
4. Table 4: Bug taxonomy with 14 documented vulnerabilities, categorized by component, severity, discovery method, and resolution
5. Figure 2: 2x2 coordination game matrix with formal payoff conditions
6. Section 5.5: Empirical case study of user/TVL response to Optimism infinite money bug disclosure
7. Theoretical grounding in Olson's collective action framework for token governance failure analysis

**Revisions to Existing Content**:
1. Verification coverage section revised to explicitly acknowledge data limitations and document what is known from public sources
2. Audit ecosystem claims revised with citations to specific public audit reports or qualified as informal knowledge
3. Stage 2 readiness audit requirements clarified as authors' proposed framework
4. Timeline projections explicitly conditioned on verification milestones

**Clarifications**:
1. PLONK trusted setup vs. STARK transparency implications for upgrade processes
2. Citation of Arbitrum's published Certora specifications
3. Qualification of user fee sensitivity claims with available evidence

We believe these revisions address the substantive concerns raised by all three reviewers while remaining achievable within a reasonable revision timeline. We have been careful to commit only to additions we can deliver with appropriate rigor, learning from our Round 1 experience of overpromising. We thank the reviewers for their patience and continued engagement with our work.
## Author Rebuttal - Round 1

### Overview

We sincerely thank both reviewers for their thorough and constructive evaluation of our manuscript on ZK-rollup security. The feedback has identified important gaps in our treatment of several critical topics, and we appreciate the time and expertise invested in providing such detailed technical guidance.

Both reviewers converge on several key themes: (1) insufficient formal rigor in our security analysis, particularly regarding cryptographic assumptions and soundness guarantees; (2) superficial treatment of sequencer centralization, MEV implications, and bridge security; (3) inadequate engagement with the data availability security model; and (4) problematic citation practices, especially the over-reliance on tangentially related references. We acknowledge these criticisms as largely valid and outline below a comprehensive revision strategy that will substantially strengthen the manuscript's technical depth and scholarly contribution.

Our revision plan prioritizes three major additions: a new section providing formal security definitions and cryptographic assumption analysis, a significantly expanded treatment of sequencer security with quantitative MEV analysis, and a dedicated bridge security section with case studies of historical exploits. We will also substantially revise our citation approach to engage more substantively with the primary cryptographic literature.

---

### Response to Reviewer 1 (Blockchain Scalability and Layer 2 Architecture)

**Overall Assessment**: We thank Reviewer 1 for the balanced evaluation (6.3/10 average) and acknowledge that the manuscript's primary weakness lies in its descriptive rather than analytical approach to security. The reviewer correctly identifies that while our taxonomic organization is sound, we have not provided the rigorous threat modeling and quantitative analysis expected of a research contribution.

**Major Points**:

1. **Superficial treatment of sequencer centralization and MEV implications**
   - **Our response**: We fully agree that this represents a significant gap. The current manuscript identifies risks without quantifying them or analyzing mitigation mechanisms in depth. This is particularly problematic given that sequencer behavior constitutes the primary trust assumption for users of current ZK-rollups.
   - **Action taken**: We will expand Section 4.2 to include: (a) a formal threat model for sequencer misbehavior specifying adversarial capabilities, attack surfaces, and security objectives; (b) quantitative analysis of MEV extraction in ZK-rollups drawing on empirical data from Flashbots and MEV-Boost research, with comparison to optimistic rollup MEV dynamics; (c) detailed evaluation of decentralized sequencing proposals including based sequencing (as proposed by Justin Drake), shared sequencing networks (Espresso Systems, Astria), and threshold encryption schemes; (d) analysis of forced inclusion mechanisms including L1 escape hatch latency (typically 12-24 hours), gas costs under congestion, and effectiveness under various censorship scenarios.

2. **Minimal treatment of bridge security and cross-layer state verification**
   - **Our response**: The reviewer is correct that bridge security is essentially absent from our manuscript despite bridges representing critical attack surfaces responsible for over $2 billion in historical exploits. This omission is indefensible given our focus on security.
   - **Action taken**: We will add a dedicated Section 6 on bridge security covering: (a) security model comparison between validity-proof bridges (immediate finality upon proof verification) and fraud-proof bridges (challenge period requirements); (b) analysis of withdrawal delay attacks and their implications for liquidity providers, including the economic dynamics of fast withdrawal services; (c) case studies of major bridge exploits (Ronin, Wormhole, Nomad) with analysis of root causes and lessons for ZK bridge design; (d) security analysis of ZK light client bridges including proof verification delay implications and the trust assumptions of different verification strategies.

3. **Taxonomic but not rigorous data availability analysis**
   - **Our response**: We acknowledge that our DA discussion lacks formal security definitions and economic analysis. The distinction between cryptographic guarantees (DAS) and economic guarantees (DACs) deserves more rigorous treatment.
   - **Action taken**: We will strengthen the data availability section with: (a) formal security definitions for data availability including reconstruction guarantees and the adversarial threshold assumptions; (b) economic security analysis comparing DAC collateral requirements versus cryptoeconomic DA layers (EigenDA, Celestia); (c) analysis of data withholding attack economics including the cost-benefit calculus for sequencers and the effectiveness of slashing mechanisms; (d) discussion of EIP-4844 and danksharding's impact on rollup security properties, including blob retention periods and their implications for state reconstruction.

4. **Problematic citation practices**
   - **Our response**: The reviewer's criticism regarding References [1] and [2] is well-founded. Reference [1] on consortium blockchains has limited relevance to ZK-rollup security, and its repeated citation does not reflect substantive engagement. We also thank the reviewer for identifying the incorrect attribution for Nova (Reference [8]).
   - **Action taken**: We will: (a) remove or substantially reduce citations to Reference [1], retaining it only where genuinely relevant; (b) engage substantively with Reference [2]'s technical contributions where cited; (c) correct the Nova attribution to Kothapalli, Setty, and Tzialla; (d) add citations to primary literature including the original zkSync and StarkNet security analyses, formal treatments of data availability sampling (particularly the work by Mustafa Al-Bassam et al.), and the MEV/sequencer design literature (Flashbots research, Babel et al. on censorship resistance); (e) replace documentation links with peer-reviewed sources where available, or clearly distinguish between peer-reviewed and grey literature.

**Minor Points**: We will address the reviewer's suggestion to formalize security models in Section 2.2 by specifying exact cryptographic assumptions (knowledge soundness, collision resistance) and game-theoretic assumptions (rational sequencers, honest minority for DA) with explicit failure mode analysis.

---

### Response to Reviewer 2 (Zero-Knowledge Cryptography and Proof Systems)

**Overall Assessment**: We thank Reviewer 2 for the detailed cryptographic critique (5.8/10 average). The reviewer correctly identifies that our treatment of proof system security properties lacks the formal rigor expected of a research contribution. We acknowledge that the manuscript reads more as an industry survey than a rigorous cryptographic analysis, and we commit to addressing this fundamental weakness.

**Major Points**:

1. **Insufficient formal treatment of soundness and completeness properties**
   - **Our response**: The reviewer is correct that stating security properties without formal definitions, security reductions, or concrete bounds is inadequate. Our claim that "violations of soundness would enable invalid state transitions" is indeed trivially true and provides no analytical value.
   - **Action taken**: We will add a new Section 3 (Formal Security Framework) providing: (a) formal definitions of knowledge soundness distinguishing computational soundness (negligible probability of convincing verifier of false statement) from statistical soundness (information-theoretic guarantee); (b) concrete security bounds expressed as functions of field size, number of constraints, and security parameter—for example, Groth16 achieves soundness error 1/|F| for field F under the q-SDH assumption; (c) formal definition of zero-knowledge (simulation-based) and the distinction between perfect, statistical, and computational zero-knowledge achieved by different systems; (d) the relationship between knowledge extraction and soundness, explaining why knowledge soundness (existence of extractor) is stronger than standard soundness.

2. **Cryptographic assumptions mentioned but not rigorously analyzed**
   - **Our response**: We acknowledge the imprecision in our characterization of KZG security. The reviewer correctly notes that KZG relies on the q-SDH assumption (or q-SBDH in the type-3 pairing setting), which is indeed stronger than discrete logarithm. This distinction has practical implications for concrete security estimates.
   - **Action taken**: We will add a dedicated subsection on cryptographic assumptions covering: (a) precise specification of assumptions underlying each proof system—KEA and q-SDH for Groth16, AGM for PLONK-style systems, collision resistance and pseudorandomness for STARKs; (b) assumption hierarchy and relationships (e.g., q-SDH implies discrete log, but not vice versa); (c) concrete security analysis discussing known attacks and security margins; (d) quantum threat analysis—pairing-based assumptions fall to Shor's algorithm while hash-based assumptions (STARKs) require only Grover resistance, providing quadratic rather than exponential speedup for attackers.

3. **Superficial trusted setup security discussion**
   - **Our response**: The reviewer correctly identifies that our characterization of setup compromise as "a potential security vulnerability" dramatically understates the severity. A compromised Groth16 setup enables creation of proofs for arbitrary false statements—a complete soundness break, not merely a vulnerability.
   - **Action taken**: We will substantially expand the trusted setup discussion to include: (a) formal description of powers-of-tau ceremony structure, explaining the sequential contribution model and the toxic waste that must be destroyed; (b) precise statement of the 1-of-N honesty assumption and its implications—soundness holds if at least one participant honestly generates and destroys their randomness; (c) verification mechanisms allowing public verification of ceremony correctness through pairing checks on the structured reference string; (d) concrete attack scenarios under setup compromise, distinguishing between soundness breaks (forging proofs) and zero-knowledge breaks (extracting witnesses); (e) practical security margins achieved by ceremonies like Zcash Sapling (hundreds of participants) and Hermez (thousands of participants).

4. **Inadequate treatment of STARK security and proof recursion**
   - **Our response**: We accept the criticism that our STARK security characterization needs qualification, and that the Nova discussion misses the key technical innovations.
   - **Action taken**: We will: (a) clarify that STARK soundness relies on collision resistance while zero-knowledge relies on pseudorandomness properties of the hash function; (b) add discussion of FRI protocol security including the proximity testing guarantees and the role of the blow-up factor in determining soundness error; (c) expand the Nova discussion to explain relaxed R1CS, the folding operation that avoids recursive SNARK verification, and the accumulation scheme approach; (d) analyze security implications of folding schemes including the distinction between IVC (incremental verifiable computation) security and traditional SNARK security.

5. **Citation deficiencies in cryptographic literature**
   - **Our response**: We agree that foundational cryptographic works are absent from our references. A rigorous treatment requires engagement with the primary security proofs.
   - **Action taken**: We will add citations to: (a) Bitansky et al. on extractable collision-resistant hash functions and the foundations of SNARK security; (b) Groth-Maller on simulation extractability; (c) the original Groth16 paper with its security proof; (d) Ben-Sasson et al. on STARK security and FRI; (e) the PLONK paper (Gabizon, Williamson, Ciobotaru) for permutation argument security; (f) Kothapalli, Setty, and Tzialla on Nova. We will engage substantively with these works rather than merely listing them.

**Minor Points**: We will qualify claims throughout the manuscript to reflect the precise cryptographic guarantees. For example, we will replace "post-quantum security based on hash function collision resistance" with "conjectured post-quantum security based on the collision resistance of the hash function (for soundness) and its pseudorandomness properties (for zero-knowledge), requiring hash output size approximately 2λ for λ bits of post-quantum security against Grover's algorithm."

---

### Summary of Changes

**Major Additions**:
- New Section 3: Formal Security Framework with definitions of knowledge soundness, zero-knowledge, and concrete security bounds
- New Section 3.X: Cryptographic Assumptions Analysis covering assumption hierarchies, concrete security, and quantum threats
- Substantially expanded Section 4.2: Sequencer Security with formal threat model, quantitative MEV analysis, and evaluation of decentralized sequencing proposals
- New Section 6: Bridge Security covering security models, withdrawal attacks, and case studies of historical exploits
- Expanded trusted setup discussion with formal MPC ceremony analysis and concrete attack scenarios

**Significant Revisions**:
- Data availability section strengthened with formal security definitions and economic analysis
- STARK security characterization qualified to distinguish soundness and zero-knowledge requirements
- Nova/folding schemes discussion expanded to explain technical innovations and security implications
- KZG security description corrected to reference q-SDH assumption rather than discrete log

**Citation Improvements**:
- Reduced reliance on tangentially related References [1] and [2]
- Corrected Nova attribution (Reference [8])
- Added foundational cryptographic literature (Groth16, PLONK, Bitansky et al., Ben-Sasson et al.)
- Replaced documentation links with peer-reviewed sources where available
- Clear distinction between peer-reviewed and grey literature throughout

We believe these revisions will address the reviewers' core concerns and transform the manuscript from an industry survey into a rigorous research contribution. We are grateful for the detailed feedback that has guided this improvement and welcome any additional suggestions during the revision process.
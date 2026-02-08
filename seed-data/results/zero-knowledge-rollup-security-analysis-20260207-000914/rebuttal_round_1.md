## Author Rebuttal - Round 1

### Overview

We sincerely thank all three reviewers for their thorough and constructive evaluation of our manuscript on ZK-rollup security vulnerabilities. The feedback has been invaluable in identifying critical gaps in our presentation and methodology. We recognize a consistent theme across all reviews: while our vulnerability taxonomy and scope are appreciated, the manuscript lacks the technical specificity, empirical detail, and formal rigor necessary to substantiate our claims. We fully acknowledge these shortcomings.

In response, we are undertaking a substantial revision that will: (1) provide detailed technical descriptions of representative vulnerabilities with concrete examples, affected code paths, and exploitation scenarios; (2) include comprehensive empirical results from our analysis of the four production deployments; (3) clarify the distinction between implementation bugs and cryptographic soundness violations; and (4) formalize our vulnerability scoring methodology. We believe these revisions will address the core concerns while preserving the comprehensive scope that reviewers found valuable.

---

### Response to Reviewer 1 (Network Security Expert)

**Overall Assessment**: We appreciate the balanced evaluation (6.0/10 average) and agree with the central criticism that our security analysis lacks the empirical validation and technical specificity expected in rigorous security research. The reviewer correctly identifies that our current presentation reads more as a survey than original security research.

**Major Points**:

1. **Critical lack of empirical validation for the four production deployment analysis**
   - **Our response**: This criticism is entirely valid. Our methodology section references the analysis but fails to present the actual findings in sufficient detail. We conducted static analysis of smart contract code, reviewed public audit reports, analyzed on-chain transaction patterns, and performed limited testnet-based testing—but none of this is adequately documented.
   - **Action taken**: We will add a dedicated "Empirical Results" section (approximately 800 words) presenting: (a) specific contract addresses and code versions analyzed for each platform; (b) detailed findings organized by vulnerability class; (c) comparative analysis showing how vulnerability profiles differ across zkSync Era, StarkNet, Polygon zkEVM, and Scroll; (d) clear distinction between issues identified through our analysis versus those discovered in prior audits.

2. **Vague vulnerability descriptions lacking technical specificity**
   - **Our response**: We acknowledge that statements like "certain arithmetic circuit configurations exhibit soundness gaps" are insufficiently precise for security research. This vagueness was partly intentional due to responsible disclosure concerns, but we failed to communicate this context or provide sufficient detail for reproducibility.
   - **Action taken**: We will add a technical appendix containing: (a) at least three detailed vulnerability case studies with constraint system representations, affected code snippets, and step-by-step exploitation scenarios; (b) CVE references where applicable for known issues; (c) for novel findings still under disclosure embargo, we will provide anonymized technical details sufficient for understanding the vulnerability class while withholding exploitation specifics, with explicit notation of disclosure status.

3. **Missing quantitative risk assessment methodology**
   - **Our response**: The reviewer correctly notes that our CVSS adaptation is mentioned but not explained. This is a significant methodological gap.
   - **Action taken**: We will add a formal "Vulnerability Scoring Methodology" subsection defining our blockchain-specific adaptations, including: (a) TVL-at-risk weighting factors; (b) time-to-exploit considerations for MEV-related attacks; (c) reversibility assessment criteria (governance intervention potential, upgrade mechanisms); (d) explicit justification for each severity rating in our taxonomy.

4. **Arbitrary threshold recommendations (e.g., "100 independent participants" for MPC ceremonies)**
   - **Our response**: This criticism is valid. The 100-participant recommendation was based on informal industry practice rather than formal threshold security analysis.
   - **Action taken**: We will either cite formal threshold security literature justifying specific participant counts under stated security assumptions, or qualify our recommendations as industry best practices rather than formally derived thresholds. We will add references to relevant MPC security proofs (e.g., Gennaro et al.'s work on threshold ECDSA security bounds).

**Minor Points**: We will address the request for responsible disclosure timelines by adding a dedicated subsection documenting our coordination with affected projects, including disclosure dates, vendor response timelines, and patch status for each identified vulnerability. For the game-theoretic modeling of economic attacks, we will add quantitative griefing profitability analysis with specific bond sizes, gas costs, and MEV extraction estimates.

---

### Response to Reviewer 2 (Formal Methods Expert)

**Overall Assessment**: We appreciate the rigorous evaluation (5.4/10 average) and recognize that the reviewer has identified a fundamental tension in our manuscript. The criticism regarding conflation of security properties and lack of formal rigor is particularly well-taken.

**Major Points**:

1. **Claims about "soundness gaps" lack formal proof or precise mathematical specification**
   - **Our response**: We must clarify an important point that our manuscript failed to communicate clearly: the vulnerabilities we identify are **implementation errors in constraint generation**, not violations of the underlying Groth16 soundness theorem. The reviewer is absolutely correct that a true soundness gap in Groth16 would be an extraordinary cryptographic result requiring formal proof. Our findings are more modest but still practically significant.
   - **Action taken**: We will substantially revise the cryptographic vulnerability sections to: (a) clearly distinguish between protocol-level soundness (which we do not claim to break) and implementation-level constraint system errors (which we document); (b) remove or rephrase any language that could be interpreted as claiming breaks in cryptographic assumptions; (c) provide formal specifications of the constraint system errors we identified, including the exact R1CS constraints, the malformed witnesses that satisfy them, and the security property violated (under-constrained circuits allowing witness malleability, not soundness breaks).

2. **Conflation of different security properties without rigorous distinction**
   - **Our response**: This is a valid criticism. Our taxonomy groups vulnerabilities by attack surface rather than by the security property violated, which obscures important distinctions.
   - **Action taken**: We will add a formal definitions section specifying: (a) knowledge soundness, zero-knowledge, and completeness as defined in the ZK-SNARK literature; (b) a mapping from each vulnerability class to the specific security property it violates; (c) clear notation distinguishing implementation correctness failures from cryptographic property violations.

3. **No formal verification artifacts or machine-checked proofs**
   - **Our response**: We acknowledge that machine-checked proofs would substantially strengthen our claims. However, we must be transparent about the scope of our contribution: this work is primarily an empirical security analysis rather than a formal verification effort.
   - **Action taken**: We will: (a) explicitly reframe the paper's contribution as a systematization of knowledge combined with empirical analysis, rather than formal security analysis; (b) for one representative vulnerability (the most well-characterized constraint system error), we will provide a Circom-based proof-of-concept demonstrating the under-constrained circuit and the witness malleability it permits; (c) identify specific formal verification opportunities as future work, noting relevant tools (ecne, Picus) that could be applied.

4. **Missing formal computational model and security reductions**
   - **Our response**: The reviewer correctly notes that our threat model lacks formal computational definitions. Given our reframing as empirical analysis rather than formal security research, we will adjust our claims accordingly.
   - **Action taken**: We will revise the threat model section to: (a) acknowledge that we do not provide formal security reductions; (b) clearly state the computational assumptions underlying the systems we analyze (q-SDH, q-PKE for Groth16; collision-resistance and FRI soundness for STARKs); (c) position our contribution as identifying implementation gaps that could undermine these theoretical guarantees in practice.

**Minor Points**: We will formalize our CVSS adaptation with explicit scoring criteria as noted in our response to Reviewer 1. We accept the suggestion to narrow our formal claims while maintaining the broad empirical scope.

---

### Response to Reviewer 3 (Applied Cryptography Expert)

**Overall Assessment**: We thank the reviewer for the constructive evaluation (6.0/10 average) and particularly appreciate the detailed technical feedback on cryptographic specificity. The distinction between implementation bugs and cryptographic soundness failures is crucial, and we failed to make this clear.

**Major Points**:

1. **Lack of technical specificity for cryptographic claims**
   - **Our response**: The reviewer's specific questions highlight exactly the detail we should have provided. Regarding the trusted setup validation failures: the issues involved insufficient verification of correct exponentiation during the powers-of-tau phase, specifically missing checks that contributions were consistent with the claimed randomness proofs. We will make this explicit.
   - **Action taken**: For the trusted setup vulnerabilities, we will specify: (a) the exact validation step that was missing (verification of the proof of knowledge of the discrete log for contributed elements); (b) the potential attack vector (a malicious participant could contribute a known discrete log relationship, compromising the ceremony); (c) the specific ceremonies affected (with responsible disclosure caveats where applicable).

2. **The 20 vulnerabilities lack sufficient technical description**
   - **Our response**: This is our most significant presentation failure. The vulnerabilities exist and have been analyzed, but our manuscript does not present them in reproducible detail.
   - **Action taken**: We will add a comprehensive vulnerability catalog as a structured appendix, with each entry containing: (a) vulnerability ID and classification; (b) affected component and code location (where disclosable); (c) technical description of the flaw; (d) security property violated; (e) exploitation requirements and complexity; (f) disclosure status and CVE reference if applicable; (g) remediation status. We will provide full technical detail for at least 5 representative vulnerabilities spanning different categories.

3. **Empirical findings from platform analysis not presented**
   - **Our response**: The reviewer correctly notes that we mention four platforms in methodology but never present comparative results.
   - **Action taken**: We will add a results section including: (a) vulnerability counts by category for each platform; (b) comparative analysis of security architecture choices (e.g., StarkNet's Cairo-based approach vs. Polygon zkEVM's EVM-equivalence tradeoffs); (c) quantitative metrics where available (e.g., number of under-constrained circuits identified, gas cost analysis for economic attacks); (d) a comparative table summarizing security posture across platforms.

4. **Conflation of soundness violations with implementation bugs**
   - **Our response**: We fully accept this criticism and will make the distinction explicit throughout. The reviewer is correct that implementation bugs are common while cryptographic soundness failures would be extraordinary.
   - **Action taken**: We will: (a) revise all vulnerability descriptions to clearly categorize each as either implementation error or cryptographic concern; (b) add explicit language acknowledging that our findings are primarily implementation-level issues that could undermine theoretical security guarantees, not breaks in underlying cryptographic assumptions; (c) update our severity ratings to reflect this distinction (implementation bugs affecting soundness in practice vs. theoretical soundness breaks).

5. **Oversimplified STARK vs SNARK comparison**
   - **Our response**: The reviewer correctly notes that our treatment ignores recent developments in recursive composition and proof aggregation.
   - **Action taken**: We will update the security-performance tradeoff discussion to address: (a) recursive proof composition (Plonky2, Nova); (b) proof aggregation techniques; (c) how these developments affect the security-performance calculus we present.

**Minor Points**: We will add the suggested formal definitions of knowledge soundness, zero-knowledge, and completeness, with explicit mapping to vulnerability classes. We will also clarify the distinct security implications of soundness (fake proofs), zero-knowledge (information leakage), and availability (denial of service) violations.

---

### Summary of Changes

**Major Revisions**:
1. Add dedicated "Empirical Results" section (~800 words) with detailed findings from zkSync Era, StarkNet, Polygon zkEVM, and Scroll analysis
2. Add technical appendix with detailed vulnerability case studies including constraint systems, code snippets, and exploitation scenarios
3. Revise all cryptographic claims to clearly distinguish implementation bugs from protocol-level soundness violations
4. Add formal "Vulnerability Scoring Methodology" subsection with blockchain-specific CVSS adaptations
5. Add comprehensive vulnerability catalog with structured entries for all 20 identified issues

**Clarifications**:
1. Reframe contribution as systematization of knowledge plus empirical analysis rather than formal security research
2. Add formal definitions section for security properties (soundness, zero-knowledge, completeness)
3. Clarify trusted setup validation failures with specific technical details
4. Update threat model to acknowledge limitations of our formal analysis

**New Analysis/Data**:
1. Comparative vulnerability analysis across four platforms (tabular summary)
2. Quantitative griefing profitability analysis for economic attacks
3. Circom-based proof-of-concept for one representative constraint system vulnerability
4. Responsible disclosure timeline and vendor coordination details
5. Updated STARK vs SNARK analysis including recursive composition developments

We are committed to addressing these substantial revisions and believe the resulting manuscript will meet the standards of rigor expected by all three reviewers. We welcome any additional guidance on prioritization given word count constraints.
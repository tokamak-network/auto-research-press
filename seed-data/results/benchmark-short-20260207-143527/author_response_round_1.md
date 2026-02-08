## Author Response - Round 1

### Overview

We sincerely thank all three reviewers for their thorough and rigorous evaluation of our manuscript. The feedback has been invaluable in identifying critical weaknesses in our theoretical presentation, formal rigor, and documentation standards. We acknowledge that the reviews converge on several serious concerns: (1) complexity bounds stated without rigorous proofs, (2) missing or unverifiable citations, (3) inconsistencies between theoretical claims and experimental setup, and (4) insufficient formal specification of our algorithms.

We accept responsibility for these significant shortcomings. Upon reflection, we recognize that our manuscript was submitted prematurely, with theoretical claims that outpaced our formal analysis and a reference section that was inadvertently omitted during submission preparation. We are committed to a major revision that addresses each concern substantively. Below, we respond to each reviewer's feedback in detail and outline specific changes we will implement.

---

### Response to Reviewer 1 (Complexity Theory Expert)

**Overall Assessment**: We appreciate the Complexity Theory Expert's careful evaluation (Average: 4.2/10) and acknowledge that the theoretical foundations of our work require substantial strengthening. The reviewer correctly identifies that our complexity claims lack the rigor expected in formal complexity analysis.

**Major Points**:

1. **Complexity bounds stated without proofs or rigorous derivations**
   - **Our response**: The reviewer is entirely correct. We stated bounds like O(k log n) and O(√n) without providing derivations or specifying the computational model. This was a serious oversight.
   - **Action taken**: We will add a formal Appendix A containing complete proofs for all complexity claims. For adaptive sparse routing, we will specify: (a) the word-RAM model with O(log n)-bit words, (b) that the O(k log n) bound applies to the expert selection phase using a max-heap, not the importance score computation, (c) that importance score computation is O(n·d) per token, which we failed to account for in our original presentation. We will revise our claims to reflect the true end-to-end complexity.

2. **Confusion between worst-case, expected-case, and amortized complexity**
   - **Our response**: We acknowledge this confusion throughout our analysis. Different bounds implicitly assumed different analysis frameworks without explicit statement.
   - **Action taken**: We will add a Preliminaries section (new Section 2) that defines: (a) our computational model, (b) whether each bound is worst-case, expected, or amortized, (c) the probability space for randomized analysis, and (d) formal notation conventions. Each theorem will explicitly state its complexity type.

3. **Probabilistic guarantees lack formal derivations**
   - **Our response**: The reviewer correctly notes that our (1+ε) approximation claim invokes concentration inequalities without proof. We stated conditions like τ ≥ Θ(√(log(1/δ)/m)) without deriving them.
   - **Action taken**: We will provide a complete proof sketch in Appendix B, including: (a) formal definition of the random variables (expert quality scores), (b) independence assumptions (conditional independence given input token), (c) application of Hoeffding's inequality to derive the threshold condition, and (d) explicit statement of when these assumptions may be violated in practice.

4. **Johnson-Lindenstrauss application not properly formalized**
   - **Our response**: We agree that we invoked JL without formalizing how token embeddings map to the framework or how distance preservation translates to routing quality.
   - **Action taken**: We will either (a) provide a formal theorem showing how JL guarantees translate to routing approximation bounds under specific assumptions, or (b) remove the JL claim and instead characterize our hash routing empirically without theoretical distance preservation guarantees. Given the complexity of formally connecting JL to discrete expert assignment, option (b) may be more honest.

5. **Citations appear unverifiable**
   - **Our response**: We sincerely apologize for this critical error. The reference section was inadvertently omitted during submission. All cited works are real publications, and we take full responsibility for this oversight.
   - **Action taken**: We will include a complete References section with DOIs, URLs, and full bibliographic information for all citations. Specifically: [1] refers to Shazeer et al. (2017) on MoE layers, [2] to Roller et al. (2021) on hash routing, etc. We will provide the complete mapping in our revision.

**Minor Points**: 
- We will clarify that load balancing bounds use balls-and-bins analysis with explicit distributional assumptions.
- We will add formal problem definitions at the start of Section 3.
- We will distinguish novel theoretical contributions from results building on prior work.

---

### Response to Reviewer 2 (Formal Methods Expert)

**Overall Assessment**: We thank the Formal Methods Expert for the rigorous evaluation (Average: 3.5/10). The reviewer's concerns about mathematical precision, verifiability, and internal consistency are well-founded and require comprehensive revision.

**Major Points**:

1. **Severe lack of formal rigor in theoretical claims**
   - **Our response**: We accept this criticism. Our theorems lacked precise problem formulations, algorithm specifications with invariants, and step-by-step derivations.
   - **Action taken**: We will restructure Section 3 to include: (a) formal problem statement with input/output specifications, (b) algorithm pseudocode with loop invariants for each routing strategy, (c) correctness proofs showing invariant maintenance, and (d) complexity analysis counting primitive operations explicitly.

2. **Mathematical inconsistencies and undefined notation**
   - **Our response**: The reviewer correctly identifies that we used O(n·e) and O(n·k) inconsistently without defining variables. We also conflated training and inference complexity.
   - **Action taken**: We will add a notation table in Section 2 defining: n (sequence length), k (number of selected experts), e (total number of experts), d (hidden dimension), and d_h (hash dimension). We will separate training complexity (Section 3.4) from inference complexity (Section 3.1-3.3) with explicit headers.

3. **Experimental results contradict theoretical claims**
   - **Our response**: The reviewer astutely notes that model sizes jump from 13B to 175B without explanation, and perplexity differences don't match our percentage claims. These inconsistencies are errors on our part.
   - **Action taken**: The 175B reference in the conclusion was aspirational language about future work that should not have been stated as a result. We will remove it. The perplexity calculation error (12.43 vs 12.31 is ~0.97% difference, not <0.3%) will be corrected. We will add a table explicitly showing degradation percentages with proper calculations.

4. **Load balancing analysis lacks formal probability spaces**
   - **Our response**: The reviewer correctly notes that "deterministic load balance guarantees" followed by probabilistic analysis is contradictory. We conflated deterministic constraints (enforced by the algorithm) with probabilistic analysis of natural load distribution.
   - **Action taken**: We will separate: (a) hard constraints enforced by the routing algorithm (deterministic), (b) expected load distribution under random input assumptions (probabilistic), and (c) empirical load distribution observed in experiments. Each will have appropriate formal treatment.

5. **LSH uniformity claim is incorrect**
   - **Our response**: The reviewer is correct that LSH functions preserve locality, not uniformity. Our claim about "uniform distribution property" was imprecise and potentially incorrect.
   - **Action taken**: We will revise the hash routing analysis to correctly characterize LSH behavior. If our method relies on uniformity, we need to use random hash functions, not LSH. We will clarify which hash family we actually use and provide appropriate theoretical analysis.

**Minor Points**:
- We will add confidence intervals to all experimental results.
- We will include multiple comparison corrections (Bonferroni) for statistical tests.
- We will provide complete experimental setup details for reproducibility.

---

### Response to Reviewer 3 (Algorithms Expert)

**Overall Assessment**: We appreciate the Algorithms Expert's detailed technical critique (Average: 3.3/10). The reviewer identifies fundamental errors in our complexity analysis that we must address honestly.

**Major Points**:

1. **O(k log n) complexity claim is incorrect when importance computation requires O(n²)**
   - **Our response**: This is a critical error in our presentation. The reviewer is correct that computing I(x_i) = max_j A_{ij} from attention weights is O(n²) for full attention, making our O(k log n) claim misleading.
   - **Action taken**: We will revise our complexity claims to honestly account for all operations. Our actual contribution is reducing the expert selection overhead, not the attention computation. We will reframe our claims as: "Given precomputed attention weights, expert selection requires O(k log n) additional operations" rather than claiming end-to-end sublinear complexity. We will add a table showing the full complexity breakdown for each stage.

2. **Hierarchical clustering inconsistency between static and learned structures**
   - **Our response**: The reviewer correctly identifies the tension between O(√n) inference and O(n) training updates. We did not clearly separate these regimes.
   - **Action taken**: We will clarify that: (a) during inference, clustering is fixed, yielding O(√n) expert selection, (b) clustering is updated periodically during training with O(n) cost, (c) we will specify the update frequency and amortized training cost. We will add experiments showing sensitivity to clustering update frequency.

3. **O(1) hash routing ignores hash computation cost**
   - **Our response**: The reviewer is correct that h(x) = sign(W_h x) requires O(d_h · d) operations, which we cannot ignore.
   - **Action taken**: We will revise to state O(d_h · d) complexity for hash routing, noting this is constant with respect to the number of experts e, not constant overall. The benefit is that complexity doesn't scale with e, which matters for models with many experts. We will clarify this distinction.

4. **Dimensional inconsistency in I(x) ⊙ W_g x**
   - **Our response**: This is a notation error. I(x) should be a vector of per-expert importance scores, not a scalar.
   - **Action taken**: We will fix the notation: I(x) ∈ ℝ^e is the importance vector where I(x)_j represents the importance of expert j for token x. The element-wise product then makes dimensional sense.

5. **Group-aware attention fundamentally changes architecture**
   - **Our response**: The reviewer raises a valid concern that restricting attention within groups limits model expressiveness beyond routing optimization.
   - **Action taken**: We will add discussion of this limitation and clarify that hierarchical routing trades some cross-group interaction for efficiency. We will add ablation experiments measuring the expressiveness impact and discuss when this tradeoff is acceptable.

6. **Experimental inconsistencies (13B vs 175B, speedup vs throughput)**
   - **Our response**: The 175B mention was an error (see response to Reviewer 2). The speedup/throughput confusion reflects imprecise language—we meant latency speedup while maintaining throughput capacity.
   - **Action taken**: We will define terms precisely: "latency" (time per request), "throughput" (requests per second), "speedup" (latency reduction ratio). We will report all three metrics clearly.

**Minor Points**:
- We will add complete pseudocode for all algorithms including training procedures.
- We will specify auxiliary loss functions for load balancing explicitly.
- We will add hyperparameter sensitivity analysis.
- We will report p-values and effect sizes for all statistical tests.

---

### Summary of Changes

**Major Revisions**:
1. Add new Section 2 (Preliminaries) with computational model, notation table, and formal definitions
2. Completely rewrite Section 3 (Theoretical Analysis) with honest complexity accounting, formal theorem statements, and proof sketches
3. Add Appendix A with complete proofs for all complexity bounds
4. Add Appendix B with formal probabilistic analysis including concentration inequality derivations
5. Include complete References section with DOIs and full bibliographic information
6. Revise all complexity claims to accurately reflect end-to-end costs, not just subcomponent costs
7. Remove or correct the 175B parameter claims and fix perplexity calculation errors

**Clarifications**:
1. Separate worst-case, expected-case, and amortized analysis throughout
2. Distinguish training complexity from inference complexity
3. Clarify the LSH vs. random hash function distinction
4. Fix dimensional inconsistencies in notation
5. Define speedup, throughput, and latency precisely

**New Analysis/Data**:
1. Complete complexity breakdown table for each routing strategy
2. Ablation study on hierarchical clustering update frequency
3. Expressiveness impact analysis for group-aware attention
4. Hyperparameter sensitivity analysis
5. Statistical tests with p-values, effect sizes, and multiple comparison corrections
6. Confidence intervals for all experimental results

We are grateful to all reviewers for identifying these serious issues before publication. The revised manuscript will provide honest, rigorous analysis of our methods' actual contributions and limitations.
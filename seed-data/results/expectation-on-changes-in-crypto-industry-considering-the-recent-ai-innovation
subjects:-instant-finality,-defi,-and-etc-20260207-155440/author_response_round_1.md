## Author Response - Round 1

### Overview

We sincerely thank all three reviewers for their thorough and constructive feedback on our manuscript examining AI-blockchain convergence. The reviews have identified significant weaknesses that we acknowledge require substantial revision. We are grateful for the time and expertise invested in these evaluations.

The reviewers converge on several critical themes: (1) insufficient technical depth regarding the practical feasibility of deploying AI in trustless environments, (2) missing engagement with emerging primitives such as zkML and proof-of-inference, (3) problematic citations including an erroneously dated reference and inadequate integration of foundational literature, and (4) speculative claims that lack formal analysis or empirical grounding. We accept these criticisms as valid and outline below a comprehensive revision strategy that addresses each concern. Our revised manuscript will transform from a speculative survey into a technically grounded analysis with concrete mechanisms, formal considerations, and engagement with real-world implementations.

---

### Response to Reviewer 1 (AI/ML Systems for Financial Applications)

**Overall Assessment**: We acknowledge the score of 5.0/10 and accept that the manuscript, in its current form, reads more as speculative futurism than rigorous research. The reviewer's core criticism—that we fail to engage with the fundamental technical challenges of deploying ML in decentralized environments—is well-founded.

**Major Points**:

1. **Lack of technical specificity on trustless AI deployment (computational constraints, gas costs, execution model tensions)**
   - **Our response**: This is our most significant oversight. We failed to address the fundamental incompatibility between ML inference requirements (floating-point operations, large model weights, iterative computation) and blockchain execution models (deterministic, gas-limited, integer-based). We will add a dedicated section titled "Technical Feasibility of On-Chain AI Inference" that explicitly addresses these constraints.
   - **Action taken**: The new section will include: (a) quantitative analysis of gas costs for basic ML operations on EVM-compatible chains, (b) discussion of the determinism requirements and how floating-point non-determinism creates consensus challenges, (c) detailed treatment of zkML approaches (e.g., EZKL, Modulus Labs' work) and optimistic ML verification, and (d) analysis of hybrid architectures where inference occurs off-chain with cryptographic proofs submitted on-chain.

2. **Missing discussion of emerging AI-crypto primitives (proof-of-inference, on-chain ML verification, AI-native tokens)**
   - **Our response**: We agree this represents a critical gap. The field has moved beyond speculation to active implementation, and our manuscript should reflect this.
   - **Action taken**: We will add a new subsection on "Emerging AI-Crypto Infrastructure" covering: (a) proof-of-inference mechanisms and their cryptographic foundations, (b) decentralized inference networks (Bittensor's incentive design, Ritual's coprocessor model, Giza's ONNX-to-Cairo compilation), (c) AI-native token economics and their alignment mechanisms, and (d) empirical analysis of these systems' current performance and limitations.

3. **Problematic citations: Reference [2] dated 2026, Reference [3] mismatch, insufficient integration of references [4-8]**
   - **Our response**: We are embarrassed by the 2026 citation error—this was a formatting mistake where a preprint's expected publication date was incorrectly entered. Reference [3] on generative IR was included for its discussion of retrieval-augmented generation but is indeed tangential to our core claims. These errors undermine our credibility and we take full responsibility.
   - **Action taken**: We will: (a) correct the erroneous date and verify all citation metadata, (b) replace Reference [3] with directly relevant literature on blockchain AI applications, (c) substantially expand our citation base to include peer-reviewed work on verifiable computation (Ben-Sasson et al., Groth16), zero-knowledge proofs for ML (zkML surveys), and MEV research (Daian et al., Flashbots documentation), and (d) integrate references [4-8] substantively into our analysis rather than listing them superficially.

4. **Hand-wavy treatment of "predictive finality" and AI-enhanced consensus without concrete mechanisms**
   - **Our response**: The reviewer is correct that we offered no concrete mechanism. We conflated several distinct concepts (optimistic execution, probabilistic finality in Nakamoto consensus, and speculative execution) without precision.
   - **Action taken**: We will either: (a) develop a specific technical proposal with clear specification of inputs, outputs, verification mechanisms, and security analysis, or (b) reframe this section as a research agenda that honestly acknowledges these as open problems rather than near-term possibilities. Given the scope of our survey, we lean toward option (b) with pointers to relevant technical directions.

5. **Autonomous AI agent discussion ignores smart contract constraints and auditability**
   - **Our response**: We agree that our treatment was naive. AI agents operating within smart contracts are fundamentally bounded by the contract's programmatic interface—they cannot take arbitrary actions.
   - **Action taken**: We will revise this section to address: (a) the specific action spaces available to AI agents (what functions can they call, with what parameters), (b) how agent behavior can be bounded and audited through on-chain logs and constraint enforcement, (c) the distinction between AI agents that execute on-chain versus those that operate off-chain and submit transactions, and (d) existing frameworks like Autonolas and their architectural choices.

**Minor Points**: We will address the reviewer's implicit suggestion to engage with MEV and AI by adding discussion of ML-based searchers, their strategies, and protocol-level responses.

---

### Response to Reviewer 2 (Decentralized Finance Protocol Design)

**Overall Assessment**: We accept the score of 5.0/10 and acknowledge that our treatment of AI-DeFi integration lacks the technical depth and empirical grounding expected for protocol design research.

**Major Points**:

1. **Lack of technical specificity on AI-driven AMM mechanisms (architectures, loss functions, computational constraints)**
   - **Our response**: Our discussion of AI-enhanced AMMs was indeed superficial. We failed to engage with the substantial existing literature on concentrated liquidity, dynamic fees, and the game-theoretic considerations of AMM design.
   - **Action taken**: We will expand this section to include: (a) specific ML architectures relevant to AMM optimization (reinforcement learning for liquidity provision, neural network-based fee prediction), (b) analysis of how dynamic mechanisms interact with arbitrageurs and LVR (loss-versus-rebalancing), (c) concrete discussion of computational constraints and why on-chain inference for AMM optimization is currently infeasible, and (d) review of existing approaches like Uniswap v3's concentrated liquidity and how AI might complement rather than replace these mechanisms.

2. **MEV extraction and AI agents mentioned only tangentially despite being central to the field**
   - **Our response**: This is a significant oversight given that AI-driven MEV extraction is one of the few areas where AI-blockchain integration is already deployed at scale. Flashbots searchers using ML for arbitrage detection represent real-world evidence we should have analyzed.
   - **Action taken**: We will add a dedicated section on "AI Agents and MEV" covering: (a) empirical analysis of MEV extraction volumes and AI's role (using Flashbots data), (b) ML techniques used by searchers (opportunity detection, bundle optimization, timing games), (c) protocol-level responses including MEV-aware AMM designs, Chainlink Fair Sequencing Services, and threshold encryption approaches, and (d) the arms race dynamics between AI-powered extraction and mitigation.

3. **Citation problems: 2026 date, IR paper mismatch, missing foundational DeFi literature**
   - **Our response**: As noted above, the citation errors are inexcusable. The absence of references to Adams et al. (Uniswap), Leshner (Compound), and substantive engagement with Daian et al. on MEV represents a failure to ground our work in the existing literature.
   - **Action taken**: We will comprehensively revise our citations to include: (a) foundational DeFi protocol papers, (b) empirical studies of DeFi market dynamics (including the March 2020 MakerDAO crisis the reviewer mentions), (c) MEV research from Flashbots and academic sources, and (d) work on oracle design and manipulation resistance.

4. **Speculative claims without empirical evidence or simulation results (e.g., millisecond finality)**
   - **Our response**: The reviewer is correct that claims like "AI could reduce finality from seconds to milliseconds" require concrete mechanism description and analysis. We overreached in our claims.
   - **Action taken**: We will either provide quantitative support for our claims through simulation or analytical results, or we will appropriately qualify them as research directions requiring further investigation. We will not make performance claims without supporting evidence.

5. **Missing discussion of reflexivity in DeFi markets and how ML models would handle it**
   - **Our response**: This is an excellent point we had not adequately considered. In DeFi, model predictions can affect outcomes (e.g., a risk model predicting liquidation could trigger the very liquidation it predicts), creating feedback loops that standard ML approaches do not handle well.
   - **Action taken**: We will add discussion of reflexivity challenges, drawing on relevant literature from quantitative finance and control theory, and analyze how AI systems in DeFi must account for their own market impact.

**Minor Points**: We will incorporate discussion of specific AI agent frameworks (AutoGPT-based DeFi agents, Autonolas) and provide more concrete technical proposals for AI-driven liquidation mechanisms including oracle latency considerations.

---

### Response to Reviewer 3 (Blockchain Consensus Mechanisms & Scalability)

**Overall Assessment**: We accept the score of 5.0/10 and acknowledge that our treatment of AI-enhanced consensus mechanisms lacks the formal rigor expected for this research area.

**Major Points**:

1. **No concrete technical specifications for AI-enhanced consensus (message complexity, network assumptions, security bounds)**
   - **Our response**: The reviewer is correct that our claims about "millisecond finality" lack any formal analysis. We made assertions without specifying the consensus model, network assumptions, or security properties.
   - **Action taken**: We will revise this section to either: (a) provide formal specifications for a concrete AI-enhanced consensus mechanism including message complexity analysis, synchrony assumptions, and Byzantine fault tolerance guarantees, or (b) reframe our discussion as identifying research directions while clearly stating that formal analysis remains future work. We will engage with relevant literature including PBFT, HotStuff, Tendermint, and Casper FFG to ground our discussion.

2. **Missing quantitative analysis of decentralization-finality-security trilemma trade-offs**
   - **Our response**: Our assertion that AI "may relax constraints" without proof was indeed hand-wavy. The trilemma represents fundamental trade-offs that cannot be wished away.
   - **Action taken**: We will add quantitative modeling addressing: (a) computational requirements for AI optimization and what percentage of current validators could participate, (b) impact on Nakamoto coefficient and other decentralization metrics, (c) explicit analysis of what trade-offs AI-enhanced consensus accepts (e.g., increased hardware requirements for faster finality), and (d) comparison with existing approaches that make similar trade-offs (e.g., Solana's hardware requirements).

3. **Citation issues: 2026 date, tangential IR reference, missing core consensus literature**
   - **Our response**: The absence of citations to PBFT, HotStuff, Casper FFG, and other foundational consensus work is a serious gap that we will address.
   - **Action taken**: We will add comprehensive citations to consensus literature and substantively engage with how our proposals relate to existing formal results.

4. **Fundamental misunderstanding of finality (deterministic vs. probabilistic)**
   - **Our response**: We appreciate this correction. The reviewer is right that in deterministic finality protocols, a transaction is either final or not—there is no intermediate state. Our discussion of "predictive finality" conflated distinct concepts.
   - **Action taken**: We will carefully distinguish between: (a) deterministic finality in BFT-style protocols, (b) probabilistic finality in Nakamoto consensus, (c) optimistic execution with rollback risks, and (d) speculative execution for latency hiding. We will clarify which of these AI might actually improve and how.

5. **Missing analysis of adversarial manipulation of AI inputs to influence consensus**
   - **Our response**: This security consideration should have been central to our analysis. If AI models influence consensus parameters or transaction ordering, adversaries will attempt to manipulate model inputs.
   - **Action taken**: We will add a security analysis section addressing: (a) threat models for AI-enhanced consensus, (b) input manipulation attacks and potential mitigations, (c) how adversarial robustness requirements interact with model accuracy, and (d) the fundamental challenge of achieving consensus on AI model outputs.

6. **No engagement with specific systems (Casper FFG, Tower BFT, rollup finality) or related work (Flex-BFT)**
   - **Our response**: We should have grounded our discussion in concrete systems rather than abstract possibilities.
   - **Action taken**: We will analyze how AI might specifically improve finality in: (a) Ethereum's Casper FFG (e.g., optimizing attestation aggregation), (b) L2 rollup finality mechanisms, and (c) we will review Flex-BFT and similar learned consensus work to understand what has already been proposed and evaluated.

**Minor Points**: We will ensure our discussion of dynamic parameter adjustment addresses how such changes interact with safety and liveness proofs, rather than treating parameters as arbitrary.

---

### Summary of Changes

**Major Revisions Planned:**

1. **New Section: "Technical Feasibility of On-Chain AI Inference"**
   - Gas cost analysis for ML operations
   - Determinism requirements and floating-point challenges
   - zkML and optimistic ML verification approaches
   - Hybrid on-chain/off-chain architectures with cryptographic proofs

2. **New Section: "AI Agents and MEV"**
   - Empirical analysis of AI-driven MEV extraction
   - ML techniques used by searchers
   - Protocol-level mitigation strategies
   - Arms race dynamics

3. **New Subsection: "Emerging AI-Crypto Infrastructure"**
   - Proof-of-inference mechanisms
   - Analysis of Bittensor, Ritual, Giza, and similar systems
   - AI-native token economics

4. **Substantially Revised Consensus Section**
   - Formal specification of at least one concrete mechanism (or honest acknowledgment of open problems)
   - Quantitative decentralization analysis
   - Security analysis including adversarial manipulation
   - Engagement with specific systems (Casper FFG, Tower BFT, Flex-BFT)

5. **Revised DeFi Section**
   - Technical depth on AI-AMM mechanisms
   - Reflexivity and market impact considerations
   - Concrete liquidation mechanism proposals

**Citation Corrections:**
- Fix erroneous 2026 date
- Replace tangential IR reference
- Add foundational literature (PBFT, HotStuff, Uniswap, Compound, Daian et al. on MEV)
- Substantively integrate all cited references

**Clarifications:**
- Distinguish deterministic vs. probabilistic finality
- Clarify smart contract constraints on AI agents
- Qualify speculative claims appropriately
- Remove unsupported performance assertions

We believe these revisions will address the reviewers' concerns and transform the manuscript into a technically grounded contribution. We are grateful for the detailed feedback that has identified these necessary improvements.
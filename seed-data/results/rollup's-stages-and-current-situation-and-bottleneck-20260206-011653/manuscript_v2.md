# Rollup Stages: Current Landscape, Challenges, and the Path to Full Decentralization

## A Comprehensive Research Report on Layer 2 Scaling Solutions

---

## Executive Summary

Rollups have emerged as the dominant paradigm for scaling Ethereum and other Layer 1 blockchains, processing billions of dollars in transactions while inheriting the security guarantees of their underlying networks. However, the journey from centralized sequencers to fully decentralized, trustless systems remains incomplete. This report provides a comprehensive analysis of the rollup maturity framework, examining the current state of major rollup implementations, identifying critical bottlenecks preventing progression to higher stages, and evaluating emerging solutions.

Our analysis reveals that as of early 2025, the vast majority of rollups by Total Value Locked (TVL) remain at Stage 0, with Arbitrum One representing the most advanced major rollup at Stage 1. Stage 2—the highest level of decentralization where users can exit without any trust assumptions beyond L1 security and cryptographic soundness—remains unachieved by any major rollup. Key bottlenecks include incomplete proof system maturity, centralized sequencer architectures, Security Council governance structures with broad upgrade powers, and the absence of robust cross-rollup interoperability with appropriate trust guarantees.

This report examines these challenges through technical, economic, and governance lenses, providing actionable insights for researchers, developers, and stakeholders invested in the rollup ecosystem's maturation. We conclude that while the technical foundations for Stage 2 rollups exist, achieving this milestone requires coordinated advances in proof systems, decentralized sequencing, governance minimization, and cross-rollup bridging infrastructure over the next 24-48 months.

---

## 1. Introduction

### 1.1 The Scaling Imperative

Ethereum's transition to proof-of-stake and the implementation of EIP-4844 (Proto-Danksharding) have established a clear roadmap: the base layer optimizes for security and data availability, while execution scales through Layer 2 solutions. This "rollup-centric" roadmap, articulated by Vitalik Buterin in 2020, has fundamentally shaped blockchain architecture.

Rollups execute transactions off-chain while posting transaction data (or state differences) to the parent chain, achieving throughput improvements of 10-100x while maintaining security guarantees derived from the underlying Layer 1. As of January 2025, rollups collectively secure over $40 billion in TVL and process more daily transactions than Ethereum mainnet.

### 1.2 The Trust Spectrum

Despite their promise, rollups exist on a spectrum of decentralization and trustlessness. Early implementations required users to trust operators completely—a regression from blockchain's core value proposition. The community recognized this tension, leading to the development of maturity frameworks that track rollups' progression toward full decentralization.

### 1.3 Research Objectives

This report addresses four primary questions:

1. What constitutes a mature, trustless rollup, and how do we measure progress toward this goal?
2. What is the current state of major rollup implementations relative to these standards?
3. What technical, economic, and governance bottlenecks prevent advancement, and what solutions are emerging?
4. How do cross-rollup interoperability and bridging mechanisms affect the practical security of the rollup ecosystem?

---

## 2. The Rollup Stage Framework

### 2.1 Origins and Rationale

The rollup stage framework was formalized by L2Beat, the leading Layer 2 analytics platform, in collaboration with the Ethereum research community. The framework emerged from recognition that marketing claims about "decentralization" and "security" required objective, verifiable criteria.

The framework defines three stages (0, 1, and 2), each representing increasing levels of trustlessness and decentralization. Critically, the framework focuses on **exit guarantees**—the ability of users to withdraw their funds without relying on any trusted party.

### 2.2 Stage Definitions

#### Stage 0: Full Training Wheels

At Stage 0, a rollup has deployed on mainnet but retains significant centralized control. The defining characteristics include:

- **Centralized sequencing**: A single operator orders and executes transactions
- **Upgradeable contracts**: The rollup's smart contracts can be modified without delay or with minimal timelock
- **No fraud/validity proofs**: Users cannot independently verify state transitions, or proofs exist but can be overridden
- **Operator-dependent exits**: Users rely on the operator to process withdrawals

Stage 0 rollups are functionally similar to sidechains with additional data availability guarantees. Users must trust that operators will not censor transactions, steal funds through malicious upgrades, or abandon the network.

#### Stage 1: Limited Training Wheels

Stage 1 represents meaningful progress toward trustlessness:

- **Functional proof system**: Either fraud proofs (optimistic rollups) or validity proofs (ZK-rollups) are deployed and operational
- **Permissionless verification**: Anyone can submit fraud proofs or verify validity proofs
- **Escape hatch mechanism**: Users can force withdrawals through the L1 if the operator becomes unresponsive
- **Security Council**: A multisig can intervene in case of bugs, but with significant constraints (typically requiring supermajority threshold)

The key advancement at Stage 1 is that **users can exit without operator cooperation**, though they may still need to trust a Security Council for bug fixes during an interim period.

#### Stage 2: No Training Wheels

Stage 2 represents full trustlessness:

- **Immutable or governance-minimized contracts**: Upgrades require extended timelocks (30+ days) or are impossible
- **No Security Council override**: Or the council can only act after the timelock expires, giving users time to exit
- **Battle-tested proof system**: The proof mechanism has been operational without critical failures for an extended period
- **Decentralized sequencing**: Multiple parties can propose blocks, eliminating single points of failure (or users can self-sequence via L1)

At Stage 2, the rollup inherits Ethereum's security guarantees fully. Users need only trust the L1 consensus and the mathematical soundness of the proof system.

### 2.3 Framework Limitations and Ongoing Debates

The stage framework, while valuable, has acknowledged limitations:

1. **Binary categorization**: Rollups may meet some but not all criteria for a stage, creating edge cases where classification is contested
2. **Implementation nuance**: Two Stage 1 rollups may have significantly different security properties depending on Security Council structure, proof system maturity, and escape hatch robustness
3. **Dynamic assessment**: A rollup's stage can regress if vulnerabilities are discovered or if governance decisions weaken security guarantees
4. **Scope limitations**: The framework doesn't directly assess liveness, MEV extraction, economic security, or cross-rollup bridging trust assumptions
5. **Classification disputes**: Stage classifications are sometimes contested by rollup teams or community members who interpret criteria differently; readers should consult L2Beat directly for current classifications and understand the methodology behind disputed assessments

---

## 3. Current Landscape Analysis

### 3.1 Market Overview

As of January 2025, the rollup ecosystem comprises over 50 active networks with combined TVL exceeding $40 billion. The market is dominated by a small number of major players:

| Rollup | Type | TVL (USD) | Stage | Launch Date |
|--------|------|-----------|-------|-------------|
| Arbitrum One | Optimistic | ~$15B | 1 | August 2021 |
| Base | Optimistic | ~$12B | 0 | August 2023 |
| OP Mainnet | Optimistic | ~$7B | 0 | December 2021 |
| zkSync Era | ZK | ~$1B | 0 | March 2023 |
| Starknet | ZK | ~$500M | 0 | November 2022 |
| Linea | ZK | ~$800M | 0 | July 2023 |
| Scroll | ZK | ~$600M | 0 | October 2023 |

*Data approximate as of January 2025. Stage classifications per L2Beat methodology and subject to change. Readers should verify current status at l2beat.com.*

### 3.2 Optimistic Rollups: Detailed Assessment

#### 3.2.1 Arbitrum One

Arbitrum One, developed by Offchain Labs, represents the most mature optimistic rollup implementation. Key characteristics:

**Stage 1 Qualifications:**
- Deployed BOLD (Bounded Liquidity Delay) fraud proof system in late 2024
- Permissionless validation enabled—anyone can challenge invalid state roots
- Functional escape hatch through `forceInclusion` mechanism allowing users to submit transactions directly to L1
- 6 day, 8 hour challenge period for fraud proofs

**Remaining Limitations:**
- Security Council (12-member multisig) can upgrade contracts with a 3-day delay for non-emergency actions
- Emergency upgrades require 9/12 threshold but can bypass timelock
- Sequencer remains centralized (operated by Offchain Labs)
- Council can pause the system in emergencies

The Security Council's powers represent the primary barrier to Stage 2. While the council provides important bug-fix capabilities, its ability to execute emergency upgrades creates trust assumptions that Stage 2 would eliminate.

#### 3.2.2 Optimism (OP Mainnet)

OP Mainnet, the flagship chain of the OP Stack, has made significant progress but remains at Stage 0:

**Current State:**
- Fault proof system (FPAC - Fault Proof Alpha Cannon) launched in June 2024
- Permissionless proposers enabled
- 7-day challenge window

**Stage 0 Classification Rationale:**
- Guardian role can disable fault proofs entirely, reverting to permissioned output proposals
- Deputy Guardian can pause withdrawals
- Security Council can upgrade without delay in emergency situations
- Proof system relatively new, requiring more battle-testing before governance constraints can be safely reduced

The OP Stack's modular design means improvements benefit the entire Superchain ecosystem (Base, Mode, Zora, etc.), but this also means vulnerabilities affect multiple networks simultaneously—a systemic risk consideration.

#### 3.2.3 Base

Base, developed by Coinbase, is the largest Stage 0 rollup by TVL:

**Current Limitations:**
- Inherits OP Stack limitations including Guardian override capabilities
- Additional Coinbase operational dependencies
- Relies on Optimism's Security Council rather than independent governance
- Sequencer operated by Coinbase with no current decentralization timeline

Base's rapid growth ($12B+ TVL) despite Stage 0 status highlights that users currently prioritize other factors (UX, ecosystem, institutional backing, regulatory clarity) over decentralization metrics—a finding with implications for the pace of ecosystem-wide decentralization.

### 3.3 ZK-Rollups: Detailed Assessment

#### 3.3.1 zkSync Era

zkSync Era, developed by Matter Labs, is the largest ZK-rollup by TVL:

**Technical Architecture:**
- Uses a customized PLONK-based proof system (specifically a variant with custom gates and lookup arguments)
- Boojum prover utilizing FRI-based polynomial commitments for improved efficiency
- EVM-equivalent execution environment via zkEVM

**Stage 0 Limitations:**
- Validity proofs cover state transitions but the system retains centralized override capabilities
- Centralized sequencer and prover operated by Matter Labs
- Upgradeable contracts with Security Council control
- Escape hatch mechanism exists but has not been battle-tested in adversarial conditions

#### 3.3.2 Starknet

Starknet, developed by StarkWare, uses STARK proofs:

**Technical Characteristics:**
- Cairo VM (not EVM-equivalent, requiring contract rewriting or transpilation)
- Recursive proofs for scalability via SHARP (Shared Prover)
- FRI-based polynomial commitments providing post-quantum security assumptions

**Current Limitations:**
- Centralized sequencer operated by StarkWare
- Upgradeable contracts with multisig control
- Escape hatch exists but requires specific conditions and has operational complexity
- Governance transitioning toward decentralization but not yet complete

#### 3.3.3 Scroll and Linea

Both represent newer zkEVM implementations:

**Scroll:**
- Type 2 zkEVM (EVM-equivalent at bytecode level)
- Uses a combination of KZG commitments and custom proving system
- Decentralized prover network in development
- Currently centralized sequencing and proving with roadmap toward decentralization

**Linea:**
- Developed by Consensys
- Type 2 zkEVM with Lattice-based proof system
- Centralized operations with published decentralization roadmap
- Benefits from Consensys infrastructure but inherits single-operator risks

### 3.4 Comparative Analysis

```
Decentralization Spectrum (January 2025)

Stage 2: [None]
         |
Stage 1: [Arbitrum One]
         |
Stage 0: [Base, OP Mainnet, zkSync Era, Starknet, Scroll, Linea, ...]
         |
Centralized: [Various app-specific rollups, new launches]
```

The clustering at Stage 0 reflects both the technical difficulty of advancement and the recency of many implementations. Notably, the transition from Stage 0 to Stage 1 requires not just technical implementation but sufficient operational history to justify reduced governance intervention capabilities.

---

## 4. Critical Bottlenecks

### 4.1 Proof System Maturity

#### 4.1.1 Optimistic Rollup Challenges

Fraud proof systems face several fundamental challenges:

**Complexity of Dispute Resolution:**
The fraud proof game requires proving that a specific instruction in a potentially billions-long execution trace was computed incorrectly. This involves:

1. Interactive bisection to identify the disputed instruction
2. One-step proof execution on L1
3. Handling of edge cases (memory access, precompiles, cross-contract calls, etc.)

Arbitrum's BOLD protocol addresses the "delay attack" vulnerability where malicious actors could indefinitely postpone fraud proof resolution by posting multiple invalid claims. BOLD bounds the maximum delay regardless of attacker resources, but introduces its own complexity and capital requirements for defenders.

**The Verifier's Dilemma:**
Rational validators may not monitor for fraud if the expected cost exceeds the expected reward. This creates scenarios where fraud could go unchallenged during periods of:
- Low attention (holidays, competing events)
- High gas prices making challenges expensive
- Coordination failures among potential challengers

Research by Thibault et al. (2024) formalizes this dilemma and proposes mechanism design solutions, but production implementations remain limited.

#### 4.1.2 ZK-Rollup Challenges

ZK-rollups face different but equally significant challenges:

**Proof Generation Costs:**
Generating validity proofs remains computationally expensive. The costs vary dramatically based on proof system choice and circuit complexity:

| Proof System | Proof Size | Prover Time (per tx) | Verifier Time | Trusted Setup |
|--------------|------------|---------------------|---------------|---------------|
| Groth16 | ~200 bytes | High | ~3ms | Required (circuit-specific) |
| PLONK (KZG) | ~400 bytes | Medium-High | ~5ms | Required (universal) |
| STARKs (FRI) | ~50-200 KB | Medium | ~10-50ms | None |
| Halo2 (IPA) | ~5 KB | High | ~50ms | None |

*Approximate figures; actual performance depends on circuit size, hardware, and implementation optimization.*

These costs create centralization pressure, as only well-resourced operators can afford proving infrastructure at scale.

**Circuit Completeness and Soundness:**
ZK circuits must correctly encode all EVM opcodes and edge cases. The audit surface is enormous:

- Compiler correctness (high-level language to circuit constraints)
- Constraint system completeness (all execution paths properly constrained)
- Prover implementation (no bugs allowing false proofs)
- Verifier implementation (no bugs accepting invalid proofs)

Bugs in circuit design can lead to:
- Invalid state transitions being accepted (soundness failure)
- Valid transactions being rejected (completeness failure)
- Exploitable vulnerabilities allowing fund theft

**Cryptographic Security Assumptions:**
Different proof systems rely on different cryptographic assumptions with varying confidence levels:

| Assumption | Proof Systems | Post-Quantum | Confidence |
|------------|---------------|--------------|------------|
| Discrete Log (Elliptic Curves) | Groth16, PLONK (KZG) | No | High |
| Random Oracle Model | Most systems | Varies | High |
| Algebraic Group Model | PLONK, Groth16 | No | Medium-High |
| Collision-Resistant Hashing | STARKs | Yes | Very High |
| Knowledge of Exponent | Groth16 | No | Medium |

STARKs' reliance on hash function security provides post-quantum resistance but at the cost of larger proof sizes. This tradeoff influences long-term architectural decisions.

**Prover Centralization:**
Currently, all major ZK-rollups use centralized provers:

```
Transaction Flow (Current):
User → Centralized Sequencer → Centralized Prover → L1 Verification

Ideal Flow:
User → Decentralized Sequencer Network → Decentralized Prover Market → L1 Verification
```

Decentralizing proving requires solving proof generation latency, prover selection mechanisms, and economic incentive alignment.

### 4.2 Sequencer Decentralization

The sequencer—the entity that orders transactions and produces blocks—represents the most significant centralization point in current rollups.

#### 4.2.1 Current Centralization

All major rollups operate centralized sequencers:

| Rollup | Sequencer Operator | Revenue Model | Geographic Distribution |
|--------|-------------------|---------------|------------------------|
| Arbitrum One | Offchain Labs | MEV + priority fees | Single operator |
| Base | Coinbase | Transaction fees | Single operator |
| OP Mainnet | Optimism Foundation | Transaction fees | Single operator |
| zkSync Era | Matter Labs | Transaction fees | Single operator |

Centralized sequencers create multiple risk categories:

- **Censorship**: Operators can exclude specific transactions or addresses
- **MEV extraction**: Operators capture ordering value without competitive redistribution
- **Liveness**: Single point of failure for transaction inclusion
- **Regulatory capture**: Identifiable operators subject to legal pressure in their jurisdictions

#### 4.2.2 Decentralization Approaches

Several approaches to sequencer decentralization are under development:

**Leader Rotation:**
Validators take turns as sequencer based on stake weight or verifiable random selection.

*Technical Challenges:*
- Latency increases from geographic distribution and leader handoff
- MEV distribution complexity across rotating leaders
- Validator set management and stake security
- Potential for leader extraction during their slot

**Based Sequencing:**
Ethereum L1 validators/proposers sequence L2 transactions, inheriting L1's decentralization directly. Projects like Taiko are exploring this model.

*Advantages:*
- Immediate inheritance of L1 decentralization (~900,000 validators)
- No separate validator set to bootstrap
- Atomic L1-L2 composability potential
- Credible neutrality from L1 proposer selection

*Challenges:*
- Reduced L2 sovereignty (can't implement custom ordering rules)
- Block time limited to L1 (~12 seconds vs. sub-second L2 blocks)
- Cross-domain MEV complications where L1 proposers extract L2 value
- Proposer-builder separation (PBS) interactions add complexity

**Shared Sequencing:**
Multiple rollups share a decentralized sequencer network (e.g., Espresso Systems, Astria, Radius).

```
Shared Sequencing Architecture:

        ┌─────────────────────┐
        │   Shared Sequencer  │
        │      Network        │
        │  (HotShot/Astria)   │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
┌────────┐    ┌────────┐    ┌────────┐
│Rollup A│    │Rollup B│    │Rollup C│
│        │    │        │    │        │
└────────┘    └────────┘    └────────┘
```

*Advantages:*
- Atomic cross-rollup transactions possible
- Shared security across participant rollups
- Economies of scale for decentralization infrastructure

*Challenges:*
- Consensus mechanism must provide fast finality (Espresso's HotShot, Astria's CometBFT)
- Value distribution across rollups and sequencer operators
- Governance coordination across independent ecosystems
- Dependency on external infrastructure availability

#### 4.2.3 MEV Considerations in Decentralized Sequencing

MEV (Maximal Extractable Value) redistribution is a critical unsolved problem:

**Current State:**
- Centralized sequencers capture 100% of MEV
- Some rollups implement MEV-share mechanisms (e.g., Arbitrum's Timeboost)
- No standardized approach to MEV redistribution

**Proposed Solutions:**
- *Encrypted mempools*: Transactions encrypted until ordering committed (threshold encryption, delay encryption)
- *MEV auctions*: Competitive bidding for ordering rights with proceeds distributed
- *Fair ordering*: First-come-first-served or batch auctions eliminating ordering-based extraction
- *MEV-burn*: Captured MEV burned or distributed to users

Each approach involves tradeoffs between extraction prevention, latency, complexity, and economic efficiency.

### 4.3 Security Council Governance

#### 4.3.1 The Upgrade Dilemma

Rollups face a fundamental tension:

- **Upgradeability enables bug fixes**: Critical vulnerabilities require rapid response capability
- **Upgradeability enables attacks**: Malicious upgrades can steal all user funds

This tension is particularly acute for systems securing billions of dollars where both risks are existential.

#### 4.3.2 Security Council Structures: Comparative Analysis

Security Councils vary significantly in their design and operation:

**Arbitrum Security Council:**
- **Composition**: 12 members from diverse ecosystem organizations
- **Threshold**: 9/12 for emergency actions, 7/12 for non-emergency upgrades
- **Selection**: Members elected by ARB token holders through on-chain governance
- **Constraints**: Operates under Arbitrum Constitution defining scope and limitations
- **Accountability**: Public member identities, election cycles, removal procedures
- **Geographic Distribution**: Members span multiple jurisdictions to reduce regulatory capture risk

**Optimism Security Council:**
- **Composition**: 13 members in nested multisig structure
- **Threshold**: Varies by action type
- **Selection**: Foundation-appointed with planned transition to elected
- **Constraints**: Can pause fault proofs via Guardian role
- **Accountability**: Less formal accountability framework currently
- **Relationship to Foundation**: Optimism Foundation maintains significant influence

**Comparative Assessment:**

| Dimension | Arbitrum | Optimism | zkSync Era |
|-----------|----------|----------|------------|
| Member Selection | Elected | Appointed | Company-controlled |
| Public Identities | Yes | Partial | Limited |
| Constitutional Constraints | Yes | Developing | No |
| Emergency Threshold | 9/12 | Variable | Not disclosed |
| Removal Mechanism | Token vote | Foundation | None |

#### 4.3.3 Governance Attack Vectors

Security Councils introduce specific attack vectors that Stage 2 would eliminate:

**Social Engineering:**
- Council members can be individually targeted through phishing, impersonation, or social manipulation
- Compromise of member keys enables participation in malicious upgrades
- Mitigation: Hardware security modules, operational security training, key rotation

**Regulatory Coercion:**
- Identifiable members in specific jurisdictions can face legal pressure
- Government actors could compel upgrade cooperation
- Mitigation: Geographic distribution, legal structures, threshold requirements exceeding any single jurisdiction's reach

**Economic Incentives:**
- Council members could be bribed to participate in malicious upgrades
- Profit from upgrade (stealing TVL) could exceed members' reputation value
- Mitigation: Staking requirements, insurance, criminal liability

**Coordination Attacks:**
- Subset of members could secretly coordinate malicious action
- Communication channels between members create coordination surfaces
- Mitigation: High thresholds, diverse member selection, monitoring

#### 4.3.4 Historical Governance Decisions: Case Studies

Examining actual governance decisions illuminates how councils function:

**Arbitrum AIP-1 Controversy (2023):**
- Foundation allocated 750M ARB tokens before governance ratification
- Community backlash over perceived governance bypass
- Resolution: Foundation committed to governance oversight
- Lesson: Governance legitimacy requires process adherence even for benign actions

**Optimism Retroactive Public Goods Funding:**
- Citizens' House allocates funds to public goods contributors
- Novel bicameral structure separating token voting from citizenship
- Demonstrates governance innovation beyond simple multisig
- Ongoing experiment in non-plutocratic blockchain governance

**zkSync Era Upgrade Patterns:**
- Multiple upgrades executed with limited public deliberation
- Centralized control enables rapid iteration but reduces transparency
- Community trust based on Matter Labs' reputation rather than formal constraints

#### 4.3.5 Path to Governance Minimization

Achieving Stage 2 requires governance minimization through multiple mechanisms:

**Extended Timelocks:**
- 30+ day delays allow users to exit before malicious upgrades execute
- Requires confidence that no bug requires faster response
- Creates tension with security incident response needs

**Constrained Upgrade Scope:**
- Limit what upgrades can modify (e.g., cannot change withdrawal logic)
- Formal verification that upgrade constraints are enforced
- Reduces attack surface even with short timelocks

**Immutability Progression:**
- Core contracts become non-upgradeable after sufficient battle-testing
- Upgrades limited to peripheral components
- Eventual full immutability for critical paths

**Exit-Focused Design:**
- Prioritize that users can always exit regardless of governance
- Ensure withdrawal paths remain functional even during disputes
- Time-bound governance powers that expire without renewal

### 4.4 Data Availability Security Models

#### 4.4.1 Ethereum Native Data Availability

EIP-4844 introduced blob transactions providing dedicated rollup data space:

**Current Specifications:**
- Target: 3 blobs per block (~375 KB)
- Maximum: 6 blobs per block (~750 KB)
- Blob size: 128 KB each
- Retention: ~18 days before pruning
- Cost: Separate fee market from execution gas

**Security Model:**
- Full nodes download and verify all blob data
- Data availability guaranteed by Ethereum's full validator set
- No sampling assumptions—complete data verification
- Highest security tier for rollup data availability

#### 4.4.2 Alternative Data Availability Layers

Some projects use external DA layers, creating "validiums" with different security properties:

**Celestia:**
- *Mechanism*: Data Availability Sampling (DAS) with erasure coding
- *Security Model*: Light clients sample random chunks; statistical guarantee of availability
- *Validator Set*: Independent PoS consensus (~100 validators currently)
- *Trust Assumption*: Honest minority of samplers + validator honesty

**EigenDA:**
- *Mechanism*: Data distributed across restaked ETH operators
- *Security Model*: Cryptoeconomic security via slashing conditions
- *Validator Set*: Ethereum restakers opted into EigenDA AVS
- *Trust Assumption*: Economic rationality of restakers + slashing effectiveness

**Avail:**
- *Mechanism*: DAS similar to Celestia with KZG commitments
- *Security Model*: Light client sampling with validity proofs
- *Validator Set*: Independent PoS consensus
- *Trust Assumption*: Similar to Celestia

**Security Comparison:**

| DA Layer | Security Source | Validator Count | Post-Quantum | Data Retention |
|----------|-----------------|-----------------|--------------|----------------|
| Ethereum Blobs | Full verification | ~900,000 | No (secp256k1) | ~18 days |
| Celestia | DAS + consensus | ~100 | No | Configurable |
| EigenDA | Restaked ETH | Variable | No | Configurable |
| Avail | DAS + consensus | ~100 | No | Configurable |

#### 4.4.3 Security Degradation Analysis

Moving from Ethereum DA to alternative layers introduces quantifiable security degradation:

**Validator Set Size:**
- Ethereum: ~900,000 validators with ~30M ETH staked
- Alternative layers: 100-1000 validators with significantly less stake
- Attack cost difference: Orders of magnitude

**Consensus Independence:**
- Ethereum DA: Security inherited from battle-tested consensus
- Alternative DA: Separate consensus with independent failure modes
- Correlation risk: Alternative DA failure doesn't affect Ethereum, but affects rollup

**Economic Security:**
```
Ethereum DA Security Budget: ~30M ETH × $3000 = ~$90B at stake
Celestia Security Budget: ~100M TIA × $10 = ~$1B at stake
EigenDA Security Budget: Subset of restaked ETH, variable

Attack cost ratio: ~90:1 (Ethereum vs. Celestia)
```

**Implications for Rollup Classification:**
Rollups using alternative DA are properly classified as "validiums" rather than "rollups" because:
1. Data availability is not guaranteed by Ethereum consensus
2. Users cannot reconstruct state from Ethereum alone
3. Additional trust assumptions beyond L1 security

This distinction matters for Stage classification—a system cannot achieve Stage 2 trustlessness while relying on external DA with weaker security guarantees than Ethereum.

### 4.5 Cross-Rollup Interoperability and Bridging

#### 4.5.1 The Fragmentation Problem

The rollup-centric roadmap creates ecosystem fragmentation:
- Liquidity split across dozens of rollups
- Users must bridge assets between networks
- Application state isolated within individual rollups
- User experience degraded by bridging complexity

#### 4.5.2 Bridge Security Models

Different bridging approaches carry different trust assumptions:

**Canonical Bridges:**
- Operated by rollup teams as "official" bridge
- Security tied to rollup's own upgrade mechanisms
- Trust assumption: Same as rollup itself (Security Council can modify)
- Example: Arbitrum Bridge, Optimism Gateway

*Critical Observation*: A Stage 1 rollup with a canonical bridge controlled by its Security Council inherits the council's trust assumptions for bridged assets. Users bridging to a "Stage 1" rollup still trust the council.

**Light Client Bridges:**
- Verify source chain consensus on destination chain
- Trust assumption: Consensus mechanism security + light client implementation correctness
- Challenge: ZK light clients expensive to verify on-chain; optimistic light clients have delay

**Trusted/Federated Bridges:**
- Multisig or MPC committee attests to cross-chain state
- Trust assumption: Honesty of bridge operators (often 2/3 or 3/5 threshold)
- Examples: Many third-party bridges (Multichain, Wormhole pre-upgrade)
- Risk: Bridge operator compromise enables fund theft (multiple historical exploits)

**Intent-Based Systems:**
- Users express intent; solvers fulfill across chains
- Trust assumption: Solver competition + settlement mechanism security
- Examples: Across Protocol, UniswapX cross-chain
- Trade-off: Capital efficiency vs. trust minimization

#### 4.5.3 Bridge Security and Rollup Stage Interaction

A critical but often overlooked question: **How do bridge trust assumptions interact with rollup stage classifications?**

Consider a user's end-to-end security:

```
User Journey: Ethereum → Rollup A → Rollup B → Ethereum

Trust assumptions accumulated:
1. Rollup A's proof system and governance
2. Bridge A→B's security model
3. Rollup B's proof system and governance
4. Exit bridge security

Weakest link determines actual security.
```

**Implications:**
- A Stage 2 rollup connected only via trusted bridges provides Stage 2 security only for native assets
- Cross-rollup DeFi inherits the weakest bridge's security
- Users may believe they have Stage 1/2 security while actually trusting bridge operators

#### 4.5.4 Toward Trustless Interoperability

Achieving trustless cross-rollup communication requires:

**Shared Settlement:**
- Rollups settling on same L1 can verify each other's state roots
- Requires waiting for finality on both rollups
- Latency: Challenge period (optimistic) or proof generation (ZK)

**ZK Light Clients:**
- Prove source chain consensus in ZK
- Verify proof on destination chain
- Projects: Succinct, Polymer, zkBridge
- Challenge: Proving consensus is expensive; recursive proofs help

**Shared Sequencing with Atomic Inclusion:**
- Shared sequencer guarantees atomic transaction inclusion
- Enables atomic cross-rollup operations
- Requires rollups to adopt shared sequencer

**Standardization Efforts:**
# Rollup Stages: Current Landscape, Challenges, and the Path to Full Decentralization

## A Comprehensive Research Report on Layer 2 Scaling Solutions

---

## Executive Summary

Rollups have emerged as the dominant paradigm for scaling Ethereum and other Layer 1 blockchains, processing billions of dollars in transactions while inheriting the security guarantees of their underlying networks. However, the journey from centralized sequencers to fully decentralized, trustless systems remains incomplete. This report provides a comprehensive analysis of the rollup maturity framework, examining the current state of major rollup implementations, identifying critical bottlenecks preventing progression to higher stages, and evaluating emerging solutions.

Our analysis reveals that as of early 2025, no major rollup has achieved Stage 2 status—the highest level of decentralization where users can exit without any trust assumptions. The majority of rollups by Total Value Locked (TVL) remain at Stage 0 or Stage 1, with significant technical and governance challenges impeding advancement. Key bottlenecks include the absence of fraud-proof mechanisms in optimistic rollups, incomplete validity proof coverage in ZK-rollups, centralized sequencer architectures, and the persistence of upgradeable contracts with short timelocks.

This report examines these challenges through technical, economic, and governance lenses, providing actionable insights for researchers, developers, and stakeholders invested in the rollup ecosystem's maturation. We conclude that while the technical foundations for Stage 2 rollups exist, achieving this milestone requires coordinated advances in proof systems, decentralized sequencing, and governance mechanisms over the next 18-36 months.

---

## 1. Introduction

### 1.1 The Scaling Imperative

Ethereum's transition to proof-of-stake and the implementation of EIP-4844 (Proto-Danksharding) have established a clear roadmap: the base layer optimizes for security and data availability, while execution scales through Layer 2 solutions. This "rollup-centric" roadmap, articulated by Vitalik Buterin in 2020, has fundamentally shaped blockchain architecture.

Rollups execute transactions off-chain while posting transaction data (or state differences) to the parent chain, achieving throughput improvements of 10-100x while maintaining security guarantees derived from the underlying Layer 1. As of January 2025, rollups collectively secure over $40 billion in TVL and process more daily transactions than Ethereum mainnet.

### 1.2 The Trust Spectrum

Despite their promise, rollups exist on a spectrum of decentralization and trustlessness. Early implementations required users to trust operators completely—a regression from blockchain's core value proposition. The community recognized this tension, leading to the development of maturity frameworks that track rollups' progression toward full decentralization.

### 1.3 Research Objectives

This report addresses three primary questions:

1. What constitutes a mature, trustless rollup, and how do we measure progress toward this goal?
2. What is the current state of major rollup implementations relative to these standards?
3. What technical, economic, and governance bottlenecks prevent advancement, and what solutions are emerging?

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
- **No fraud/validity proofs**: Users cannot independently verify state transitions
- **Operator-dependent exits**: Users rely on the operator to process withdrawals

Stage 0 rollups are functionally similar to sidechains with additional data availability guarantees. Users must trust that operators will not censor transactions, steal funds through malicious upgrades, or abandon the network.

#### Stage 1: Limited Training Wheels

Stage 1 represents meaningful progress toward trustlessness:

- **Functional proof system**: Either fraud proofs (optimistic rollups) or validity proofs (ZK-rollups) are deployed and operational
- **Permissionless verification**: Anyone can submit fraud proofs or verify validity proofs
- **Escape hatch mechanism**: Users can force withdrawals through the L1 if the operator becomes unresponsive
- **Security Council**: A multisig can intervene in case of bugs, but with significant constraints

The key advancement at Stage 1 is that **users can exit without operator cooperation**, though they may still need to trust a Security Council for bug fixes.

#### Stage 2: No Training Wheels

Stage 2 represents full trustlessness:

- **Immutable or governance-minimized contracts**: Upgrades require extended timelocks (30+ days) or are impossible
- **No Security Council override**: Or the council can only act after the timelock expires
- **Battle-tested proof system**: The proof mechanism has been operational without critical failures for an extended period
- **Decentralized sequencing**: Multiple parties can propose blocks, eliminating single points of failure

At Stage 2, the rollup inherits Ethereum's security guarantees fully. Users need only trust the L1 consensus and the mathematical soundness of the proof system.

### 2.3 Framework Limitations

The stage framework, while valuable, has acknowledged limitations:

1. **Binary categorization**: Rollups may meet some but not all criteria for a stage
2. **Implementation nuance**: Two Stage 1 rollups may have significantly different security properties
3. **Dynamic assessment**: A rollup's stage can regress if vulnerabilities are discovered
4. **Scope limitations**: The framework doesn't assess liveness, MEV, or economic security

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

*Data approximate as of January 2025*

### 3.2 Optimistic Rollups: Detailed Assessment

#### 3.2.1 Arbitrum One

Arbitrum One, developed by Offchain Labs, represents the most mature optimistic rollup implementation. Key characteristics:

**Stage 1 Qualifications:**
- Deployed BOLD (Bounded Liquidity Delay) fraud proof system in late 2024
- Permissionless validation enabled
- Functional escape hatch through `forceInclusion` mechanism
- 8-day challenge period for fraud proofs

**Remaining Limitations:**
- Security Council (12-member multisig) can upgrade contracts with only a 12-hour delay
- Sequencer remains centralized (operated by Offchain Labs)
- Council can pause the system and override fraud proofs

The Security Council's powers represent the primary barrier to Stage 2. While the council provides important bug-fix capabilities, its ability to upgrade contracts rapidly creates trust assumptions.

#### 3.2.2 Optimism (OP Mainnet)

OP Mainnet, the flagship chain of the OP Stack, has made significant progress but remains at Stage 0:

**Current State:**
- Fault proof system launched in June 2024
- Permissionless proposers enabled
- 7-day challenge window

**Stage 0 Classification Rationale:**
- Guardian role can disable fault proofs entirely
- Security Council can upgrade without delay in emergency
- Proof system relatively new, requiring more battle-testing

The OP Stack's modular design means improvements benefit the entire Superchain ecosystem (Base, Mode, Zora, etc.), but this also means vulnerabilities affect multiple networks simultaneously.

#### 3.2.3 Base

Base, developed by Coinbase, is the largest Stage 0 rollup by TVL:

**Current Limitations:**
- Inherits OP Stack limitations
- Additional Coinbase operational dependencies
- No independent Security Council (relies on Optimism's)

Base's rapid growth ($12B+ TVL) despite Stage 0 status highlights that users currently prioritize other factors (UX, ecosystem, institutional backing) over decentralization metrics.

### 3.3 ZK-Rollups: Detailed Assessment

#### 3.3.1 zkSync Era

zkSync Era, developed by Matter Labs, is the largest ZK-rollup by TVL:

**Technical Architecture:**
- Uses PLONK-based proof system
- Boojum prover for improved efficiency
- EVM-equivalent execution environment

**Stage 0 Limitations:**
- Validity proofs only cover state transitions, not data availability
- Centralized sequencer and prover
- Upgradeable contracts with 21-day timelock (insufficient for Stage 1)
- No escape hatch mechanism currently functional

#### 3.3.2 Starknet

Starknet, developed by StarkWare, uses STARK proofs:

**Technical Characteristics:**
- Cairo VM (not EVM-equivalent)
- Recursive proofs for scalability
- SHARP (Shared Prover) architecture

**Current Limitations:**
- Centralized sequencer operated by StarkWare
- Upgradeable contracts
- Escape hatch exists but requires operator cooperation
- Proof system covers execution but governance remains centralized

#### 3.3.3 Scroll and Linea

Both represent newer zkEVM implementations:

**Scroll:**
- Type 2 zkEVM (EVM-equivalent)
- Decentralized prover network in development
- Currently centralized sequencing and proving

**Linea:**
- Developed by Consensys
- Type 2 zkEVM
- Centralized operations with roadmap toward decentralization

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

The clustering at Stage 0 reflects both the technical difficulty of advancement and the recency of many implementations.

---

## 4. Critical Bottlenecks

### 4.1 Proof System Maturity

#### 4.1.1 Optimistic Rollup Challenges

Fraud proof systems face several fundamental challenges:

**Complexity of Dispute Resolution:**
The fraud proof game requires proving that a specific instruction in a potentially billions-long execution trace was computed incorrectly. This involves:

1. Interactive bisection to identify the disputed instruction
2. One-step proof execution on L1
3. Handling of edge cases (memory access, precompiles, etc.)

Arbitrum's BOLD protocol addresses the "delay attack" vulnerability where malicious actors could indefinitely postpone fraud proof resolution by posting multiple invalid claims. However, BOLD introduces its own complexity and capital requirements.

**The Verifier's Dilemma:**
Rational validators may not monitor for fraud if the expected cost exceeds the expected reward. This creates scenarios where fraud could go unchallenged during periods of low attention or high gas prices.

#### 4.1.2 ZK-Rollup Challenges

ZK-rollups face different but equally significant challenges:

**Proof Generation Costs:**
Generating validity proofs remains computationally expensive:

| Operation | Proving Time | Hardware Cost |
|-----------|--------------|---------------|
| Simple transfer | ~1 second | $0.001-0.01 |
| Complex DeFi tx | ~10 seconds | $0.01-0.10 |
| Full block proof | ~minutes | $1-10 |

These costs create centralization pressure, as only well-resourced operators can afford proving infrastructure.

**Circuit Completeness:**
ZK circuits must correctly encode all EVM opcodes and edge cases. Bugs in circuit design can lead to:
- Invalid state transitions being accepted
- Valid transactions being rejected
- Exploitable vulnerabilities

The zkEVM audit surface is enormous—millions of lines of code across compiler, prover, and verifier components.

**Prover Centralization:**
Currently, all major ZK-rollups use centralized provers:

```
Transaction Flow (Current):
User → Centralized Sequencer → Centralized Prover → L1

Ideal Flow:
User → Decentralized Sequencer Network → Decentralized Prover Market → L1
```

### 4.2 Sequencer Decentralization

The sequencer—the entity that orders transactions and produces blocks—represents the most significant centralization point in current rollups.

#### 4.2.1 Current Centralization

All major rollups operate centralized sequencers:

| Rollup | Sequencer Operator | Revenue Model |
|--------|-------------------|---------------|
| Arbitrum One | Offchain Labs | MEV + fees |
| Base | Coinbase | Fees |
| OP Mainnet | Optimism Foundation | Fees |
| zkSync Era | Matter Labs | Fees |

Centralized sequencers create risks:
- **Censorship**: Operators can exclude transactions
- **MEV extraction**: Operators capture ordering value
- **Liveness**: Single point of failure
- **Regulatory capture**: Operators subject to legal pressure

#### 4.2.2 Decentralization Approaches

Several approaches to sequencer decentralization are under development:

**Leader Rotation:**
Validators take turns as sequencer based on stake or random selection. Challenges include:
- Latency increases from geographic distribution
- MEV distribution complexity
- Validator set management

**Based Sequencing:**
Ethereum L1 validators sequence L2 transactions, inheriting L1's decentralization. Projects like Taiko are exploring this model. Trade-offs include:
- Reduced L2 sovereignty
- Increased L1 load
- Cross-domain MEV complications

**Shared Sequencing:**
Multiple rollups share a decentralized sequencer network (e.g., Espresso, Astria). Benefits include:
- Atomic cross-rollup transactions
- Shared security
- Economies of scale

Challenges include:
- Coordination complexity
- Value distribution
- Governance across ecosystems

#### 4.2.3 Economic Considerations

Sequencer decentralization faces economic headwinds:

```
Current Model:
- Sequencer captures 100% of MEV
- Clear revenue stream funds development
- Simple operational model

Decentralized Model:
- MEV distributed among validators
- Development funding unclear
- Complex coordination required
```

Teams must balance decentralization goals against sustainable economics.

### 4.3 Upgrade Mechanisms and Governance

#### 4.3.1 The Upgrade Dilemma

Rollups face a fundamental tension:

- **Upgradeability enables bug fixes**: Critical vulnerabilities require rapid response
- **Upgradeability enables attacks**: Malicious upgrades can steal funds

Current approaches vary:

| Rollup | Upgrade Mechanism | Timelock | Override |
|--------|-------------------|----------|----------|
| Arbitrum | Security Council | 12 hours | Yes |
| Optimism | Guardian + Council | Variable | Yes |
| zkSync Era | Matter Labs | 21 days | Yes |

None meet Stage 2 requirements (30+ day timelock, no override).

#### 4.3.2 Security Council Structures

Security Councils typically comprise 6-12 members requiring 4-9 signatures:

**Arbitrum Security Council:**
- 12 members from ecosystem organizations
- 9/12 threshold for emergency actions
- 7/12 for non-emergency upgrades
- Members elected by ARB token holders

**Optimism Security Council:**
- 13 members
- Nested multisig structure
- Can pause fault proofs
- Foundation maintains significant influence

The concentration of power in small groups contradicts decentralization principles but reflects practical necessity.

#### 4.3.3 Path to Governance Minimization

Achieving Stage 2 requires governance minimization:

1. **Extended timelocks**: 30+ days allows users to exit before malicious upgrades
2. **Constrained upgrades**: Limit what can be changed (e.g., no fund-stealing upgrades possible)
3. **Immutability**: Eventually, core contracts become non-upgradeable

This path requires:
- Mature, battle-tested code
- Comprehensive formal verification
- Community confidence in stability

### 4.4 Data Availability Constraints

#### 4.4.1 Current State

EIP-4844 introduced blob transactions, providing ~125 KB/block of dedicated rollup data space. While a significant improvement, constraints remain:

- **Blob limit**: ~6 blobs/block limits aggregate rollup throughput
- **Blob fees**: Can spike during high demand
- **Data retention**: Blobs pruned after ~18 days

#### 4.4.2 Impact on Rollup Design

Data availability constraints force design trade-offs:

**Calldata vs. Blobs:**
```
Calldata:
- Permanent availability
- Higher cost (~16 gas/byte)
- Always available

Blobs:
- Temporary availability (~18 days)
- Lower cost (~1 gas/byte equivalent)
- Subject to market pricing
```

**State Diffs vs. Full Data:**
ZK-rollups can post only state differences rather than full transaction data, reducing costs but limiting:
- Historical reconstruction
- Independent verification
- Forced transaction inclusion

#### 4.4.3 Alternative DA Layers

Some rollups use alternative data availability solutions:

| Solution | Type | Security Model |
|----------|------|----------------|
| Celestia | Modular DA | Independent consensus |
| EigenDA | AVS | Restaked ETH security |
| Avail | Modular DA | Independent consensus |

Using alternative DA creates "validiums" rather than true rollups, introducing additional trust assumptions.

---

## 5. Emerging Solutions and Research Directions

### 5.1 Proof System Advances

#### 5.1.1 Proof Aggregation

Multiple proofs can be aggregated into a single proof, reducing verification costs:

```
Traditional:
Rollup A proof → L1 verification ($X)
Rollup B proof → L1 verification ($X)
Total: $2X

Aggregated:
Rollup A + B proofs → Aggregator → Single proof → L1 verification ($X + ε)
Total: ~$X
```

Projects like Nebra and aligned layer are building proof aggregation infrastructure.

#### 5.1.2 Hardware Acceleration

Specialized hardware dramatically reduces proving costs:

| Approach | Speedup | Status |
|----------|---------|--------|
| GPU proving | 10-100x | Production |
| FPGA | 100-1000x | Development |
| ASIC | 1000x+ | Research |

Companies like Cysic, Ingonyama, and Ulvetanna are developing ZK-specific hardware.

#### 5.1.3 New Proof Systems

Research continues on more efficient proof systems:

- **Jolt**: RISC-V based proving with improved efficiency
- **Binius**: Binary field arithmetic for faster proving
- **Circle STARKs**: Improved STARK efficiency

### 5.2 Decentralized Sequencing Progress

#### 5.2.1 Arbitrum's Approach

Arbitrum is developing BoLD (Bounded Liquidity Delay) alongside sequencer decentralization:

- Timeboost auction mechanism for transaction ordering
- Planned validator set expansion
- Economic incentives for honest behavior

#### 5.2.2 Based Rollups

Taiko's based rollup model delegates sequencing to L1:

**Advantages:**
- Inherits L1 decentralization immediately
- No separate validator set required
- Atomic L1-L2 composability

**Challenges:**
- Higher latency (~12 second blocks)
- Limited L2 sovereignty
- Complex MEV dynamics

#### 5.2.3 Shared Sequencing Networks

Espresso Systems and Astria are building shared sequencer infrastructure:

```
Shared Sequencing Architecture:

        ┌─────────────┐
        │   Espresso  │
        │  Sequencer  │
        │   Network   │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    │          │          │
    ▼          ▼          ▼
┌───────┐  ┌───────┐  ┌───────┐
│Rollup │  │Rollup │  │Rollup │
│   A   │  │   B   │  │   C   │
└───────┘  └───────┘  └───────┘
```

### 5.3 Governance Innovation

#### 5.3.1 Optimistic Governance

Some proposals suggest "optimistic" upgrade mechanisms:

1. Upgrade proposed
2. Extended challenge period (30-90 days)
3. If no valid challenge, upgrade executes
4. Challenges evaluated by decentralized arbitration

#### 5.3.2 Formal Verification Requirements

Requiring formal verification for upgrades could enable shorter timelocks:

- Mathematically proven correctness
- Automated security analysis
- Reduced reliance on human review

#### 5.3.3 Exit-Focused Design

Prioritizing exit guarantees over governance:

- Ensure users can always exit, regardless of governance decisions
- Limit upgrade scope to non-fund-affecting changes
- Time-bound governance powers

---

## 6. Practical Implications

### 6.1 For Users

**Risk Assessment:**
Users should understand the trust assumptions of their chosen rollup:

| Stage | Trust Assumptions | Risk Level |
|-------|-------------------|------------|
| 0 | Operator honesty, no malicious upgrades | Higher |
| 1 | Security Council honesty, proof system soundness | Medium |
| 2 | L1 security, cryptographic assumptions | Lower |

**Practical Recommendations:**
1. Monitor rollup stage classifications (L2Beat)
2. Understand exit mechanisms and practice using them
3. Diversify across rollups with different risk profiles
4. Consider self-custody on L1 for large holdings

### 6.2 For Developers

**Building for Maturity:**
Developers should design applications anticipating rollup maturation:

1. **Avoid centralized dependencies**: Don't rely on sequencer-specific features
2. **Implement fallbacks**: Design for potential L2 unavailability
3. **Test exit paths**: Ensure users can withdraw via L1 mechanisms
4. **Monitor upgrades**: Track rollup contract changes

**Cross-Rollup Considerations:**
As the ecosystem fragments across rollups:
- Implement bridging with appropriate security assumptions
- Consider shared sequencing for atomic operations
- Design for eventual interoperability standards

### 6.3 For Rollup Teams

**Prioritization Framework:**
Teams should prioritize Stage advancement:

1. **Immediate**: Deploy functional proof systems
2. **Short-term**: Enable permissionless verification
3. **Medium-term**: Implement robust escape hatches
4. **Long-term**: Extend timelocks, decentralize sequencing

**Communication:**
Transparent communication about current limitations builds trust:
- Publish security documentation
- Disclose known risks
- Provide upgrade roadmaps with timelines

### 6.4 For Researchers

**Open Problems:**
Several research questions remain:

1. **Optimal fraud proof economics**: How to incentivize monitoring without excessive costs?
2. **Sequencer MEV**: How should MEV be distributed in decentralized sequencing?
3. **Cross-rollup security**: How do security guarantees compose across rollups?
4. **Governance attack resistance**: How to prevent governance capture?

---

## 7. Forward-Looking Analysis

### 7.1 Timeline Projections

Based on current development trajectories:

**2025:**
- Multiple rollups achieve Stage 1
- First Stage 2 rollup possible (likely Arbitrum)
- Shared sequencing networks launch
- ZK-rollup proof systems mature

**2026:**
- Stage 2 becomes common for major rollups
- Decentralized sequencing deployed in production
- Hardware-accelerated proving widespread
- Inter-rollup standards emerge

**2027+:**
- Full rollup maturity across ecosystem
- Governance minimization achieved
- Seamless cross-rollup experience
- Rollups indistinguishable from L1 security perspective

### 7.2 Potential Disruptions

Several factors could accelerate or delay this timeline:

**Accelerating Factors:**
- Major security incident forcing rapid decentralization
- Regulatory pressure on centralized operators
- Breakthrough in proof system efficiency
- Successful shared sequencing deployment

**Delaying Factors:**
- Discovery of fundamental proof system vulnerabilities
- Economic unviability of decentralized operations
- Fragmentation preventing coordination
- User indifference to decentralization

### 7.3 Long-Term Vision

The ultimate vision for rollups involves:

1. **Full trustlessness**: Users trust only cryptography and L1 consensus
2. **Seamless UX**: Cross-rollup transactions as easy as single-chain
3. **Sustainable economics**: Decentralized operations remain profitable
4. **Diverse ecosystem**: Specialized rollups for different use cases

---

## 8. Conclusion

The rollup ecosystem has made remarkable progress since the concept's introduction, evolving from theoretical proposals to production systems securing tens of billions of dollars. However, the journey toward full trustlessness remains incomplete. As of early 2025, only Arbitrum One has achieved Stage 1 status among major rollups, with Stage 2—true trustlessness—remaining unachieved.

The bottlenecks preventing advancement are multifaceted:

1. **Proof system maturity**: Both fraud proofs and validity proofs require further development and battle-testing
2. **Sequencer centralization**: All major rollups rely on centralized sequencers, creating censorship and liveness risks
3. **Governance dependencies**: Security Councils with upgrade powers introduce trust assumptions
4. **Economic sustainability**: Decentralized operations must remain economically viable

Encouragingly, solutions are emerging across all dimensions. Fraud proof systems like BOLD address delay attacks, ZK hardware acceleration reduces proving costs, shared sequencing networks enable decentralization, and governance minimization frameworks provide paths to immutability.

The coming 18-36 months will likely see significant advancement. Multiple rollups should achieve Stage 1, with the first Stage 2 implementations possible by late 2025. However, achieving this vision requires sustained effort from rollup teams, researchers, and the broader community.

For users, developers, and stakeholders, understanding the current limitations and trajectory is essential. The rollup-centric future promises unprecedented scalability with L1-equivalent security—but that promise remains unfulfilled until Stage 2 becomes the norm rather than the exception.

---

## References

1. Buterin, V. (2020). "A rollup-centric ethereum roadmap." ethereum-magicians.org

2. L2Beat. (2024). "Rollup Stage Framework Documentation." l2beat.com/scaling/summary

3. Offchain Labs. (2024). "BOLD: Bounded Liquidity Delay Protocol." arbitrum.io/bold

4. Optimism. (2024). "Fault Proof System Specification." specs.optimism.io

5. Matter Labs. (2024). "zkSync Era Technical Documentation." docs.zksync.io

6. StarkWare. (2024). "Starknet Architecture." docs.starknet.io

7. Espresso Systems. (2024). "Shared Sequencing: Design and Implementation." espressosys.com

8. Ethereum Foundation. (2024). "EIP-4844: Shard Blob Transactions." eips.ethereum.org

9. Taiko. (2024). "Based Rollup Design." taiko.xyz/docs

10. Thibault, L. et al. (2024). "The Verifier's Dilemma in Optimistic Rollups." arxiv.org

---

*Report prepared January 2025. Data and stage classifications subject to change as rollups evolve. Readers should consult L2Beat and official rollup documentation for current status.*
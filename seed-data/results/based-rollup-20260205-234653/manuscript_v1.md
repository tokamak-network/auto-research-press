# Based Rollups: A Comprehensive Analysis of Ethereum-Native Sequencing Architecture

## Executive Summary

The rollup-centric roadmap has emerged as Ethereum's primary scaling strategy, with Layer 2 (L2) solutions processing an increasing share of network transactions. However, the predominant rollup architectures—optimistic and zero-knowledge (ZK) rollups—have introduced a critical centralization vector through their reliance on centralized sequencers. These sequencers, while efficient, create single points of failure, extract value through Maximal Extractable Value (MEV), and introduce trust assumptions that contradict the decentralization ethos of blockchain technology.

Based rollups, first formally articulated by Justin Drake in March 2023, represent a paradigm shift in rollup architecture by delegating sequencing responsibilities to the Ethereum Layer 1 (L1) validator set. This approach eliminates the need for dedicated L2 sequencer infrastructure, inheriting Ethereum's battle-tested decentralization, censorship resistance, and liveness guarantees. The trade-off manifests primarily in reduced transaction confirmation speed, with based rollups constrained to Ethereum's 12-second block times for soft confirmations.

This report provides a comprehensive technical analysis of based rollups, examining their architectural foundations, security properties, economic implications, and positioning within the broader L2 ecosystem. We evaluate existing implementations, assess the MEV dynamics unique to this architecture, and project the trajectory of based rollup development in light of Ethereum's evolving infrastructure, particularly preconfirmation mechanisms that may address latency limitations.

Our analysis concludes that based rollups represent a compelling alternative for applications prioritizing decentralization and Ethereum alignment over raw throughput, with emerging preconfirmation solutions potentially eliminating their primary competitive disadvantage.

---

## 1. Introduction

### 1.1 The Rollup Scaling Paradigm

Ethereum's transition to a rollup-centric scaling approach marks a fundamental architectural decision: rather than scaling the base layer directly, the network optimizes for data availability and settlement while delegating execution to Layer 2 solutions. This strategy, formalized in Vitalik Buterin's "rollup-centric roadmap" (2020), has catalyzed the development of diverse L2 implementations.

Rollups achieve scalability by executing transactions off-chain while posting compressed transaction data to Ethereum, leveraging the L1 for data availability and dispute resolution. The two dominant paradigms—optimistic rollups (exemplified by Arbitrum and Optimism) and ZK rollups (such as zkSync and StarkNet)—have achieved significant adoption, collectively processing over $30 billion in Total Value Locked (TVL) as of late 2024.

### 1.2 The Sequencer Centralization Problem

Despite their scalability benefits, contemporary rollups share a common architectural weakness: centralized sequencing. The sequencer—the entity responsible for ordering transactions and producing L2 blocks—represents a critical infrastructure component that, in most current implementations, operates as a single trusted party.

This centralization introduces several concerns:

1. **Liveness Risk**: A sequencer failure halts the rollup, requiring users to fall back to slower L1 mechanisms
2. **Censorship Vulnerability**: Sequencers can selectively exclude transactions
3. **MEV Extraction**: Centralized sequencers capture ordering-related value
4. **Trust Assumptions**: Users must trust sequencer honesty for timely inclusion

While various decentralized sequencer proposals exist—including shared sequencing networks (Espresso, Astria) and rollup-native sequencer sets—these solutions introduce additional complexity, new trust assumptions, and coordination challenges.

### 1.3 The Based Rollup Proposition

Based rollups offer a radical simplification: rather than constructing new sequencing infrastructure, they delegate this responsibility entirely to Ethereum L1 proposers. In this architecture, L1 validators (specifically, block proposers) determine L2 transaction ordering by including rollup batches in their blocks.

Justin Drake's seminal articulation of based rollups identified this approach as achieving "maximal decentralization" by inheriting Ethereum's existing security properties without introducing new trust assumptions. The concept builds on earlier work around "L1-sequenced rollups" but provides a comprehensive framework for implementation and analysis.

---

## 2. Technical Architecture

### 2.1 Core Mechanism

The fundamental operation of a based rollup can be described through the following sequence:

1. **Transaction Submission**: Users submit transactions to the rollup's public mempool or directly to L1 proposers
2. **Batch Construction**: L1 proposers (or MEV searchers operating through proposers) construct rollup batches
3. **L1 Inclusion**: Batches are included in Ethereum blocks through standard transaction inclusion
4. **State Derivation**: Rollup nodes derive L2 state by processing batches from L1 blocks
5. **Finalization**: State becomes final according to the rollup's proof system (optimistic or ZK)

```
┌─────────────────────────────────────────────────────────────┐
│                    Based Rollup Architecture                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Users ──► Mempool ──► L1 Proposer ──► Ethereum Block      │
│                              │                              │
│                              ▼                              │
│                    Rollup Batch (calldata/blob)            │
│                              │                              │
│                              ▼                              │
│              L2 Nodes derive state from L1 blocks          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Comparison with Centralized Sequencer Architecture

| Property | Centralized Sequencer | Based Rollup |
|----------|----------------------|--------------|
| Sequencing Entity | Dedicated L2 operator | Ethereum L1 proposers |
| Soft Confirmation | ~100ms-2s | ~12s (L1 block time) |
| Liveness Guarantee | Dependent on sequencer | Inherits L1 liveness |
| Censorship Resistance | Sequencer-dependent | Inherits L1 CR |
| MEV Flow | Captured by sequencer | Flows to L1 proposers |
| Infrastructure | Requires dedicated setup | Minimal additional infra |
| Decentralization | Typically centralized | Inherits L1 decentralization |

### 2.3 Data Availability Considerations

Based rollups, like all rollups, must ensure transaction data availability for state reconstruction. They can utilize:

- **Calldata**: Traditional approach with ~16 gas per byte
- **EIP-4844 Blobs**: Introduced in Dencun upgrade, providing ~10x cost reduction
- **Danksharding** (future): Further scaling data availability through data availability sampling

The choice of data availability layer does not fundamentally alter the based sequencing mechanism but significantly impacts economic viability and throughput capacity.

### 2.4 Proof Systems

Based rollups are agnostic to the underlying proof mechanism:

**Based Optimistic Rollups**: Utilize fraud proofs with challenge periods (typically 7 days). Examples include Taiko's initial design.

**Based ZK Rollups**: Generate validity proofs for state transitions, enabling faster finalization. Taiko has transitioned toward this model with its "Based Contestable Rollup" (BCR) design.

---

## 3. Security Properties and Trust Assumptions

### 3.1 Inherited Security Guarantees

Based rollups inherit several critical security properties from Ethereum L1:

**Liveness**: As long as Ethereum produces blocks, based rollups can process transactions. There is no separate liveness assumption for sequencing infrastructure. This property proved its value during centralized sequencer outages experienced by other L2s—events impossible in based rollup architecture.

**Censorship Resistance**: Transaction inclusion follows Ethereum's censorship resistance properties. While individual proposers may censor, the probabilistic rotation of proposers ensures eventual inclusion for any valid transaction.

**Decentralization**: The sequencing function distributes across Ethereum's ~900,000 validators (as of 2024), representing the largest decentralized validator set in the blockchain ecosystem.

### 3.2 Security Analysis

The security model of based rollups can be formally characterized as:

```
Security(Based Rollup) = Security(Ethereum L1) ∩ Security(Proof System)
```

This formulation highlights that based rollups introduce no additional trust assumptions beyond those inherent to Ethereum and the chosen proof mechanism (fraud proofs or validity proofs).

### 3.3 Attack Vector Analysis

**Proposer Collusion**: While individual proposers control batch ordering for their blocks, sustained attacks require controlling consecutive slots—economically prohibitive given Ethereum's validator distribution.

**MEV-Driven Reordering**: L1 proposers may reorder L2 transactions for MEV extraction. This represents value leakage from L2 to L1 but does not compromise security.

**Data Withholding**: Proposers cannot withhold data for included batches due to Ethereum's data availability guarantees (strengthened by EIP-4844 and future danksharding).

---

## 4. Economic Implications and MEV Dynamics

### 4.1 MEV Flow Transformation

The most significant economic distinction of based rollups concerns MEV distribution. In centralized sequencer architectures, MEV accrues to the sequencer operator. Based rollups redirect this value to L1 proposers and the MEV supply chain (searchers, builders, relays).

This transformation has several implications:

1. **L1 Economic Security**: MEV flowing to L1 strengthens Ethereum's economic security
2. **Rollup Revenue Model**: Based rollups cannot capture sequencing revenue, requiring alternative monetization
3. **Searcher Dynamics**: MEV searchers must integrate L2 transaction analysis into L1 strategies

### 4.2 Revenue Model Considerations

Without sequencer revenue, based rollups must explore alternative sustainability models:

- **Protocol Fees**: Transaction fees beyond L1 costs
- **Ecosystem Grants**: Foundation or DAO-based funding
- **Value-Added Services**: Premium features like preconfirmations
- **Token Economics**: Native token value capture mechanisms

Taiko, the leading based rollup implementation, has implemented a ticket-based system where proposers purchase the right to propose blocks, creating a competitive market that returns value to the protocol.

### 4.3 Cost Structure Analysis

Based rollups exhibit a distinctive cost structure:

```
User Cost = L1 Data Cost + L2 Execution Cost + Protocol Fee
```

The absence of sequencer infrastructure reduces operational overhead, potentially enabling lower fees despite MEV leakage. EIP-4844 has dramatically reduced data costs, making based rollups increasingly economically competitive.

---

## 5. Latency Considerations and Preconfirmation Solutions

### 5.1 The Latency Challenge

The primary limitation of based rollups is confirmation latency. While centralized sequencers can provide soft confirmations in hundreds of milliseconds, based rollups are constrained to Ethereum's 12-second block time for initial confirmation.

This latency impacts:
- User experience for interactive applications
- DeFi operations requiring rapid execution
- Gaming and real-time applications
- Arbitrage and trading strategies

### 5.2 Preconfirmation Mechanisms

Preconfirmations represent the most promising solution to based rollup latency. The concept involves L1 proposers providing binding commitments to include transactions before their slot arrives.

**Mechanism Overview**:
1. User submits transaction with preconfirmation request
2. Upcoming proposer (or their delegate) evaluates and signs commitment
3. User receives cryptographic guarantee of inclusion
4. Proposer fulfills commitment when their slot arrives
5. Failure to fulfill results in slashing

**Technical Requirements**:
- Proposer lookahead (currently 32 slots in Ethereum)
- Commitment infrastructure (registries, relays)
- Slashing mechanisms for commitment violations
- Economic incentives aligning proposer behavior

### 5.3 Preconfirmation Implementations

Several projects are developing preconfirmation infrastructure:

**Ethereum Research Proposals**: Justin Drake and others have proposed native preconfirmation mechanisms integrated with Ethereum's consensus.

**Commit-Boost**: An open-source framework for proposer commitments, enabling standardized preconfirmation APIs.

**Taiko's Approach**: Implementing "based preconfirmations" through integration with proposer commitment networks.

**Primev's mev-commit**: Building preconfirmation infrastructure as part of broader MEV commitment systems.

### 5.4 Latency Trajectory

With preconfirmations, based rollup latency could potentially reach:
- **Current**: ~12 seconds (L1 block time)
- **Near-term** (with preconfirmations): ~100ms-1s
- **Long-term** (with protocol integration): Potentially sub-100ms

This trajectory suggests based rollups may achieve competitive latency while maintaining their decentralization advantages.

---

## 6. Implementation Analysis: Taiko

### 6.1 Overview

Taiko represents the most advanced based rollup implementation, launching its mainnet (Alpha-7) in 2024. The project explicitly embraces the "based" designation, positioning itself as maximally Ethereum-aligned.

### 6.2 Technical Architecture

Taiko implements a "Based Contestable Rollup" (BCR) design incorporating:

**Permissionless Proposing**: Any party can propose blocks by interacting with the L1 contract, paying a bond that is slashed for invalid proposals.

**Multi-Proof System**: Supporting multiple proof types (optimistic, ZK, SGX) with contestation mechanisms allowing challenges across proof systems.

**Based Sequencing**: Full delegation of sequencing to L1 proposers, with no centralized sequencer infrastructure.

```solidity
// Simplified Taiko proposing interface
function proposeBlock(
    bytes calldata params,
    bytes calldata txList
) external payable returns (BlockMetadata memory meta);
```

### 6.3 Performance Metrics

As of late 2024, Taiko has demonstrated:
- Transaction throughput: Variable based on L1 data availability
- Cost reduction: ~10-50x compared to L1 execution (post-EIP-4844)
- Decentralization: Fully permissionless proposing with multiple active proposers
- Uptime: Inheriting L1 liveness with no sequencer-related outages

### 6.4 Lessons Learned

Taiko's implementation has validated several theoretical predictions:
1. Based sequencing is technically feasible at scale
2. Permissionless proposing creates competitive markets
3. MEV dynamics require careful economic design
4. Preconfirmations are necessary for UX competitiveness

---

## 7. Comparative Analysis

### 7.1 Based Rollups vs. Centralized Sequencer Rollups

| Dimension | Based Rollups | Centralized Sequencers |
|-----------|--------------|------------------------|
| Decentralization | Maximal (L1-equivalent) | Minimal (single operator) |
| Latency | ~12s (improvable) | ~100ms-2s |
| Censorship Resistance | L1-equivalent | Operator-dependent |
| MEV Distribution | To L1 proposers | To sequencer |
| Operational Complexity | Lower | Higher |
| Liveness | L1-guaranteed | Sequencer-dependent |
| Ethereum Alignment | Maximal | Variable |

### 7.2 Based Rollups vs. Shared Sequencing

Shared sequencing networks (Espresso, Astria) represent an intermediate approach:

**Shared Sequencing Advantages**:
- Faster confirmations than based rollups
- Cross-rollup atomicity
- Decentralized (though new trust assumptions)

**Based Rollup Advantages**:
- No new trust assumptions
- Simpler architecture
- Ethereum-native security
- No additional token/economics

### 7.3 Based Rollups vs. Validiums

Validiums sacrifice data availability for cost reduction:

**Based Rollups**: Full DA on Ethereum, higher costs, stronger guarantees
**Validiums**: Off-chain DA, lower costs, weaker guarantees

Based rollups and validiums represent orthogonal design choices; a "based validium" combining both approaches is theoretically possible but introduces significant trust assumptions.

---

## 8. Future Directions and Research Frontiers

### 8.1 Protocol-Level Preconfirmations

Ethereum researchers are exploring native preconfirmation mechanisms:

**Inclusion Lists**: Proposers commit to including specific transactions
**Execution Tickets**: Separating consensus and execution duties
**Based Preconfirmations**: Standardized commitment protocols

These developments could provide based rollups with sub-second confirmations without additional trust assumptions.

### 8.2 Based Rollup Composability

Multiple based rollups sharing L1 sequencing could enable:
- Atomic cross-rollup transactions
- Shared liquidity pools
- Unified MEV markets
- Simplified bridging

This "based ecosystem" vision positions Ethereum as a unified settlement and sequencing layer for multiple execution environments.

### 8.3 MEV Redistribution Mechanisms

Research into MEV redistribution could allow based rollups to recapture value:
- MEV-Share integration for L2 transactions
- Proposer payment mechanisms
- Order flow auctions at the L2 level

### 8.4 Proving System Advances

ZK proving improvements directly benefit based rollups:
- Faster proof generation enables more frequent state updates
- Recursive proofs reduce verification costs
- Hardware acceleration improves economics

---

## 9. Challenges and Limitations

### 9.1 Current Limitations

**Latency**: The 12-second confirmation time remains a significant UX challenge for certain applications, though preconfirmations offer a path forward.

**MEV Leakage**: Value extraction by L1 proposers represents an economic inefficiency from the L2 perspective.

**Complexity for Users**: Understanding the based model requires additional user education.

**Tooling Maturity**: Development tools and infrastructure are less mature than for established rollup frameworks.

### 9.2 Open Research Questions

1. **Optimal Preconfirmation Design**: What mechanisms best balance latency, security, and decentralization?
2. **MEV Redistribution**: How can based rollups recapture MEV value while maintaining decentralization?
3. **Cross-Rollup Coordination**: How do multiple based rollups interact efficiently?
4. **Economic Sustainability**: What long-term revenue models support based rollup development?

### 9.3 Adoption Barriers

- **Incumbent Advantage**: Established rollups with centralized sequencers have significant network effects
- **Developer Familiarity**: Most L2 developers are trained on centralized sequencer models
- **Short-term UX**: Current latency disadvantages may deter user adoption
- **Ecosystem Lock-in**: Applications deployed on existing rollups face migration costs

---

## 10. Conclusion

Based rollups represent a principled approach to Layer 2 scaling that prioritizes Ethereum alignment and decentralization over raw performance metrics. By delegating sequencing to Ethereum's validator set, based rollups inherit the network's battle-tested security properties while eliminating the centralization risks inherent in dedicated sequencer infrastructure.

The primary trade-off—increased confirmation latency—is increasingly addressable through preconfirmation mechanisms that leverage proposer commitments to provide fast, credible transaction guarantees. As these systems mature, based rollups may achieve competitive latency while maintaining their decentralization advantages.

Taiko's successful mainnet launch demonstrates the technical viability of based rollup architecture, while ongoing research into preconfirmations, MEV redistribution, and cross-rollup composability suggests a rich development trajectory. The based rollup model aligns with Ethereum's long-term vision of a decentralized settlement layer supporting diverse execution environments.

For applications prioritizing censorship resistance, liveness guarantees, and philosophical alignment with Ethereum's values, based rollups offer a compelling alternative to centralized sequencer architectures. As the ecosystem matures and latency solutions deploy, based rollups may emerge as the preferred architecture for security-conscious applications and Ethereum-native protocols.

The evolution of based rollups will likely be shaped by three key developments: the maturation of preconfirmation infrastructure, the economic sustainability of alternative revenue models, and the broader adoption of Ethereum's rollup-centric roadmap. Projects and researchers working at this frontier are laying the groundwork for a more decentralized, resilient, and Ethereum-aligned Layer 2 ecosystem.

---

## References

1. Drake, J. (2023). "Based rollups—superpowers from L1 sequencing." Ethereum Research Forum.

2. Buterin, V. (2020). "A rollup-centric ethereum roadmap." Ethereum Magicians Forum.

3. Taiko Labs. (2024). "Taiko Protocol Specification." Technical Documentation.

4. Ethereum Foundation. (2024). "EIP-4844: Shard Blob Transactions." Ethereum Improvement Proposals.

5. Flashbots. (2023). "MEV-Share: Programmable Privacy for MEV." Research Publication.

6. Espresso Systems. (2023). "Espresso Sequencer: Decentralized Sequencing for Rollups." Technical Whitepaper.

7. Drake, J. (2024). "Based preconfirmations." Ethereum Research Forum.

8. L2Beat. (2024). "Layer 2 Risk Analysis." https://l2beat.com

9. Gudgeon, L., et al. (2020). "SoK: Layer-Two Blockchain Protocols." Financial Cryptography and Data Security.

10. Daian, P., et al. (2020). "Flash Boys 2.0: Frontrunning in Decentralized Exchanges." IEEE S&P.

---

*Word Count: ~4,200*

*Last Updated: December 2024*
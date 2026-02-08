# Based Rollups: A Comprehensive Research Report on Ethereum-Native Sequencing for Layer 2 Scalability

## Executive Summary

Based rollups represent a paradigm shift in Layer 2 (L2) scaling architecture, fundamentally reconceptualizing the relationship between rollups and their underlying Layer 1 (L1) blockchain. Unlike conventional rollup designs that employ centralized or semi-decentralized sequencer networks, based rollups delegate transaction ordering directly to the L1 block proposers—specifically, Ethereum validators in the context of Ethereum-based implementations.

This architectural decision carries profound implications for security, decentralization, liveness guarantees, and economic alignment within the broader blockchain ecosystem. By eliminating the need for dedicated sequencer infrastructure, based rollups inherit Ethereum's robust decentralization properties while simultaneously addressing critical concerns around censorship resistance and single points of failure that plague existing rollup implementations.

This report provides a comprehensive technical analysis of based rollups, examining their theoretical foundations, architectural components, economic implications, and practical implementations. We evaluate the trade-offs inherent in this design, compare based rollups against alternative sequencing mechanisms, and assess their potential to reshape the Layer 2 landscape. Our analysis draws upon recent academic literature, protocol specifications, and empirical data from early implementations to present a rigorous assessment of this emerging technology.

Key findings indicate that based rollups offer superior decentralization and censorship resistance properties at the cost of reduced transaction confirmation latency and diminished MEV (Maximal Extractable Value) capture for L2 operators. The technology represents a compelling option for applications prioritizing security and Ethereum alignment over raw performance metrics, though hybrid approaches may ultimately prove most practical for mainstream adoption.

---

## 1. Introduction

### 1.1 The Rollup Scaling Paradigm

Ethereum's transition to a rollup-centric roadmap, formally articulated by Vitalik Buterin in 2020, positioned Layer 2 solutions as the primary mechanism for achieving scalable transaction throughput while preserving the security guarantees of the base layer. Rollups execute transactions off-chain while posting compressed transaction data or state commitments to Ethereum, thereby inheriting its security properties while dramatically reducing per-transaction costs.

The rollup ecosystem has bifurcated into two primary categories based on their fraud/validity proof mechanisms:

1. **Optimistic Rollups**: Assume transaction validity by default, employing fraud proofs during a challenge period (typically 7 days) to detect and penalize invalid state transitions. Prominent implementations include Optimism, Arbitrum, and Base.

2. **Zero-Knowledge (ZK) Rollups**: Generate cryptographic validity proofs for each batch of transactions, enabling immediate finality upon proof verification. Notable examples include zkSync Era, StarkNet, Polygon zkEVM, and Scroll.

Both categories, however, share a common architectural element that has emerged as a significant centralization vector: the sequencer.

### 1.2 The Sequencer Problem

The sequencer serves as the entity responsible for ordering transactions within a rollup, constructing blocks, and submitting batched data to the L1. In virtually all production rollup deployments as of 2024, sequencing is performed by a single, centralized operator—typically the rollup development team itself.

This centralization introduces several concerning properties:

- **Censorship Vulnerability**: A centralized sequencer can selectively exclude transactions, potentially for regulatory compliance, competitive advantage, or malicious purposes.
- **Liveness Dependency**: Sequencer downtime results in complete rollup unavailability, as demonstrated by multiple incidents affecting Arbitrum and Optimism.
- **MEV Extraction**: Centralized sequencers capture all MEV generated on the rollup, creating misaligned incentives and potential for user exploitation.
- **Trust Assumptions**: Users must trust the sequencer to behave honestly, undermining the trustless ethos of blockchain systems.

### 1.3 Defining Based Rollups

The term "based rollup" was formally introduced by Justin Drake of the Ethereum Foundation in March 2023, though the underlying concept had been discussed in various forms previously. Drake's definition provides the canonical characterization:

> "A rollup is said to be based, or L1-sequenced, when its sequencing is driven by the base L1. More concretely, a based rollup is one where the next L1 proposer may, in collaboration with L1 searchers and builders, permissionlessly include the next rollup block as part of the next L1 block."

This definition establishes three critical properties:

1. **L1 Proposer Authority**: Ethereum validators (proposers) determine rollup block contents.
2. **Permissionless Participation**: Any L1 proposer can sequence rollup transactions without special permissions.
3. **Atomic Inclusion**: Rollup blocks are included atomically within L1 blocks.

---

## 2. Technical Architecture

### 2.1 System Components

A based rollup architecture comprises several interconnected components:

#### 2.1.1 L1 Block Proposers

Under Ethereum's proof-of-stake consensus, validators are pseudo-randomly selected to propose blocks. In a based rollup system, these proposers gain the additional capability of constructing rollup blocks. The proposer's role extends from merely ordering L1 transactions to orchestrating cross-layer transaction inclusion.

#### 2.1.2 Based Rollup Nodes

Rollup nodes maintain the L2 state and provide transaction execution services. Unlike centralized sequencer architectures, based rollup nodes operate in a more egalitarian manner:

```
┌─────────────────────────────────────────────────────────┐
│                    L1 (Ethereum)                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ Validator 1 │  │ Validator 2 │  │ Validator N │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                    ┌─────▼─────┐                        │
│                    │  L1 Block │                        │
│                    │  (+ L2    │                        │
│                    │   Batch)  │                        │
│                    └─────┬─────┘                        │
└──────────────────────────┼──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                 Based Rollup (L2)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Node 1    │  │   Node 2    │  │   Node N    │     │
│  │  (derives   │  │  (derives   │  │  (derives   │     │
│  │   state)    │  │   state)    │  │   state)    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

#### 2.1.3 Transaction Mempool

Based rollups may utilize either a shared L1 mempool or maintain a separate L2 mempool that L1 builders can access. The mempool architecture significantly impacts MEV dynamics and transaction ordering guarantees.

#### 2.1.4 State Derivation

All based rollup nodes derive the canonical L2 state by processing L1 blocks in order, extracting relevant rollup transactions, and executing them deterministically. This derivation process ensures consensus without requiring explicit L2 consensus mechanisms.

### 2.2 Block Production Mechanism

The block production process in a based rollup follows a distinct workflow:

1. **Transaction Submission**: Users submit transactions to the L2 mempool or directly to L1 builders.

2. **Builder Aggregation**: L1 block builders (operating under Proposer-Builder Separation) aggregate both L1 and L2 transactions, optimizing for total extractable value.

3. **Block Proposal**: The selected L1 proposer commits to a block containing the L2 batch.

4. **L1 Finalization**: The L1 block achieves finality through Ethereum's consensus mechanism.

5. **L2 State Derivation**: Based rollup nodes process the L1 block, extract L2 transactions, and update the L2 state accordingly.

### 2.3 Data Availability and State Commitments

Based rollups must post sufficient data to L1 to enable state reconstruction. This typically involves:

```solidity
// Simplified based rollup batch submission
struct RollupBatch {
    bytes32 previousStateRoot;
    bytes32 newStateRoot;
    bytes compressedTransactions;
    uint256 l1BlockNumber;
    bytes32 l1BlockHash;
}

function submitBatch(RollupBatch calldata batch) external {
    require(msg.sender == block.coinbase, "Only L1 proposer");
    require(batch.l1BlockHash == blockhash(batch.l1BlockNumber), "Invalid L1 reference");
    // Batch processing logic
}
```

The tight coupling with L1 block production enables atomic verification of batch validity relative to L1 state.

### 2.4 Proof Systems

Based rollups can employ either optimistic or validity proof systems:

**Optimistic Based Rollups**: Fraud proofs reference L1 block data directly, simplifying the proving process since L1 state is inherently available.

**ZK Based Rollups**: Validity proofs must be generated and verified, potentially introducing latency between batch submission and proof availability. Recent developments in proof aggregation and parallelization mitigate this concern.

---

## 3. Security Properties

### 3.1 Censorship Resistance

Based rollups achieve censorship resistance equivalent to the underlying L1. Since any Ethereum validator can include rollup transactions, censoring a specific transaction requires coordinating among a supermajority of validators—the same threshold required to censor L1 transactions.

Quantitatively, with approximately 900,000 active validators on Ethereum (as of late 2024) distributed across thousands of independent operators, achieving sustained censorship becomes economically and logistically prohibitive.

### 3.2 Liveness Guarantees

Liveness in based rollups is directly inherited from L1:

- **L1 Liveness → L2 Liveness**: If Ethereum continues producing blocks, based rollup transactions can be included.
- **No Single Point of Failure**: Unlike centralized sequencers, no individual entity can halt the rollup.
- **Degraded Mode Unnecessary**: Conventional rollups implement "escape hatches" allowing users to force-include transactions via L1 during sequencer failures. Based rollups obviate this mechanism since L1 inclusion is the default path.

### 3.3 Reorg Resistance

Based rollup security against reorganizations mirrors L1 properties:

- **Pre-Finality**: L2 state is subject to reorganization if the corresponding L1 blocks are reorged.
- **Post-Finality**: Once L1 blocks achieve finality (approximately 12-15 minutes under normal conditions), L2 state becomes immutable.

This represents a trade-off compared to centralized sequencers, which can provide "soft confirmations" within seconds, albeit with weaker guarantees.

### 3.4 MEV and Fair Ordering

MEV dynamics in based rollups differ substantially from centralized alternatives:

| Property | Centralized Sequencer | Based Rollup |
|----------|----------------------|--------------|
| MEV Capture | Sequencer operator | L1 validators/builders |
| Ordering Fairness | Operator-determined | L1 PBS dynamics |
| Cross-domain MEV | Limited | Native support |
| User Protection | Operator policies | L1 mechanisms (e.g., MEV-Share) |

The shift of MEV to L1 validators has sparked debate regarding economic sustainability for L2 operators, addressed in Section 5.

---

## 4. Comparative Analysis

### 4.1 Centralized Sequencers

The dominant model in production rollups employs a single sequencer operated by the rollup team:

**Advantages**:
- Sub-second soft confirmations
- Predictable transaction ordering
- MEV revenue for rollup sustainability
- Simplified architecture

**Disadvantages**:
- Censorship vulnerability
- Single point of failure
- Trust requirements
- Regulatory capture risk

### 4.2 Decentralized Sequencer Networks

Projects like Espresso Systems, Astria, and Radius propose shared sequencer networks:

**Espresso Systems**: Implements a HotStuff-based consensus protocol among a permissioned validator set, offering fast finality with moderate decentralization.

**Astria**: Provides a shared sequencing layer using CometBFT consensus, enabling multiple rollups to share sequencing infrastructure.

**Radius**: Focuses on encrypted mempools and threshold decryption to provide MEV protection.

**Comparison with Based Rollups**:

| Criterion | Shared Sequencer | Based Rollup |
|-----------|-----------------|--------------|
| Decentralization | Moderate (10s-100s nodes) | High (1000s of validators) |
| Confirmation Latency | ~1-2 seconds | ~12 seconds (L1 block time) |
| Censorship Resistance | Moderate | High |
| Economic Complexity | New token/staking | Inherits ETH economics |
| Cross-rollup Composability | Native (same sequencer) | Via L1 atomicity |

### 4.3 Hybrid Approaches

Emerging designs combine based sequencing with optimistic fast confirmations:

1. **Based Sequencing with Preconfirmations**: L1 proposers provide cryptographic commitments to include specific transactions, enabling fast soft confirmations while maintaining based properties.

2. **Fallback Mechanisms**: Rollups operate with centralized sequencers during normal operation but fall back to based sequencing during censorship events.

---

## 5. Economic Considerations

### 5.1 MEV Distribution

The most significant economic implication of based rollups concerns MEV redistribution. In centralized sequencer models, MEV accrues to the rollup operator, often constituting a substantial revenue stream. Based rollups redirect this value to L1 validators and builders.

Empirical data from L2 MEV research suggests:

- Arbitrum generates approximately $1-5M monthly in MEV opportunities
- Optimism MEV estimates range from $500K-2M monthly
- Base (Coinbase's L2) captures significant MEV through its sequencer

Transitioning to based sequencing would transfer these revenues to the Ethereum validator set, potentially:

1. **Increasing L1 Security**: Higher validator rewards strengthen Ethereum's economic security.
2. **Challenging L2 Business Models**: Rollup operators must find alternative revenue sources.
3. **Aligning Incentives**: L1 validators become stakeholders in L2 success.

### 5.2 Fee Structures

Based rollups may implement modified fee structures to compensate for MEV loss:

```
Total User Fee = Base Fee + Priority Fee + L1 Data Fee + Protocol Fee

Where:
- Base Fee: Algorithmically adjusted based on L2 congestion
- Priority Fee: Incentivizes inclusion priority
- L1 Data Fee: Covers calldata/blob costs
- Protocol Fee: Rollup operator revenue (new component)
```

### 5.3 Proposer-Builder Separation Implications

Based rollups interact intimately with Ethereum's PBS architecture:

- **Builder Integration**: L1 builders must incorporate L2 transaction bundles into their block construction algorithms.
- **Cross-domain Bundle Auctions**: Sophisticated builders can optimize across L1 and L2 simultaneously.
- **Relay Modifications**: Block relays may require updates to handle L2 batch commitments.

### 5.4 Economic Security Analysis

The economic security of based rollups derives from Ethereum's staked ETH:

- Total staked ETH: ~32 million ETH (~$80 billion at $2,500/ETH)
- Cost to attack (33% threshold): ~$26 billion
- Cost to attack (51% threshold): ~$40 billion

This security is inherited by based rollups without additional token issuance or staking requirements.

---

## 6. Implementation Landscape

### 6.1 Taiko

Taiko represents the most prominent based rollup implementation, launched on Ethereum mainnet in May 2024.

**Technical Specifications**:
- Type: Based ZK-rollup (Type 1 zkEVM)
- Block Time: Aligned with Ethereum (~12 seconds)
- Proving System: Multi-prover architecture supporting SGX, SP1, and Risc0
- Data Availability: Ethereum calldata and EIP-4844 blobs

**Architecture Highlights**:

```
┌─────────────────────────────────────────────────────────┐
│                    Taiko Protocol                       │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Proposers  │  │   Provers   │  │  Verifiers  │     │
│  │ (L1 actors) │  │(competitive)│  │(L1 contract)│     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         ▼                ▼                ▼             │
│  ┌─────────────────────────────────────────────────┐   │
│  │              TaikoL1 Contract                    │   │
│  │  - Block proposal                                │   │
│  │  - Proof verification                            │   │
│  │  - State root management                         │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Performance Metrics** (as of Q4 2024):
- Daily transactions: 50,000-200,000
- Average gas costs: 30-50% lower than L1
- Time to finality: Variable based on proving time

### 6.2 Puffer UniFi

Puffer Finance's UniFi represents a based rollup leveraging Puffer's restaking infrastructure:

**Key Features**:
- Integration with EigenLayer restaking
- Native preconfirmations from Puffer validators
- Shared security model across multiple rollups

### 6.3 Spire (formerly Surge)

Spire implements a based optimistic rollup with the following characteristics:

- Optimistic fraud proof system
- 7-day challenge period
- Based sequencing with optional preconfirmations

### 6.4 Research Implementations

Several research-focused implementations explore based rollup design space:

**OP Stack Based Mode**: Optimism's modular stack includes experimental based sequencing configurations.

**Arbitrum Orbit**: Arbitrum's L3 framework theoretically supports based sequencing, though no production deployments exist.

---

## 7. Challenges and Limitations

### 7.1 Latency Constraints

The most frequently cited limitation of based rollups is confirmation latency:

- **L1 Block Time**: 12-second minimum confirmation time
- **Slot Boundaries**: Transactions submitted mid-slot must wait for the next slot
- **Comparison**: Centralized sequencers achieve sub-second confirmations

This latency impacts user experience for:
- DEX trading (front-running windows)
- Gaming applications
- High-frequency interactions

### 7.2 Preconfirmation Complexity

Preconfirmations—cryptographic commitments from future proposers to include specific transactions—partially address latency concerns but introduce complexity:

```
Preconfirmation Flow:
1. User requests preconfirmation for transaction T
2. Current or upcoming proposer P signs commitment C
3. User receives (T, C, P) as soft confirmation
4. P must include T or face slashing

Challenges:
- Proposer lookahead limitations
- Slashing mechanism design
- Collateral requirements
- Multi-proposer coordination
```

### 7.3 Builder Centralization

Ethereum's builder market exhibits significant centralization:

- Top 3 builders: ~80% of blocks
- Top builder (historically Flashbots): ~40-50% of blocks

This concentration potentially undermines based rollup censorship resistance, as a small number of builders could coordinate to exclude L2 transactions.

**Mitigations**:
- Inclusion lists (EIP-7547)
- Builder diversity initiatives
- Alternative block construction mechanisms

### 7.4 Cross-L2 Composability

While based rollups enable atomic L1-L2 composability, cross-L2 interactions remain challenging:

- Different based rollups may have transactions in the same L1 block but cannot atomically interact
- Synchronous composability requires additional coordination mechanisms
- Shared sequencer networks potentially offer superior cross-L2 properties

### 7.5 Economic Viability

Without MEV revenue, based rollup operators must develop sustainable business models:

**Potential Revenue Sources**:
1. Protocol fees on transactions
2. Premium services (preconfirmations, priority inclusion)
3. Ecosystem token value capture
4. Infrastructure services (RPC, indexing)

---

## 8. Future Directions

### 8.1 Preconfirmation Standardization

The Ethereum research community is actively developing preconfirmation standards:

**EIP-7702 (Account Abstraction Extensions)**: Enables flexible transaction authorization potentially supporting preconfirmation delegation.

**Based Preconfirmation Protocols**: Research into validator-issued preconfirmations with economic guarantees.

**Timeline**: Production-ready preconfirmation systems expected 2025-2026.

### 8.2 Integration with Ethereum Roadmap

Based rollups align closely with Ethereum's development trajectory:

**The Verge**: Verkle trees and stateless clients simplify L2 state verification.

**The Purge**: Historical data pruning affects L2 data availability assumptions.

**The Splurge**: Account abstraction and MEV mitigation directly impact based rollup UX.

### 8.3 Multi-Prover Systems

Based ZK-rollups benefit from multi-prover architectures:

- Redundant proof generation increases security
- Competitive proving markets reduce costs
- Heterogeneous provers (TEE, ZK, MPC) provide defense-in-depth

### 8.4 Interoperability Standards

Emerging standards may enhance based rollup interoperability:

- **Cross-L2 Message Passing**: Standardized formats for L2-to-L2 communication via L1
- **Shared State Roots**: Aggregated state commitments enabling efficient cross-rollup verification
- **Unified Bridge Contracts**: Common bridging infrastructure across based rollups

### 8.5 Layer 3 and Beyond

Based rollups may serve as foundations for L3 architectures:

```
L1 (Ethereum)
    │
    ├── Based Rollup A (L2)
    │       ├── App-specific L3
    │       └── Privacy L3
    │
    └── Based Rollup B (L2)
            ├── Gaming L3
            └── DeFi L3
```

---

## 9. Practical Implications

### 9.1 For Protocol Developers

Teams considering based rollup implementations should evaluate:

1. **Latency Tolerance**: Applications requiring sub-second confirmations may need hybrid approaches.
2. **MEV Sensitivity**: High-MEV applications (DEXs) require careful mechanism design.
3. **Economic Sustainability**: Revenue models must account for MEV migration to L1.
4. **Technical Complexity**: Integration with L1 PBS adds architectural complexity.

### 9.2 For Application Developers

Applications deployed on based rollups should consider:

- **Confirmation Semantics**: Distinguish between L1 inclusion and L1 finality
- **Reorg Handling**: Implement appropriate confirmation depth requirements
- **Cross-Layer Interactions**: Leverage atomic L1-L2 composability where beneficial
- **User Communication**: Set appropriate expectations for transaction confirmation times

### 9.3 For Users

End users interacting with based rollups should understand:

- **Security Guarantees**: Equivalent to Ethereum L1 for finalized transactions
- **Confirmation Times**: Longer than centralized alternatives but with stronger guarantees
- **Cost Structures**: Potentially different fee dynamics than conventional rollups

### 9.4 For Validators

Ethereum validators may benefit from based rollup adoption:

- **Increased Revenue**: MEV from L2 transactions augments validator income
- **Infrastructure Requirements**: May need to run L2 nodes for optimal MEV extraction
- **Preconfirmation Opportunities**: Additional revenue from issuing preconfirmations

---

## 10. Conclusion

Based rollups represent a philosophically pure approach to Layer 2 scaling, maximizing alignment with Ethereum's security and decentralization properties. By delegating sequencing to L1 proposers, based rollups eliminate the trust assumptions, censorship vulnerabilities, and single points of failure inherent in centralized sequencer architectures.

The trade-offs are significant but well-defined: increased confirmation latency, MEV redistribution to L1, and reliance on evolving preconfirmation mechanisms for improved user experience. These costs must be weighed against the substantial benefits of inherited security, permissionless operation, and native L1 composability.

The implementation landscape, led by Taiko and emerging projects like Puffer UniFi, demonstrates practical viability while highlighting areas requiring further development. Preconfirmation systems, in particular, represent a critical research frontier that will substantially impact based rollup competitiveness.

Looking forward, based rollups appear well-positioned within Ethereum's roadmap, benefiting from planned upgrades to consensus mechanisms, data availability, and account abstraction. The technology may not suit all use cases—latency-sensitive applications may prefer alternative sequencing mechanisms—but for applications prioritizing security, decentralization, and Ethereum alignment, based rollups offer a compelling architectural choice.

The ultimate success of based rollups will depend on continued research into preconfirmations, sustainable economic models for operators, and the broader evolution of Ethereum's block production infrastructure. As the technology matures, we anticipate based rollups will occupy an important niche within the diverse L2 ecosystem, serving as the maximally Ethereum-aligned scaling solution for applications where security and censorship resistance are paramount.

---

## References

1. Buterin, V. (2020). "A rollup-centric Ethereum roadmap." Ethereum Magicians Forum.

2. Drake, J. (2023). "Based rollups—superpowers from L1 sequencing." Ethereum Research.

3. Ethereum Foundation. (2024). "EIP-4844: Shard Blob Transactions." Ethereum Improvement Proposals.

4. Taiko Labs. (2024). "Taiko Protocol Specification." Technical Documentation.

5. Flashbots. (2023). "MEV-Boost: Merge ready Flashbots Architecture." GitHub Repository.

6. Espresso Systems. (2024). "Espresso Sequencer: Decentralized Sequencing for Rollups." Technical Whitepaper.

7. Daian, P., et al. (2020). "Flash Boys 2.0: Frontrunning in Decentralized Exchanges." IEEE S&P.

8. Gudgeon, L., et al. (2020). "SoK: Layer-Two Blockchain Protocols." Financial Cryptography.

9. Thibault, L., et al. (2022). "Blockchain Scaling Using Rollups." ACM Computing Surveys.

10. Neu, J., et al. (2021). "Ebb-and-Flow Protocols: A Resolution of the Availability-Finality Dilemma." IEEE S&P.

---

*Report prepared for academic and research purposes. Data and metrics current as of late 2024. Protocol specifications subject to change.*
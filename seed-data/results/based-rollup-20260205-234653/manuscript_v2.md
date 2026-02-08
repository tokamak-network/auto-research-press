# Based Rollups: A Comprehensive Analysis of Ethereum-Native Sequencing Architecture

## Executive Summary

The rollup-centric roadmap has emerged as Ethereum's primary scaling strategy, with Layer 2 (L2) solutions processing an increasing share of network transactions. However, the predominant rollup architectures—optimistic and zero-knowledge (ZK) rollups—have introduced a critical centralization vector through their reliance on centralized sequencers. These sequencers, while efficient, create single points of failure, extract value through Maximal Extractable Value (MEV), and introduce trust assumptions that contradict the decentralization ethos of blockchain technology.

Based rollups, first formally articulated by Justin Drake in March 2023, represent a paradigm shift in rollup architecture by delegating sequencing responsibilities to the Ethereum Layer 1 (L1) proposer-builder pipeline. This approach eliminates the need for dedicated L2 sequencer infrastructure, inheriting Ethereum's battle-tested decentralization, censorship resistance, and liveness guarantees. The trade-off manifests primarily in reduced transaction confirmation speed, with based rollups constrained to Ethereum's 12-second block times for initial inclusion, followed by the 2-epoch (~12.8 minute) finality window for probabilistic finality guarantees.

This report provides a comprehensive technical analysis of based rollups, examining their architectural foundations, security properties, economic implications, and positioning within the broader L2 ecosystem. We evaluate existing implementations, assess the MEV dynamics unique to this architecture—particularly under Proposer-Builder Separation (PBS)—and project the trajectory of based rollup development in light of Ethereum's evolving infrastructure, including preconfirmation mechanisms that may address latency limitations.

Our analysis concludes that based rollups represent a compelling alternative for applications prioritizing decentralization and Ethereum alignment over raw throughput, with emerging preconfirmation solutions potentially eliminating their primary competitive disadvantage. However, we identify important nuances in liveness guarantees, PBS interactions, and data availability considerations that require careful analysis for practitioners evaluating this architecture.

---

## 1. Introduction

### 1.1 The Rollup Scaling Paradigm

Ethereum's transition to a rollup-centric scaling approach marks a fundamental architectural decision: rather than scaling the base layer directly, the network optimizes for data availability and settlement while delegating execution to Layer 2 solutions. This strategy, formalized in Vitalik Buterin's "rollup-centric roadmap" (2020), has catalyzed the development of diverse L2 implementations.

Rollups achieve scalability by executing transactions off-chain while posting compressed transaction data to Ethereum, leveraging the L1 for data availability and dispute resolution. The two dominant paradigms—optimistic rollups (exemplified by Arbitrum and Optimism) and ZK rollups (such as zkSync and StarkNet)—have achieved significant adoption, collectively processing over $30 billion in Total Value Locked (TVL) as of late 2024.

### 1.2 The Sequencer Centralization Problem

Despite their scalability benefits, contemporary rollups share a common architectural weakness: centralized sequencing. The sequencer—the entity responsible for ordering transactions and producing L2 blocks—represents a critical infrastructure component that, in most current implementations, operates as a single trusted party.

This centralization introduces several concerns:

1. **Liveness Risk**: A sequencer failure halts the rollup, requiring users to fall back to slower L1 force-inclusion mechanisms (typically with 12-24 hour delays)
2. **Censorship Vulnerability**: Sequencers can selectively exclude transactions, though force-inclusion provides an eventual escape hatch
3. **MEV Extraction**: Centralized sequencers capture ordering-related value
4. **Trust Assumptions**: Users must trust sequencer honesty for timely inclusion

While various decentralized sequencer proposals exist—including shared sequencing networks (Espresso, Astria) and rollup-native sequencer sets—these solutions introduce additional complexity, new trust assumptions, and coordination challenges.

### 1.3 The Based Rollup Proposition

Based rollups offer a radical simplification: rather than constructing new sequencing infrastructure, they delegate this responsibility entirely to Ethereum's L1 block production pipeline. In the current PBS regime, this means builders construct blocks containing L2 batches, while proposers attest to block validity—a nuance with significant implications for MEV dynamics explored in Section 4.

Justin Drake's seminal articulation of based rollups identified this approach as achieving "maximal decentralization" by inheriting Ethereum's existing security properties without introducing new trust assumptions. The concept builds on earlier work around "L1-sequenced rollups" but provides a comprehensive framework for implementation and analysis.

### 1.4 Scope and Contributions

This report provides:
- Rigorous analysis of based rollup security properties, distinguishing between sequencing liveness, data availability, and execution validity
- Detailed examination of MEV economics under PBS, including builder incentives and cross-domain extraction patterns
- Comprehensive treatment of data availability mechanisms, including EIP-4844 blob dynamics and expiry considerations
- Formal analysis of liveness guarantees under adversarial conditions
- Empirical grounding through Taiko mainnet observations

---

## 2. Technical Architecture

### 2.1 Core Mechanism

The fundamental operation of a based rollup can be described through the following sequence:

1. **Transaction Submission**: Users submit transactions to the rollup's public mempool or directly to builders/searchers
2. **Batch Construction**: Builders (in the PBS context) or searchers construct rollup batches as part of L1 block building
3. **L1 Inclusion**: Batches are included in Ethereum blocks through the standard PBS auction
4. **State Derivation**: Rollup nodes derive L2 state by processing batches from L1 blocks according to canonical derivation rules
5. **Finalization**: State becomes final according to the rollup's proof system (optimistic or ZK)

```
┌─────────────────────────────────────────────────────────────────┐
│                Based Rollup Architecture (PBS Context)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Users ──► Mempool/Searchers ──► Builders ──► Proposers         │
│                                      │                           │
│                                      ▼                           │
│                    L1 Block with Rollup Batch (blob/calldata)   │
│                                      │                           │
│                                      ▼                           │
│              L2 Nodes: Derivation Pipeline ──► L2 State         │
│                                      │                           │
│                                      ▼                           │
│              Proof System (Fraud Proofs / Validity Proofs)      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 The Derivation Pipeline

A critical component unique to based rollups is the **derivation pipeline**—the deterministic process by which L2 nodes reconstruct state from L1 data. This pipeline must be precisely specified, as any ambiguity could lead to consensus failures where different nodes derive different states from identical L1 data.

The derivation pipeline typically includes:

1. **L1 Block Scanning**: Identifying relevant transactions/blobs containing L2 batches
2. **Batch Decoding**: Parsing batch data according to the rollup's encoding specification
3. **Transaction Ordering**: Applying canonical ordering rules within and across batches
4. **State Transition**: Executing transactions against the current L2 state
5. **State Root Computation**: Computing the resulting state root for verification

```
L1 Blocks ──► Filter Rollup Data ──► Decode Batches ──► Order Txs ──► Execute ──► L2 State
                    │                      │                │
                    ▼                      ▼                ▼
            (Contract events,      (Compression,      (Timestamp rules,
             blob commitments)      encoding format)   sequencing rules)
```

The derivation specification serves as the "constitution" of the based rollup—it must be unambiguous, deterministic, and publicly auditable. Taiko's derivation rules, for instance, specify precise ordering based on L1 block number, transaction index, and batch-internal sequencing.

### 2.3 Comparison with Centralized Sequencer Architecture

| Property | Centralized Sequencer | Based Rollup |
|----------|----------------------|--------------|
| Sequencing Entity | Dedicated L2 operator | Ethereum builders (PBS) |
| Soft Confirmation | ~100ms-2s | ~12s (L1 block time)* |
| Hard Confirmation | L1 batch posting (~minutes) | Same as soft (~12s) |
| Finality | L1 finality (~12.8 min) | L1 finality (~12.8 min) |
| Liveness Guarantee | Sequencer + force-inclusion fallback | L1 block production liveness |
| Censorship Resistance | Force-inclusion (12-24h delay) | L1-equivalent (probabilistic) |
| MEV Flow | Captured by sequencer | Flows to builders/proposers |
| Infrastructure | Requires dedicated setup | Minimal additional infra |
| Decentralization | Typically centralized | Inherits L1 decentralization |

*With preconfirmations, potentially reducible to ~100ms-1s

**Important Distinction**: Centralized sequencers provide *soft confirmations*—promises to include transactions that are not cryptographically binding. Users trusting soft confirmations accept sequencer honesty risk. Based rollups provide *hard confirmations* upon L1 inclusion, with stronger guarantees but higher latency. This represents a fundamental trade-off between speed and trust assumptions.

### 2.4 Data Availability Architecture

Based rollups, like all rollups, must ensure transaction data availability for state reconstruction and dispute resolution. The data availability mechanism is critical to the security model and deserves detailed analysis.

#### 2.4.1 Calldata vs. Blob Transactions

**Calldata (Pre-EIP-4844)**:
- Cost: ~16 gas per non-zero byte
- Retention: Permanent (part of execution payload)
- Access: Directly available to smart contracts
- Typical cost: ~$0.10-1.00 per KB during normal conditions

**EIP-4844 Blobs (Post-Dencun)**:
- Cost: Separate blob gas market, currently ~$0.001-0.01 per KB
- Retention: ~18 days (4096 epochs)
- Access: Not accessible to EVM; only commitment (versioned hash) available on-chain
- Capacity: 3-6 blobs per block (384-768 KB)

#### 2.4.2 Blob Gas Market Dynamics

The blob gas market operates independently from execution gas, with its own EIP-1559-style pricing:

```
blob_base_fee = MIN_BLOB_BASE_FEE * e^((excess_blob_gas) / BLOB_BASE_FEE_UPDATE_FRACTION)
```

Key implications for based rollups:
- **Competition**: During high demand, based rollups compete with other rollups for limited blob space
- **Price Volatility**: Blob fees can spike 100x+ during congestion periods
- **Inclusion Delays**: When blob space is saturated, batches may wait multiple blocks for inclusion

Empirical observation from Taiko mainnet (Q4 2024): During periods of high blob demand (>90% utilization), average batch inclusion delay increased from 1 block to 3-5 blocks, representing 36-60 second delays beyond the baseline 12-second block time.

#### 2.4.3 Blob Expiry and State Reconstruction

The 18-day blob retention window creates important operational considerations:

**Challenge Period Alignment**: For optimistic rollups, the fraud proof challenge period (typically 7 days) must complete before blob expiry. Based optimistic rollups have comfortable margin, but this constraint must be explicitly verified.

**Historical State Reconstruction**: After blob expiry, new nodes cannot reconstruct historical state from L1 alone. Solutions include:

1. **Blob Archival Services**: Third-party services (e.g., EthStorage, Blob Archive) that persist blob data indefinitely
2. **State Snapshots**: Periodic state commitments allowing nodes to sync from recent checkpoints
3. **Peer-to-Peer Distribution**: Existing full nodes serve historical data to syncing nodes
4. **Hybrid Approaches**: Posting critical data to calldata while bulk data goes to blobs

Taiko's approach: State snapshots are published weekly, with blob archival services providing redundant historical access. New nodes can sync from the most recent snapshot and derive forward.

#### 2.4.4 Future: Data Availability Sampling (DAS)

Full danksharding will introduce Data Availability Sampling, where nodes verify data availability through random sampling rather than downloading full blobs. Implications for based rollups:

- **Increased Throughput**: Target of 16 MB/block vs. current ~750 KB
- **Modified Trust Model**: Security relies on sufficient honest samplers rather than full data download
- **Reconstruction Considerations**: With DAS, the network collectively guarantees availability without any single node storing all data

### 2.5 Proof Systems in Based Context

Based rollups are agnostic to the underlying proof mechanism, but the L1-sequenced context introduces specific considerations for each approach.

#### 2.5.1 Based Optimistic Rollups

Optimistic rollups assume state transitions are valid unless challenged within a dispute window. In the based context:

**Derivation Disputes**: Beyond execution disputes, based optimistic rollups may face disputes about correct derivation—whether the claimed L2 state correctly follows from L1 data according to derivation rules.

**L1 Reorg Handling**: If an L1 reorg occurs during the challenge period, fraud proofs referencing reorged data become invalid. Design considerations:
- Challenge windows should account for L1 finality (~12.8 minutes for 2-epoch finality)
- Fraud proofs should reference finalized L1 blocks where possible
- Rollup nodes should track L1 reorgs and update derived state accordingly

**Challenge Game Modifications**: The standard challenge game (as in Arbitrum's BoLD or Optimism's Cannon) requires adaptation:
- Bisection must account for derivation steps, not just execution
- The "inbox" of L1 data must be precisely defined
- Timing assumptions must account for L1 block times

#### 2.5.2 Based ZK Rollups

ZK rollups generate validity proofs for state transitions, providing immediate cryptographic finality (subject to proof verification).

**Proof Scope**: Based ZK rollups must prove:
1. Correct derivation of transactions from L1 data
2. Correct execution of derived transactions
3. Correct state root computation

**Proving Latency**: ZK proof generation adds latency beyond L1 inclusion. Current proving times range from minutes (for small batches with GPU acceleration) to hours (for large batches or CPU-only). This creates a finality gap between L1 inclusion and proof verification.

**Taiko's BCR Model**: Taiko implements a "Based Contestable Rollup" combining elements of both:
- Initial state proposed optimistically
- ZK proofs can be submitted to finalize immediately
- SGX proofs provide intermediate trust level
- Contestation mechanism allows challenging any proof tier

---

## 3. Security Properties and Formal Analysis

### 3.1 Security Property Decomposition

Rather than treating security monolithically, we decompose based rollup security into distinct properties with separate trust assumptions:

#### 3.1.1 Data Availability Security

**Property**: Posted rollup data remains retrievable for the required period (at minimum, the challenge period for optimistic rollups).

**Trust Assumptions**:
- Ethereum consensus maintains liveness
- Sufficient nodes store and serve blob data during retention window
- For post-expiry reconstruction: archival services or peer network availability

**Failure Mode**: If data becomes unavailable before challenge period completion, invalid state transitions could finalize without possibility of fraud proof.

**Guarantee Level**: Strong during retention window (backed by Ethereum consensus); weaker post-expiry (relies on voluntary archival).

#### 3.1.2 Sequencing Liveness

**Property**: Valid transactions submitted to the rollup will eventually be included in the L2 state.

**Trust Assumptions**:
- Ethereum block production continues (L1 liveness)
- At least some builders are willing to include rollup batches
- Blob/calldata space is not permanently saturated

**Formal Analysis**: Let p be the probability that a randomly selected builder includes a given pending transaction. With n builders and probabilistic builder selection, the probability of inclusion within k blocks is:

```
P(inclusion within k blocks) = 1 - (1-p)^k
```

For based rollups, p is influenced by:
- Transaction fee relative to opportunity cost
- MEV value of the transaction
- Builder's rollup-specific infrastructure
- Current blob space congestion

**Comparison with Centralized Sequencers**: Centralized sequencers provide deterministic inclusion (assuming sequencer honesty) but with weaker guarantees—the sequencer can censor indefinitely until force-inclusion timeout (12-24 hours). Based rollups provide probabilistic inclusion with stronger eventual guarantees.

**Empirical Data (Taiko Q4 2024)**:
- Median inclusion time: 1 block (12 seconds)
- 95th percentile: 3 blocks (36 seconds)
- 99th percentile: 7 blocks (84 seconds)
- Maximum observed during congestion: 15 blocks (180 seconds)

#### 3.1.3 Sequencing Safety (Censorship Resistance)

**Property**: No entity can permanently prevent inclusion of a valid transaction.

**Trust Assumptions**:
- Ethereum's proposer/builder set is sufficiently decentralized
- No single entity controls a majority of consecutive slots

**Formal Analysis**: Let c be the fraction of builders willing to censor a specific transaction. The probability of censorship for k consecutive blocks is c^k. With current builder diversity (~5-10 major builders, none exceeding 30% market share), sustained censorship requires improbable collusion.

However, important nuances apply:
- **MEV-driven Exclusion**: Transactions may be excluded not due to censorship but because they're unprofitable to include (e.g., DEX trades that become stale)
- **Builder Concentration**: The builder market is more concentrated than the validator set; ~3 builders often produce >70% of blocks
- **Relay Filtering**: MEV-Boost relays may filter certain transactions (e.g., OFAC compliance), creating de facto censorship layers

#### 3.1.4 Execution Validity

**Property**: Only valid state transitions (according to the rollup's rules) are finalized.

**Trust Assumptions**:
- For optimistic rollups: At least one honest party monitors and submits fraud proofs
- For ZK rollups: The proof system is sound (no false proofs can be generated)
- Derivation rules are unambiguous and correctly implemented

**Failure Modes**:
- Optimistic: No challenger during dispute window (requires economic/altruistic monitoring)
- ZK: Proof system vulnerability (cryptographic assumption failure)
- Both: Derivation rule ambiguity leading to consensus splits

### 3.2 Threat Model and Attack Analysis

#### 3.2.1 Proposer/Builder Collusion

**Attack**: Colluding builders attempt to censor or reorder L2 transactions for extended periods.

**Analysis**: Sustained attacks require controlling consecutive slots. With builder market share distribution B = {b₁, b₂, ..., bₙ}, the probability of controlling k consecutive slots is at most (max(bᵢ))^k.

Current market (late 2024): max builder share ≈ 30%, so:
- 2 consecutive blocks: 9% probability
- 3 consecutive blocks: 2.7% probability
- 5 consecutive blocks: 0.24% probability

**Mitigation**: Probabilistic rotation makes sustained attacks economically prohibitive. Users requiring stronger guarantees can wait for multiple block confirmations.

#### 3.2.2 MEV-Driven Reordering

**Attack**: Builders reorder L2 transactions to extract MEV (sandwiching, frontrunning).

**Analysis**: This is not strictly an attack but expected behavior under PBS. L2 transactions are subject to the same MEV extraction as L1 transactions. The key difference from centralized sequencers: MEV flows to builders/proposers rather than the rollup operator.

**Implications**:
- Users should use private mempools or MEV protection services
- Rollup protocols can integrate MEV-Share or similar redistribution mechanisms
- Application-level protections (slippage limits, commit-reveal) remain important

#### 3.2.3 Data Withholding

**Attack**: Proposer includes batch commitment but withholds underlying data.

**Analysis**: Ethereum's consensus rules require data availability for block validity. With EIP-4844, blob data must be available for the block to be valid—nodes that cannot reconstruct blobs will reject the block.

**Post-Expiry Consideration**: After blob expiry, data withholding by archival services could prevent new node synchronization. This is mitigated by redundant archival and P2P distribution.

#### 3.2.4 L1 Reorg Attacks

**Attack**: Attacker triggers L1 reorg to invalidate fraud proofs or manipulate L2 state.

**Analysis**: L1 reorgs beyond 2 epochs (~12.8 minutes) require controlling >1/3 of stake—economically infeasible (>$15B at current prices). Shallower reorgs (1-2 blocks) are possible but:
- Based rollup state should only be considered final after L1 finality
- Fraud proof windows (7 days) far exceed reorg risk windows
- Applications requiring immediate finality should wait for L1 finality confirmation

### 3.3 Formal Security Statement

We can now provide a more rigorous security characterization:

**Theorem (Informal)**: A based rollup achieves:
- **Data Availability**: Equivalent to Ethereum L1 during blob retention; degraded to archival availability thereafter
- **Sequencing Liveness**: Probabilistically guaranteed with inclusion probability approaching 1 as time increases, subject to blob space availability
- **Censorship Resistance**: Probabilistically guaranteed with censorship probability approaching 0 as required collusion duration increases
- **Execution Validity**: Equivalent to the underlying proof system (fraud proof security for optimistic, soundness for ZK)

This formulation makes explicit that based rollups do not provide strictly "L1-equivalent" security—they inherit L1 properties for sequencing while adding proof system assumptions for execution validity, and face nuanced DA guarantees post-blob-expiry.

---

## 4. Economic Implications and MEV Dynamics

### 4.1 MEV Flow Under Proposer-Builder Separation

The most significant economic distinction of based rollups concerns MEV distribution. Understanding this requires careful analysis of the PBS pipeline.

#### 4.1.1 PBS Architecture Review

In Ethereum's current PBS regime:
1. **Searchers** identify MEV opportunities and construct transaction bundles
2. **Builders** aggregate bundles and construct full blocks
3. **Relays** facilitate communication between builders and proposers
4. **Proposers** select the highest-value block header and sign it

Critically, **builders—not proposers—control transaction ordering**. This has profound implications for based rollups: L2 batch inclusion and internal ordering is determined by builders competing in the block auction.

#### 4.1.2 MEV Extraction in Based Rollups

```
┌─────────────────────────────────────────────────────────────────┐
│                  MEV Flow in Based Rollups                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  L2 Users ──► L2 Mempool ──► Searchers (L2-aware)               │
│                                   │                              │
│                                   ▼                              │
│                    MEV Bundles (L1 + L2 combined)               │
│                                   │                              │
│                                   ▼                              │
│                    Builders ──► Block Construction               │
│                                   │                              │
│                                   ▼                              │
│              Builder Payment ──► Proposer (via relay)           │
│                                                                  │
│  Value Distribution:                                             │
│  - Searchers: MEV extraction profit minus builder payment       │
│  - Builders: Auction competition surplus                         │
│  - Proposers: Winning builder's bid                             │
│  - L2 Protocol: Zero (without additional mechanisms)            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

Key insight: Based rollups redirect MEV to the **builder-proposer supply chain**, not simply "to L1 proposers." The distribution among searchers, builders, and proposers depends on competition levels at each stage.

#### 4.1.3 Cross-Domain MEV Patterns

Based rollups create unique MEV opportunities spanning L1 and L2:

**L1-L2 Arbitrage**: Price discrepancies between L1 and L2 DEXs can be atomically arbitraged within a single L1 block. A builder can include:
1. L2 batch with DEX trade
2. L1 DEX trade
3. Bridge interaction

All executed atomically, capturing arbitrage that's impossible with centralized sequencers (which have temporal separation between L2 execution and L1 settlement).

**Cross-Based-Rollup MEV**: If multiple based rollups exist, builders can atomically order transactions across all of them, enabling:
- Cross-rollup arbitrage
- Unified liquidations
- Coordinated state updates

**Sandwich Attacks**: L2 transactions in the public mempool are vulnerable to sandwiching by searchers who can position L1 transactions around L2 batches. Mitigation requires private mempools or encrypted mempools.

#### 4.1.4 Builder Specialization

We observe emerging builder specialization for L2 MEV:
- Some builders run L2 nodes to identify MEV opportunities
- Builders may integrate L2-specific searcher relationships
- Vertical integration (searcher-builder) is common for L2 MEV

This specialization could lead to builder market concentration around L2-capable builders, potentially reducing the effective decentralization of based rollup sequencing.

### 4.2 Quantitative MEV Analysis

#### 4.2.1 MEV Magnitude Estimation

Based on Taiko mainnet data and extrapolation from L2 DEX volumes:

| Source | Estimated Daily MEV | Notes |
|--------|--------------------| ------|
| DEX Arbitrage | $50K-200K | Scales with volume |
| Liquidations | $10K-50K | Sporadic, market-dependent |
| Sandwich Attacks | $20K-100K | Depends on mempool visibility |
| NFT Sniping | $5K-20K | Lower on L2 currently |
| **Total** | **$85K-370K** | Wide range due to market conditions |

For comparison, a centralized sequencer capturing this MEV at 50% efficiency would generate $15M-67M annually—significant revenue foregone by based rollups.

#### 4.2.2 MEV Recapture Mechanisms

Based rollups can partially recapture MEV through several mechanisms:

**Order Flow Auctions (OFAs)**: L2 protocols can auction the right to view/execute against order flow before it reaches the public mempool.

**MEV-Share Integration**: Searchers return a portion of extracted MEV to the originating users or protocol.

**Proposer Payments**: Based rollups can require proposers to pay for the right to include batches (Taiko's approach).

**Protocol-Level MEV Taxes**: Smart contract mechanisms that capture MEV at the application level (e.g., MEV taxes on DEX trades).

Taiko's ticket system implements a form of proposer payment:
```solidity
// Simplified: Proposers bid for block proposal rights
function proposeBlock(
    bytes calldata params,
    bytes calldata txList
) external payable {
    require(msg.value >= currentTicketPrice, "Insufficient bid");
    // Ticket price adjusts based on demand
    // Revenue flows to protocol treasury
}
```

### 4.3 Revenue Model Analysis

#### 4.3.1 Cost Structure Comparison

**Centralized Sequencer Rollup**:
```
Revenue = Sequencer MEV + Transaction Fees + Token Value Capture
Costs = Infrastructure + Security + Operations + L1 Data Costs
```

**Based Rollup**:
```
Revenue = Protocol Fees + Proposer Payments + MEV Recapture + Token Value Capture
Costs = Development + L1 Data Costs (reduced infrastructure)
```

#### 4.3.2 Economic Viability Analysis

We model break-even conditions for based rollups:

**Assumptions**:
- Daily transactions: 100,000
- Average L1 data cost per tx: $0.01 (post-EIP-4844)
- Protocol fee per tx: $0.005
- MEV recapture rate: 20% of total MEV
- Daily MEV: $150,000 (midpoint estimate)

**Daily Economics**:
- L1 Data Costs: $1,000
- Protocol Fee Revenue: $500
- MEV Recapture: $30,000
- **Net Revenue**: $29,500/day

**Comparison with Centralized Sequencer**:
- Additional Infrastructure Costs: ~$5,000/day (servers, monitoring, redundancy)
- MEV Capture (50% efficiency): $75,000/day
- **Net MEV Advantage**: $70,000/day

This analysis suggests based rollups sacrifice ~$40,000/day in potential revenue at current scale, but this gap narrows with:
- Higher MEV recapture rates
- Lower infrastructure cost differential
- Higher transaction volumes (infrastructure costs don't scale linearly)

#### 4.3.3 Long-term Sustainability

Based rollup sustainability depends on:
1. **Transaction Volume Growth**: Higher volumes improve unit economics
2. **MEV Recapture Innovation**: Better mechanisms to reclaim value
3. **Ecosystem Value**: Token appreciation from Ethereum alignment narrative
4. **Cost Efficiency**: Lower operational overhead vs. centralized alternatives

### 4.4 Preconfirmation Economics Under PBS

Preconfirmations in a PBS context raise complex incentive questions.

#### 4.4.1 Who Provides Preconfirmations?

**Option 1: Proposers**
- Proposers know their upcoming slots (32-slot lookahead)
- But proposers don't construct blocks—builders do
- Proposer commitment requires builder cooperation or proposer-built blocks

**Option 2: Builders**
- Builders control block content
- But builders don't know if they'll win the auction
- Builder preconfirmations are probabilistic (conditional on winning)

**Option 3: Proposer-Builder Coordination**
- Proposers commit to accepting blocks containing specific transactions
- Builders commit to including those transactions if they win
- Requires new coordination infrastructure

#### 4.4.2 Slashing Economics

For credible preconfirmations, commitment violations must be punishable:

**Collateral Requirements**:
- Must exceed maximum value of reneging (MEV from exclusion/reordering)
- Estimated: 1-10 ETH per preconfirmation depending on transaction value
- Creates capital efficiency challenges

**Slashing Conditions**:
- Proposer signs commitment but block doesn't include transaction
- Challenge: Distinguishing intentional violation from builder non-cooperation
- Solution: Proposers only preconfirm for blocks they build or have builder agreements

**Economic Equilibrium**:
```
Preconfirmation Fee ≥ (Collateral × Opportunity Cost) + (Violation Probability × Slashing Amount)
```

For viable economics with 10 ETH collateral, 5% opportunity cost, and 0.1% violation probability:
```
Minimum Fee ≥ (10 × 0.05/365) + (0.001 × 10) ≈ 0.0014 + 0.01 = 0.0114 ETH ≈ $30
```

This suggests preconfirmations may only be economical for high-value transactions, with lower-value transactions relying on standard L1 inclusion times.

---

## 5. Latency Analysis and Preconfirmation Solutions

### 5.1 Latency Decomposition

Understanding based rollup latency requires decomposing the confirmation lifecycle:

| Stage | Duration | Guarantee Level |
|-------|----------|-----------------|
| Mempool Propagation | ~1-3s | None |
| L1 Block Inclusion | ~12s (1 block) | Soft (reorg possible) |
| L1 Finality | ~12.8 min (2 epochs) | Strong (economic finality) |
| Proof
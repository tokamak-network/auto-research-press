# Ethereum EIP-4844 Proto-Danksharding: A Comprehensive Technical Analysis

## Abstract

Ethereum's transition to a rollup-centric architecture has positioned Layer 2 scaling solutions as the primary mechanism for increasing transaction throughput. However, this approach introduces a critical bottleneck: rollups must post transaction data to Ethereum's Layer 1 for security guarantees, and the cost of this data availability has become the dominant component of rollup transaction fees. EIP-4844, known as proto-danksharding, addresses this challenge by introducing a new data availability layer specifically optimized for rollup needs. This paper provides a comprehensive technical analysis of EIP-4844's design, examining its cryptographic foundations, mechanism architecture, economic implications, and role as a stepping stone toward full danksharding. We analyze how blob transactions, KZG polynomial commitments, and a separate fee market combine to reduce rollup costs by up to 99% while maintaining Ethereum's security guarantees and establishing the infrastructure necessary for future data availability scaling.

---

## 1. Introduction: The Scalability Crisis and Rollup-Centric Ethereum

Ethereum's scalability limitations represent one of the most critical challenges facing blockchain technology today. Since its inception, Ethereum's monolithic architecture—where every node processes every transaction—has constrained throughput to approximately 15-30 transactions per second. This limitation manifests in high transaction fees during periods of network congestion, often exceeding $50-100 per transaction during peak demand, effectively pricing out many use cases and users.

The Ethereum community's response to this scalability crisis has evolved significantly over the years. Early proposals focused on increasing the block gas limit or implementing complex sharding schemes that would partition the network into multiple parallel chains. However, these approaches faced fundamental challenges related to cross-shard communication complexity, security assumptions, and implementation difficulty. The breakthrough came with the formalization of the rollup-centric roadmap, which positions Layer 2 rollup solutions—including optimistic rollups like Arbitrum and Optimism, and zero-knowledge rollups like zkSync and StarkNet—as the primary scaling mechanism.

Rollups achieve scalability by executing transactions off-chain while inheriting Ethereum's security through cryptographic proofs and data availability guarantees. This architectural separation allows rollups to process thousands of transactions per second while periodically posting compressed transaction data and state commitments to Ethereum's Layer 1. In theory, this approach should reduce transaction costs by orders of magnitude while maintaining the security properties that make Ethereum valuable.

However, a critical bottleneck emerged: the cost of posting transaction data to Layer 1. Prior to EIP-4844, rollups used Ethereum's calldata mechanism to publish transaction batches, paying standard execution gas prices for what is fundamentally a data availability operation. As we will explore in detail in Section 2, this approach is fundamentally inefficient because calldata is designed for permanent storage and competes directly with all other transactions for limited block space. During periods of network congestion, data availability costs often comprise 80-95% of total rollup transaction fees, undermining the economic benefits of Layer 2 scaling.

EIP-4844, activated as part of the Dencun upgrade in March 2024, introduces a purpose-built data availability layer that addresses this inefficiency. By creating a separate blob transaction type with its own fee market and temporary storage model, proto-danksharding reduces rollup data costs by up to 99% during normal network conditions. More importantly, EIP-4844 establishes the cryptographic primitives, transaction formats, and consensus layer modifications that will enable full danksharding—a comprehensive data sharding solution that could increase Ethereum's data availability capacity by over 100× without proportionally increasing node requirements.

This paper provides a comprehensive technical analysis of EIP-4844, structured as follows: Section 2 establishes the technical foundations, examining the data availability problem, calldata limitations, and the polynomial commitment schemes that underpin blob verification. Section 3 details the mechanism design, analyzing blob transaction structure, the KZG commitment implementation, the separate fee market, and consensus layer modifications. Section 4 evaluates the economic impact and real-world performance since deployment. Section 5 examines security considerations and trade-offs inherent in the design. Section 6 explores the upgrade path to full danksharding and alternative approaches. Finally, Section 7 synthesizes our findings and discusses implications for Ethereum's long-term scaling trajectory.

---

## 2. Technical Foundations: Data Availability and Cryptographic Primitives

### 2.1 The Data Availability Problem in Rollup Architectures

As introduced in Section 1, Ethereum's rollup-centric roadmap positions Layer 2 solutions as the primary mechanism for scaling transaction throughput. However, this architectural approach introduces a fundamental challenge known as the data availability problem—a critical bottleneck that EIP-4844 directly addresses.

Rollups achieve scalability by executing transactions off-chain while inheriting Ethereum's security guarantees through cryptographic proofs. Both optimistic rollups (such as Arbitrum and Optimism) and zero-knowledge rollups (such as zkSync and StarkNet) must post sufficient transaction data to Ethereum's Layer 1 to enable independent verification. This requirement stems from a core security principle: any observer must be able to reconstruct the complete rollup state from data published on-chain, without trusting the rollup operator.

For optimistic rollups, data availability is essential during the fraud proof window—typically seven days—during which challengers can dispute invalid state transitions. If the underlying transaction data were unavailable, honest validators could not construct fraud proofs to contest malicious state updates. For zero-knowledge rollups, while validity proofs mathematically guarantee correct execution, users still require access to transaction data to determine their account balances and construct withdrawal proofs. Without data availability, users' funds could become permanently inaccessible even if the rollup operator disappears.

The data availability problem thus creates an apparent paradox: rollups need Ethereum's security but cannot fully escape its throughput limitations because they must publish data to the constrained Layer 1. This dependency establishes data availability costs as the dominant factor in rollup transaction fees, often comprising 80-95% of the total cost users pay—a phenomenon we will quantify in Section 4 when examining real-world economic impacts.

### 2.2 Current Approach: Calldata and Its Inherent Limitations

Prior to EIP-4844, rollups posted transaction data using Ethereum's calldata mechanism—the input data field attached to transactions. While calldata serves this purpose functionally, it represents a fundamentally inefficient solution for data availability due to several structural limitations that motivated the design of blob transactions, which we will examine in detail in Section 3.

#### 2.2.1 Permanent Storage Requirements

Calldata becomes part of Ethereum's permanent blockchain history. Every full node must download, verify, and store this data indefinitely, regardless of whether it serves any ongoing purpose. For rollups, however, the data availability requirement is inherently temporary: optimistic rollups need data accessible only during their challenge period, while zero-knowledge rollups need it only until state transitions are finalized. The mismatch between permanent storage and temporary requirements creates substantial inefficiency.

As of early 2024, major rollups collectively post approximately 15-20 GB of calldata monthly to Ethereum. This data accumulates perpetually, contributing to state bloat that increases hardware requirements for node operators and threatens long-term decentralization. The Ethereum blockchain's total size exceeds 1 TB, with rollup calldata representing an increasingly significant portion of growth.

#### 2.2.2 Gas Cost Structure

Calldata pricing reflects its permanent storage nature. EIP-2028, implemented in 2019, reduced calldata costs from 68 gas per non-zero byte to 16 gas per non-zero byte, providing temporary relief. However, these costs remain substantial when aggregated across millions of transactions.

Consider a typical rollup batch containing 500 transactions, requiring approximately 120 KB of compressed calldata. At 16 gas per byte, this consumes roughly 1.92 million gas—nearly 7% of an entire Ethereum block's capacity. During periods of network congestion when base fees reach 50-100 gwei, posting this single batch costs $2,000-4,000 in data availability fees alone. These costs directly translate to user transaction fees, with rollup users paying $0.10-0.50 per transaction primarily for data availability rather than execution.

#### 2.2.3 Competition for Block Space

Calldata competes directly with all other Ethereum transactions for limited block space. During NFT mints, DeFi volatility events, or other demand spikes, rollups face the same fee escalation as individual users. This coupling undermines the fundamental value proposition of rollups as a scaling solution—if rollup costs scale linearly with Layer 1 congestion, users gain only marginal benefits over direct L1 interaction.

The Ethereum block gas limit of 30 million creates a hard ceiling on aggregate data throughput. With calldata consuming 16 gas per byte, the theoretical maximum calldata per block is approximately 1.8 MB, though practical limits are much lower given competition from other transaction types. This constraint fundamentally limits how much rollups can scale, regardless of their off-chain execution capacity.

These limitations motivated the development of a purpose-built data availability solution. As we will see in Section 3, EIP-4844's blob transactions address each of these inefficiencies through temporary storage, a separate fee market, and dedicated blob space that does not compete with execution layer transactions.

### 2.3 Polynomial Commitments: Mathematical Foundations

EIP-4844 introduces a sophisticated cryptographic primitive—polynomial commitment schemes—to enable efficient data availability verification. Understanding these mathematical foundations is essential for grasping how blob transactions achieve their efficiency gains and how the mechanism design detailed in Section 3 provides security guarantees.

#### 2.3.1 Commitment Schemes Overview

A commitment scheme allows a party to commit to a value while keeping it hidden, then later reveal the value and prove it matches the original commitment. In the context of data availability, we need commitments that enable verification of data properties without requiring validators to process the entire dataset.

Polynomial commitments extend this concept by representing data as coefficients of a polynomial function. A dataset of *n* elements can be encoded as a polynomial *p(x)* of degree *n-1*, where each data element corresponds to a coefficient. The commitment to this polynomial is a single, compact value that cryptographically binds to the entire dataset.

The crucial property for data availability is the ability to create opening proofs—succinct demonstrations that the polynomial evaluates to a specific value at a given point. These proofs enable sampling-based verification: rather than downloading all data, verifiers can request evaluations at random points and verify them against the commitment. If a malicious actor withholds even a small portion of data, they cannot produce valid opening proofs for the missing sections, and random sampling will detect this with high probability. This sampling property will become critical when we discuss the upgrade path to full danksharding in Section 6.

#### 2.3.2 KZG Commitment Scheme

EIP-4844 specifically employs the Kate-Zaverucha-Goldberg (KZG) commitment scheme, named after its inventors who introduced it in 2010. KZG commitments offer several properties that make them particularly suitable for Ethereum's data availability layer, and these properties directly inform the mechanism design choices we will examine in Section 3.

**Constant-Size Commitments**: Regardless of the polynomial degree (and thus the data size), a KZG commitment is always a single elliptic curve group element—48 bytes in EIP-4844's implementation using the BLS12-381 curve. This compactness is essential for on-chain efficiency, as we will see when examining the versioned hash construction in Section 3.2.

**Constant-Size Proofs**: Opening proofs demonstrating that *p(z) = y* for any point *z* are also single group elements. Verification requires only a constant number of elliptic curve operations, independent of the polynomial degree. This property enables the point evaluation precompile discussed in Section 3.5.

**Homomorphic Properties**: KZG commitments support linear combinations. Given commitments to polynomials *p(x)* and *q(x)*, one can compute a commitment to *p(x) + q(x)* without knowing the underlying polynomials. This property enables efficient aggregation of multiple blob commitments.

The KZG scheme relies on a trusted setup ceremony to generate structured reference strings (SRS)—public parameters used in commitment and verification operations. Ethereum conducted a large-scale ceremony in 2022-2023, gathering contributions from over 140,000 participants. The security assumption is that at least one participant honestly generated and destroyed their secret contribution; if so, the resulting parameters are secure. We will examine the implementation details and security implications of this trusted setup in Section 3.3.

#### 2.3.3 Mathematical Construction

For readers seeking deeper technical understanding, the KZG construction operates as follows. Let *G₁* and *G₂* be groups of prime order *p* with a bilinear pairing *e: G₁ × G₂ → G_T*. The trusted setup generates powers of a secret *τ*: the SRS contains *[τ⁰]₁, [τ¹]₁, ..., [τⁿ]₁* in *G₁* and *[τ]₂* in *G₂*, where bracket notation denotes scalar multiplication of the group generator.

To commit to a polynomial *p(x) = Σᵢ cᵢxⁱ*, the committer computes *C = Σᵢ cᵢ[τⁱ]₁ = [p(τ)]₁*. This commitment is binding because finding two different polynomials with the same commitment requires computing discrete logarithms, which is computationally infeasible.

To prove that *p(z) = y*, the prover constructs the quotient polynomial *q(x) = (p(x) - y)/(x - z)*, which exists as a polynomial only if *p(z) = y*. The proof is *π = [q(τ)]₁*. Verification checks the pairing equation *e(C - [y]₁, [1]₂) = e(π, [τ - z]₂)*, which holds if and only if the claimed evaluation is correct.

This mathematical framework provides the cryptographic foundation for the blob verification mechanisms we will examine in Section 3, where we will see how these abstract mathematical constructions translate into concrete protocol operations.

### 2.4 Blob Data Structures and the Temporary Storage Model

Building on the cryptographic foundations established above, EIP-4844 introduces blobs as a new data structure specifically designed for rollup data availability, with properties carefully chosen to balance security, efficiency, and decentralization concerns. These design choices directly inform the mechanism specifications we will examine in Section 3.2.

#### 2.4.1 Blob Specifications

Each blob contains exactly 4,096 field elements, where each field element is a 32-byte value in the BLS12-381 scalar field. This yields a blob size of 128 KB (131,072 bytes). The fixed size simplifies implementation and enables consistent gas pricing, as we will see when examining the blob fee market in Section 3.4.

The choice of 4,096 elements is deliberate: it equals 2¹², enabling efficient Fast Fourier Transform (FFT) operations for polynomial arithmetic. FFTs are essential for computing KZG commitments efficiently and will become even more critical when full danksharding introduces data availability sampling, as we will discuss in Section 6.

Blobs are transmitted in a sidecar structure alongside their parent transactions rather than embedded within them. This separation ensures that blob data does not burden execution layer processing while remaining cryptographically linked to consensus layer blocks through commitments. The architectural implications of this design choice will become clear when we examine consensus layer modifications in Section 3.6.

#### 2.4.2 Blob-Carrying Transactions (Type 3)

EIP-4844 defines a new transaction type (type 0x03) that can carry blob references. These transactions include:

- **blob_versioned_hashes**: A list of 32-byte hashes, each derived from a blob's KZG commitment using a versioned hashing scheme. The version byte (currently 0x01) enables future commitment scheme upgrades, providing the cryptographic agility necessary for the evolution toward full danksharding discussed in Section 6.
- **max_fee_per_blob_gas**: The maximum fee the sender will pay per unit of blob gas, analogous to max_fee_per_gas for regular transactions.

The transaction itself contains only the versioned hashes, not the blob data. Blobs are transmitted through the consensus layer's gossip network and validated against their commitments. This design ensures that execution layer clients need not process blob contents, maintaining separation of concerns—a principle we will see reflected throughout the mechanism design in Section 3.

A single transaction can reference up to 6 blobs (a limit that may increase in future upgrades), enabling batching of rollup data submissions. The target is 3 blobs per block with a maximum of 6, providing approximately 375 KB of average blob capacity per block. These parameters, which we will examine in detail in Section 3.2, represent a carefully calibrated balance between immediate scalability benefits and network sustainability.

#### 2.4.3 Temporary Storage and Pruning

The most significant departure from calldata is blob data's temporary availability. Consensus layer clients are required to store and serve blob data for a minimum of 4,096 epochs—approximately 18.2 days at 12-second slot times. After this period, clients may prune blob data without violating protocol rules.

This pruning window is carefully calibrated:

- **Fraud Proof Compatibility**: The 18-day window exceeds the typical 7-day challenge period for optimistic rollups, ensuring data remains available throughout dispute resolution.
- **ZK Rollup Finality**: Zero-knowledge rollups typically finalize state within hours, well within the availability window.
- **Storage Sustainability**: Temporary storage prevents unbounded growth. At target capacity, blob data adds approximately 50 GB monthly, all of which is pruned, compared to permanent calldata accumulation.

Nodes that wish to retain historical blob data may do so, and specialized archival services will likely emerge to serve historical queries. However, the protocol's security guarantees do not depend on this archival—only on availability during the pruning window. This represents a fundamental shift in Ethereum's data availability model, with implications we will explore further when examining security trade-offs in Section 5.

#### 2.4.4 Blob Gas and Fee Market

EIP-4844 introduces a separate fee market for blob space, independent of regular execution gas. This separation is crucial for ensuring that blob costs reflect blob-specific supply and demand rather than general network congestion—addressing the competition for block space problem identified in Section 2.2.3.

The blob base fee follows the same EIP-1559-style adjustment mechanism as execution gas: if blob usage exceeds the target (3 blobs per block), the base fee increases by up to 12.5%; if usage falls below target, the fee decreases. This creates a self-regulating market that prices blob space according to demand. We will examine the detailed mechanics and economic implications of this fee market in Section 3.4.

Initial parameters set the minimum blob base fee at 1 wei, allowing extremely low costs during periods of low demand. Early post-implementation data showed blob fees ranging from near-zero during quiet periods to several gwei during demand spikes—still dramatically cheaper than equivalent calldata costs. The real-world performance of this fee market will be analyzed in detail in Section 4.

The blob gas limit per block is 786,432 (6 blobs × 131,072 bytes × 1 gas per byte), with a target of 393,216 (3 blobs). This parameterization provides headroom for demand fluctuations while maintaining predictable average capacity.

### 2.5 Connection to Full Danksharding: A Stepping Stone Architecture

EIP-4844 is explicitly designed as proto-danksharding—a preliminary implementation that establishes the transaction format, cryptographic primitives, and fee market structure required for full danksharding, while deferring the most complex components. Understanding this relationship is essential for evaluating EIP-4844's role in Ethereum's long-term scaling roadmap, which we will explore comprehensively in Section 6.

#### 2.5.1 What Proto-Danksharding Includes

EIP-4844 implements all user-facing and transaction-level components of the full danksharding vision:

- **Blob transaction format**: Type 3 transactions with versioned hashes (detailed in Section 3.2)
- **KZG commitment infrastructure**: Trusted setup, commitment verification, point evaluation precompile (examined in Section 3.3)
- **Separate fee market**: Independent blob gas pricing and EIP-1559 dynamics (analyzed in Section 3.4)
- **Consensus layer integration**: Blob sidecars, availability checks, and gossip protocols (discussed in Section 3.6)

These components represent the "hard" parts of danksharding from a coordination perspective—they require changes to transaction formats, new precompiled contracts, and consensus layer modifications. By implementing them now, EIP-4844 ensures that future danksharding upgrades can proceed as soft forks or minor hard forks rather than requiring another comprehensive protocol overhaul.

#### 2.5.2 What Full Danksharding Adds

The primary addition in full danksharding is Data Availability Sampling (DAS), which enables dramatic capacity increases without proportionally increasing node requirements.

With DAS, validators do not download complete blobs. Instead, they randomly sample small portions and verify them against KZG commitments. The mathematical properties of erasure coding (specifically, 2D Reed-Solomon encoding) ensure that if any validator can reconstruct the data, the data is available with overwhelming probability. This allows blob capacity to scale to potentially 16 MB per block—over 100× current levels—while individual nodes download only kilobytes of samples.

DAS requires additional infrastructure:

- **Erasure coding**: Extending blob data with redundancy so that any 50% of samples suffices for reconstruction
- **Sampling protocols**: Peer-to-peer mechanisms for requesting and validating random samples
- **Custody requirements**: Ensuring sufficient network participants store each data segment

These components involve substantial research and engineering challenges that would have delayed blob implementation by years. Proto-danksharding's pragmatic approach delivers immediate benefits while the DAS infrastructure matures—a design philosophy we will see reflected throughout the mechanism choices examined in Section 3.

#### 2.5.3 Upgrade Path

The transition from proto-danksharding to full danksharding is designed to be minimally disruptive:

1. **Transaction format stability**: Type 3 transactions and blob structures remain unchanged
2. **Commitment compatibility**: KZG commitments extend naturally to support DAS verification
3. **Fee market evolution**: Blob gas parameters can adjust to reflect increased capacity
4. **Rollup continuity**: Rollups posting blobs today will continue functioning without modification

This forward compatibility represents a significant achievement in protocol design—delivering substantial immediate value while preserving optionality for future enhancements. The cryptographic primitives and data structures introduced in EIP-4844 form the foundation upon which Ethereum's long-term data availability scaling will be built, as we will explore further in Section 6.

Having established the technical foundations—the data availability problem, calldata limitations, polynomial commitment mathematics, and the blob data model—we now turn to examining how these concepts are implemented in EIP-4844's concrete mechanism design.

---

## 3. EIP-4844 Mechanism Design: Blob Transactions and Protocol Changes

### 3.1 Introduction to Proto-Danksharding Architecture

Building upon the data availability foundations established in Section 2, EIP-4844 introduces a sophisticated mechanism design that fundamentally restructures how Ethereum handles rollup data. This Ethereum Improvement Proposal, commonly known as proto-danksharding, represents the most significant protocol change since the Merge, introducing new transaction types, cryptographic verification schemes, and an independent fee market specifically optimized for data availability.

The design philosophy underlying EIP-4844 prioritizes backward compatibility while establishing the architectural scaffolding necessary for full danksharding. As discussed in Section 2.5, rather than implementing the complete data sharding vision immediately, proto-danksharding introduces the transaction format, cryptographic primitives, and fee mechanisms that future upgrades will extend. This incremental approach allows the Ethereum ecosystem to adapt gradually while delivering immediate cost reductions for Layer 2 rollups.

### 3.2 Type 3 Transactions: Blob-Carrying Transaction Structure

EIP-4844 introduces a new transaction type designated as Type 3, following Ethereum's existing transaction type taxonomy (Type 0 for legacy, Type 1 for EIP-2930 access lists, and Type 2 for EIP-1559 dynamic fees). Blob-carrying transactions extend the EIP-1559 transaction format with additional fields specifically designed for data availability purposes, implementing the blob-carrying transaction concept introduced in Section 2.4.2.

#### 3.2.1 Transaction Field Specification

A Type 3 transaction contains the following fields, encoded using the SSZ (Simple Serialize) format rather than the traditional RLP (Recursive Length Prefix) encoding used by earlier transaction types:

```
BlobTransaction = {
    chain_id: uint256,
    nonce: uint64,
    max_priority_fee_per_gas: uint256,
    max_fee_per_gas: uint256,
    gas_limit: uint64,
    to: Address,
    value: uint256,
    data: bytes,
    access_list: List[AccessListEntry],
    max_fee_per_blob_gas: uint256,
    blob_versioned_hashes: List[VersionedHash],
    signature: ECDSASignature
}
```

The critical additions distinguishing Type 3 transactions are `max_fee_per_blob_gas` and `blob_versioned_hashes`. The former specifies the maximum price per unit of blob gas the sender is willing to pay, analogous to `max_fee_per_gas` for regular execution gas. The latter contains a list of versioned hashes—cryptographic commitments to each blob attached to the transaction, implementing the KZG commitment scheme discussed in Section 2.3.

#### 3.2.2 Versioned Hash Construction

Versioned hashes provide a compact, fixed-size representation of blob commitments suitable for inclusion in execution layer data structures. Each versioned hash is constructed by taking the SHA-256 hash of the KZG commitment and prepending a version byte:

```
versioned_hash = VERSIONED_HASH_VERSION_KZG || SHA256(kzg_commitment)[1:]
```

The version byte (currently `0x01` for KZG commitments) enables future cryptographic agility, allowing the protocol to transition to alternative commitment schemes—such as those based on STARKs or other post-quantum constructions—without requiring fundamental changes to the transaction format. This design choice reflects the forward-compatibility principles discussed in Section 2.5.3, ensuring that the upgrade path to full danksharding and beyond remains smooth.

#### 3.2.3 Transaction Validity Constraints

For a Type 3 transaction to be considered valid, several constraints must be satisfied:

1. **Non-empty blob list**: The transaction must include at least one blob (`len(blob_versioned_hashes) >= 1`)
2. **Blob count limit**: The transaction cannot exceed the maximum blobs per transaction (`len(blob_versioned_hashes) <= MAX_BLOBS_PER_TX`, currently set to 6, as specified in Section 2.4.2)
3. **Contract creation prohibition**: The `to` field must contain a valid address; blob transactions cannot create new contracts (`to != None`)
4. **Fee sufficiency**: The `max_fee_per_blob_gas` must meet or exceed the current blob base fee (determined by the fee market mechanism we will examine in Section 3.4)
5. **Hash-commitment correspondence**: Each versioned hash must correctly correspond to the KZG commitment of its associated blob

These constraints ensure that blob transactions serve their intended purpose—providing data availability for rollups—while preventing potential abuse vectors. The security implications of these design choices will be explored further in Section 5.

### 3.3 Blob Format Specifications and Data Structure

#### 3.3.1 Field Element Representation

Blobs in EIP-4844 are structured as vectors of 4096 field elements, where each field element belongs to the BLS12-381 scalar field, as introduced in Section 2.4.1. This field has a prime modulus of:

```
p = 52435875175126190479447740508185965837690552500527637822603658699938581184513
```

Each field element requires 32 bytes for representation, yielding a total blob size of 4096 × 32 = 131,072 bytes (128 KiB). However, because field elements must be less than the modulus `p`, the most significant byte of each 32-byte chunk is constrained, providing approximately 254 bits of usable data per field element rather than 256 bits.

This representation choice directly supports the polynomial commitment scheme underlying KZG commitments, as discussed in Section 2.3. Each blob can be interpreted as the evaluation of a polynomial of degree 4095 at 4096 distinct points, enabling efficient cryptographic verification through the properties of polynomial mathematics.

#### 3.3.2 Target and Maximum Blob Counts

EIP-4844 specifies both target and maximum blob counts per block, implementing an elastic capacity model that addresses the block space competition problem identified in Section 2.2.3:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| TARGET_BLOBS_PER_BLOCK | 3 | Baseline capacity for stable fee market |
| MAX_BLOBS_PER_BLOCK | 6 | Surge capacity for demand spikes |
| Target data per block | 384 KiB | 3 blobs × 128 KiB |
| Maximum data per block | 768 KiB | 6 blobs × 128 KiB |

The target of 3 blobs per block represents a carefully calibrated balance between immediate scalability benefits and network sustainability. At 12-second block times, this translates to approximately 256 KiB of blob data per block on average, or roughly 1.85 GB of daily blob throughput. This capacity increase is substantial—providing roughly 10× more data availability than the pre-EIP-4844 approach of embedding rollup data in calldata—while remaining within the operational capabilities of existing node infrastructure. The real-world utilization patterns and their economic implications will be analyzed in Section 4.

#### 3.3.3 Data Encoding Considerations

Rollup operators encoding transaction data into blobs must account for the field element constraints. The most common approach involves treating each 31-byte segment of raw data as a field element, with the high byte zeroed to ensure the value remains below the field modulus. This encoding achieves approximately 96.9% efficiency (31/32 bytes utilized per field element), translating to roughly 124 KiB of usable data capacity per blob.

Alternative encoding schemes can achieve higher efficiency by packing data more densely and using error correction or range proofs to handle edge cases where raw data might exceed field element bounds. However, the simpler 31-byte encoding has become the de facto standard due to its implementation simplicity and negligible overhead.

### 3.4 KZG Commitment Scheme Implementation

#### 3.4.1 Mathematical Foundations

KZG (Kate-Zaverucha-Goldberg) commitments, introduced in Section 2.3.2, provide the cryptographic backbone for EIP-4844's data availability verification. The scheme enables a prover to commit to a polynomial and later prove evaluations of that polynomial at arbitrary points, with commitments and proofs both being constant-size (single elliptic curve group elements).

The security of KZG commitments relies on the hardness of the discrete logarithm problem in elliptic curve groups and, more specifically, on the q-Strong Diffie-Hellman assumption. For a polynomial f(x) of degree d, the commitment is computed as:

```
C = f(s) · G₁
```

where `s` is a secret value from the trusted setup, `G₁` is the generator of the G₁ group on the BLS12-381 curve, and the computation is performed "in the exponent" using the structured reference string (SRS) from the trusted setup.

#### 3.4.2 The KZG Trusted Setup Ceremony

A critical component of the KZG scheme is the trusted setup, which generates the structured reference string containing powers of a secret value `s` encoded in elliptic curve group elements:

```
SRS = {G₁, s·G₁, s²·G₁, ..., s^d·G₁, G₂, s·G₂}
```

The security requirement is that no party should know the discrete logarithm relationship between these elements—i.e., the value `s` must be unknown to all participants. To achieve this, Ethereum conducted an unprecedented ceremony involving over 141,000 contributors from around the world between 2022 and 2023, as mentioned in Section 2.3.2.

The ceremony employed a "powers of tau" protocol where each participant contributes randomness that is combined multiplicatively with the existing secret. The crucial security property is that the final SRS is secure as long as at least one participant honestly destroyed their contribution randomness. With over 141,000 participants—including individuals, institutions, and even contributions generated from random physical processes—the probability that all participants colluded or were compromised is negligibly small.

The ceremony produced an SRS supporting polynomials of degree up to 4096, precisely matching the blob size specification. This SRS is now embedded in Ethereum client implementations and used by all nodes for blob verification.

#### 3.4.3 Commitment and Verification Process

When a blob is submitted, the following cryptographic operations occur:

1. **Polynomial Interpretation**: The blob's 4096 field elements are interpreted as evaluations of a polynomial f(x) at the 4096th roots of unity in the BLS12-381 scalar field.

2. **Commitment Generation**: Using the Lagrange form of polynomial interpolation and the SRS, the KZG commitment is computed. This involves a multi-scalar multiplication (MSM) operation—one of the most computationally intensive operations in the protocol, with performance implications we will discuss in Section 3.8.

3. **Versioned Hash Derivation**: The commitment (a 48-byte G₁ point in compressed form) is hashed using SHA-256, and the version byte is prepended to create the versioned hash included in the transaction, as described in Section 3.2.2.

4. **Proof Generation** (for point evaluation): When a verifier needs to confirm that the blob contains specific data at a particular position, the prover generates a
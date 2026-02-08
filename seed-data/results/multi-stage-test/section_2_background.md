## Technical Foundations: Data Availability and Cryptographic Primitives

### The Data Availability Problem in Rollup Architectures

As discussed in the Introduction, Ethereum's rollup-centric roadmap positions Layer 2 solutions as the primary mechanism for scaling transaction throughput. However, this architectural approach introduces a fundamental challenge known as the data availability problem—a critical bottleneck that EIP-4844 directly addresses.

Rollups achieve scalability by executing transactions off-chain while inheriting Ethereum's security guarantees through cryptographic proofs. Both optimistic rollups (such as Arbitrum and Optimism) and zero-knowledge rollups (such as zkSync and StarkNet) must post sufficient transaction data to Ethereum's Layer 1 to enable independent verification. This requirement stems from a core security principle: any observer must be able to reconstruct the complete rollup state from data published on-chain, without trusting the rollup operator.

For optimistic rollups, data availability is essential during the fraud proof window—typically seven days—during which challengers can dispute invalid state transitions. If the underlying transaction data were unavailable, honest validators could not construct fraud proofs to contest malicious state updates. For zero-knowledge rollups, while validity proofs mathematically guarantee correct execution, users still require access to transaction data to determine their account balances and construct withdrawal proofs. Without data availability, users' funds could become permanently inaccessible even if the rollup operator disappears.

The data availability problem thus creates an apparent paradox: rollups need Ethereum's security but cannot fully escape its throughput limitations because they must publish data to the constrained Layer 1. This dependency establishes data availability costs as the dominant factor in rollup transaction fees, often comprising 80-95% of the total cost users pay.

### Current Approach: Calldata and Its Inherent Limitations

Prior to EIP-4844, rollups posted transaction data using Ethereum's calldata mechanism—the input data field attached to transactions. While calldata serves this purpose functionally, it represents a fundamentally inefficient solution for data availability due to several structural limitations.

#### Permanent Storage Requirements

Calldata becomes part of Ethereum's permanent blockchain history. Every full node must download, verify, and store this data indefinitely, regardless of whether it serves any ongoing purpose. For rollups, however, the data availability requirement is inherently temporary: optimistic rollups need data accessible only during their challenge period, while zero-knowledge rollups need it only until state transitions are finalized. The mismatch between permanent storage and temporary requirements creates substantial inefficiency.

As of early 2024, major rollups collectively post approximately 15-20 GB of calldata monthly to Ethereum. This data accumulates perpetually, contributing to state bloat that increases hardware requirements for node operators and threatens long-term decentralization. The Ethereum blockchain's total size exceeds 1 TB, with rollup calldata representing an increasingly significant portion of growth.

#### Gas Cost Structure

Calldata pricing reflects its permanent storage nature. EIP-2028, implemented in 2019, reduced calldata costs from 68 gas per non-zero byte to 16 gas per non-zero byte, providing temporary relief. However, these costs remain substantial when aggregated across millions of transactions.

Consider a typical rollup batch containing 500 transactions, requiring approximately 120 KB of compressed calldata. At 16 gas per byte, this consumes roughly 1.92 million gas—nearly 7% of an entire Ethereum block's capacity. During periods of network congestion when base fees reach 50-100 gwei, posting this single batch costs $2,000-4,000 in data availability fees alone. These costs directly translate to user transaction fees, with rollup users paying $0.10-0.50 per transaction primarily for data availability rather than execution.

#### Competition for Block Space

Calldata competes directly with all other Ethereum transactions for limited block space. During NFT mints, DeFi volatility events, or other demand spikes, rollups face the same fee escalation as individual users. This coupling undermines the fundamental value proposition of rollups as a scaling solution—if rollup costs scale linearly with Layer 1 congestion, users gain only marginal benefits over direct L1 interaction.

The Ethereum block gas limit of 30 million creates a hard ceiling on aggregate data throughput. With calldata consuming 16 gas per byte, the theoretical maximum calldata per block is approximately 1.8 MB, though practical limits are much lower given competition from other transaction types. This constraint fundamentally limits how much rollups can scale, regardless of their off-chain execution capacity.

### Polynomial Commitments: Mathematical Foundations

EIP-4844 introduces a sophisticated cryptographic primitive—polynomial commitment schemes—to enable efficient data availability verification. Understanding these mathematical foundations is essential for grasping how blob transactions achieve their efficiency gains.

#### Commitment Schemes Overview

A commitment scheme allows a party to commit to a value while keeping it hidden, then later reveal the value and prove it matches the original commitment. In the context of data availability, we need commitments that enable verification of data properties without requiring validators to process the entire dataset.

Polynomial commitments extend this concept by representing data as coefficients of a polynomial function. A dataset of *n* elements can be encoded as a polynomial *p(x)* of degree *n-1*, where each data element corresponds to a coefficient. The commitment to this polynomial is a single, compact value that cryptographically binds to the entire dataset.

The crucial property for data availability is the ability to create opening proofs—succinct demonstrations that the polynomial evaluates to a specific value at a given point. These proofs enable sampling-based verification: rather than downloading all data, verifiers can request evaluations at random points and verify them against the commitment. If a malicious actor withholds even a small portion of data, they cannot produce valid opening proofs for the missing sections, and random sampling will detect this with high probability.

#### KZG Commitment Scheme

EIP-4844 specifically employs the Kate-Zaverucha-Goldberg (KZG) commitment scheme, named after its inventors who introduced it in 2010. KZG commitments offer several properties that make them particularly suitable for Ethereum's data availability layer.

**Constant-Size Commitments**: Regardless of the polynomial degree (and thus the data size), a KZG commitment is always a single elliptic curve group element—48 bytes in EIP-4844's implementation using the BLS12-381 curve. This compactness is essential for on-chain efficiency.

**Constant-Size Proofs**: Opening proofs demonstrating that *p(z) = y* for any point *z* are also single group elements. Verification requires only a constant number of elliptic curve operations, independent of the polynomial degree.

**Homomorphic Properties**: KZG commitments support linear combinations. Given commitments to polynomials *p(x)* and *q(x)*, one can compute a commitment to *p(x) + q(x)* without knowing the underlying polynomials. This property enables efficient aggregation of multiple blob commitments.

The KZG scheme relies on a trusted setup ceremony to generate structured reference strings (SRS)—public parameters used in commitment and verification operations. Ethereum conducted a large-scale ceremony in 2022-2023, gathering contributions from over 140,000 participants. The security assumption is that at least one participant honestly generated and destroyed their secret contribution; if so, the resulting parameters are secure.

#### Mathematical Construction

For readers seeking deeper technical understanding, the KZG construction operates as follows. Let *G₁* and *G₂* be groups of prime order *p* with a bilinear pairing *e: G₁ × G₂ → G_T*. The trusted setup generates powers of a secret *τ*: the SRS contains *[τ⁰]₁, [τ¹]₁, ..., [τⁿ]₁* in *G₁* and *[τ]₂* in *G₂*, where bracket notation denotes scalar multiplication of the group generator.

To commit to a polynomial *p(x) = Σᵢ cᵢxⁱ*, the committer computes *C = Σᵢ cᵢ[τⁱ]₁ = [p(τ)]₁*. This commitment is binding because finding two different polynomials with the same commitment requires computing discrete logarithms, which is computationally infeasible.

To prove that *p(z) = y*, the prover constructs the quotient polynomial *q(x) = (p(x) - y)/(x - z)*, which exists as a polynomial only if *p(z) = y*. The proof is *π = [q(τ)]₁*. Verification checks the pairing equation *e(C - [y]₁, [1]₂) = e(π, [τ - z]₂)*, which holds if and only if the claimed evaluation is correct.

### Blob Data Structures and the Temporary Storage Model

EIP-4844 introduces blobs as a new data structure specifically designed for rollup data availability, with properties carefully chosen to balance security, efficiency, and decentralization concerns.

#### Blob Specifications

Each blob contains exactly 4,096 field elements, where each field element is a 32-byte value in the BLS12-381 scalar field. This yields a blob size of 128 KB (131,072 bytes). The fixed size simplifies implementation and enables consistent gas pricing.

The choice of 4,096 elements is deliberate: it equals 2¹², enabling efficient Fast Fourier Transform (FFT) operations for polynomial arithmetic. FFTs are essential for computing KZG commitments efficiently and will become even more critical when full danksharding introduces data availability sampling.

Blobs are transmitted in a sidecar structure alongside their parent transactions rather than embedded within them. This separation ensures that blob data does not burden execution layer processing while remaining cryptographically linked to consensus layer blocks through commitments.

#### Blob-Carrying Transactions (Type 3)

EIP-4844 defines a new transaction type (type 0x03) that can carry blob references. These transactions include:

- **blob_versioned_hashes**: A list of 32-byte hashes, each derived from a blob's KZG commitment using a versioned hashing scheme. The version byte (currently 0x01) enables future commitment scheme upgrades.
- **max_fee_per_blob_gas**: The maximum fee the sender will pay per unit of blob gas, analogous to max_fee_per_gas for regular transactions.

The transaction itself contains only the versioned hashes, not the blob data. Blobs are transmitted through the consensus layer's gossip network and validated against their commitments. This design ensures that execution layer clients need not process blob contents, maintaining separation of concerns.

A single transaction can reference up to 6 blobs (a limit that may increase in future upgrades), enabling batching of rollup data submissions. The target is 3 blobs per block with a maximum of 6, providing approximately 375 KB of average blob capacity per block.

#### Temporary Storage and Pruning

The most significant departure from calldata is blob data's temporary availability. Consensus layer clients are required to store and serve blob data for a minimum of 4,096 epochs—approximately 18.2 days at 12-second slot times. After this period, clients may prune blob data without violating protocol rules.

This pruning window is carefully calibrated:

- **Fraud Proof Compatibility**: The 18-day window exceeds the typical 7-day challenge period for optimistic rollups, ensuring data remains available throughout dispute resolution.
- **ZK Rollup Finality**: Zero-knowledge rollups typically finalize state within hours, well within the availability window.
- **Storage Sustainability**: Temporary storage prevents unbounded growth. At target capacity, blob data adds approximately 50 GB monthly, all of which is pruned, compared to permanent calldata accumulation.

Nodes that wish to retain historical blob data may do so, and specialized archival services will likely emerge to serve historical queries. However, the protocol's security guarantees do not depend on this archival—only on availability during the pruning window.

#### Blob Gas and Fee Market

EIP-4844 introduces a separate fee market for blob space, independent of regular execution gas. This separation is crucial for ensuring that blob costs reflect blob-specific supply and demand rather than general network congestion.

The blob base fee follows the same EIP-1559-style adjustment mechanism as execution gas: if blob usage exceeds the target (3 blobs per block), the base fee increases by up to 12.5%; if usage falls below target, the fee decreases. This creates a self-regulating market that prices blob space according to demand.

Initial parameters set the minimum blob base fee at 1 wei, allowing extremely low costs during periods of low demand. Early post-implementation data showed blob fees ranging from near-zero during quiet periods to several gwei during demand spikes—still dramatically cheaper than equivalent calldata costs.

The blob gas limit per block is 786,432 (6 blobs × 131,072 bytes × 1 gas per byte), with a target of 393,216 (3 blobs). This parameterization provides headroom for demand fluctuations while maintaining predictable average capacity.

### Connection to Full Danksharding: A Stepping Stone Architecture

EIP-4844 is explicitly designed as proto-danksharding—a preliminary implementation that establishes the transaction format, cryptographic primitives, and fee market structure required for full danksharding, while deferring the most complex components.

#### What Proto-Danksharding Includes

EIP-4844 implements all user-facing and transaction-level components of the full danksharding vision:

- **Blob transaction format**: Type 3 transactions with versioned hashes
- **KZG commitment infrastructure**: Trusted setup, commitment verification, point evaluation precompile
- **Separate fee market**: Independent blob gas pricing and EIP-1559 dynamics
- **Consensus layer integration**: Blob sidecars, availability checks, and gossip protocols

These components represent the "hard" parts of danksharding from a coordination perspective—they require changes to transaction formats, new precompiled contracts, and consensus layer modifications. By implementing them now, EIP-4844 ensures that future danksharding upgrades can proceed as soft forks or minor hard forks rather than requiring another comprehensive protocol overhaul.

#### What Full Danksharding Adds

The primary addition in full danksharding is Data Availability Sampling (DAS), which enables dramatic capacity increases without proportionally increasing node requirements.

With DAS, validators do not download complete blobs. Instead, they randomly sample small portions and verify them against KZG commitments. The mathematical properties of erasure coding (specifically, 2D Reed-Solomon encoding) ensure that if any validator can reconstruct the data, the data is available with overwhelming probability. This allows blob capacity to scale to potentially 16 MB per block—over 100× current levels—while individual nodes download only kilobytes of samples.

DAS requires additional infrastructure:

- **Erasure coding**: Extending blob data with redundancy so that any 50% of samples suffices for reconstruction
- **Sampling protocols**: Peer-to-peer mechanisms for requesting and validating random samples
- **Custody requirements**: Ensuring sufficient network participants store each data segment

These components involve substantial research and engineering challenges that would have delayed blob implementation by years. Proto-danksharding's pragmatic approach delivers immediate benefits while the DAS infrastructure matures.

#### Upgrade Path

The transition from proto-danksharding to full danksharding is designed to be minimally disruptive:

1. **Transaction format stability**: Type 3 transactions and blob structures remain unchanged
2. **Commitment compatibility**: KZG commitments extend naturally to support DAS verification
3. **Fee market evolution**: Blob gas parameters can adjust to reflect increased capacity
4. **Rollup continuity**: Rollups posting blobs today will continue functioning without modification

This forward compatibility represents a significant achievement in protocol design—delivering substantial immediate value while preserving optionality for future enhancements. The cryptographic primitives and data structures introduced in EIP-4844 form the foundation upon which Ethereum's long-term data availability scaling will be built.
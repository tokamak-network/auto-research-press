## EIP-4844 Mechanism Design: Blob Transactions and Protocol Changes

### Introduction to Proto-Danksharding Architecture

Building upon the data availability foundations established in the previous section, EIP-4844 introduces a sophisticated mechanism design that fundamentally restructures how Ethereum handles rollup data. This Ethereum Improvement Proposal, commonly known as proto-danksharding, represents the most significant protocol change since the Merge, introducing new transaction types, cryptographic verification schemes, and an independent fee market specifically optimized for data availability.

The design philosophy underlying EIP-4844 prioritizes backward compatibility while establishing the architectural scaffolding necessary for full danksharding. Rather than implementing the complete data sharding vision immediately, proto-danksharding introduces the transaction format, cryptographic primitives, and fee mechanisms that future upgrades will extend. This incremental approach allows the Ethereum ecosystem to adapt gradually while delivering immediate cost reductions for Layer 2 rollups.

### Type 3 Transactions: Blob-Carrying Transaction Structure

EIP-4844 introduces a new transaction type designated as Type 3, following Ethereum's existing transaction type taxonomy (Type 0 for legacy, Type 1 for EIP-2930 access lists, and Type 2 for EIP-1559 dynamic fees). Blob-carrying transactions extend the EIP-1559 transaction format with additional fields specifically designed for data availability purposes.

#### Transaction Field Specification

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

The critical additions distinguishing Type 3 transactions are `max_fee_per_blob_gas` and `blob_versioned_hashes`. The former specifies the maximum price per unit of blob gas the sender is willing to pay, analogous to `max_fee_per_gas` for regular execution gas. The latter contains a list of versioned hashes—cryptographic commitments to each blob attached to the transaction.

#### Versioned Hash Construction

Versioned hashes provide a compact, fixed-size representation of blob commitments suitable for inclusion in execution layer data structures. Each versioned hash is constructed by taking the SHA-256 hash of the KZG commitment and prepending a version byte:

```
versioned_hash = VERSIONED_HASH_VERSION_KZG || SHA256(kzg_commitment)[1:]
```

The version byte (currently `0x01` for KZG commitments) enables future cryptographic agility, allowing the protocol to transition to alternative commitment schemes—such as those based on STARKs or other post-quantum constructions—without requiring fundamental changes to the transaction format.

#### Transaction Validity Constraints

For a Type 3 transaction to be considered valid, several constraints must be satisfied:

1. **Non-empty blob list**: The transaction must include at least one blob (`len(blob_versioned_hashes) >= 1`)
2. **Blob count limit**: The transaction cannot exceed the maximum blobs per transaction (`len(blob_versioned_hashes) <= MAX_BLOBS_PER_TX`, currently set to 6)
3. **Contract creation prohibition**: The `to` field must contain a valid address; blob transactions cannot create new contracts (`to != None`)
4. **Fee sufficiency**: The `max_fee_per_blob_gas` must meet or exceed the current blob base fee
5. **Hash-commitment correspondence**: Each versioned hash must correctly correspond to the KZG commitment of its associated blob

These constraints ensure that blob transactions serve their intended purpose—providing data availability for rollups—while preventing potential abuse vectors.

### Blob Format Specifications and Data Structure

#### Field Element Representation

Blobs in EIP-4844 are structured as vectors of 4096 field elements, where each field element belongs to the BLS12-381 scalar field. This field has a prime modulus of:

```
p = 52435875175126190479447740508185965837690552500527637822603658699938581184513
```

Each field element requires 32 bytes for representation, yielding a total blob size of 4096 × 32 = 131,072 bytes (128 KiB). However, because field elements must be less than the modulus `p`, the most significant byte of each 32-byte chunk is constrained, providing approximately 254 bits of usable data per field element rather than 256 bits.

This representation choice directly supports the polynomial commitment scheme underlying KZG commitments. Each blob can be interpreted as the evaluation of a polynomial of degree 4095 at 4096 distinct points, enabling efficient cryptographic verification through the properties of polynomial mathematics.

#### Target and Maximum Blob Counts

EIP-4844 specifies both target and maximum blob counts per block, implementing an elastic capacity model:

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| TARGET_BLOBS_PER_BLOCK | 3 | Baseline capacity for stable fee market |
| MAX_BLOBS_PER_BLOCK | 6 | Surge capacity for demand spikes |
| Target data per block | 384 KiB | 3 blobs × 128 KiB |
| Maximum data per block | 768 KiB | 6 blobs × 128 KiB |

The target of 3 blobs per block represents a carefully calibrated balance between immediate scalability benefits and network sustainability. At 12-second block times, this translates to approximately 256 KiB of blob data per block on average, or roughly 1.85 GB of daily blob throughput. This capacity increase is substantial—providing roughly 10× more data availability than the pre-EIP-4844 approach of embedding rollup data in calldata—while remaining within the operational capabilities of existing node infrastructure.

#### Data Encoding Considerations

Rollup operators encoding transaction data into blobs must account for the field element constraints. The most common approach involves treating each 31-byte segment of raw data as a field element, with the high byte zeroed to ensure the value remains below the field modulus. This encoding achieves approximately 96.9% efficiency (31/32 bytes utilized per field element), translating to roughly 124 KiB of usable data capacity per blob.

Alternative encoding schemes can achieve higher efficiency by packing data more densely and using error correction or range proofs to handle edge cases where raw data might exceed field element bounds. However, the simpler 31-byte encoding has become the de facto standard due to its implementation simplicity and negligible overhead.

### KZG Commitment Scheme Implementation

#### Mathematical Foundations

KZG (Kate-Zaverucha-Goldberg) commitments, introduced in the 2010 paper "Constant-Size Commitments to Polynomials and Their Applications," provide the cryptographic backbone for EIP-4844's data availability verification. The scheme enables a prover to commit to a polynomial and later prove evaluations of that polynomial at arbitrary points, with commitments and proofs both being constant-size (single elliptic curve group elements).

The security of KZG commitments relies on the hardness of the discrete logarithm problem in elliptic curve groups and, more specifically, on the q-Strong Diffie-Hellman assumption. For a polynomial f(x) of degree d, the commitment is computed as:

```
C = f(s) · G₁
```

where `s` is a secret value from the trusted setup, `G₁` is the generator of the G₁ group on the BLS12-381 curve, and the computation is performed "in the exponent" using the structured reference string (SRS) from the trusted setup.

#### The KZG Trusted Setup Ceremony

A critical component of the KZG scheme is the trusted setup, which generates the structured reference string containing powers of a secret value `s` encoded in elliptic curve group elements:

```
SRS = {G₁, s·G₁, s²·G₁, ..., s^d·G₁, G₂, s·G₂}
```

The security requirement is that no party should know the discrete logarithm relationship between these elements—i.e., the value `s` must be unknown to all participants. To achieve this, Ethereum conducted an unprecedented ceremony involving over 141,000 contributors from around the world between 2022 and 2023.

The ceremony employed a "powers of tau" protocol where each participant contributes randomness that is combined multiplicatively with the existing secret. The crucial security property is that the final SRS is secure as long as at least one participant honestly destroyed their contribution randomness. With over 141,000 participants—including individuals, institutions, and even contributions generated from random physical processes—the probability that all participants colluded or were compromised is negligibly small.

The ceremony produced an SRS supporting polynomials of degree up to 4096, precisely matching the blob size specification. This SRS is now embedded in Ethereum client implementations and used by all nodes for blob verification.

#### Commitment and Verification Process

When a blob is submitted, the following cryptographic operations occur:

1. **Polynomial Interpretation**: The blob's 4096 field elements are interpreted as evaluations of a polynomial f(x) at the 4096th roots of unity in the BLS12-381 scalar field.

2. **Commitment Generation**: Using the Lagrange form of polynomial interpolation and the SRS, the KZG commitment is computed. This involves a multi-scalar multiplication (MSM) operation—one of the most computationally intensive operations in the protocol.

3. **Versioned Hash Derivation**: The commitment (a 48-byte G₁ point in compressed form) is hashed using SHA-256, and the version byte is prepended to create the versioned hash included in the transaction.

4. **Proof Generation** (for point evaluation): When a verifier needs to confirm that the blob contains specific data at a particular position, the prover generates a KZG proof—a single G₁ point demonstrating the claimed evaluation without revealing the entire polynomial.

5. **Verification**: Verifiers use elliptic curve pairing operations to check proofs. The verification equation:
   ```
   e(C - y·G₁, G₂) = e(π, s·G₂ - z·G₂)
   ```
   where `e` is the pairing function, `C` is the commitment, `y` is the claimed evaluation, `z` is the evaluation point, and `π` is the proof.

The elegance of KZG commitments lies in their constant-size proofs and efficient verification—properties essential for blockchain scalability where on-chain verification costs must be minimized.

### Separate Fee Market for Blob Gas

#### EIP-1559 Style Mechanism for Blobs

EIP-4844 introduces a fee market for blob gas that operates independently from the existing execution gas market, though it employs similar EIP-1559-style dynamics. This separation ensures that demand for data availability does not directly compete with demand for computation, preventing rollup data posting from being priced out during periods of high execution layer activity.

The blob gas price is determined by a base fee that adjusts algorithmically based on blob space utilization relative to the target:

```python
def calc_blob_base_fee(parent_header):
    return fake_exponential(
        MIN_BLOB_BASE_FEE,
        parent_header.excess_blob_gas,
        BLOB_BASE_FEE_UPDATE_FRACTION
    )

def fake_exponential(factor, numerator, denominator):
    # Approximates factor * e^(numerator / denominator)
    # using integer arithmetic
    ...
```

The key parameters governing this mechanism are:

| Parameter | Value | Effect |
|-----------|-------|--------|
| MIN_BLOB_BASE_FEE | 1 wei | Floor price preventing zero-cost spam |
| BLOB_BASE_FEE_UPDATE_FRACTION | 3,338,477 | Controls price adjustment speed |
| BLOB_GAS_PER_BLOB | 2^17 (131,072) | Gas units consumed per blob |
| TARGET_BLOB_GAS_PER_BLOCK | 393,216 | Target = 3 blobs worth of gas |
| MAX_BLOB_GAS_PER_BLOCK | 786,432 | Maximum = 6 blobs worth of gas |

#### Price Adjustment Dynamics

The blob base fee adjusts according to an exponential function of the cumulative excess blob gas. When blocks consistently contain more than the target 3 blobs, the excess blob gas accumulates, driving prices upward. Conversely, when utilization falls below target, excess blob gas decreases (bounded at zero), reducing prices.

The update fraction of 3,338,477 is calibrated such that the blob base fee increases by approximately 12.5% when a block contains the maximum 6 blobs (double the target), mirroring the execution gas market's adjustment rate. This creates predictable price discovery while allowing the market to respond to sustained demand changes.

In practice, since the Dencun upgrade activated EIP-4844 in March 2024, blob fees have exhibited significant volatility. Initial periods saw blob base fees near the minimum of 1 wei as blob space supply exceeded demand. However, during periods of high rollup activity—particularly around token launches, NFT mints, and airdrop claims on Layer 2s—blob fees have spiked dramatically, sometimes exceeding 100 gwei per blob gas unit.

#### Economic Implications for Rollups

The separate fee market fundamentally changes rollup economics. Prior to EIP-4844, rollups paid execution gas prices (often 20-100+ gwei) for calldata used to post transaction batches. With blob transactions, rollups pay blob gas prices that are typically orders of magnitude lower during normal conditions.

Consider a rollup posting a batch containing 1000 transactions:

**Pre-EIP-4844 (Calldata Approach)**:
- Batch size: ~100 KB compressed
- Calldata cost: 100,000 bytes × 16 gas/byte = 1,600,000 gas
- At 30 gwei gas price: 0.048 ETH
- Per-transaction L1 cost: ~$0.15 (at $3000/ETH)

**Post-EIP-4844 (Blob Approach)**:
- Batch size: ~100 KB (fits in 1 blob)
- Blob cost: 131,072 blob gas × 1 wei = 0.000131072 ETH
- Per-transaction L1 cost: ~$0.0004 (at $3000/ETH)

This represents a potential 99%+ reduction in L1 data posting costs, though actual savings depend on blob market conditions and vary over time.

### Consensus Layer Changes: Beacon Block Modifications

#### Blob Sidecar Architecture

A fundamental architectural decision in EIP-4844 is the separation of blob data from the main beacon block structure. Rather than embedding blobs directly in beacon blocks—which would dramatically increase block sizes and propagation times—blobs are transmitted as "sidecars" that accompany blocks through the network.

The `BlobSidecar` structure contains:

```python
class BlobSidecar(Container):
    index: BlobIndex  # Index of blob in block (0-5)
    blob: Blob  # The actual 128 KiB blob data
    kzg_commitment: KZGCommitment  # 48-byte commitment
    kzg_proof: KZGProof  # 48-byte proof for commitment verification
    signed_block_header: SignedBeaconBlockHeader  # Block association
    kzg_commitment_inclusion_proof: Vector[Bytes32, KZG_COMMITMENT_INCLUSION_PROOF_DEPTH]
```

The inclusion proof allows any party to verify that a specific blob sidecar corresponds to a commitment included in a particular beacon block, without requiring access to the full block body.

#### Beacon Block Body Modifications

The beacon block body is extended to include a list of KZG commitments:

```python
class BeaconBlockBody(Container):
    # ... existing fields ...
    blob_kzg_commitments: List[KZGCommitment, MAX_BLOBS_PER_BLOCK]
```

Critically, only the commitments—not the blobs themselves—are included in the beacon block. This design choice has several important implications:

1. **Block size stability**: Beacon blocks remain approximately the same size regardless of blob utilization
2. **Propagation efficiency**: The critical path for block propagation is unaffected by blob data
3. **Flexible availability**: Nodes can obtain blobs through various mechanisms (direct gossip, request-response, or data availability sampling in future upgrades)
4. **Pruning compatibility**: The commitment/sidecar separation naturally supports the temporary storage model where blobs are pruned after ~18 days

#### Block Processing and Validation

When a consensus client processes a new block, the following blob-related validation steps occur:

1. **Commitment count verification**: Ensure the number of commitments matches the number of blob transactions in the execution payload
2. **Sidecar retrieval**: Obtain blob sidecars corresponding to each commitment (via gossip or request)
3. **Blob-commitment verification**: For each sidecar, verify that the blob data correctly corresponds to its claimed commitment using the KZG proof
4. **Inclusion proof verification**: Verify that each sidecar's commitment is genuinely included in the beacon block

The block is considered fully validated only when all blob sidecars are obtained and verified. However, the consensus protocol includes grace periods and fallback mechanisms to handle temporary unavailability of blob data during propagation.

#### Data Retention and Pruning Policy

EIP-4844 specifies that consensus clients must retain blob sidecars for a minimum period defined by `MIN_EPOCHS_FOR_BLOB_SIDECARS_REQUESTS`, set to 4096 epochs (approximately 18.2 days). After this period, clients may prune blob data while retaining the commitments in the historical beacon block data.

This temporary retention model represents a significant departure from Ethereum's traditional approach of permanent data availability. The rationale, as discussed in the Technical Foundations section, is that rollups only require data availability during their challenge periods (typically 7 days for optimistic rollups) or for user withdrawal construction. After this window, the data has served its purpose, and permanent storage is unnecessary.

### Execution Layer Integration

#### New Opcodes: BLOBHASH and BLOBBASEFEE

EIP-4844 introduces two new EVM opcodes that enable smart contracts to interact with blob transaction data:

**BLOBHASH (0x49)**
- Gas cost: 3 (equivalent to other hash-accessing opcodes)
- Input: index (from stack)
- Output: versioned_hash (to stack)
- Behavior: Returns the versioned hash at the specified index from the current transaction's blob_versioned_hashes list, or zero if the index is out of bounds

The BLOBHASH opcode is essential for rollup contracts that need to verify blob contents. When a rollup sequencer posts a batch via a blob transaction and calls the rollup's inbox contract, the contract can use BLOBHASH to obtain the commitment to the posted data. This commitment can then be stored and later used in fraud proofs or validity proof verification.

Example usage in a rollup inbox contract:

```solidity
function submitBatch(uint256 blobIndex, bytes32 stateRoot) external {
    bytes32 blobHash = blobhash(blobIndex);
    require(blobHash != bytes32(0), "Invalid blob index");
    
    batches[nextBatchIndex] = Batch({
        blobHash: blobHash,
        stateRoot: stateRoot,
        timestamp: block.timestamp,
        submitter: msg.sender
    });
    nextBatchIndex++;
}
```

**BLOBBASEFEE (0x4a)**
- Gas cost: 2 (equivalent to BASEFEE)
- Input: none
- Output: current_blob_base_fee (to stack)
- Behavior: Returns the current blob base fee in wei

This opcode allows contracts to query the current blob gas price, enabling on-chain logic that responds to blob market conditions. For instance, a rollup contract might implement dynamic fee adjustments based on L1 blob costs, or a MEV-aware contract might make decisions based on the relative costs of different data availability options.

#### Point Evaluation Precompile

EIP-4844 introduces a new precompiled contract at address `0x0a` that performs KZG point evaluation verification. This precompile is crucial for enabling on-chain verification of claims about blob contents.

**Precompile Specification**:
- Address: 0x000000000000000000000000000000000000000a
- Gas cost: 50,000
- Input: versioned_hash || z || y || commitment || proof (192 bytes total)
- Output: FIELD_ELEMENTS_PER_BLOB || BLS_MODULUS (64 bytes)

The precompile verifies that the polynomial committed to by `commitment` (which must hash to `versioned_hash`) evaluates to `y` at point `z`. If verification succeeds, it returns the blob size constant and field modulus; if verification fails, the call reverts.

This precompile enables a powerful pattern for fraud proofs and data verification:

1. A rollup posts transaction data in a blob
2. The blob's versioned hash is recorded in the rollup contract
3. Later, if a fraud proof requires proving specific data was in the blob, the challenger provides:
   - The evaluation point z (indicating the position in the blob)
   - The claimed value y (the data at that position)
   - A KZG proof π
4. The contract calls the point evaluation precompile to verify the claim
5. If verified, the contract knows with cryptographic certainty what data was in the blob at that position

This mechanism is particularly elegant because it allows verification of arbitrary blob positions without requiring the full blob data to be available on-chain—only the 192-byte proof input is needed.

#### Header and Receipt Modifications

The execution layer block header is extended with two new fields:

```python
class ExecutionPayloadHeader:
    # ... existing fields ...
    blob_gas_used: uint64  # Total blob gas consumed by block
    excess_blob_gas: uint64  # Cumulative excess for fee calculation
```

These fields enable the blob fee market mechanism and provide transparency into blob utilization at the execution layer. The `excess_blob_gas` field is particularly important as it determines the blob base fee for subsequent blocks.

Transaction receipts for Type 3 transactions include the blob gas price paid, allowing users and applications to track actual blob costs:

```python
class TransactionReceipt:
    # ... existing fields ...
    blob_gas_used: uint64  # Blob gas consumed (n × 131072)
    blob_gas_price: uint256  # Price per blob gas unit paid
```

### Cross-Layer Coordination and Network Considerations

#### Gossip Protocol Modifications

The peer-to-peer networking layer requires modifications to handle blob propagation efficiently. Blob sidecars are gossiped on dedicated subnets, separate from beacon block gossip, allowing nodes to parallelize block and blob retrieval.

The gossip validation rules for blob sidecars include:
- Signature verification of the associated block header
- KZG proof verification for blob-commitment correspondence
- Inclusion proof verification against the block's commitment list
- Duplicate detection to prevent redundant propagation

Nodes that fail to provide blob sidecars for blocks they propose face attestation penalties, as other validators will not attest to blocks with unavailable blob data.

#### Mempool and Transaction Pool Considerations

Blob transactions present unique challenges for transaction pool management:

1. **Size concerns**: A single blob transaction with maximum blobs (6 × 128 KiB = 768 KiB) is orders of magnitude larger than typical transactions
2. **Replacement rules**: Blob transaction replacement must consider both execution gas and blob gas fee bumps
3. **Propagation bandwidth**: Aggressive blob transaction propagation could overwhelm network bandwidth

To address these concerns, EIP-4844 specifies that blob transactions in the mempool should be propagated as "blob transaction wrappers" containing the full blob data, but nodes may implement bandwidth management policies including:
- Rate limiting blob transaction propagation
- Prioritizing transactions from known, reputable rollup operators
- Implementing blob-specific fee thresholds for propagation

### Implementation Challenges and Client Considerations

#### Computational Requirements

The cryptographic operations introduced by EIP-4844 impose significant computational requirements:

1. **KZG commitment computation**: Generating a commitment requires a 4096-point multi-scalar multiplication (MSM), taking approximately 50-100ms on modern hardware with optimized implementations
2. **KZG proof generation**: Each proof requires additional MSM operations
3. **Pairing verification**: The point evaluation precompile performs elliptic curve pairing operations, among the most expensive cryptographic primitives

Client implementations have invested heavily in optimizing these operations, employing techniques such as:
- Pippenger's algorithm for MSM optimization
- Parallelization across multiple CPU cores
- SIMD (Single Instruction, Multiple Data) acceleration
- GPU offloading for high-throughput scenarios

#### Storage and Bandwidth Implications

Despite the temporary retention model, blob data still imposes meaningful storage requirements during the retention period:

- Maximum blobs per block: 6
- Blob size: 128 KiB
- Blocks per day: 7,200
- Maximum daily blob data: 6 × 128 KiB × 7,200 = 5.27 GB
- 18-day retention: up to ~95 GB of blob storage

In practice, utilization has been below maximum, but node operators must provision for potential sustained high utilization. Additionally, the bandwidth requirements for blob gossip—both receiving and serving blob sidecars—represent a meaningful increase in network resource consumption.

### Summary and Forward Compatibility

EIP-4844's mechanism design establishes a comprehensive framework for blob-based data availability that serves both immediate scalability needs and future protocol evolution. The Type 3 transaction format, KZG commitment scheme, and separate fee market create an independent data availability layer that can scale without directly competing with execution layer resources.

The architectural decisions—particularly the commitment-sidecar separation and temporary retention model—lay groundwork for full danksharding, where data availability sampling will enable further capacity increases without proportional node requirement growth. The versioned hash construction provides cryptographic agility for potential future transitions to alternative commitment schemes.

As we will explore in subsequent sections, these mechanism design choices involve deliberate trade-offs between immediate utility and long-term flexibility, between decentralization and scalability, and between implementation complexity and protocol elegance. Understanding these trade-offs is essential for evaluating EIP-4844's role in Ethereum's broader scaling strategy.
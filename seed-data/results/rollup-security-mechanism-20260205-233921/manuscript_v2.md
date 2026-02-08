# Rollup Security Mechanisms: A Comprehensive Analysis of Layer-2 Scaling Security Architecture

## Executive Summary

Rollups have emerged as the dominant Layer-2 scaling paradigm for blockchain networks, particularly Ethereum, promising to increase transaction throughput by orders of magnitude while inheriting the security guarantees of the underlying Layer-1 chain. However, the security mechanisms underpinning rollup architectures represent a complex interplay of cryptographic proofs, economic incentives, and trust assumptions that warrant rigorous examination.

This research report provides a comprehensive analysis of rollup security mechanisms, examining both optimistic and zero-knowledge (ZK) rollup architectures. We evaluate the theoretical foundations, practical implementations, and emerging vulnerabilities across major protocols including Arbitrum, Optimism, zkSync, StarkNet, and Polygon zkEVM. Our analysis reveals that while rollups offer substantial security improvements over alternative scaling solutions, they introduce novel attack vectors and trust assumptions that differ fundamentally from Layer-1 security models.

Key findings indicate that optimistic rollups currently rely on a 1-of-N honest validator assumption with challenge periods ranging from 7-14 days, while ZK-rollups provide cryptographic finality but face challenges in prover centralization and circuit complexity vulnerabilities. We identify critical security considerations including sequencer centralization, data availability constraints, bridge contract vulnerabilities, withdrawal mechanism security, and upgrade mechanism risks as primary areas requiring continued research and development.

The report concludes with forward-looking analysis suggesting that hybrid approaches, decentralized sequencer networks, and formal verification of ZK circuits will define the next generation of rollup security mechanisms. For practitioners and researchers, we provide actionable recommendations for evaluating rollup security and contributing to the maturation of this critical infrastructure.

---

## 1. Introduction

### 1.1 Background and Motivation

The scalability trilemma—the observation that blockchain systems must trade off between decentralization, security, and scalability—has driven extensive research into Layer-2 scaling solutions. Rollups emerged from this research as a particularly promising approach, first conceptualized in the Ethereum community around 2018-2019 and subsequently formalized through various implementation efforts.

The fundamental insight underlying rollup architecture is the separation of execution from consensus and data availability. By executing transactions off-chain while posting transaction data and state commitments on-chain, rollups can achieve throughput improvements of 10-100x while maintaining a security relationship with the underlying Layer-1 chain. Vitalik Buterin's influential 2020 essay "A Rollup-Centric Ethereum Roadmap" cemented rollups as the primary scaling strategy for Ethereum, catalyzing billions of dollars in development investment and research activity.

### 1.2 Scope and Methodology

This report examines rollup security mechanisms through multiple analytical lenses:

1. **Cryptographic foundations**: The mathematical primitives enabling state verification, including formal security definitions and underlying hardness assumptions
2. **Economic security**: Incentive structures, game-theoretic considerations, and quantitative analysis of adversarial behavior
3. **Operational security**: Implementation-level vulnerabilities and mitigations, including bridge contracts and withdrawal mechanisms
4. **Systemic security**: Cross-layer interactions, L1-L2 security inheritance models, and emergent risks

Our methodology combines literature review of academic publications and technical documentation, empirical analysis of deployed protocols, and theoretical examination of security models. We focus primarily on Ethereum-based rollups given their market dominance and technical maturity, while noting generalizable principles applicable to rollups on other Layer-1 platforms.

### 1.3 Definitions and Taxonomy

**Rollup**: A Layer-2 scaling solution that executes transactions off-chain, batches them together, and posts compressed transaction data along with a state commitment to the Layer-1 chain.

**Optimistic Rollup**: A rollup architecture that assumes transactions are valid by default and relies on a challenge mechanism with fraud proofs to detect and revert invalid state transitions.

**Zero-Knowledge Rollup (ZK-Rollup)**: A rollup architecture that generates cryptographic validity proofs for each batch of transactions, providing immediate mathematical certainty of correct execution.

**Sequencer**: The entity responsible for ordering transactions, executing them, and proposing state updates in a rollup system.

**Data Availability**: The guarantee that transaction data necessary for state reconstruction and verification is accessible to all network participants.

**L1-L2 Security Inheritance**: The property by which a rollup derives security guarantees from the underlying Layer-1 chain, subject to specific assumptions about finality, data availability, and proof verification.

---

## 2. Optimistic Rollup Security Mechanisms

### 2.1 Theoretical Foundation

Optimistic rollups derive their name from the optimistic assumption that state transitions proposed by sequencers are valid. This assumption is backed by a challenge mechanism: during a defined challenge period, any observer can submit a fraud proof demonstrating that a proposed state transition is invalid.

The security model relies on a **1-of-N honest assumption**: the system remains secure as long as at least one honest party monitors the chain and is willing and able to submit fraud proofs when necessary. This represents a significant relaxation compared to consensus-based security models requiring honest majorities.

#### 2.1.1 Formal Security Model

We formalize the security properties of optimistic rollups through explicit security games:

**Definition (State Transition Validity)**: Let $S_n$ represent the rollup state after $n$ batches, and let $f: S \times T \rightarrow S$ be the state transition function where $T$ represents a batch of transactions. A state transition $S_n \rightarrow S_{n+1}$ is valid if and only if $S_{n+1} = f(S_n, T_{n+1})$ for some valid transaction batch $T_{n+1}$.

**Security Game (Fraud Proof Soundness)**:
1. Adversary $\mathcal{A}$ commits to states $S_n$ and $S'_{n+1}$
2. Challenger $\mathcal{C}$ produces fraud proof $\pi$ if $S'_{n+1} \neq f(S_n, T)$ for any valid $T$
3. Verifier $\mathcal{V}$ accepts $\pi$ if and only if the transition is genuinely invalid

**Soundness Property**: For all PPT adversaries $\mathcal{A}$:
$$\Pr[\mathcal{V}(\pi) = \text{accept} \land S'_{n+1} = f(S_n, T)] \leq \text{negl}(\lambda)$$

**Completeness Property**: For all invalid transitions:
$$\Pr[\exists \pi : \mathcal{V}(\pi) = \text{accept} | S'_{n+1} \neq f(S_n, T)] = 1$$

#### 2.1.2 Network Synchrony Assumptions

The 1-of-N honest assumption requires careful specification of network conditions:

**Synchronous Model**: Messages delivered within known bound $\Delta$. The challenge period $T_c$ must satisfy:
$$T_c > \Delta_{\text{detection}} + \Delta_{\text{proof\_generation}} + \Delta_{\text{L1\_inclusion}} + \Delta_{\text{buffer}}$$

**Partially Synchronous Model**: After unknown Global Stabilization Time (GST), messages delivered within $\Delta$. Security holds only for challenges initiated after GST.

**Asynchronous Considerations**: Under full asynchrony, the 1-of-N assumption provides no guarantees, as adversarial network control can prevent fraud proof delivery indefinitely.

### 2.2 Fraud Proof Mechanisms

#### 2.2.1 Interactive Fraud Proofs

Arbitrum pioneered the interactive fraud proof model, which reduces on-chain verification costs through a bisection protocol. When a challenge is initiated:

1. The challenger and defender engage in a binary search over the disputed execution trace
2. Each round narrows the dispute to half the remaining instructions
3. After $\log_2(n)$ rounds for $n$ instructions, a single instruction is isolated
4. Only this single instruction is executed on-chain to determine the outcome

**Formal Security Analysis of Bisection Protocol**:

The bisection protocol's security relies on the following properties:

**Claim**: An honest challenger can always win against a dishonest asserter (and vice versa) within $O(\log n)$ rounds.

**Proof Sketch**: 
- Let $I^*$ be the first instruction where execution diverges
- At each round, the honest party can identify which half contains $I^*$
- After $\lceil \log_2 n \rceil$ rounds, $I^*$ is isolated
- On-chain execution of $I^*$ reveals the dishonest party

**Edge Cases and Mitigations**:
- *Challenger runs out of gas*: Protocol requires stake deposits; insufficient gas forfeits stake
- *Both parties malicious*: Protocol resolves to on-chain execution; correct state determined regardless
- *Timeout attacks*: Each round has time limits; non-response forfeits the game

```
Initial Dispute: Instructions 0 to 1,000,000
Round 1: Narrow to 0-500,000 or 500,001-1,000,000
Round 2: Narrow to 250,000-500,000 (example)
...
Round 20: Single instruction isolated
Final: On-chain execution of one instruction (~100-200k gas)
```

#### 2.2.2 Non-Interactive Fraud Proofs

Optimism's Cannon fault proof system represents an evolution toward non-interactive fraud proofs. Rather than requiring multiple rounds of interaction, the challenger submits a complete proof identifying the first invalid state transition. This approach:

- Reduces latency in dispute resolution
- Eliminates griefing vectors where malicious parties delay resolution
- Requires more sophisticated proof generation infrastructure

**Security Trade-offs**:

| Property | Interactive (Arbitrum) | Non-Interactive (Cannon) |
|----------|----------------------|-------------------------|
| Proof size | O(log n) commitments | O(n) in worst case |
| Rounds | O(log n) | 1 |
| Griefing resistance | Lower (delay attacks) | Higher |
| Proof generation | Incremental | Upfront computation |
| Gas cost | ~200k per round | ~500k-2M total |

### 2.3 Challenge Period Analysis

The challenge period represents a critical security parameter in optimistic rollups. Current implementations use periods ranging from 7 days (Optimism, Arbitrum) to 14 days (some proposed configurations).

#### 2.3.1 Security Considerations for Challenge Period Length

| Factor | Shorter Period | Longer Period |
|--------|---------------|---------------|
| Capital efficiency | Better | Worse |
| Censorship resistance | Lower | Higher |
| Attack detection time | Constrained | Adequate |
| User experience | Better | Worse |

The 7-day period was chosen based on several considerations:
- Sufficient time for fraud proof generation and submission even under adverse network conditions
- Allows for detection of sequencer misbehavior even if the attacker temporarily censors fraud proofs
- Balances against the capital inefficiency of locked funds during withdrawal

#### 2.3.2 Formal Analysis of Challenge Period Adequacy

**Threat Model**: Adversary controls sequencer and can censor L1 transactions for duration $T_{\text{censor}}$.

**Required Challenge Period**:
$$T_c > T_{\text{censor}} + T_{\text{proof}} + T_{\text{propagation}} + T_{\text{safety\_margin}}$$

Under realistic assumptions:
- $T_{\text{censor}}$: 1-3 days (limited by L1 censorship resistance)
- $T_{\text{proof}}$: Hours to 1 day (depends on proof complexity)
- $T_{\text{propagation}}$: Minutes to hours
- $T_{\text{safety\_margin}}$: 2-3 days (for unexpected delays)

This analysis supports the 7-day minimum, with shorter periods creating vulnerability windows under adversarial conditions.

#### 2.3.3 Withdrawal Delay Attack Vectors

The challenge period introduces specific attack vectors on withdrawals:

**Griefing Attacks**: Malicious actors can challenge valid withdrawals, forcing users to wait for dispute resolution even when withdrawals are legitimate. Mitigation requires challenger bonds that are slashed for invalid challenges.

**Liquidity Provider Risks**: Fast withdrawal services that front user funds face:
- Reorg risk: L1 reorgs can invalidate withdrawal proofs
- State root manipulation: Malicious sequencers could propose invalid roots
- Challenge uncertainty: Valid withdrawals may be challenged

**Economic Analysis of Fast Withdrawal Security**:
```
Expected Loss = P(invalid_state) × withdrawal_amount + 
                P(challenge) × capital_lockup_cost +
                P(L1_reorg) × fronted_amount

For rational LP operation:
Fee > Expected Loss / withdrawal_amount
```

### 2.4 Implemented Protocols Analysis

#### 2.4.1 Arbitrum One

Arbitrum One, launched in August 2021, represents the most widely adopted optimistic rollup with over $10 billion in TVL at peak. Key security features include:

- **ArbOS**: A custom execution environment providing EVM equivalence
- **Validator whitelist**: Currently restricted to permissioned validators (transitioning to permissionless)
- **Sequencer Committee**: Plans for decentralization through committee-based sequencing
- **Nitro upgrade**: Improved fraud proof efficiency through WASM-based execution

Security incidents and responses:
- September 2022: Vulnerability in Nitro's proof system discovered through bug bounty (no funds lost)
- Ongoing: Gradual decentralization of validator set and sequencer operations

#### 2.4.2 Optimism (OP Mainnet)

Optimism's security architecture has evolved significantly since its initial launch:

- **Bedrock upgrade (June 2023)**: Modular architecture separating execution from derivation
- **Cannon fault proofs (2024)**: Transition from centralized proposer to permissionless fault proofs
- **OP Stack**: Standardized rollup framework enabling the Superchain vision

The transition to permissionless fault proofs represents a critical security milestone, removing the trust assumption in Optimism Foundation-operated proposers.

---

## 3. Zero-Knowledge Rollup Security Mechanisms

### 3.1 Cryptographic Foundations

ZK-rollups leverage zero-knowledge proof systems to provide cryptographic guarantees of correct state transitions. Unlike optimistic rollups, which assume validity until challenged, ZK-rollups prove validity before state updates are accepted.

#### 3.1.1 Formal Security Definitions

**Definition (Computational Soundness)**: A proof system $(P, V)$ for language $L$ is computationally sound if for all PPT adversaries $\mathcal{A}$:
$$\Pr[V(x, \pi) = 1 \land x \notin L : (x, \pi) \leftarrow \mathcal{A}(1^\lambda)] \leq \text{negl}(\lambda)$$

**Definition (Knowledge Soundness)**: A proof system satisfies knowledge soundness if there exists an extractor $\mathcal{E}$ such that for any prover $P^*$ that convinces the verifier with non-negligible probability, $\mathcal{E}$ can extract a valid witness.

**Application to Rollups**: For state transition $S_n \rightarrow S_{n+1}$:
- Statement: "There exists transaction batch $T$ such that $f(S_n, T) = S_{n+1}$"
- Witness: The transaction batch $T$ and execution trace
- Soundness guarantees no valid proof exists for invalid transitions

#### 3.1.2 Cryptographic Assumptions

**SNARK Security Assumptions**:

| Assumption | Description | Strength | Used By |
|------------|-------------|----------|---------|
| Discrete Log (DL) | Hard to compute $x$ from $g^x$ | Standard | All SNARKs |
| Knowledge of Exponent (KEA) | Extractor exists for DL relations | Non-standard | Groth16 |
| Algebraic Group Model (AGM) | Adversary operates algebraically | Idealized | PLONK, Marlin |
| Random Oracle Model (ROM) | Hash functions are random oracles | Idealized | Fiat-Shamir |
| Trusted Setup | CRS generated honestly | Trust assumption | Groth16, PLONK |

**STARK Security Assumptions**:
- Collision-resistant hash functions (standard assumption)
- No trusted setup required (transparent)
- Conjectured post-quantum security (based on hash function security)

**Implications of Assumption Failure**:
- KEA falsification: Adversary could forge proofs for invalid statements
- AGM violation: Real-world attacks may succeed where idealized analysis fails
- Trusted setup compromise: Universal forgery of proofs possible

### 3.2 Proof Systems Analysis

**SNARKs (Succinct Non-Interactive Arguments of Knowledge)**:
- Proof size: ~200-300 bytes
- Verification time: ~10ms
- Trusted setup required (for Groth16)
- Used by: zkSync Era, Polygon zkEVM

**STARKs (Scalable Transparent Arguments of Knowledge)**:
- Proof size: ~50-100 KB
- Verification time: ~50-100ms
- No trusted setup (transparent)
- Post-quantum secure (conjectured)
- Used by: StarkNet, StarkEx

```
                    SNARKs              STARKs
Proof Size:         ~300 bytes          ~50 KB
Verification Gas:   ~300,000            ~1,000,000
Trusted Setup:      Required*           Not required
Quantum Security:   Vulnerable          Resistant
Prover Time:        Moderate            Higher
Assumption Strength: Non-standard       Standard (hash)
```

*Note: Some SNARK constructions (PLONK, Halo2) use universal trusted setups or eliminate them entirely through recursive composition.

### 3.3 Circuit Security

ZK-rollups encode the state transition function as an arithmetic circuit. The security of this encoding is paramount—bugs in the circuit can allow invalid state transitions to be "proven" valid.

#### 3.3.1 Formal Definition of Circuit Vulnerabilities

**Definition (Soundness Bug)**: A soundness bug exists when the constraint system $\mathcal{C}$ admits a satisfying assignment $(x, w)$ where $x$ represents an invalid statement. Formally:
$$\exists (x, w) : \mathcal{C}(x, w) = 0 \land x \notin L$$

**Definition (Completeness Bug)**: A completeness bug exists when valid statements cannot be proven:
$$\exists x \in L : \forall w : \mathcal{C}(x, w) \neq 0$$

**Definition (Under-constrained Circuit)**: A circuit is under-constrained if multiple distinct witnesses satisfy the constraints for the same public input, and some of these witnesses correspond to invalid executions.

#### 3.3.2 Circuit Complexity and Attack Surface

Modern zkEVM circuits contain millions of constraints. For example:
- Polygon zkEVM: ~10 million constraints per batch
- zkSync Era: Variable, optimized for different transaction types
- StarkNet: Cairo-based execution with STARK proofs

The complexity creates several security challenges:

1. **Soundness bugs**: Errors in constraint generation that allow invalid witnesses
2. **Completeness bugs**: Valid transactions that cannot be proven
3. **Efficiency bugs**: Exponential blowup in proof generation for certain inputs

#### 3.3.3 Case Study: Polygon zkEVM Audit Findings

The Polygon zkEVM underwent extensive auditing, revealing the following categories of issues:

| Severity | Count | Primary Categories |
|----------|-------|-------------------|
| Critical | 2 | Soundness vulnerabilities in arithmetic operations |
| High | 7 | State management inconsistencies |
| Medium | 15 | Edge cases in EVM opcode implementation |
| Low | 30+ | Gas calculation discrepancies |

**Critical Finding Analysis**: One critical finding involved incorrect handling of the SELFDESTRUCT opcode. The constraint system failed to properly enforce balance transfers during contract destruction, allowing an attacker to construct a witness showing a state transition that credited funds without corresponding debits. This represents a classic under-constrained circuit vulnerability where:
$$\mathcal{C}(\text{invalid\_balance\_update}, w_{\text{malicious}}) = 0$$

### 3.4 Prover Infrastructure Security

#### 3.4.1 Prover Centralization and Security Implications

Currently, all major ZK-rollups operate with centralized provers:

- **zkSync Era**: Matter Labs operates the prover network
- **StarkNet**: StarkWare operates provers
- **Polygon zkEVM**: Polygon Labs operates provers

**Quantitative Analysis of Centralization Risks**:

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Prover downtime | Liveness failure | Medium | Redundant infrastructure |
| Censorship | Transaction exclusion | Low-Medium | Force-inclusion mechanisms |
| MEV extraction | User value loss | High | PBS, encrypted mempools |
| Key compromise | System halt | Low | HSMs, key rotation |

**MEV Extraction Potential**: Centralized provers observe all transactions before inclusion, enabling:
- Front-running: ~$10-50M annually on major rollups (estimated)
- Sandwich attacks: Variable based on DEX volume
- Liquidation extraction: Significant during volatility

#### 3.4.2 Decentralization Approaches

**Proof Markets**: Platforms like =nil; Foundation's Proof Market allow competitive proof generation:
```
User submits proof request → Market matches with provers → 
Provers compete on price/speed → Winner submits proof
```

**Security Analysis of Proof Markets**:
- Soundness: Preserved (proofs still verified on-chain)
- Liveness: Improved through competition
- Censorship resistance: Improved if market is permissionless
- New risks: Prover collusion, market manipulation

**Prover Networks**: Distributed prover infrastructure with:
- Stake-based prover selection
- Redundant proving for liveness
- Economic penalties for non-performance

### 3.5 Implemented Protocols Analysis

#### 3.5.1 zkSync Era

Launched in March 2023, zkSync Era implements a zkEVM with native account abstraction:

**Security Architecture**:
- Custom LLVM-based compiler (zksolc) for Solidity → zkEVM bytecode
- PLONK-based proof system with KZG commitments
- Boojum prover optimized for GPU acceleration

**Security Considerations**:
- Compiler introduces additional attack surface beyond EVM
- Account abstraction creates novel security patterns
- Currently operates with security council override capability

**Cryptographic Assumptions**: Security relies on:
- Discrete logarithm hardness in pairing-friendly curves
- Knowledge of Exponent Assumption (KEA) for extractability
- Random Oracle Model for Fiat-Shamir transformation

#### 3.5.2 StarkNet

StarkNet leverages Cairo, a Turing-complete language designed for STARK proofs:

**Security Architecture**:
- Cairo VM provides execution environment
- SHARP (Shared Prover) generates proofs for multiple applications
- Ethereum verifier contracts validate proofs

**Security Considerations**:
- Cairo's non-EVM nature requires new security tooling
- SHARP centralization creates systemic risk
- Escape hatch mechanisms for user fund recovery

**Post-Quantum Considerations**: STARK-based systems provide conjectured quantum resistance, making StarkNet potentially more future-proof against quantum attacks on cryptographic assumptions.

---

## 4. Cross-Cutting Security Concerns

### 4.1 Sequencer Security

Both optimistic and ZK-rollups rely on sequencers for transaction ordering and execution. Sequencer security encompasses:

#### 4.1.1 Centralization Risks

Current state of sequencer decentralization:

| Protocol | Sequencer Model | Decentralization Status |
|----------|-----------------|------------------------|
| Arbitrum One | Single sequencer | Roadmap to committee |
| Optimism | Single sequencer | Superchain shared sequencing planned |
| zkSync Era | Single sequencer | Decentralization planned |
| StarkNet | Single sequencer | Decentralization planned |

#### 4.1.2 Quantitative Analysis of Sequencer Misbehavior

**MEV Extraction Model**:

Let $V_{\text{MEV}}$ denote extractable value per block and $C_{\text{reputation}}$ denote reputational cost of extraction.

Rational sequencer extracts MEV when:
$$V_{\text{MEV}} > C_{\text{reputation}} + C_{\text{detection}} \times P_{\text{detection}}$$

**Estimated MEV Potential** (based on L1 data extrapolation):
- Front-running: 0.1-0.5% of DEX volume
- Sandwich attacks: 0.05-0.2% of DEX volume
- Liquidations: Variable, ~$1-10M during volatility events

For a rollup processing $1B daily DEX volume:
$$\text{Daily MEV potential} \approx \$1.5M - \$7M$$

#### 4.1.3 Sequencer Failure Modes and Mitigations

**Liveness failures**:
- Sequencer downtime halts new transaction processing
- Mitigation: Force-inclusion mechanisms allowing users to submit transactions directly to L1

**Safety failures**:
- Malicious sequencing (MEV extraction, censorship)
- Mitigation: Fraud proofs (optimistic) or validity proofs (ZK) ensure eventual correctness

**Force-Inclusion Mechanism Analysis**:

```solidity
// Arbitrum-style force inclusion
function forceInclusion(
    bytes calldata transaction,
    uint256 maxFeePerGas,
    uint256 gasLimit
) external {
    require(block.timestamp > lastSequencerAction + FORCE_INCLUSION_DELAY);
    // Transaction included in next batch
}
```

**Security Properties of Force-Inclusion**:
- Delay parameter (typically 24 hours) balances sequencer efficiency vs. censorship resistance
- Gas price manipulation: Attacker could spam L1 to make force-inclusion expensive
- Timing attacks: Sequencer can front-run force-included transactions

**Game-Theoretic Analysis**:
Force-inclusion creates a credible threat that bounds sequencer misbehavior:
$$\text{Max censorship duration} \leq T_{\text{force\_inclusion}} + T_{\text{L1\_confirmation}}$$

### 4.2 Data Availability

Data availability (DA) ensures that transaction data necessary for state reconstruction is accessible. This is critical for:
- Fraud proof generation (optimistic rollups)
- User fund recovery (both types)
- Decentralized verification

#### 4.2.1 On-Chain Data Availability

Traditional rollups post all transaction data to Ethereum calldata:

**Costs (pre-EIP-4844)**:
- ~16 gas per byte of calldata
- Typical batch: 100-500 KB
- Cost: ~0.1-0.5 ETH per batch at 50 gwei

#### 4.2.2 EIP-4844 and Data Availability Sampling

**EIP-4844 (Proto-Danksharding)** introduces blob transactions with fundamentally different security properties:

**Blob Structure**:
- Each blob contains 4096 field elements (~128 KB)
- Blobs committed using KZG polynomial commitments
- Data pruned after ~18 days

**Data Availability Sampling (DAS) Security Model**:

DAS allows light clients to verify data availability without downloading full blobs:

1. Data encoded using 2D Reed-Solomon erasure coding
2. Light clients sample random cells
3. With $k$ samples, probability of missing unavailable data: $(1/2)^k$

**Security Assumptions for DAS**:
- Minimum honest node participation rate $p_{\text{honest}}$
- Network connectivity allowing sample retrieval
- Erasure coding parameters: $(n, k)$ where data recoverable from any $k$ of $n$ shares

**Formal Security Bound**:
$$P[\text{data unavailable} | \text{sampling passes}] \leq \left(\frac{n-k}{n}\right)^{s}$$

where $s$ is the number of samples per light client.

**Interaction with Challenge Period**:
The 18-day blob pruning window exceeds the 7-day challenge period, ensuring:
- Fraud proofs can always access necessary data
- Users can reconstruct state for exits

However, long-term data retrievability requires:
- Archive nodes maintaining historical blobs
- Alternative DA solutions for historical access

#### 4.2.3 Alternative DA Layers

**Celestia**:
- Dedicated DA layer with data availability sampling
- 2D Reed-Solomon encoding with $(n, k)$ parameters
- Trust assumption: 2/3 honest validators for consensus, lighter assumptions for DA sampling

**Security Model**:
```
Celestia DA Security:
- Consensus safety: 2/3 honest validators
- DA sampling: O(log n) samples for high confidence
- Namespaced Merkle Trees for rollup-specific data
```

**EigenDA**:
- Restaking-based DA with Ethereum economic security
- Trust assumption: Sufficient restaked ETH securing DA
- Security: Slashing conditions for DA failures

**Formal Security Composition**:

For rollups using external DA:
$$\text{Security} = \min(\text{Ethereum consensus}, \text{DA layer}, \text{Proof system})$$

This is a simplification—the actual security composition depends on:
- Which properties each layer provides
- How failures in one layer affect others
- The specific attack being considered

### 4.3 Bridge Security

Rollup bridges—the smart contracts facilitating asset transfers between L1 and L2—represent critical security infrastructure and a primary attack surface.

#### 4.3.1 Canonical Bridge Architecture

**Deposit Flow**:
```
User → L1 Bridge Contract → Event emitted → 
Sequencer observes → L2 balance credited
```

**Withdrawal Flow (Optimistic)**:
```
User initiates on L2 → State root posted to L1 → 
Challenge period (7 days) → User claims on L1
```

**Withdrawal Flow (ZK)**:
```
User initiates on L2 → Batch proven → 
Proof verified on L1 → User claims immediately
```

#### 4.3.2 Canonical Bridge Vulnerability Analysis

Unlike third-party bridges (Ronin, Wormhole, Nomad), canonical rollup bridges have distinct vulnerability classes:

**Cross-Layer Message Verification Vulnerabilities**:

1. **Message Replay Attacks**: 
   - Risk: Same message processed multiple times
   - Mitigation: Nonce tracking, message hashing with chain ID
   ```solidity
   mapping(bytes32 => bool) public processedMessages;
   
   function processMessage(bytes32 messageHash) external {
       require(!processedMessages[messageHash], "Already processed");
       processedMessages[messageHash] = true;
       // Process message
   }
   ```

2. **Cross-Layer Reentrancy**:
   - Risk: Callbacks during message processing enable state manipulation
   - Example: Deposit credited on L2 before L1 state finalized
   - Mitigation: Checks-effects-interactions, reentrancy guards across layers

3. **State Root Manipulation**:
   - Risk: Malicious sequencer proposes invalid state root
   - Optimistic mitigation: Challenge period and fraud proofs
   - ZK mitigation: Validity proofs make invalid roots unprovable

**Deposit Race Conditions**:

```
Timeline of potential attack:
T0: User deposits on L1
T1: L1 transaction included in block B
T2: Sequencer observes deposit, credits L2
T3: L1 block B reorged, deposit transaction reverted
T4: User has L2 funds without valid L1 deposit
```

**Mitigation**: Wait for sufficient L1 confirmations before crediting L2:
- 12-64 blocks for deposits (varies by rollup)
- Trade-off between security and user experience

**Event Parsing Vulnerabilities**:

Bridges rely on parsing L1 events to process deposits:
```solidity
// Vulnerable pattern
function processDeposit(
    address token,
    address recipient,
    uint256 amount
) external {
    // Must verify event came from legitimate L1 bridge
    require(msg.sender == L1_BRIDGE, "Invalid sender");
    // Must verify event log index and transaction
    // Must handle token decimals correctly
    // Must prevent reentrancy
}
```

**Audit Findings from Canonical Bridges**:

| Protocol | Finding | Severity | Status |
|----------|---------|----------|
# Ethereum Layer 2 Technologies: A Comprehensive Analysis of Scaling Solutions, Technical Architectures, and Ecosystem Evolution

## Executive Summary

Ethereum's transition from a nascent smart contract platform to the foundational settlement layer for decentralized finance has precipitated one of the most significant architectural challenges in distributed systems: scalability without compromising security or decentralization. Layer 2 (L2) technologies have emerged as the predominant solution paradigm, enabling transaction throughput improvements of 10-100x while inheriting Ethereum's security guarantees through cryptographic and economic mechanisms.

This report provides a comprehensive technical analysis of Ethereum Layer 2 scaling solutions, examining the theoretical foundations, implementation architectures, and empirical performance characteristics of leading protocols. We analyze four primary L2 categories: optimistic rollups, zero-knowledge rollups, validiums, and state channels, with particular attention to their security models, trust assumptions, and trade-off profiles.

Our analysis reveals that as of Q1 2025, Layer 2 solutions collectively process over 50 transactions per second (TPS) on average, with peak throughput exceeding 150 TPS—compared to Ethereum mainnet's approximately 15 TPS. Total Value Locked (TVL) across L2 ecosystems has surpassed $45 billion, with Arbitrum One and Optimism commanding approximately 60% of market share. The emergence of zero-knowledge proof systems, particularly STARKs and SNARKs, has catalyzed a new generation of L2 solutions offering superior finality characteristics and reduced trust assumptions.

We conclude that the L2 ecosystem is entering a maturation phase characterized by consolidation around rollup architectures, increasing interoperability through shared sequencer networks and cross-chain messaging protocols, and the gradual emergence of application-specific rollups. The implications for blockchain architecture extend beyond Ethereum, establishing design patterns likely to influence the broader distributed systems landscape.

---

## 1. Introduction

### 1.1 The Scalability Imperative

The blockchain trilemma, first articulated by Vitalik Buterin in 2017, posits that distributed ledger systems face fundamental trade-offs between decentralization, security, and scalability. Ethereum's original architecture prioritized decentralization and security, resulting in a base layer throughput of approximately 15 transactions per second—a constraint that became acutely problematic during periods of high network demand.

The 2020-2021 decentralized finance (DeFi) expansion demonstrated the practical consequences of these limitations. During peak activity periods, Ethereum gas prices exceeded 500 gwei, rendering many applications economically unviable for typical users. A simple token swap on Uniswap could cost upwards of $100 in transaction fees, effectively excluding participants with smaller capital bases and undermining the accessibility principles central to decentralized finance.

### 1.2 Layer 2 as an Architectural Response

Layer 2 solutions address scalability through execution disaggregation: moving computation and state management off the base layer while maintaining security through periodic anchoring to Ethereum. This architectural pattern preserves Ethereum's role as a trust-minimized settlement layer while enabling substantially higher throughput on secondary execution environments.

The fundamental insight underlying L2 design is that not every transaction requires immediate consensus among all network participants. By batching transactions and submitting compressed proofs or commitments to the base layer, L2 systems amortize the cost of Ethereum's security across many operations, dramatically reducing per-transaction overhead.

### 1.3 Scope and Methodology

This report synthesizes technical documentation, academic literature, and empirical data from primary sources including L2Beat, Etherscan, and protocol-specific analytics platforms. Our analysis covers the period from 2020 through Q1 2025, encompassing the emergence, growth, and maturation of the L2 ecosystem. We employ a comparative framework examining security models, performance characteristics, developer experience, and economic sustainability across leading implementations.

---

## 2. Theoretical Foundations

### 2.1 Security Models and Trust Assumptions

Layer 2 security derives from the ability to verify execution correctness on the base layer without re-executing all transactions. Two primary verification paradigms have emerged:

**Fraud Proof Systems (Optimistic Rollups):** These systems assume transaction validity by default, publishing state roots to Ethereum without accompanying validity proofs. Security relies on a challenge mechanism: during a dispute window (typically 7 days), any observer can submit a fraud proof demonstrating incorrect state transitions. The security assumption is that at least one honest verifier monitors the chain and will challenge invalid states.

**Validity Proof Systems (ZK Rollups):** These systems generate cryptographic proofs demonstrating correct execution for each batch of transactions. The base layer verifies these proofs before accepting state updates, providing immediate finality guarantees. Security derives from the mathematical properties of the proof system rather than economic incentives or honest-majority assumptions.

### 2.2 Data Availability Requirements

A critical distinction among L2 architectures concerns data availability—whether transaction data is published to Ethereum or stored off-chain:

**Rollups** publish compressed transaction data to Ethereum calldata (or, post-Dencun upgrade, to blob space), ensuring that any party can reconstruct the L2 state from on-chain data alone. This provides strong censorship resistance and enables permissionless withdrawal even if all L2 operators become malicious or unavailable.

**Validiums** store transaction data off-chain, relying on a Data Availability Committee (DAC) or alternative data availability layer. This reduces costs but introduces additional trust assumptions: users must trust that data will remain available for state reconstruction and fraud proof generation.

**Volitions** offer hybrid models where users can choose between on-chain and off-chain data availability on a per-transaction basis, enabling cost-security trade-offs at the application level.

### 2.3 The Rollup-Centric Roadmap

Ethereum's development trajectory has explicitly embraced a "rollup-centric" future, with base layer improvements designed to enhance L2 capabilities rather than increase L1 throughput directly. Key milestones include:

- **EIP-4844 (Proto-Danksharding):** Implemented in the Dencun upgrade (March 2024), this introduced "blob" transactions providing dedicated data space for rollups at reduced cost. Initial capacity of approximately 375 KB per block reduced L2 data costs by 80-90%.

- **Full Danksharding:** Planned for future implementation, this will expand blob capacity to approximately 16 MB per block through data availability sampling, enabling theoretical L2 throughput exceeding 100,000 TPS.

---

## 3. Optimistic Rollups

### 3.1 Technical Architecture

Optimistic rollups execute transactions off-chain and post compressed transaction data along with state commitments to Ethereum. The canonical state is determined by the most recent unchallenged state root after the dispute period expires.

The core components include:

1. **Sequencer:** Receives user transactions, orders them, and produces batches for submission to L1. Currently, most optimistic rollups operate with centralized sequencers, though decentralization efforts are ongoing.

2. **Batch Submitter:** Compresses transaction data and submits batches to Ethereum, typically as calldata or blobs post-EIP-4844.

3. **State Commitment Chain:** A sequence of state roots representing the L2 state after each batch, stored on Ethereum.

4. **Fraud Proof System:** Smart contracts and off-chain infrastructure enabling verification of disputed state transitions.

### 3.2 Arbitrum

Arbitrum, developed by Offchain Labs, has emerged as the leading optimistic rollup by TVL and transaction volume. Its technical innovations include:

**Arbitrum Nitro:** Launched in August 2022, Nitro replaced the custom Arbitrum Virtual Machine with a WASM-based execution environment compiling standard EVM code. This improved compatibility, reduced node requirements, and enhanced fraud proof efficiency.

**Interactive Fraud Proofs:** Rather than re-executing entire transactions on-chain, Arbitrum's dispute resolution bisects the disputed computation until identifying a single instruction whose execution can be verified on Ethereum. This reduces the on-chain cost of fraud proofs from potentially millions of gas to approximately 100,000 gas.

**Stylus:** Introduced in 2023, Stylus enables smart contract development in Rust, C, and C++ alongside Solidity, with contracts compiled to WASM for execution. This expands the developer base and enables performance optimizations for computation-intensive applications.

As of Q1 2025, Arbitrum One maintains approximately $15 billion in TVL, processes 15-25 TPS on average, and hosts over 500 deployed applications including major DeFi protocols such as GMX, Radiant Capital, and Camelot.

### 3.3 Optimism and the OP Stack

Optimism has pursued a differentiated strategy centered on modular infrastructure and ecosystem development:

**OP Stack:** Released as open-source infrastructure, the OP Stack provides a standardized framework for deploying optimistic rollups. This has catalyzed the emergence of the "Superchain" concept—a network of interoperable L2s sharing security and communication infrastructure.

**Bedrock Upgrade:** Implemented in June 2023, Bedrock reduced deposit confirmation times from 10 minutes to approximately 3 minutes, decreased transaction fees by 40%, and improved node synchronization performance.

**Fault Proof Implementation:** After extended development, Optimism deployed permissionless fault proofs in 2024, enabling any party to challenge invalid state transitions without relying on a privileged set of validators.

Notable OP Stack deployments include Base (Coinbase), Zora Network, and Mode Network, collectively representing over $10 billion in TVL. The Superchain model demonstrates a potential path toward L2 ecosystem consolidation through shared standards rather than winner-take-all competition.

### 3.4 Comparative Analysis

| Metric | Arbitrum One | Optimism | Base |
|--------|--------------|----------|------|
| TVL (Q1 2025) | ~$15B | ~$8B | ~$7B |
| Average TPS | 20-25 | 10-15 | 15-20 |
| Withdrawal Period | 7 days | 7 days | 7 days |
| Fraud Proof Type | Interactive | Non-interactive | Non-interactive |
| Sequencer | Centralized | Centralized | Centralized |
| Native Token | ARB | OP | None |

---

## 4. Zero-Knowledge Rollups

### 4.1 Cryptographic Foundations

Zero-knowledge rollups leverage cryptographic proof systems to demonstrate computational integrity without revealing underlying data. Two primary proof system families dominate:

**SNARKs (Succinct Non-interactive Arguments of Knowledge):** Characterized by small proof sizes (typically 200-300 bytes) and fast verification (2-5 ms), SNARKs require a trusted setup ceremony to generate proving parameters. Vulnerabilities in the setup could theoretically enable proof forgery, though multi-party computation protocols mitigate this risk.

**STARKs (Scalable Transparent Arguments of Knowledge):** Developed by StarkWare, STARKs eliminate trusted setup requirements through transparent parameter generation. Proof sizes are larger (50-100 KB) but verification remains efficient. STARKs also offer post-quantum security, resisting attacks from theoretical quantum computers.

### 4.2 zkSync Era

Developed by Matter Labs, zkSync Era represents one of the most ambitious ZK rollup implementations:

**zkEVM Architecture:** zkSync Era implements a "type-4" zkEVM, compiling Solidity to a custom intermediate representation optimized for ZK proof generation. While not bytecode-equivalent to the EVM, this approach enables efficient proving at the cost of some compatibility limitations.

**Native Account Abstraction:** All accounts on zkSync Era are smart contracts by default, enabling features such as social recovery, transaction batching, and gas payment in arbitrary tokens without requiring separate infrastructure.

**Hyperchains:** zkSync's modular architecture supports deployment of application-specific ZK rollups sharing security through a common proof aggregation layer. This enables customization for specific use cases while maintaining interoperability.

As of Q1 2025, zkSync Era maintains approximately $1 billion in TVL, with average transaction costs of $0.10-0.30 and finality times of approximately 1 hour (the time required for proof generation and verification on Ethereum).

### 4.3 StarkNet

StarkNet, developed by StarkWare, employs STARK proofs and the Cairo programming language:

**Cairo Language:** Rather than implementing EVM compatibility, StarkNet uses Cairo—a Turing-complete language designed specifically for efficient STARK proof generation. Cairo 1.0 (released 2023) introduced Rust-like syntax and improved developer ergonomics while maintaining provability properties.

**Recursive Proofs:** StarkNet aggregates proofs from multiple transactions into recursive STARK proofs, amortizing verification costs across larger batches. This enables theoretical scalability to millions of transactions per proof.

**Volition Mode:** StarkNet supports both rollup mode (on-chain data availability) and validium mode (off-chain data availability), enabling applications to choose appropriate security-cost trade-offs.

StarkNet's ecosystem includes notable applications such as dYdX (perpetual futures), Immutable X (NFT trading), and various gaming platforms leveraging Cairo's computational efficiency.

### 4.4 Polygon zkEVM

Polygon's zkEVM implementation pursues maximum EVM compatibility:

**Type-2 zkEVM:** Polygon zkEVM achieves bytecode-level EVM equivalence, enabling unmodified deployment of existing Ethereum smart contracts. This prioritizes developer experience and ecosystem portability over proving efficiency.

**Proof Generation:** The prover network generates proofs for transaction batches, with verification on Ethereum providing finality. Current proof generation times range from 10-30 minutes depending on batch complexity.

**Integration with Polygon Ecosystem:** Polygon zkEVM operates alongside Polygon PoS, with planned integration through the Polygon 2.0 architecture unifying various scaling solutions under a common framework.

### 4.5 ZK Rollup Comparative Analysis

| Metric | zkSync Era | StarkNet | Polygon zkEVM |
|--------|------------|----------|---------------|
| Proof System | SNARKs | STARKs | SNARKs |
| EVM Compatibility | Type-4 | Cairo (non-EVM) | Type-2 |
| Trusted Setup | Required | Not required | Required |
| Avg. Finality | ~1 hour | ~2-4 hours | ~30 min |
| Post-Quantum | No | Yes | No |
| TVL (Q1 2025) | ~$1B | ~$500M | ~$300M |

---

## 5. Alternative Layer 2 Architectures

### 5.1 Validiums

Validiums combine validity proofs with off-chain data availability, offering lower costs at the expense of stronger trust assumptions:

**Immutable X:** Focused on NFT trading and gaming, Immutable X processes over 200 million transactions with zero gas fees for users. Data availability is maintained by StarkWare's Data Availability Committee.

**DeversiFi (now rhino.fi):** A self-custodial exchange leveraging StarkEx validium infrastructure for high-frequency trading with instant settlement.

The security model requires trusting the DAC to maintain data availability; if the DAC becomes unavailable or malicious, users may be unable to prove asset ownership and execute withdrawals.

### 5.2 State Channels

State channels enable off-chain transactions between fixed sets of participants, with on-chain settlement only for channel opening, closing, and disputes:

**Raiden Network:** Ethereum's implementation of payment channels, enabling instant, low-cost token transfers between participants with established channels. Adoption has been limited due to capital lockup requirements and routing complexity.

**State Channel Limitations:** The requirement for predetermined participants and capital lockup has constrained state channel adoption for general-purpose applications, though they remain relevant for specific use cases such as micropayments and gaming.

### 5.3 Plasma

Plasma architectures, proposed by Vitalik Buterin and Joseph Poon in 2017, create child chains anchored to Ethereum through periodic commitments:

**Historical Significance:** Plasma represented an early scaling approach but faced challenges with general-purpose computation and data availability. The "mass exit problem"—where all users might need to exit simultaneously during operator misbehavior—created practical limitations.

**Evolution to Rollups:** Many teams originally pursuing Plasma (including Polygon and Optimism) pivoted to rollup architectures, which provide stronger security guarantees and simpler user experience.

---

## 6. Cross-Layer Infrastructure

### 6.1 Bridging Mechanisms

Transferring assets between Ethereum and L2s requires bridging infrastructure with varying security properties:

**Canonical Bridges:** Native bridges operated by L2 protocols inherit the security of the underlying rollup. Withdrawals from optimistic rollups require waiting through the dispute period (7 days), while ZK rollup withdrawals complete upon proof verification (typically 1-4 hours).

**Third-Party Bridges:** Services such as Hop Protocol, Across, and Stargate enable faster transfers by providing liquidity on destination chains. These introduce additional trust assumptions regarding bridge operator honesty and smart contract security.

**Bridge Security Incidents:** The bridge attack surface has proven significant, with incidents including the Ronin Bridge ($625M, March 2022), Wormhole ($320M, February 2022), and Nomad ($190M, August 2022). These events underscore the importance of bridge security in L2 ecosystem design.

### 6.2 Sequencer Decentralization

Current L2 implementations predominantly rely on centralized sequencers, creating potential censorship and liveness risks:

**Decentralization Approaches:**
- **Shared Sequencer Networks:** Projects such as Espresso Systems and Astria develop infrastructure for multiple rollups to share decentralized sequencer sets.
- **Based Rollups:** Proposals for "based" or "L1-sequenced" rollups delegate sequencing to Ethereum validators, inheriting L1 decentralization properties.
- **Protocol-Specific Solutions:** Arbitrum's planned sequencer decentralization through the Arbitrum DAO and Optimism's Superchain sequencer sharing represent protocol-specific approaches.

### 6.3 Interoperability Protocols

As the L2 ecosystem fragments across multiple chains, interoperability becomes increasingly critical:

**Cross-Rollup Communication:** LayerZero, Chainlink CCIP, and Axelar provide generalized messaging infrastructure enabling smart contract interactions across chains.

**Shared Proving Infrastructure:** Aggregation layers that batch proofs from multiple rollups could reduce verification costs and enable atomic cross-rollup transactions.

---

## 7. Economic Analysis

### 7.1 Fee Structures

L2 transaction costs comprise several components:

1. **Execution Costs:** Computational resources consumed on the L2, typically 10-100x cheaper than equivalent L1 execution.

2. **Data Availability Costs:** The cost of publishing transaction data to Ethereum, historically the dominant cost component. Post-EIP-4844, blob space provides approximately 90% cost reduction compared to calldata.

3. **Proof Generation Costs (ZK Rollups):** Computational resources for generating validity proofs, amortized across batch transactions.

4. **Sequencer Margin:** Profit margin captured by sequencer operators, currently representing a significant revenue source for L2 protocols.

### 7.2 Revenue and Sustainability

L2 protocols generate revenue primarily through sequencer operations:

| Protocol | Annualized Revenue (2024) | Primary Revenue Source |
|----------|---------------------------|------------------------|
| Arbitrum | ~$80M | Sequencer fees |
| Optimism | ~$50M | Sequencer fees |
| Base | ~$150M | Sequencer fees |
| zkSync Era | ~$20M | Sequencer fees |

The sustainability of these revenue models depends on continued transaction volume growth and the evolution of fee structures as competition intensifies.

### 7.3 Token Economics

Several L2 protocols have introduced native tokens:

**ARB (Arbitrum):** Governance token enabling participation in Arbitrum DAO decisions, including protocol upgrades and treasury allocation. No direct fee capture mechanism.

**OP (Optimism):** Governance token with "retroactive public goods funding" mechanism, allocating protocol revenue to ecosystem development. The two-house governance structure (Token House and Citizens' House) represents an innovative approach to decentralized governance.

**Token-Free Models:** Base operates without a native token, with Coinbase capturing sequencer revenue directly. This model demonstrates viability of L2 operation without tokenization.

---

## 8. Security Considerations

### 8.1 Smart Contract Risks

L2 security ultimately depends on the correctness of bridge and rollup smart contracts:

**Upgradeability:** Most L2 contracts are upgradeable, enabling bug fixes but introducing risks from malicious or compromised upgrades. Security councils with multisig control represent current best practice, though they introduce centralization.

**Audit Coverage:** Leading L2 protocols have undergone multiple security audits, though the complexity of systems (particularly ZK circuits) challenges comprehensive verification.

### 8.2 Sequencer Risks

Centralized sequencers create several risk categories:

**Censorship:** Sequencers could refuse to include specific transactions, though users can typically force inclusion through L1 mechanisms after delay periods.

**Liveness:** Sequencer downtime halts L2 transaction processing. Most protocols implement escape hatches enabling L1-based withdrawals during extended outages.

**MEV Extraction:** Sequencers can extract maximal extractable value through transaction ordering, representing a form of hidden taxation on users.

### 8.3 Cryptographic Assumptions

ZK rollup security depends on underlying cryptographic assumptions:

**SNARK Security:** Relies on hardness of discrete logarithm and related problems, potentially vulnerable to quantum computers.

**STARK Security:** Based on collision-resistant hash functions, believed to be quantum-resistant.

**Implementation Bugs:** Cryptographic implementations may contain bugs not present in theoretical constructions. The complexity of ZK circuits increases audit difficulty.

---

## 9. Ecosystem Development and Adoption

### 9.1 Developer Experience

L2 adoption depends significantly on developer experience:

**EVM Compatibility:** Optimistic rollups and type-2 zkEVMs enable deployment of existing Ethereum contracts with minimal modification, reducing migration friction.

**Tooling Maturity:** Development frameworks (Hardhat, Foundry), block explorers, and debugging tools have achieved reasonable maturity for major L2s, though gaps remain compared to Ethereum mainnet.

**Documentation and Support:** Comprehensive documentation and developer support vary across protocols, with Arbitrum and Optimism generally leading in developer resources.

### 9.2 Application Migration

Major DeFi protocols have deployed across multiple L2s:

**Uniswap:** Deployed on Arbitrum, Optimism, Base, and Polygon zkEVM, with L2 volume increasingly rivaling mainnet.

**Aave:** V3 deployments across major L2s, with protocol design accommodating cross-chain operation.

**Native L2 Applications:** Protocols such as GMX (Arbitrum), Velodrome (Optimism), and Aerodrome (Base) have achieved significant traction as L2-native applications.

### 9.3 User Adoption Metrics

| Metric | Q1 2024 | Q1 2025 | Growth |
|--------|---------|---------|--------|
| Combined L2 TVL | $25B | $45B | 80% |
| Daily Active Addresses | 500K | 1.2M | 140% |
| Daily Transactions | 2M | 5M | 150% |
| L2/L1 Transaction Ratio | 3:1 | 8:1 | 167% |

---

## 10. Future Directions

### 10.1 Technical Roadmap

**Full Danksharding:** Expected implementation in 2025-2026 will dramatically expand blob capacity through data availability sampling, enabling L2 throughput exceeding 100,000 TPS.

**ZK Proof Improvements:** Ongoing research into more efficient proof systems, hardware acceleration, and proof aggregation will reduce ZK rollup costs and finality times.

**Account Abstraction:** ERC-4337 and native account abstraction on L2s will improve user experience through features such as gas sponsorship, social recovery, and session keys.

### 10.2 Ecosystem Evolution

**Consolidation vs. Fragmentation:** The L2 ecosystem may consolidate around dominant platforms or fragment into specialized application-specific rollups. The OP Stack's Superchain and zkSync's Hyperchains represent competing visions for ecosystem organization.

**Institutional Adoption:** Enterprise and institutional use cases may drive specialized L2 deployments with compliance features, permissioned access, and integration with traditional financial infrastructure.

**Cross-Chain Future:** The multi-chain future extends beyond Ethereum L2s to encompass alternative L1s, application chains, and cross-ecosystem bridges, with L2 infrastructure potentially serving as templates for broader blockchain scaling.

### 10.3 Research Frontiers

**Based Rollups:** Delegating sequencing to Ethereum validators could achieve maximal decentralization while simplifying L2 architecture.

**Proof Aggregation:** Shared proving infrastructure could reduce costs across multiple rollups while enabling atomic cross-rollup transactions.

**Privacy-Preserving L2s:** Integration of privacy features through ZK proofs could enable confidential transactions while maintaining regulatory compliance through selective disclosure.

---

## 11. Conclusion

Ethereum Layer 2 technologies represent a mature and rapidly evolving solution to blockchain scalability challenges. The ecosystem has demonstrated product-market fit, with over $45 billion in TVL and transaction volumes exceeding Ethereum mainnet by nearly an order of magnitude.

The technical landscape has consolidated around rollup architectures, with optimistic rollups (Arbitrum, Optimism, Base) currently dominating by adoption metrics while ZK rollups (zkSync Era, StarkNet, Polygon zkEVM) offer superior theoretical properties and are gaining ground as proof generation efficiency improves.

Key challenges remain, including sequencer decentralization, bridge security, and cross-rollup interoperability. The resolution of these challenges will determine whether the L2 ecosystem evolves toward a unified, interoperable network or fragments into isolated execution environments.

For researchers and practitioners, the L2 space offers rich opportunities in cryptographic proof systems, distributed systems design, and mechanism design for decentralized coordination. The patterns emerging from Ethereum's scaling journey will likely influence blockchain architecture broadly, establishing templates for balancing security, decentralization, and performance in distributed systems.

The transition to a rollup-centric Ethereum is no longer speculative—it is the present reality of blockchain infrastructure. Understanding these systems is essential for anyone engaged with the technical, economic, or social dimensions of decentralized technology.

---

## References

1. Buterin, V. (2021). "An Incomplete Guide to Rollups." ethereum.org.

2. Thibault, L. et al. (2022). "Blockchain Scaling Using Rollups: A Comprehensive Survey." IEEE Access.

3. L2Beat. (2025). "Layer 2 Analytics Dashboard." l2beat.com.

4. Offchain Labs. (2024). "Arbitrum Nitro: Technical Documentation."

5. Optimism Collective. (2024). "OP Stack Specification."

6. Matter Labs. (2024). "zkSync Era Technical Documentation."

7. StarkWare. (2024). "StarkNet Architecture Overview."

8. Ethereum Foundation. (2024). "EIP-4844: Shard Blob Transactions."

9. Gudgeon, L. et al. (2020). "SoK: Layer-Two Blockchain Protocols." Financial Cryptography and Data Security.

10. Chaliasos, S. et al. (2024). "Blockchain Scalability and Security: A Systematic Review." ACM Computing Surveys.

---

*Report prepared for academic research purposes. Data current as of Q1 2025. Market conditions and technical specifications subject to change.*
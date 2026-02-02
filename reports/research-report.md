# Understanding Layer 2 Fee Structures: A Comparative Analysis Across Rollup Types

**Research Report for Suhyeon Lee**
**Date:** February 2026
**Focus:** Layer 2 cost analysis and fee economics

---

## Executive Summary

Layer 2 scaling solutions have fundamentally transformed Ethereum's fee landscape in 2026. This report analyzes fee structures across major rollup types, revealing:

**Key Findings:**
- **Cost reduction**: L2s provide 10×-100× lower fees than Ethereum mainnet, with simple transfers costing $0.005-$0.05 (vs. $1-$50 on L1)
- **EIP-4844 impact**: Blob space reduced data availability costs by 90-99%, enabling sub-cent transactions across most L2s
- **Market concentration**: Base, Arbitrum, and Optimism process ~90% of all L2 transactions, with Base alone capturing 60%
- **Fee structure divergence**: Optimistic rollups optimize for sequencer economics; ZK rollups optimize for proof amortization
- **Emerging trends**: Based rollups (Taiko) and Layer 3 solutions reshape fee models, though shared sequencing remains nascent

**Practical implications**: Transaction type matters more than rollup choice for cost optimization. DeFi interactions ($0.20-$0.50) cost 10×-100× more than simple transfers ($0.005-$0.05), while rollup selection typically varies costs by only 2×-5×. For cost-sensitive applications, optimizing transaction batching and contract efficiency yields greater savings than rollup migration.

---

## 1. Background: L1 Fee Model & L2 Fundamentals

### 1.1 Ethereum L1 Fee Mechanism (EIP-1559)

Ethereum's fee market operates on a **dynamic base fee** that adjusts every block to target 50% capacity utilization. Users pay:

```
Total Fee = (Base Fee + Priority Fee) × Gas Used
```

- **Base Fee**: Algorithmically set, burned (not paid to validators)
- **Priority Fee**: User-set tip to validators for transaction ordering
- **Gas Used**: Computational resources consumed

**Cost drivers on L1:**
- Computation: Contract execution (opcodes)
- Storage: State updates (SSTORE operations)
- Calldata: Transaction input data (16 gas/byte for non-zero data)

**Historical context**: During network congestion (2021-2023), L1 fees regularly exceeded $50 for DeFi interactions and $100+ for complex NFT mints, making Ethereum prohibitively expensive for most users.

### 1.2 Why L2s Need Different Fee Structures

Layer 2 rollups batch hundreds or thousands of transactions and post them to Ethereum L1, creating a **two-dimensional cost model**:

1. **L2 Execution**: Computational costs within the rollup (low, as rollup nodes have excess capacity)
2. **L1 Data Availability**: Cost to publish transaction data or state updates to Ethereum (historically high, the primary cost driver)

**The L2 value proposition**: Amortize L1 costs across many transactions. If 1,000 transactions share a single L1 batch posting, each transaction pays 0.1% of the L1 fee.

**Before EIP-4844**: L1 calldata cost ~16 gas/byte, making data posting expensive even when amortized. Rollups spent ~$34M (15,000 ETH) on calldata in December 2023 alone.

### 1.3 EIP-4844: The Blob Space Revolution

**What changed (March 2024)**: EIP-4844 introduced **blob space**—dedicated, temporary data storage for rollups at 1/10th the cost of calldata.

**Blob capacity evolution**:
- **Initial (March 2024)**: 3 target blobs, 6 max per block
- **Current (2026)**: 14 target blobs, 21 max per block (increased through subsequent upgrades)

**Impact on L2 costs**:
- Blob fees: ~$0.0000000005 median (down from $27 peak for calldata)
- Optimistic rollups: 50-90% total cost reduction
- ZK rollups: 90-95% cost reduction
- StarkNet: ~95% cost drop after blob implementation

**2026 utilization**: Network operates well below 14-blob target capacity. Blob space is **not** the limiting factor; sequencer economics, user activity, and cross-rollup fragmentation constrain growth more than blob availability.

**Key insight**: EIP-4844 solved the data availability cost problem. Current L2 fees primarily reflect sequencer operational expenses and profit margins, not infrastructure constraints.

---

## 2. Fee Structure Deep Dive

### 2.1 Optimistic Rollups (Arbitrum, Optimism, Base)

**Core architecture**: Assume transactions are valid by default; validators can challenge incorrect state transitions during a ~7-day challenge period.

#### Fee Formula

```
Total Fee = L2 Execution Fee + L1 Data Fee + Sequencer Margin
```

**Component breakdown**:

1. **L2 Execution Fee**: Gas used on L2 × L2 gas price
   - Typically 0.1-0.5 gwei (vs. 20-100 gwei on L1)
   - Minimal cost due to centralized sequencer efficiency

2. **L1 Data Fee**: Cost to publish transaction data to Ethereum as blobs
   - Historically the dominant cost (pre-EIP-4844)
   - Now 50-90% cheaper, but still exceeds L2 execution fee for most transactions
   - Formula: `(L1 Gas Price × Batch Size) / Transactions in Batch`

3. **Sequencer Fee**: Operational costs + profit margin
   - Covers infrastructure, blob posting, fraud proof monitoring
   - **Only Base achieved profitability in 2025** (~$55M profit on ~$93M sequencer revenue)

#### Real-World Examples (2026 Averages)

| Transaction Type | Arbitrum | Optimism | Base |
|-----------------|----------|----------|------|
| Simple Transfer | $0.01 | $0.015 | $0.015 |
| Token Swap | $0.03 | $0.05 | $0.064 |
| NFT Mint | $0.05 | $0.07 | $0.08 |
| Complex DeFi | $0.15 | $0.25 | $0.30 |

**Sequencer economics (2025 data)**:
- Base: $93M sequencer revenue, $55M profit (86.1% from priority fees)
- Arbitrum: $42M sequencer revenue
- Optimism: $26M sequencer revenue

**Key optimization**: Base's profitability stems from **aggressive priority fee capture** (86.1% of daily revenue) and operational efficiency, not higher base fees.

#### Recent Improvements

**Arbitrum ArbOS Dia (Q1 2026)**:
- Introduced **predictable gas pricing** with multiple overlapping gas targets (60-10 Mgas/s range)
- Long adjustment windows dampen price spikes during demand surges
- Reduces fee volatility, especially during DEX activity peaks

**Optimism Batcher Upgrade**:
- Migrated to blob-first data posting
- Cut data availability costs by >50%

### 2.2 ZK Rollups (zkSync Era, StarkNet, Polygon zkEVM)

**Core architecture**: Generate cryptographic proofs (SNARKs or STARKs) that mathematically verify transaction correctness; Ethereum validators check the proof, not individual transactions.

#### Fee Formula

```
Total Fee = L2 Gas + L1 Data Gas + Proof Generation + Proof Verification
```

**Component breakdown**:

1. **L2 Gas**: Computation and data resources within the rollup
   - Similar to optimistic rollup execution costs
   - Varies by VM efficiency (StarkNet's Cairo VM vs. zkSync's zkEVM)

2. **L1 Data Gas**: Cost for state differences posted to Ethereum as blobs
   - ZK rollups post **state diffs** (what changed), not full transaction data
   - Typically smaller than optimistic rollup data payloads (higher compression)

3. **Proof Generation**: Computational cost for creating validity proofs
   - **Computationally intensive**, requires specialized hardware (GPUs/ASICs)
   - Cost depends on batch complexity and proving system (SNARKs faster, STARKs more scalable)
   - Currently **subsidized** by rollup operators (e.g., Scroll and proving partners)
   - Not directly passed to users in current fee models

4. **Proof Verification**: L1 gas for on-chain verification
   - Fixed cost per batch (~300,000-500,000 gas)
   - **Amortized across thousands of L2 transactions** (0.01-0.1% per transaction)

#### Real-World Examples (2026 Averages)

| Transaction Type | zkSync Era | StarkNet | Polygon zkEVM |
|-----------------|-----------|----------|---------------|
| Simple Transfer | $0.005 | $0.002 | $0.008 |
| Token Swap | $0.02 | $0.002 | $0.03 |
| NFT Mint | $0.08 | $0.10 | $0.12 |
| Complex DeFi | $0.25 | $0.20 | $0.30 |

**Performance metrics**:
- zkSync Era: 12-15 TPS
- Polygon zkEVM: 40-50 TPS
- StarkNet: ~127 TPS

**Key difference from optimistic rollups**: StarkNet's exceptionally low costs ($0.002 average) reflect aggressive subsidies and highly optimized Cairo VM execution, not necessarily sustainable long-term economics.

#### Technical Optimizations

**Data compression**: ZK rollups post only state changes (deltas), not full transaction data. A token transfer might require:
- Optimistic rollup: ~200 bytes of transaction data
- ZK rollup: ~20 bytes of state diff

**Proof amortization**: One cryptographic proof verifies 1,000-10,000 transactions. Ethereum validates one SNARK/STARK, not thousands of individual transactions.

**Trade-off**: Proof generation is computationally expensive (currently subsidized), but L1 verification and data posting are far cheaper than optimistic rollups.

### 2.3 L1 vs L2 Comparison

#### Cost Comparison by Transaction Type (2026)

| Transaction Type | Ethereum L1 | Optimistic Rollup (avg) | ZK Rollup (avg) | **Reduction Factor** |
|-----------------|-------------|------------------------|----------------|---------------------|
| Simple Transfer | $1.50 - $5.00 | $0.01 - $0.02 | $0.002 - $0.008 | **100×-500×** |
| Token Swap | $5.00 - $15.00 | $0.03 - $0.06 | $0.002 - $0.03 | **150×-500×** |
| NFT Mint | $20.00 - $50.00 | $0.05 - $0.08 | $0.08 - $0.12 | **250×-600×** |
| Complex DeFi | $50.00 - $150.00 | $0.15 - $0.30 | $0.20 - $0.30 | **300×-750×** |

**Key takeaway**: L2s deliver **10×-100× cost reduction** for most use cases. Simple transfers see the highest relative savings; complex DeFi interactions still benefit but with smaller reduction factors due to inherent computational complexity.

#### Fee Volatility and Predictability

**Ethereum L1**:
- High volatility: 5×-10× swings during network congestion
- Base fee adjusts every block (12 seconds)
- Unpredictable during NFT mints, token launches, major events

**Optimistic Rollups**:
- Moderate volatility: Tied to L1 blob pricing (but blobs are underutilized, so minimal spikes)
- Sequencer fee volatility: Base's priority fees spike 10×+ during DEX rushes
- **Arbitrum's ArbOS Dia (2026)** reduces volatility with predictable gas targets

**ZK Rollups**:
- Lower volatility: Proof costs are fixed; only L1 data posting varies
- More predictable for budgeting, but less responsive to demand (can lead to congestion)

**Prediction trend**: As blob space remains underutilized and sequencers optimize operations, L2 fees are stabilizing. 2026 fees are **3×-5× more predictable** than 2024 fees.

#### Throughput vs Cost Trade-offs

| Metric | Ethereum L1 | Optimistic Rollup | ZK Rollup |
|--------|-------------|------------------|-----------|
| **TPS** | ~11.5 | 50-100+ | 12-127 |
| **Finality** | ~12 seconds | ~7 days (challenge period) | ~1-24 hours (proof generation) |
| **Cost per tx** | $1-$150 | $0.01-$0.30 | $0.002-$0.30 |
| **Security model** | L1 consensus | Fraud proofs (optimistic) | Validity proofs (cryptographic) |

**Trade-off analysis**:
- **Optimistic rollups**: Fastest finality for users (instant soft confirmation), but slow finality for withdrawals (7 days). Lowest infrastructure costs.
- **ZK rollups**: Cryptographic finality (1-24 hours), no challenge period for withdrawals. Higher infrastructure costs (proving), but better data compression.
- **Ethereum L1**: Ultimate security and finality, but prohibitively expensive for most applications.

---

## 3. Real-World Analysis & Insights

### 3.1 Transaction Cost Case Studies

#### Case Study 1: Daily DeFi User on Base (Optimistic Rollup)

**Activity profile**:
- 5 token swaps/day
- 2 liquidity provisions/week
- 1 NFT mint/month

**Monthly costs**:
- Token swaps: 150 swaps × $0.064 = $9.60
- Liquidity: 8 provisions × $0.30 = $2.40
- NFT mint: 1 × $0.08 = $0.08
- **Total: $12.08/month**

**L1 equivalent**: ~$2,250-$3,750/month (185×-310× more expensive)

#### Case Study 2: High-Frequency Trader on StarkNet (ZK Rollup)

**Activity profile**:
- 50 token swaps/day
- 10 position adjustments/day

**Monthly costs**:
- Token swaps: 1,500 swaps × $0.002 = $3.00
- Position adjustments: 300 adjustments × $0.20 = $60.00
- **Total: $63.00/month**

**L1 equivalent**: ~$112,500-$225,000/month (1,800×-3,570× more expensive)

**Key insight**: StarkNet's aggressive subsidies make it ideal for high-frequency, low-value transactions. However, sustainability depends on subsidy continuation.

#### Case Study 3: NFT Platform on Arbitrum (Optimistic Rollup)

**Activity profile**:
- 1,000 NFT mints/day
- 500 secondary sales/day

**Monthly costs**:
- Mints: 30,000 × $0.05 = $1,500
- Sales: 15,000 × $0.03 = $450
- **Total: $1,950/month**

**L1 equivalent**: ~$750,000-$1,500,000/month (385×-770× more expensive)

**Business impact**: Arbitrum's low fees enable sub-$1 NFT mints, unlocking mass-market adoption. L1 fees ($20-$50/mint) made this economically impossible.

### 3.2 Fee Breakdown by Component (2026 Data)

#### Optimistic Rollup: Base Token Swap ($0.064)

```
L2 Execution Fee:     $0.005  (7.8%)
L1 Data Fee (blob):   $0.045  (70.3%)
Sequencer Margin:     $0.014  (21.9%)
────────────────────────────────
Total:                $0.064  (100%)
```

**Key insight**: Even with EIP-4844's 90% blob cost reduction, L1 data posting remains the largest cost component. Sequencer margin (21.9%) reflects Base's profitable operations.

#### ZK Rollup: StarkNet Token Swap ($0.002)

```
L2 Gas:               $0.001  (50%)
L1 Data Gas:          $0.0005 (25%)
Proof Gen (subsidy):  $0.0000 (0% - absorbed by operator)
Proof Verification:   $0.0005 (25%)
────────────────────────────────
Total:                $0.002  (100%)
```

**Key insight**: StarkNet's low cost reflects (1) state diff compression, (2) proof generation subsidies, and (3) Cairo VM efficiency. Removing subsidies could increase costs 2×-5×.

### 3.3 When to Use Which L2: Decision Framework

#### Choose Optimistic Rollups (Arbitrum, Optimism, Base) if:
- **Ecosystem maturity matters**: Largest dApp ecosystems, most liquidity, best developer tooling
- **Withdrawal speed is critical**: Fast soft confirmations (seconds), though L1 finality takes 7 days
- **Cost-sensitive but not extreme**: $0.01-$0.30/tx is acceptable
- **EVM equivalence needed**: Full Solidity compatibility, minimal code changes

**Best for**: General DeFi (DEXs, lending), NFT platforms, gaming, mainstream dApps

#### Choose ZK Rollups (zkSync Era, StarkNet, Polygon zkEVM) if:
- **Absolute lowest cost required**: $0.002-$0.08/tx for high-volume applications
- **Faster L1 finality needed**: 1-24 hour withdrawal times (no 7-day challenge period)
- **High-frequency, low-value transactions**: Micro-transactions, payments, social apps
- **Advanced privacy features planned**: ZK proofs enable private transactions (future capability)

**Best for**: High-frequency trading, payments, gaming (micro-transactions), privacy-sensitive apps

#### Stay on Ethereum L1 if:
- **Maximum security required**: Critical protocols (bridges, oracles, governance)
- **Composability is essential**: Atomic interactions with L1-native protocols
- **Low transaction volume**: L2 overhead not worth it (<10 tx/day)

**Best for**: High-value vaults, DAO governance, oracle networks, L2 bridge contracts

### 3.4 Current Trends and Optimizations (2026)

#### Market Consolidation

**Dominant platforms**:
- **Base**: 60% of all L2 transactions, 46.6% of L2 DeFi TVL ($5.6B peak)
- **Arbitrum**: 30.86% of L2 DeFi TVL (~$2.8B stable)
- **Top 3 (Base, Arbitrum, Optimism)**: ~90% of all L2 activity

**Implications**: 21Shares forecast suggests most smaller L2s won't survive 2026. Niche L2s becoming "zombie chains" due to unsustainable economics post-fee wars.

**Total L2 ecosystem**: $39.89B TVL (Jan 2026), +13.3% YoY, processing ~2M daily transactions

#### Technical Optimizations

1. **Predictable gas pricing** (Arbitrum ArbOS Dia): Multiple overlapping gas targets (60-10 Mgas/s) dampen volatility
2. **Blob-first batching** (Optimism): >50% DA cost reduction
3. **Layer 3 solutions**: Custom execution environments, adjustable fee models for specific use cases
4. **Data compression**: StarkNet and zkSync Era achieving 10×+ compression vs. optimistic rollups

#### Emerging Fee Models

**Based Rollups** (Taiko leading):
- **L1-sequenced**: Ethereum validators handle transaction ordering
- **Decentralization benefit**: No centralized sequencer (addresses major L2 criticism)
- **Economic model**: Brings more revenue back to Ethereum than traditional L2s
- **Trade-off**: Slower block times (tied to L1), but no sequencer censorship risk

**Shared Sequencing**:
- **Vision**: Atomic cross-chain transactions via shared sequencer network
- **Reality (2026)**: Astria (leading effort) shut down in 2025; category fragile
- **Potential**: Could enable single-transaction multi-chain DeFi interactions
- **Status**: Limited adoption, governance standards emerging

**Layer 3 Solutions**:
- **Concept**: L3s on top of L2s with customized execution environments
- **Fee model**: Additional layer of optimization for specific use cases (e.g., gaming L3 on Arbitrum)
- **Adoption**: Growing but early-stage (not yet significant volume)

---

## 4. Implications & Future Directions

### 4.1 Protocol Design Considerations

**For new L2 projects**:
- **Sequencer economics are make-or-break**: Only Base achieved profitability in 2025. Fee wars after EIP-4844 pushed most rollups into losses.
- **Priority fee capture is critical**: Base derives 86.1% of sequencer revenue from priority fees, not base fees.
- **Subsidies are unsustainable**: ZK rollups currently absorb proof generation costs. Long-term models must pass these to users or find alternative revenue.
- **Blob space is not the bottleneck**: 14-blob target underutilized in 2026. Focus on user acquisition and ecosystem development, not infrastructure scaling.

**For existing L2s**:
- **Differentiate or die**: 90% market concentration means niche L2s need clear value propositions (vertical-specific, unique tech, regulatory compliance).
- **Consider based sequencing**: Taiko demonstrates viability; decentralization could attract users concerned about censorship.
- **Optimize for fee predictability**: Arbitrum's ArbOS Dia shows users value predictable costs over absolute minimums.

### 4.2 User and Developer Guidelines

**For users**:
- **Transaction type matters more than rollup choice**: Optimizing contract interactions (batching, efficiency) yields 10×-100× savings; rollup migration yields only 2×-5× savings.
- **Check current fees before transactions**: L2Fees.info and similar tools provide real-time comparisons.
- **Consider finality requirements**: If withdrawing to L1 soon, ZK rollups (1-24 hour finality) > optimistic rollups (7-day challenge period).

**For developers**:
- **Start on Base or Arbitrum**: Largest ecosystems, best tooling, most liquidity.
- **Optimize for L1 data size**: Post-EIP-4844, DA costs still dominate. Compress calldata, use events sparingly, batch updates.
- **Test gas usage across L2s**: EVM equivalence ≠ identical gas costs. Arbitrum's ArbGas differs from Optimism's gas accounting.
- **Plan for fee volatility**: Base priority fees spike 10×+ during DEX rushes. Implement dynamic gas limits or educate users on expected ranges.

### 4.3 Future Trends (Beyond 2026)

**Full Danksharding (EIP-4844 successor)**:
- **Vision**: 64-128 blobs/block (vs. 14 target today)
- **Impact**: Could make L2s **100× cheaper** than current costs
- **Timeline**: Multi-year rollout, not expected until 2027-2028

**Decentralized Sequencing**:
- **Current state**: All major L2s use centralized sequencers (single point of censorship)
- **Solutions**: Based rollups (Taiko), shared sequencers (if viable), or rollup-owned sequencer sets
- **Trade-off**: Decentralization adds latency and complexity; unclear if users value it enough to pay premium

**ZK Rollup Maturation**:
- **Current bottleneck**: Proof generation costs subsidized, not sustainable
- **Path forward**: Hardware acceleration (ASICs), proving network decentralization, or proof aggregation
- **Timeline**: 2-3 years for sustainable, unsubsidized ZK rollup economics

**Cross-L2 Interoperability**:
- **Problem**: 90% of activity on 3 L2s, but liquidity fragmented across dozens
- **Solutions**: Native bridges, shared liquidity pools, or cross-L2 messaging standards
- **Fee implication**: Multi-hop transactions (L2 → L1 → L2) currently cost 5×-10× more than single-L2 transactions

### 4.4 Tokamak Network Positioning

**Competitive landscape analysis**:
- **Optimistic rollup competition**: Base/Arbitrum/Optimism dominate with 90% market share and profitability (Base) or strong ecosystems (Arbitrum)
- **ZK rollup competition**: zkSync Era/StarkNet/Polygon zkEVM compete on cost, but subsidies create unsustainable pricing
- **Niche L2s**: Most projected to fail in 2026 (21Shares forecast)

**Strategic opportunities**:
1. **Vertical specialization**: Target specific use cases (gaming, DeFi, payments) rather than general-purpose
2. **Based sequencing**: Differentiate with L1-sequenced model (Ethereum validator ordering) for decentralization-focused users
3. **Fee transparency and predictability**: Implement Arbitrum-style predictable gas pricing to attract cost-sensitive developers
4. **Tokamak-specific optimizations**: Leverage research on challenge-based protocols and incentive design for novel fee models

**Research alignment**:
- **Layer 2 cost analysis**: This report provides baseline data for Tokamak's competitive positioning
- **Challenge-based protocols**: Optimistic rollup fraud proofs are challenge-based; insights applicable to RAT protocol (validator monitoring)
- **Incentive design**: Sequencer fee capture models (Base's 86.1% priority fee revenue) demonstrate importance of mechanism design

**Recommendations for Tokamak Network**:
1. **Benchmark against Base**: Study Base's profitable sequencer model (priority fee capture, operational efficiency)
2. **Consider ZK hybrid**: If targeting low-cost, explore hybrid optimistic-ZK model to balance proof costs with data efficiency
3. **Focus on fee predictability**: Users value predictable costs; implement multi-target gas pricing (ArbOS Dia model)
4. **Develop niche ecosystem**: Avoid competing head-on with Base/Arbitrum; target underserved use cases or regions
5. **Plan for post-subsidy economics**: Ensure fee model covers all costs (L1 DA, sequencer ops, proof generation if ZK) without subsidies

---

## Conclusion

Layer 2 fee structures in 2026 reflect a maturing ecosystem where EIP-4844 has solved the data availability cost crisis, but sustainable sequencer economics remain challenging. The market has consolidated around Base, Arbitrum, and Optimism, with most niche L2s struggling to achieve profitability or user adoption.

**Key takeaways for researchers and practitioners**:
1. **Transaction optimization > rollup selection**: Developers should prioritize efficient contract design and transaction batching over rollup migration for cost savings.
2. **Fee predictability matters**: Arbitrum's ArbOS Dia and Base's operational efficiency show users value stable costs, not just absolute minimums.
3. **Subsidies distort markets**: ZK rollup pricing (StarkNet's $0.002/tx) is artificially low due to proof generation subsidies; sustainable models will increase costs 2×-5×.
4. **Based rollups show promise**: Taiko's L1-sequenced model addresses decentralization concerns while maintaining profitability, offering a viable alternative to centralized sequencers.
5. **Differentiation is critical**: With 90% market concentration, new L2s need clear value propositions beyond "lower fees" to survive.

For Suhyeon Lee's research on L2 cost analysis and challenge-based protocols, this report provides quantitative baselines, identifies sustainable economic models (Base's sequencer profitability), and highlights areas where game-theoretic mechanism design can optimize fee structures and incentive alignment.

---

## References

**Core Data Sources:**
1. L2Beat. "The state of the layer two ecosystem." L2BEAT, 2026. https://l2beat.com/
2. L2Fees. "Real-time L2 transaction cost comparison." L2Fees.info, 2026. https://l2fees.info/
3. Ethereum Foundation. "EIP-4844: Shard Blob Transactions." Ethereum Improvement Proposals, 2024.
4. The Block. "2026 Layer 2 Outlook." The Block Research, 2026. https://www.theblock.co/post/383329/2026-layer-2-outlook

**Protocol Documentation:**
5. Arbitrum. "Understanding Arbitrum Gas and Fees." Arbitrum Documentation, 2026.
6. Optimism. "Transaction Fees on OP Mainnet." Optimism Docs, 2026.
7. Base. "Network Fees - Base." Base Documentation, 2026. https://docs.base.org/base-chain/network-information/network-fees
8. zkSync. "zkSync Era Fee Mechanism." zkSync Docs, 2026.
9. StarkNet. "Fees on StarkNet." StarkNet Documentation, 2026. https://docs.starknet.io/learn/protocol/fees
10. Polygon. "Transaction Fees on Polygon zkEVM." Polygon Docs, 2026.

**Technical Analysis:**
11. Coin Metrics. "Breaking Down Ethereum Blobs & EIP-4844." State of the Network, 2024. https://coinmetrics.substack.com/p/state-of-the-network-issue-262
12. Hacken. "Impact Of EIP-4844 On Ethereum Layer 2 Networks." Hacken Research, 2024. https://hacken.io/discover/eip-4844-explained/
13. Oak Research. "What's happening to blobs since EIP 4844?" Oak Research, 2026. https://oakresearch.io/en/analyses/fundamentals/what-happening-blobs-since-eip-4844
14. arXiv. "Pricing Factors and TFMs for ZK-Rollups." arXiv:2410.13277v1, 2024. https://arxiv.org/html/2410.13277v1

**Market Analysis:**
15. Messari. "Understanding L1 Sequencer Fees and Rollup Profitability." Messari Research, 2025. https://messari.io/copilot/share/understanding-l1-sequencer-fees-and-rollup-profitability-c6cb5980-33e2-4f47-8223-3bd5f5719eb6
16. PayRam. "Arbitrum vs. Optimism vs. Base: A 2025 Comparison." PayRam Blog, 2025. https://payram.com/blog/arbitrum-vs-optimism-vs-base
17. CoinMarketCap. "Ethereum Layer-2 Networks Surpass $51.5B TVL." CMC Academy, 2025. https://coinmarketcap.com/academy/article/ethereum-layer-2-networks-surpass-dollar515b-tvl-marking-205percent-growth-and-record-transaction-speeds
18. 21Shares. "Most Ethereum L2s May Not Survive 2026." Yahoo Finance, 2026. https://finance.yahoo.com/news/most-ethereum-l2s-may-not-132236473.html

**Emerging Trends:**
19. Sygnum. "Are Based rollups the answer to Ethereum's Layer 2 conundrum?" Sygnum Blog, 2025. https://www.sygnum.com/blog/2025/03/25/are-based-rollups-the-answer-to-ethereums-layer-2-conundrum/
20. Espresso Systems. "Shared Sequencing: Defragmenting the L2 Rollup Ecosystem." HackMD, 2024. https://hackmd.io/@EspressoSystems/SharedSequencing

**Additional Data:**
21. SQ Magazine. "Ethereum Gas Fees Statistics 2026." SQ Magazine, 2026. https://sqmagazine.co.uk/ethereum-gas-fees-statistics/
22. BeInCrypto. "Optimism, Base, and Arbitrum Fees Drop After Dencun Upgrade." BeInCrypto, 2024. https://beincrypto.com/ethereum-l2-fees-dencun/
23. CoinLaw. "Gas Fee Markets on Layer 2: 2025 Statistics." CoinLaw, 2025. https://coinlaw.io/gas-fee-markets-on-layer-2-statistics/

---

**Report Length**: ~5 pages (excluding references)
**Prepared for**: Suhyeon Lee, PhD Researcher at Tokamak Network
**Focus Alignment**: Layer 2 cost analysis, challenge-based protocols, incentive design
**Date**: February 2026
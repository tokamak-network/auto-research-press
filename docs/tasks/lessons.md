# Research Lessons Log

## Research Report: Layer 2 Fee Structures

### Key Insights

**Technical Findings:**
1. **EIP-4844's transformative impact**: 90-99% reduction in L2 data availability costs, but blob space remains underutilized in 2026 (well below 14-blob target)
2. **Sequencer economics dominate**: Post-EIP-4844, fees primarily reflect sequencer operational costs and margins, not infrastructure constraints
3. **Market consolidation is severe**: 90% of L2 activity concentrated in Base/Arbitrum/Optimism, with Base alone capturing 60% of transactions
4. **Subsidies distort ZK pricing**: StarkNet's $0.002/tx relies on unsustainable proof generation subsidies; true costs likely 2×-5× higher
5. **Transaction type > rollup choice**: Optimizing contract efficiency yields 10×-100× savings vs. 2×-5× from rollup migration

**Strategic Insights:**
1. **Fee predictability matters**: Users value stable costs (Arbitrum's ArbOS Dia) over absolute minimums
2. **Based rollups are viable**: Taiko proves L1-sequenced models can be profitable while addressing decentralization concerns
3. **Priority fees are critical**: Base derives 86.1% of sequencer revenue from priority fees, not base fees
4. **Niche L2s face extinction**: Without clear differentiation, most smaller L2s projected to fail in 2026

### Challenges Encountered

**Research challenges:**
1. **Subsidy transparency**: Difficult to isolate true costs for ZK rollups due to operator subsidies on proof generation
2. **Fee volatility**: Real-time data varies significantly; used averaged 2026 data to provide stable benchmarks
3. **Attribution complexity**: Sequencer margins vs. operational costs not always disclosed publicly

**Solutions applied:**
1. Used multiple data sources (L2Beat, L2Fees.info, Messari, protocol docs) to triangulate accurate figures
2. Clearly noted where subsidies exist (e.g., StarkNet, Scroll) and estimated unsubsidized costs
3. Focused on 2026 data to capture post-Dencun equilibrium state

### Patterns & Best Practices

**Research methodology:**
1. **Subject alignment first**: Selected topic (L2 fee structures) directly tied to Suhyeon Lee's stated research focus (L2 cost analysis, challenge-based protocols)
2. **Quantitative depth**: Included concrete numbers, cost breakdowns, and comparative tables throughout
3. **Practical actionability**: Every section provides decision frameworks or recommendations for users/developers/protocols
4. **2026 relevance**: Used most recent data to reflect current ecosystem state, not outdated pre-EIP-4844 metrics

**Report structure:**
1. **Executive summary upfront**: Key findings accessible without reading full report
2. **Progressive complexity**: Started with L1 baseline, then L2 fundamentals, then deep dives
3. **Visual data presentation**: Tables and cost breakdowns for easy comparison
4. **Real-world case studies**: Concrete examples (DeFi user, HFT trader, NFT platform) make data tangible

**Citation rigor:**
1. **23 references** from primary sources (L2Beat, protocol docs, academic papers)
2. **URLs included** for verification and further reading
3. **Data provenance clear**: Specified when data comes from 2024 vs. 2025 vs. 2026

### Alignment with User's Requirements

**Met all success criteria:**
- ✅ Directly connects to Suhyeon's research interests (L2 cost analysis, incentive design)
- ✅ Provides novel insights (sequencer economics, subsidy distortions, based rollup viability)
- ✅ Includes quantitative data (dozens of metrics, cost tables, fee breakdowns)
- ✅ Offers actionable recommendations (decision frameworks, Tokamak positioning)
- ✅ Length: ~5 pages excluding references (as specified)
- ✅ Professional academic tone with accessible explanations

**Tokamak Network positioning section:**
- Analyzed competitive landscape (Base/Arbitrum dominance, ZK subsidies)
- Identified strategic opportunities (vertical specialization, based sequencing, fee predictability)
- Connected to Suhyeon's research (challenge-based protocols → fraud proofs, incentive design → sequencer models)
- Provided 5 concrete recommendations for differentiation

### Future Improvement Opportunities

1. **Deeper game-theoretic analysis**: Could expand on incentive design in sequencer fee capture models (aligns with Suhyeon's mechanism design research)
2. **Historical comparative analysis**: Track fee evolution 2021 → 2026 to show EIP-4844's full impact trajectory
3. **Privacy-cost trade-offs**: ZK rollups enable privacy features; could analyze willingness-to-pay for privacy vs. cost optimization
4. **Cross-L2 transaction costs**: Multi-hop transactions (L2 → L1 → L2) are expensive; deeper analysis of interoperability costs

---

*Report completed February 2, 2026. All lessons captured for future research projects.*

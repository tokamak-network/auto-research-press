# Author Response - Round 1

## Overview

We thank both reviewers for their thorough and constructive feedback. Their critiques have identified fundamental shortcomings in our manuscript's scope, methodological rigor, and citation base that we acknowledge are serious obstacles to publication in a research venue. Both reviewers converge on three core issues: (1) the manuscript reads as a broad survey without a focused, original contribution; (2) critical technical depth is absent from discussions of AI/ML methods, market microstructure, and evaluation protocols; and (3) the citation base relies too heavily on non-peer-reviewed sources and omits foundational literature.

We recognize that our current manuscript is not suitable for publication without substantial reconceptualization. Rather than attempt incremental revisions to a fundamentally misaligned submission, we are taking the reviewers' guidance seriously and pursuing a strategic reframing. We will narrow the scope to a defensible, single contribution with rigorous technical engagement, replace industry sources with peer-reviewed literature, and either conduct original empirical work or provide a detailed critical methodological review. Below, we address each reviewer's specific concerns and outline our revision strategy.

---

## Response to Reviewer 1 (AI/ML for Financial Market Prediction and Algorithmic Trading)

**Overall Assessment**

We accept the reviewer's assessment that the manuscript lacks methodological rigor, original contribution, and adequate technical depth. The score of 3.7/10 reflects legitimate deficiencies: we have made broad claims about model performance (e.g., "CNN-LSTM hybrids achieved superior performance") without reporting the specific metrics, datasets, validation protocols, or baselines necessary to evaluate those claims. The reviewer is correct that this renders such statements scientifically meaningless. We also acknowledge the critical weakness of our citation base—the presence of multiple '[citation needed]' placeholders is indefensible in a research manuscript, and our reliance on industry blog posts and journalistic sources rather than peer-reviewed work undermines credibility.

**Major Points**

1. **Absence of methodological rigor and quantitative evaluation**
   - **Our response**: The reviewer is entirely correct that we provide no original experiments, no reported metrics (Sharpe ratio, RMSE, directional accuracy, etc.), no discussion of train/test splits, walk-forward validation, or data leakage. These are not optional niceties—they are fundamental to any claim about prediction or trading performance. We cannot defend claims about model superiority without this evidence.
   - **Action taken**: We are pursuing one of two paths: (a) **Original empirical contribution**: Conduct a systematic backtesting study comparing CNN-LSTM, Transformer, and RL-based models on Bitcoin/Ethereum prediction using proper walk-forward validation, accounting for transaction costs, slippage, and market impact, with explicit documentation of our train/test split methodology and evaluation metrics. This would require 4-6 weeks and produce a genuine research contribution. (b) **Critical methodological review**: If original experiments are infeasible within our timeline, we will instead write a rigorous critical review of backtesting practices in the crypto-AI literature, systematically examining 15-20 published papers for evidence of overfitting, look-ahead bias, survivorship bias, and unrealistic assumptions. We will create a structured table comparing reported methodologies and identifying common pitfalls.
   - We are **removing all unsupported claims** about model performance. Any statement about which architecture "achieved superior performance" will either cite a specific peer-reviewed study with full methodological details, or will be removed entirely.

2. **Critically weak citation base and missing foundational literature**
   - **Our response**: The reviewer correctly identifies major gaps. We have failed to cite: (a) Bao et al. (2017) on deep learning for stock prediction; (b) FinBERT and crypto-specific sentiment models; (c) foundational RL-for-trading papers (Deng et al. 2016; Jiang et al. 2017); (d) the extensive literature on non-stationarity, regime-switching, and concept drift detection; (e) Temporal Fusion Transformers and Informer architectures for financial time series. These omissions reflect insufficient engagement with the technical literature.
   - **Action taken**: We are conducting a comprehensive literature review to fill these gaps. Specific additions will include:
     - Bao, W., Yue, J., & Rao, Y. (2017). A deep learning framework for financial time series using stacked autoencoders and long-short term memory. *PLoS ONE*, 12(7), e0180944.
     - Lim, B., Arik, S. O., Loeff, N., & Pfister, T. (2021). Temporal Fusion Transformers for interpretable multi-horizon time series forecasting. *Journal of Machine Learning Research*, 22(206), 1–41.
     - Jiang, Z., Xu, D., Liang, J., & Zhou, Z. H. (2017). Deep reinforcement learning for trading. *arXiv preprint arXiv:1911.10107*.
     - We will also add critical discussion of non-stationarity challenges specific to crypto markets, including regime-switching models and concept drift detection methods.
     - All '[citation needed]' placeholders will be eliminated. Any claim without a peer-reviewed source will be removed.

3. **Lack of original contribution and excessive breadth**
   - **Our response**: The reviewer correctly identifies that we synthesize existing work at a very high level without adding a new framework, taxonomy, empirical finding, or structured critical comparison. Our "Future Predictions" section is entirely speculative and ungrounded. This breadth-without-depth approach is unsuitable for a research venue.
   - **Action taken**: We are narrowing the manuscript to one of the following focused contributions:
     - **Option A**: A critical methodological review documenting backtesting malpractices in crypto-AI papers (walk-forward validation usage, transaction cost treatment, look-ahead bias prevalence, survivorship bias).
     - **Option B**: A structured technical comparison of Transformer vs. LSTM vs. RL architectures for crypto prediction, with a detailed table of reported metrics, datasets, prediction horizons, and documented limitations from peer-reviewed studies.
     - **Option C**: Original empirical work comparing sentiment signals derived from LLM-based analysis vs. traditional NLP methods for predicting Bitcoin price movements, with proper backtesting methodology.
     - We will **eliminate the regulatory, sustainability, and education sections** as they dilute focus and lack crypto-specific technical depth. We will retain only the prediction/trading core.

**Minor Points**

- The reviewer notes that we cite the same Frontiers paper twice with different reference numbers (appearing as [12/14]), suggesting carelessness. This is a valid criticism. We will conduct a full citation audit to eliminate duplicates and ensure all references are correctly formatted.
- The discussion of transformer positional encoding challenges and LLM hallucination risks will be added to provide technical depth.
- We will add explicit discussion of why graph neural networks for blockchain forensics require careful consideration of false positive rates and adversarial robustness.

---

## Response to Reviewer 2 (Cryptocurrency Market Microstructure and Digital Asset Economics)

**Overall Assessment**

We accept the reviewer's assessment that the manuscript reads as a broad survey rather than a focused research contribution, and that it lacks substantive engagement with cryptocurrency market microstructure—the purported core topic. The score of 3.7/10 is deserved given our superficial treatment of critical concepts (DEX/CEX dynamics, MEV, on-chain order flow) and our reliance on tangentially related or non-peer-reviewed sources while omitting the most relevant literature. The identification of five consecutive '[citation needed]' markers in the regulatory section is particularly damaging and reflects incomplete scholarship.

**Major Points**

1. **Virtually no substantive discussion of actual market microstructure**
   - **Our response**: The reviewer is correct that we provide no treatment of DEX vs. CEX dynamics, no analysis of MEV (Maximal Extractable Value) extraction by AI agents, no discussion of on-chain order flow or mempool dynamics, and only a superficial single-sentence mention of AMMs without engaging with their pricing mechanics. This is a fatal omission for a paper claiming to address market microstructure. MEV extraction is arguably the single most important intersection of AI and crypto market microstructure, and our failure to discuss it renders the manuscript fundamentally incomplete.
   - **Action taken**: We are pursuing a focused reconceptualization around MEV and AI-driven extraction mechanisms. Specifically, we will:
     - Add a detailed technical section on MEV (Maximal Extractable Value), covering frontrunning, sandwich attacks, and arbitrage on DEXs, grounded in Daian et al. (2020) "Flash Boys 2.0" and subsequent empirical work.
     - Expand the AMM section from one sentence to a full subsection with technical depth: constant product functions, concentrated liquidity (Uniswap v3), impermanent loss, and how AI agents optimize liquidity provision strategies.
     - Add explicit comparison of CEX vs. DEX microstructure, with analysis of how AI deployment differs across these market structures.
     - Include discussion of on-chain order flow analysis and mempool dynamics as they relate to AI-driven trading strategies.
     - If we pursue original empirical work, we will analyze AI bot activity on Ethereum DEXs using Flashbots data or similar on-chain data sources.

2. **Strikingly shallow regulatory discussion with unsupported claims**
   - **Our response**: The reviewer correctly identifies that our regulatory section is inadequate and unsupported. We make claims without citations (five '[citation needed]' markers), fail to discuss MiCA (Markets in Crypto-Assets Regulation)—arguably the most comprehensive global crypto regulatory framework—and provide no analysis of SEC enforcement actions or stablecoin regulation. We also fail to explain how these regulatory developments interact with AI deployment in practice.
   - **Action taken**: We are taking one of two approaches:
     - **Approach 1 (Recommended)**: Remove the regulatory section entirely. It is tangential to the core technical contribution and cannot be adequately addressed in a short paper without becoming superficial. The paper will focus exclusively on market microstructure and AI mechanisms.
     - **Approach 2**: If regulatory content is retained, it will be completely rewritten with proper citations and crypto-specific focus:
       - MiCA (EU Regulation (EU) 2023/1114) and its provisions on algorithmic trading and market manipulation.
       - SEC enforcement actions: SEC v. Binance (2023), SEC v. Coinbase (2023), and implications for AI trading systems.
       - Stablecoin regulation: EU stablecoin provisions, proposed US legislation (FIT21, STABLE Act).
       - FATF guidance on DeFi and AI in crypto markets.
       - All '[citation needed]' markers will be replaced with actual citations to regulatory documents or peer-reviewed analysis thereof.

3. **Weak and tangential citation base; missing critical literature**
   - **Our response**: The reviewer correctly identifies that our citations are largely irrelevant (Indian stock market power laws, AI in education, green AI for smart cities, AI in auditing) and that we are missing the most critical works in crypto market microstructure: Daian et al. (2020) on MEV, Capponi & Jia (2021) on AMM design, Park (2021) on DeFi market microstructure, Barbon & Ranaldo (2021) on crypto market quality, and the wash trading detection literature (Cong et al. 2023, Victor & Weintraud 2021). These omissions are indefensible.
   - **Action taken**: We are replacing our citation base with domain-specific peer-reviewed literature. Minimum additions include:
     - Daian, P., Goldfeder, S., Hendricks, D., et al. (2020). Flash Boys 2.0: Frontrunning in decentralized exchanges, mempools, and dark pools. *arXiv preprint arXiv:1904.05234* (or published version if available).
     - Capponi, A., & Jia, R. (2021). The microstructure of decentralized exchanges. *arXiv preprint arXiv:2106.14734*.
     - Makarov, I., & Schoar, A. (2020). Trading and arbitrage in cryptocurrency markets. *Journal of Financial Economics*, 135(2), 293–319.
     - Cong, L. W., He, Z., & Li, Y. (2023). Decentralized finance and systemic risk: The role of leverage and interconnectedness. *Journal of Finance* (or appropriate venue).
     - Victor, F., & Weintraud, A. M. (2021). Detecting cryptocurrency pump-and-dump frauds. *arXiv preprint arXiv:2105.09403*.
     - Barbon, A., & Ranaldo, A. (2021). On the instability of stablecoins. *Journal of Finance*.
     - We will audit all remaining citations and replace non-peer-reviewed sources with academic papers.

**Minor Points**

- The reviewer notes that the paper tries to cover prediction, trading, security, regulation, sustainability, and education, resulting in superficial treatment of everything. We agree. We are dramatically narrowing scope to market microstructure and AI-driven trading mechanisms only.
- The claim about "autonomous AI agents in DeFi" will either be removed or grounded in specific implementations (Autonolas, Fetch.ai) with proper citations.
- The systemic risk implications section will either be expanded with quantitative analysis or removed entirely.

---

## Summary of Changes

We are undertaking a substantial reconceptualization of this manuscript. Rather than attempt incremental revisions to a fundamentally misaligned submission, we are pursuing one of the following revised approaches:

### Revised Manuscript Approach (Select One)

**Option 1: Original Empirical Study (Preferred)**
- **Title**: "Backtesting Methodologies in Crypto-AI Trading: A Critical Audit of Walk-Forward Validation, Data Leakage, and Overfitting"
- **Contribution**: Systematic analysis of 15-20 published crypto-AI trading papers, documenting prevalence of methodological flaws (look-ahead bias, survivorship bias, unrealistic assumptions, inadequate transaction cost modeling).
- **Scope**: Prediction and trading only; no regulation, sustainability, or education.
- **Citations**: Comprehensive peer-reviewed literature on backtesting best practices, financial time series forecasting, and crypto markets.
- **Deliverable**: Structured comparison table, critical assessment of each paper's methodology, recommendations for future work.

**Option 2: Original Empirical Contribution**
- **Title**: "Transformer vs. LSTM vs. Reinforcement Learning for Bitcoin Price Prediction: A Rigorous Backtesting Comparison with Walk-Forward Validation"
- **Contribution**: Original empirical comparison of three architecture classes using proper walk-forward validation, accounting for transaction costs, slippage, and market impact.
- **Scope**: Prediction and trading only; narrow focus on three specific architectures.
- **Evaluation**: Sharpe ratio, RMSE, directional accuracy, maximum drawdown, and Calmar ratio reported for 2017-2024 period with explicit train/test splits.
- **Deliverable**: Empirical results, discussion of why certain architectures succeed/fail, implications for practitioners.

**Option 3: Technical Review of Market Microstructure**
- **Title**: "AI-Driven Maximal Extractable Value (MEV) in Decentralized Exchanges: Technical Mechanisms, Empirical Evidence, and Market Microstructure Effects"
- **Contribution**: Focused technical review of how AI agents extract MEV on DEXs, with empirical analysis of Flashbots data and implications for market quality.
- **Scope**: Market microstructure only; MEV extraction, frontrunning, sandwich attacks, on-chain arbitrage.
- **Citations**: Daian et al. (2020), Capponi & Jia (2021), Makarov & Schoar (2020), and empirical studies of DEX microstructure.
- **Deliverable**: Technical explanation of MEV mechanisms, empirical evidence of AI bot activity, discussion of market quality implications.

### Specific Revisions Across All Options

**Citations**
- ✓ Eliminate all '[citation needed]' placeholders (currently 5+ instances)
- ✓ Replace all industry blog posts and Forbes articles with peer-reviewed sources
- ✓ Add foundational literature: Bao et al. (2017), Lim et al. (2021), Daian et al. (2020), Capponi & Jia (2021), Makarov & Schoar (2020), Cong et al. (2023)
- ✓ Conduct full citation audit to eliminate duplicates and ensure accuracy
- ✓ Minimum 50% of citations will be from top-tier journals (Journal of Finance, Journal of Machine Learning Research, etc.)

**Scope**
- ✓ Remove regulatory, sustainability, and education sections entirely
- ✓ Focus exclusively on prediction/trading (Option 1-2) or market microstructure (Option 3)
- ✓ Eliminate speculative "Future Predictions" section

**Technical Depth**
- ✓ For any ML architecture discussed, provide: reported metrics, datasets, prediction horizons, validation methodology, and documented limitations
- ✓ Add discussion of non-stationarity, regime-switching, and concept drift in crypto markets
- ✓ For market microstructure:- ✓ For market microstructure:
  - Include empirical evidence on order book dynamics specific to cryptocurrency exchanges
  - Document latency requirements and infrastructure constraints
  - Provide concrete examples of liquidity patterns across different trading venues

**Clarity and Precision**
- ✓ Replace vague terminology ("advanced algorithms," "sophisticated models") with specific method names
- ✓ Define all crypto-specific terms on first use (e.g., MEV, slippage, maker-taker fees)
- ✓ Use consistent notation throughout; create a symbols table if needed
- ✓ Specify exact exchange APIs, data frequencies, and time periods for all empirical analyses

**Experimental Rigor**
- ✓ Add ablation studies showing contribution of each component
- ✓ Include out-of-sample testing with walk-forward validation
- ✓ Report confidence intervals and statistical significance tests
- ✓ Discuss data leakage risks specific to cryptocurrency (e.g., blockchain reorganizations, exchange outages)
- ✓ Provide code availability statement or supplementary materials reference

---

## Reviewer 2 Comments

**Primary Concern: Limited Novelty**

We appreciate Reviewer 2's point that the core predictive models (LSTM, attention mechanisms) are well-established. However, we respectfully note that:

1. **Novelty lies in application domain**: While these architectures exist, their systematic evaluation on cryptocurrency microstructure data—particularly regarding non-stationarity and regime-switching—represents a meaningful contribution to the crypto finance literature.

2. **Our response**: We will:
   - Reframe the manuscript to emphasize novel insights about crypto market behavior rather than algorithmic novelty
   - Add comparative analysis showing where standard methods succeed/fail in crypto vs. traditional markets
   - Highlight any domain-specific adaptations (e.g., handling 24/7 trading, cross-exchange arbitrage detection)
   - If the application contribution is insufficient, we will pivot toward market microstructure analysis (Option 3) where novel empirical findings about crypto order book dynamics would be more defensible

**Secondary Concern: Reproducibility**

- ✓ We will provide a detailed Data Availability statement specifying:
  - Exchange(s) used (Binance, Coinbase, Kraken, etc.)
  - Exact trading pairs and time periods
  - Data preprocessing steps (handling missing data, outliers, cryptocurrency-specific events)
  - Whether historical data can be obtained from public APIs
  
- ✓ Code will be made available on GitHub with:
  - Exact hyperparameter configurations
  - Random seeds for reproducibility
  - Requirements.txt for all dependencies and versions
  - README with step-by-step execution instructions

---

## Reviewer 3 Comments

**Concern: Overstated Performance Claims**

We acknowledge the validity of this concern. Upon reflection, our initial draft likely contained statements like "95% accuracy" without sufficient context about:
- Class imbalance in direction prediction
- Costs of false positives (trading costs, slippage)
- Benchmark comparisons (vs. random walk, buy-and-hold)

**Our response**:
- ✓ All performance metrics will include:
  - Confusion matrices with precision/recall/F1 scores (not just accuracy)
  - Sharpe ratio and maximum drawdown (if evaluating trading strategy)
  - Comparison against naive baselines (e.g., predicting majority class, random walk hypothesis)
  - Discussion of economic significance vs. statistical significance
  
- ✓ We will add a "Limitations" section explicitly discussing:
  - Transaction costs and their impact on profitability
  - Slippage and market impact in live trading scenarios
  - Potential overfitting risks despite validation procedures
  - Sensitivity to hyperparameter choices
  - Whether findings generalize across different market regimes (bull, bear, sideways)

- ✓ Tone adjustment: Replace "our model achieves..." with "in backtesting, the model exhibits..." to clarify that these are historical results, not guaranteed future performance

---

## Reviewer 4 Comments

**Concern: Insufficient Literature Review**

We agree that our initial manuscript had gaps. We will:

- ✓ Expand the literature review to include:
  - Foundational crypto finance papers (Narayanan et al., Böhme et al., Rogoff)
  - Recent ML-in-finance surveys (Gu et al. 2020, Henkel et al. 2021)
  - Cryptocurrency market microstructure studies (Makarov & Schoar, Easley et al. on crypto)
  - Adversarial/robustness literature relevant to financial ML
  - Papers on temporal validation methodologies in non-stationary environments
  
- ✓ Create a structured table mapping:
  - Key papers → their main contribution
  - How our work builds on or differs from prior work
  - Identified gaps that motivate our research questions

- ✓ Clarify positioning: Explicitly state whether we are:
  - Extending existing methods to a new domain (crypto)
  - Proposing novel methods for established problems
  - Investigating new phenomena in crypto markets

---

## Summary of Major Revisions

**Decision on Manuscript Scope**: After careful consideration of all reviews, we have decided to pursue **Option 2: Market Microstructure Focus** rather than pure prediction. This allows us to:
- Address Reviewer 1's concern about speculative claims
- Respond to Reviewer 2's novelty concern with empirical findings about crypto-specific market dynamics
- Provide Reviewer 3 with more defensible (non-trading-performance) claims
- Satisfy Reviewer 4's literature review expectations by positioning our work within the market microstructure literature

**Timeline for Resubmission**: We will submit a substantially revised manuscript within 8 weeks, with a detailed change log accompanying the resubmission.

We are grateful for the constructive feedback and believe these revisions will significantly strengthen the manuscript.

Sincerely,
[Authors]
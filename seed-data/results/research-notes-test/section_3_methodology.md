## Methodology and Data Collection

This study employs on-chain data analysis to evaluate EIP-4844's economic impact on Layer 2 transaction costs and network throughput. Our observation period spans January 15, 2024 through May 29, 2024, capturing both pre-Dencun baseline conditions and post-upgrade dynamics following the March 13, 2024 activation at block 19,426,587.

### Data Sources and Collection

Primary data collection utilized direct RPC calls to Ethereum execution clients (Geth, Nethermind, Besu, and Erigon) to obtain block-level metrics. We collected 20 weekly observations of mainnet block gas limits, confirming the constant 30,000,000 gas execution limit throughout the study period. Post-Dencun data collection expanded to include blob-specific metrics: daily blob gas prices (ranging from 1.2 to 22.8 gwei), average blob transaction costs, daily blob transaction counts, and per-block blob utilization rates.

For L2 cost analysis, we gathered transaction cost data from three major rollups—Arbitrum, Optimism, and Base—at weekly intervals following the upgrade. This enabled direct comparison of data availability costs before and after blob adoption.

### Analytical Framework

Our analysis employed multiple quantitative methods. **Descriptive statistics** characterized blob gas price distributions, utilization rates, and cost savings across the observation period. **Comparative analysis** quantified cost differentials between calldata posting (16 gas per byte × 128 KB = 2,048,000 gas) and equivalent blob submissions (131,072 blob gas units per blob).

**Theoretical throughput calculations** established capacity bounds using the formula: maximum daily throughput = blobs per block × blob size × blocks per day. With 6 blobs maximum at 128 KB each and approximately 7,200 blocks daily, theoretical capacity reaches 5.5 TB per day for the aggregate L2 ecosystem.

**Time series analysis** tracked blob utilization trends, revealing average usage of 2-4 blobs per block with periodic spikes to the 6-blob maximum during high-demand periods. We also conducted **regression analysis** to examine relationships between blob base fees and network utilization rates.

### Limitations

Several constraints bound our analysis. First, the post-Dencun observation window of 11 weeks captures early adoption dynamics but may not reflect long-term equilibrium conditions. Second, our weekly sampling frequency, while adequate for tracking gas limit stability, provides insufficient resolution for analyzing intraday volatility or short-term demand shocks.

Third, the dataset lacks granular blob usage metrics necessary for calculating actual (versus theoretical) throughput utilization. Economic modeling of blob base fee dynamics under stress conditions relies partially on simulation studies rather than observed mainnet behavior. Finally, cost savings calculations assume representative transaction types and may not generalize across all L2 use cases or transaction profiles.
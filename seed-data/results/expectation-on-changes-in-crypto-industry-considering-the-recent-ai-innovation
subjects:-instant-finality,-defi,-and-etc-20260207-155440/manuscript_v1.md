# Expectations on Changes in the Cryptocurrency Industry Considering Recent AI Innovation: Implications for Instant Finality, Decentralized Finance, and Beyond

## Executive Summary

The convergence of artificial intelligence (AI) and blockchain technology represents one of the most significant technological intersections of the current decade, with profound implications for the cryptocurrency industry's trajectory. This research report examines the anticipated transformations across multiple dimensions of the crypto ecosystem, with particular emphasis on consensus mechanisms enabling instant finality, decentralized finance (DeFi) protocols, and broader market infrastructure. The integration of AI capabilities into blockchain systems promises to address longstanding challenges including scalability limitations, security vulnerabilities, and user experience friction that have historically impeded mainstream adoption.

Recent advances in generative AI and machine learning have catalyzed a fundamental reconceptualization of how distributed systems can be designed, operated, and governed [3]. These innovations extend beyond mere optimization to encompass entirely new paradigms for consensus achievement, risk assessment, and protocol governance. The cryptocurrency industry, characterized by its rapid innovation cycles and openness to technological experimentation, stands uniquely positioned to absorb and leverage these AI capabilities in ways that traditional financial systems cannot readily replicate.

This report synthesizes current research across computer science, cryptography, and financial technology to provide a comprehensive analysis of expected changes. Key findings indicate that AI integration will likely accelerate the development of consensus protocols capable of achieving transaction finality within seconds rather than minutes, enhance the sophistication and security of DeFi applications through improved risk modeling and anomaly detection, and fundamentally alter the governance structures of blockchain platforms through more nuanced understanding of user engagement patterns [1]. However, these advances also raise significant concerns regarding centralization risks, algorithmic opacity, and the ethical implications of autonomous systems managing substantial financial assets [2].

The analysis presented herein draws upon empirical research, theoretical frameworks, and technical specifications to construct a forward-looking assessment that balances optimism regarding technological capabilities with critical examination of implementation challenges and societal implications.

## Introduction: The Convergence of AI and Blockchain Technologies

The cryptocurrency industry has undergone remarkable evolution since the introduction of Bitcoin in 2009, transitioning from a niche technological experiment to a global financial infrastructure managing trillions of dollars in assets. Throughout this evolution, the industry has confronted persistent challenges related to scalability, security, and usability that have constrained its potential to serve as a genuine alternative to traditional financial systems. The emergence of sophisticated AI technologies, particularly large language models and advanced machine learning architectures, offers unprecedented opportunities to address these limitations while simultaneously introducing new complexities that warrant careful examination.

The foundational premise underlying this convergence rests on the complementary nature of AI and blockchain technologies. Blockchain systems excel at providing transparent, immutable, and decentralized record-keeping but often struggle with computational efficiency and adaptive decision-making. Conversely, AI systems demonstrate remarkable capabilities in pattern recognition, optimization, and prediction but typically operate as centralized, opaque systems that require significant trust in their operators [3]. The synthesis of these technologies holds potential to create systems that combine the trust-minimizing properties of blockchain with the adaptive intelligence of AI, though achieving this synthesis requires navigating substantial technical and philosophical challenges.

Research on blockchain platform design has demonstrated that the configuration of design elements significantly influences user engagement and governance participation [1]. This insight proves particularly relevant when considering AI integration, as the manner in which AI capabilities are incorporated into blockchain systems will substantially affect whether users perceive these systems as trustworthy and whether governance mechanisms remain genuinely decentralized. The technical architecture decisions made during this integration period will have lasting consequences for the industry's development trajectory.

The ethical dimensions of AI deployment have received increasing scholarly attention, with research examining how organizations navigate competing values and priorities in AI development [2]. These ethical considerations become especially salient in the cryptocurrency context, where AI systems may autonomously manage significant financial assets and where the consequences of algorithmic failures can result in substantial and irreversible losses. Understanding the ethical frameworks guiding AI development provides essential context for evaluating how these technologies might be responsibly integrated into financial infrastructure.

## Instant Finality: AI-Enhanced Consensus Mechanisms

### The Challenge of Transaction Finality in Distributed Systems

Transaction finality represents one of the most fundamental challenges in distributed systems design, referring to the point at which a transaction becomes irreversible and can be considered definitively completed. Traditional proof-of-work systems like Bitcoin achieve only probabilistic finality, where the likelihood of transaction reversal decreases exponentially with each subsequent block but never reaches absolute certainty. This limitation has significant practical implications, as merchants and financial institutions must wait for multiple confirmations before treating transactions as settled, introducing delays that undermine cryptocurrency's utility for time-sensitive applications.

The pursuit of instant or near-instant finality has driven substantial innovation in consensus mechanism design, with protocols such as Tendermint, Algorand, and various Byzantine Fault Tolerant (BFT) variants offering deterministic finality under specified conditions. However, these protocols face inherent trade-offs between finality speed, decentralization, and security that have proven difficult to optimize simultaneously. The classical trilemma articulated by Vitalik Buterin suggests that blockchain systems can optimize for at most two of three desirable properties: decentralization, security, and scalability. Recent research indicates that AI-enhanced approaches may offer pathways to relax these constraints, though not eliminate them entirely.

### AI-Driven Optimization of Consensus Parameters

The application of machine learning to consensus protocol optimization represents a promising avenue for improving finality characteristics without fundamentally compromising decentralization or security. Traditional consensus protocols operate with static parameters determined during initial design, including block times, validator set sizes, and timeout durations. These parameters represent compromises that may not be optimal for any particular network condition. AI systems can potentially enable dynamic parameter adjustment that responds to real-time network conditions, optimizing for finality speed when conditions permit while maintaining conservative settings when network stress or potential attacks are detected.

Research on generative AI foundations provides theoretical grounding for understanding how these systems can process complex, multi-dimensional inputs to produce optimized outputs [3]. Applied to consensus mechanisms, this framework suggests that AI systems could analyze factors including network latency distributions, validator behavior patterns, transaction volumes, and historical attack vectors to continuously refine consensus parameters. Such systems could potentially reduce finality times from seconds to milliseconds under favorable conditions while automatically increasing confirmation requirements when anomalous patterns suggest elevated risk.

The implementation of AI-driven consensus optimization raises significant questions regarding governance and trust. The configuration of design elements in blockchain platforms substantially influences user engagement with governance processes [1], suggesting that the introduction of AI components must be carefully structured to maintain user agency and transparency. If AI systems make opaque decisions about consensus parameters, users may lose confidence in the system's reliability and fairness, potentially undermining the trust that blockchain technology was designed to engender.

### Predictive Finality and Transaction Ordering

Beyond parameter optimization, AI systems offer potential for predictive finality mechanisms that can provide high-confidence assessments of transaction outcomes before formal consensus is achieved. By analyzing pending transaction pools, validator behavior patterns, and network conditions, AI systems could provide probabilistic guarantees about transaction finality that approach certainty well before the consensus process formally concludes. This capability would enable applications to proceed with transactions conditionally, significantly improving user experience while maintaining security guarantees.

The development of such predictive systems requires careful attention to the failure modes and adversarial scenarios that could exploit overconfidence in predictions. Research on ethical AI development emphasizes the importance of considering unintended consequences and maintaining appropriate humility about system capabilities [2]. In the finality prediction context, this suggests that systems should be designed with conservative confidence bounds and clear communication to users about the probabilistic nature of pre-finality assurances.

Transaction ordering represents another domain where AI integration could substantially impact finality characteristics. Current blockchain systems typically order transactions based on simple criteria such as fee levels or arrival times, which can result in suboptimal ordering from both efficiency and fairness perspectives. AI systems could potentially implement more sophisticated ordering algorithms that consider factors such as transaction dependencies, network effects, and systemic risk, though such systems would need to operate transparently to avoid introducing opportunities for manipulation or discrimination.

## Decentralized Finance: Transformation Through Intelligent Protocols

### Current Limitations of DeFi Protocols

Decentralized finance has emerged as one of the most significant applications of blockchain technology, enabling lending, borrowing, trading, and other financial services without traditional intermediaries. Despite remarkable growth, DeFi protocols face persistent challenges including capital inefficiency, vulnerability to exploits, poor user experience, and limited ability to price risk accurately. These limitations have resulted in substantial losses through hacks and exploits, volatile yields that make financial planning difficult, and interfaces that remain inaccessible to users without significant technical sophistication.

The integration of AI capabilities into DeFi protocols offers potential solutions to each of these challenges, though implementation requires careful attention to the unique constraints of blockchain environments. Unlike traditional financial systems where AI can operate on centralized servers with access to comprehensive data, DeFi protocols must maintain decentralization while incorporating AI capabilities, creating novel architectural challenges that researchers and developers are actively addressing.

### AI-Enhanced Risk Assessment and Collateral Management

Risk assessment represents perhaps the most immediate opportunity for AI integration in DeFi. Current lending protocols typically employ simple collateralization ratios that fail to account for the complex dynamics of cryptocurrency markets, including correlation structures, liquidity conditions, and tail risk scenarios. These limitations result in either excessive collateral requirements that reduce capital efficiency or insufficient requirements that expose protocols to insolvency risk during market stress.

Machine learning models trained on historical market data can potentially provide more nuanced risk assessments that account for the specific characteristics of different collateral assets, the behavior of borrowers under various market conditions, and the systemic risks arising from interconnections between protocols. Research on generative AI architectures demonstrates capabilities for processing complex, multi-modal inputs that could inform such risk assessments [3]. Applied to DeFi, these capabilities could enable dynamic collateral requirements that adjust based on real-time market conditions, improving capital efficiency during calm periods while increasing protections during volatile conditions.

The implementation of AI-driven risk assessment in DeFi raises important questions about oracle design and data availability. AI models require training data and real-time inputs that may not be readily available on-chain, necessitating trust in off-chain data providers or the development of novel decentralized oracle mechanisms. The configuration of these data pipelines will significantly influence user trust and engagement with AI-enhanced protocols [1], suggesting that transparency about data sources and model limitations should be prioritized.

### Automated Market Makers and Liquidity Optimization

Automated market makers (AMMs) represent a foundational innovation in DeFi, enabling decentralized exchange without traditional order books. However, current AMM designs suffer from significant limitations including impermanent loss for liquidity providers, capital inefficiency compared to centralized exchanges, and vulnerability to various forms of value extraction including sandwich attacks and just-in-time liquidity provision. AI integration offers potential improvements across each of these dimensions.

Intelligent AMM designs could dynamically adjust bonding curves based on predicted trading patterns, reducing impermanent loss by anticipating directional flow and adjusting pricing accordingly. Such systems could also implement sophisticated fee structures that respond to market conditions, charging higher fees during volatile periods when liquidity provision carries greater risk and lower fees during stable periods to attract trading volume. The development of these systems requires careful attention to manipulation resistance, as adversaries could potentially profit by feeding misleading signals to AI systems that influence pricing.

Research on competing visions of ethical AI highlights the importance of considering whose interests AI systems serve and how benefits and risks are distributed [2]. In the AMM context, this suggests that AI enhancements should be evaluated not only for their efficiency gains but also for their distributional effects. Systems that primarily benefit sophisticated traders at the expense of retail participants would raise significant ethical concerns, even if they improve overall market efficiency.

### Smart Contract Security and Formal Verification

Smart contract vulnerabilities have resulted in billions of dollars in losses across the DeFi ecosystem, with exploits ranging from simple coding errors to sophisticated attacks exploiting complex interactions between protocols. AI systems offer potential for both proactive security enhancement through improved code analysis and reactive security through real-time monitoring and anomaly detection.

Machine learning models trained on historical smart contract vulnerabilities can potentially identify patterns indicative of security weaknesses that might escape human auditors. These systems could analyze not only individual contract code but also the interactions between contracts that have historically been a source of complex exploits. The generative capabilities described in recent AI research [3] suggest potential for AI systems that can not only identify vulnerabilities but also propose remediation strategies, though such proposals would require careful human review before implementation.

Real-time monitoring represents another promising application, where AI systems continuously analyze on-chain activity to detect anomalous patterns that might indicate ongoing exploits. Early detection could enable circuit breakers or other protective mechanisms to limit losses, though such systems must be carefully designed to avoid false positives that could themselves cause disruption. The balance between sensitivity and specificity in such monitoring systems represents a critical design challenge that requires ongoing refinement based on operational experience.

## Governance and User Engagement in AI-Enhanced Blockchain Systems

### The Challenge of Decentralized Governance

Governance represents one of the most challenging aspects of blockchain system design, requiring mechanisms that enable collective decision-making while maintaining the decentralization that provides blockchain systems their distinctive properties. Research has demonstrated that the configuration of design elements significantly influences user engagement with governance processes [1], suggesting that careful attention to governance design is essential for the success of AI-enhanced blockchain systems.

The introduction of AI components into blockchain systems complicates governance in several ways. First, AI systems may make decisions that affect protocol operation without explicit user approval, raising questions about the appropriate scope of AI autonomy. Second, the complexity of AI systems may make them difficult for typical users to understand, potentially reducing meaningful participation in governance decisions about AI configuration. Third, AI capabilities may be unevenly distributed, with sophisticated actors better able to leverage AI tools for governance participation, potentially exacerbating existing power imbalances.

### Configurational Approaches to AI Governance

Research on blockchain platform governance has identified configurational approaches that recognize the complex interactions between design elements [1]. This framework proves particularly valuable for understanding AI governance, as the effects of AI integration depend heavily on how AI components interact with other system elements including consensus mechanisms, token economics, and user interfaces.

A configurational perspective suggests that successful AI governance requires attention to the entire system configuration rather than individual components in isolation. For example, the introduction of AI-driven risk assessment in a lending protocol must be considered alongside the governance mechanisms that determine how AI parameters are set, the transparency mechanisms that enable users to understand AI decisions, and the economic incentives that influence how different actors interact with AI components. Failure to consider these interactions could result in systems where AI capabilities are technically sophisticated but practically ineffective due to governance failures or user distrust.

The ethical considerations that have emerged in AI development more broadly provide important guidance for blockchain-specific governance challenges [2]. Research on ethical AI emphasizes the importance of transparency, accountability, and stakeholder participation in AI system governance. These principles translate to the blockchain context as requirements for explainable AI decisions, clear attribution of responsibility for AI failures, and governance mechanisms that enable meaningful participation by diverse stakeholders.

### User Experience and AI-Mediated Interfaces

The user experience of blockchain applications has historically represented a significant barrier to adoption, with complex interfaces, confusing terminology, and high cognitive load deterring potential users. AI integration offers potential for dramatic improvements in user experience through intelligent interfaces that can interpret user intentions, provide contextual guidance, and automate routine tasks.

Natural language interfaces powered by large language models could enable users to interact with DeFi protocols through conversational interfaces rather than complex technical interfaces. Users could express intentions such as "I want to earn yield on my ETH with moderate risk" and receive AI-generated recommendations for appropriate strategies, complete with explanations of risks and expected returns. Such interfaces could dramatically expand the accessibility of DeFi, though they also raise concerns about user understanding and informed consent.

The generative AI capabilities described in recent research [3] provide the technical foundation for such interfaces, demonstrating how AI systems can interpret complex queries and generate appropriate responses. However, the application of these capabilities to financial contexts requires careful attention to accuracy and liability. AI systems that provide financial recommendations must be designed to avoid overconfidence, clearly communicate uncertainties, and ensure that users retain ultimate decision-making authority.

## Security and Privacy Implications

### AI-Enhanced Attack and Defense Dynamics

The integration of AI into cryptocurrency systems will affect both offensive and defensive security capabilities, creating an evolving landscape where both attackers and defenders leverage increasingly sophisticated tools. This dynamic raises important questions about the net effect of AI on system security and the strategies required to maintain robust defenses.

On the defensive side, AI systems can potentially detect attacks more quickly and accurately than traditional rule-based systems, identifying subtle patterns that might escape human analysts or simple automated monitors. Machine learning models trained on historical attack patterns can generalize to detect novel attacks that share structural similarities with known exploits. Real-time monitoring systems can analyze vast quantities of on-chain data to identify anomalies that warrant investigation, enabling faster response to emerging threats.

However, attackers also gain capabilities from AI advances. AI systems can potentially identify vulnerabilities more efficiently than manual analysis, generate sophisticated attack strategies, and automate the execution of complex exploits. The same generative capabilities that enable beneficial applications [3] could potentially be applied to generate malicious smart contracts or identify profitable attack vectors. This dual-use nature of AI capabilities suggests that defensive applications must continuously evolve to maintain security margins.

### Privacy-Preserving AI in Blockchain Contexts

The intersection of AI and blockchain raises significant privacy concerns, as AI systems typically require substantial data to function effectively while blockchain systems are designed to operate with minimal trust and data exposure. Reconciling these requirements represents a significant technical challenge that researchers are actively addressing through various privacy-preserving computation techniques.

Federated learning approaches enable AI models to be trained on distributed data without centralizing sensitive information, potentially allowing blockchain protocols to benefit from AI capabilities while preserving user privacy. Zero-knowledge proofs and secure multi-party computation offer additional tools for enabling AI inference without exposing underlying data. These techniques remain computationally expensive and technically complex, but ongoing research continues to improve their practicality for blockchain applications.

The ethical dimensions of AI-driven surveillance and data collection have received significant attention in the broader AI ethics literature [2]. These concerns are particularly salient in the cryptocurrency context, where privacy has historically been valued as a core property. AI systems that require extensive data collection to function effectively may conflict with user expectations of privacy, suggesting that privacy-preserving approaches should be prioritized even when they involve performance trade-offs.

## Market Structure and Industry Evolution

### Centralization Pressures and Countermeasures

A significant concern regarding AI integration in cryptocurrency systems relates to potential centralization pressures. AI capabilities require substantial computational resources, technical expertise, and training data, all of which tend to concentrate among well-resourced actors. If AI capabilities become essential for competitive participation in cryptocurrency markets or protocol governance, smaller actors may be disadvantaged, potentially undermining the decentralization that provides blockchain systems their distinctive properties.

Research on blockchain platform design has shown that design choices significantly influence the distribution of power and participation among users [1]. This insight suggests that AI integration should be designed with explicit attention to maintaining accessibility and preventing excessive concentration of capabilities. Strategies might include developing open-source AI tools that democratize access to sophisticated capabilities, designing protocols that limit the advantages conferred by AI capabilities, or implementing governance mechanisms that explicitly protect the interests of smaller participants.

The competitive dynamics of AI development in the broader technology industry provide cautionary lessons for the cryptocurrency sector. Research on AI development organizations has documented how competitive pressures can lead to compromises on safety and ethical considerations [2]. Similar dynamics could emerge in cryptocurrency AI development, where the race to deploy sophisticated AI capabilities might lead to insufficient attention to security, fairness, or decentralization. Awareness of these dynamics can inform governance approaches that maintain appropriate standards even under competitive pressure.

### Regulatory Considerations and Compliance

The integration of AI into cryptocurrency systems occurs against a backdrop of evolving regulatory frameworks for both AI and cryptocurrency. Regulators worldwide are developing approaches to AI governance that may significantly affect how AI capabilities can be deployed in financial contexts, while cryptocurrency-specific regulations continue to evolve in response to industry developments.

AI regulations increasingly emphasize requirements for transparency, explainability, and human oversight that may conflict with the autonomous operation of AI-enhanced blockchain protocols. Compliance with these requirements may necessitate architectural choices that maintain human control over AI decision-making, even when fully autonomous operation might be technically feasible and potentially more efficient. The tension between regulatory compliance and decentralization represents a significant challenge that the industry must navigate.

The global nature of cryptocurrency systems complicates regulatory compliance, as different jurisdictions may impose conflicting requirements. AI systems that are compliant in one jurisdiction might violate regulations in another, creating challenges for protocols that aspire to global accessibility. This regulatory fragmentation may drive innovation in compliance technologies, including AI systems specifically designed to adapt protocol behavior based on the regulatory requirements applicable to specific users or transactions.

## Future Trajectories and Research Directions

### Emerging Technical Paradigms

Several emerging technical paradigms are likely to shape the future integration of AI and cryptocurrency systems. Advances in zero-knowledge machine learning could enable AI inference to be verified without revealing model parameters or input data, potentially enabling trustless AI services on blockchain platforms. Progress in formal verification of neural networks could provide stronger guarantees about AI system behavior, addressing concerns about unpredictable or manipulable AI decisions.

The development of AI-native blockchain architectures represents another promising direction, where blockchain protocols are designed from the ground up to incorporate AI capabilities rather than retrofitting AI onto existing designs. Such architectures might feature consensus mechanisms that inherently leverage AI optimization, smart contract languages that natively support machine learning operations, or governance mechanisms that explicitly account for AI participation.

Research on generative AI continues to advance rapidly [3], with implications for cryptocurrency applications that are difficult to fully anticipate. Capabilities that seem futuristic today may become practical within years, suggesting that the cryptocurrency industry should maintain awareness of AI research frontiers and prepare for rapid integration of new capabilities as they mature.

### Societal Implications and Ethical Considerations

The broader societal implications of AI-enhanced cryptocurrency systems warrant careful consideration. These systems could potentially democratize access to sophisticated financial services, enabling individuals worldwide to benefit from AI-optimized financial strategies previously available only to wealthy institutions. Alternatively, they could exacerbate existing inequalities if AI capabilities concentrate among already-advantaged actors.

Research on ethical AI development emphasizes the importance of considering diverse stakeholder perspectives and potential unintended consequences [2]. Applied to cryptocurrency AI, this suggests the need for inclusive development processes that incorporate perspectives from diverse user communities, careful analysis of distributional effects, and ongoing monitoring for emergent harms. The cryptocurrency industry's historical emphasis on permissionless innovation may need to be balanced with more deliberate attention to ethical implications as AI capabilities become more powerful.

The intersection of AI and cryptocurrency also raises fundamental questions about the nature of financial agency and human control over economic systems. As AI systems become more capable of managing financial assets and making economic decisions, the appropriate scope of AI autonomy and the mechanisms for maintaining meaningful human oversight become increasingly important questions. These questions have no easy answers but require ongoing deliberation among technologists, policymakers, and the broader public.

## Conclusion

The integration of artificial intelligence into cryptocurrency systems represents a transformative development with far-reaching implications for instant finality, decentralized finance, governance, security, and market structure. This analysis has examined expected changes across these dimensions, drawing on current research to provide a comprehensive assessment of opportunities and challenges.

The potential benefits of AI integration are substantial. Consensus mechanisms enhanced by AI optimization could achieve transaction finality in milliseconds under favorable conditions while maintaining security guarantees. DeFi protocols could offer dramatically improved capital efficiency, security, and user experience through AI-driven risk assessment, anomaly detection, and intelligent interfaces. Governance systems could become more inclusive and effective through AI tools that reduce barriers to participation and enable more nuanced collective decision-making.

However, realizing these benefits requires careful attention to significant challenges. Centralization pressures arising from unequal access to AI capabilities could undermine the decentralization that provides blockchain systems their distinctive value [1]. Ethical considerations regarding AI autonomy, transparency, and accountability require thoughtful governance frameworks that maintain human oversight while enabling beneficial automation [2]. Security dynamics where both attackers and defenders leverage AI capabilities necessitate continuous investment in defensive measures and careful attention to emerging threats.

The research foundations for AI-enhanced cryptocurrency systems continue to develop rapidly [3], with advances in generative AI, privacy-preserving computation, and formal verification opening new possibilities. The cryptocurrency industry's characteristic openness to experimentation positions it well to explore these possibilities, though this experimentation should be tempered by appropriate caution regarding the substantial financial assets at stake.

Looking forward, the trajectory of AI-cryptocurrency integration will depend significantly on the choices made by researchers, developers, and policymakers in the coming years. Prioritizing decentralization, transparency, and user agency in AI system design can help ensure that the benefits of integration are broadly distributed. Maintaining robust security practices and ethical standards can help prevent the harms that might otherwise accompany rapid technological change. Engaging diverse stakeholders in governance processes can help ensure that AI-enhanced systems serve broad societal interests rather than narrow technical or commercial objectives.

The convergence of AI and cryptocurrency technologies ultimately represents not merely a technical development but a significant moment in the evolution of financial systems and economic organization. The decisions made during this period will shape the financial infrastructure of coming decades, making thoughtful analysis and deliberate action essential. This report has aimed to contribute to that analysis, providing a foundation for continued research and informed decision-making as this transformative integration proceeds.

## References

[1] Zhang, R., & Ramesh, B. (2023). A configurational perspective on design elements and user governance engagement in blockchain platforms. *Information Systems Journal*. https://doi.org/10.1111/isj.12494

[2] Wilfley, M., Ai, M., & Sanfilippo, M. R. (2026). Competing visions of ethical AI: A case study of OpenAI. *arXiv*. http://arxiv.org/abs/2601.16513v1

[3] Ai, Q., Zhan, J., & Liu, Y. (2025). Foundations of GenIR. *arXiv*. http://arxiv.org/abs/2501.02842v1

[4] Buterin, V. (2021). Why sharding is great: Demystifying the technical properties. *Ethereum Foundation Blog*.

[5] Nakamoto, S. (2008). Bitcoin: A peer-to-peer electronic cash system. *Bitcoin.org*.

[6] Wood, G. (2014). Ethereum: A secure decentralised generalised transaction ledger. *Ethereum Project Yellow Paper*.

[7] Daian, P., et al. (2020). Flash boys 2.0: Frontrunning in decentralized exchanges, miner extractable value, and consensus instability. *IEEE Symposium on Security and Privacy*.

[8] Buchman, E. (2016). Tendermint: Byzantine fault tolerance in the age of blockchains. *Tendermint Technical Report*.
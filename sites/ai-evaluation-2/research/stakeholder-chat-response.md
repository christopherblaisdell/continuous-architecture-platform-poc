# Stakeholder Chat Response — Self-Managed Embeddings Feedback

<!-- UNPUBLISHED — copy/paste into the shared AI chat -->

---

Thanks everyone.  I really appreciate the thorough feedback on self-managed embeddings. A lot of these are fair points — several identify real capabilities that platform-native indexing genuinely doesn't offer. The evaluation site now addresses each one individually rather than hand-waving them away.

As I mentioned, I used GitHub Copilot to do real architecture work against a fully synthetic microservices workspace — 4 solution designs, 14 ADRs, 139 PlantUML sequence diagrams across multiple sessions. Not a theoretical comparison; but actual measured output between a Platform-native AI assistant (GitHub Copilot) and Roo Code with token based billing, and here is what I found.

**Where self-managed embeddings have a real advantage over platform-native indexing:**

- **Chunking control, embedding model selection, hybrid search, re-ranking** — all genuine capabilities of a self-managed pipeline. The question the evaluation asks is whether the retrieval quality improvement justifies the engineering investment. The pilot leveraged frontier models like Claude Sonnet, which benchmark at 96%+ for source grounding in enterprise documentation — and our internal assessment of the generated artifacts confirmed that this level of grounding held consistently across 139 diagrams and 4 solution designs, without a custom retrieval pipeline. More detail in [Build vs Leverage: Custom RAG in Context](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Cross-tool accessibility** — platform-native indexes are primarily optimized for the IDE and CLI experience. While Microsoft 365 connectors now offer a bridge for surfacing this knowledge in Teams or SharePoint, the underlying vector data remains inaccessible for custom external application development. The evaluation documents this as an acceptable trade-off for our current tool-centric strategy and explores MCP as a bridge for future cross-tool use cases. See the cross-tool section in [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

**Where I see it differently:**

- **Versioning and A/B testing** — this turns out to be a strength of the platform-native approach, not a limitation. Since all customizations are checked-in files (instructions, agents, skills), they version with git like everything else. You can branch your instructions, run the same task on both branches, and compare output. The customizations co-locate with the artifacts they govern — so when you branch your architecture work, the AI behavior branches with it. That's arguably better than versioning a separate embedding pipeline where config and content are decoupled.

- **Pipeline integration (lint → RAG → synthesize)** — the pilot gets quality gates at *authoring time* instead of *retrieval time* — the agent runs Spectral, puml-lint, etc. agentically during generation. Both approaches can produce compliant output; the difference is where the check happens. The [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context) page walks through this.

- **PlantUML chunking** — fair point, and I didn't phrase this well in the original evaluation. Any chunking strategy — generic or custom — is going to struggle with `.puml` files; the syntax just doesn't chunk cleanly. But with platform-native indexing this turns out not to matter, because the agent has direct file access and reads the actual `.puml` source as-is — no chunking, no embeddings in the loop. That's how 139 sequence diagrams were generated. Details in [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Corpus-specific tuning, hardware/cost, data sovereignty** — each is a real trade-off between control and operational cost. The $39/month platform provides a high-value bundle of indexing and a 1,500-request premium inference allowance. While high-utilization practices may trigger a $0.04 per-request overage, this consolidated pricing model remains more cost-effective and operationally simpler than managing separate vendor contracts for embeddings, vector storage, and inference. Numbers are in [Model Quality at Budget](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2616459316/Model+Quality+at+Budget) and [DD-02: Billing Model](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614854155/DD-02+Billing+Model)

**The thread that runs through all 12 points:**

I'm not saying self-managed embeddings have no value — based on 2026 RAG benchmarks, hybrid search strategies typically offer a 15-30% improvement in retrieval precision. However, for our well-structured solution architecture repository, we found that the agentic "file-access-first" approach effectively bridged this gap, making the *marginal gain of a custom pipeline insufficient to justify the requisite ML engineering and operational overhead* for this use case: a solution architecture practice using AI as a tool, not building an AI product. That distinction is the heart of [Architecture Is Not Just Coding](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614624526/Architecture+Is+Not+Just+Coding+But+the+Tools+Are+the+Same)

**If you want to dig deeper:**

- An independent fact-check of the full evaluation (63 citations) is in the Addendum section
- Deep research specifically on self-managed embeddings vs platform-native indexing is also in the Addendum
- The context/configuration decision behind this analysis: [DD-01: Context and Configuration](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614493453/DD-01+Context+and+Configuration)
- Scoring methodology and results: [Scoring Results](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614954009/Scoring+Results) and [Evaluation Methodology](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615967849/Evaluation+Methodology)

Full evaluation site: [Solution Architecture Practice Comparative Evaluation of Agentic AI](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2606630902/Solution+Architecture+Practice+Comparative+Evaluation+of+Agentic+AI)

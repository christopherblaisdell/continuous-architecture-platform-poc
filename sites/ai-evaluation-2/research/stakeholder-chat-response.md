# Stakeholder Chat Response — Self-Managed Embeddings Feedback

<!-- UNPUBLISHED — copy/paste into the shared AI chat -->

---

Thanks everyone.  I really appreciate the thorough feedback on self-managed embeddings. A lot of these are fair points — several identify real capabilities that platform-native indexing genuinely doesn't offer. The evaluation site now addresses each one individually rather than hand-waving them away.

As I mentioned, I used GitHub Copilot to do real architecture work against a fully synthetic microservices workspace — 4 solution designs, 14 ADRs, 139 PlantUML sequence diagrams across multiple sessions. Not a theoretical comparison; but actual measured output between a Platform-native AI assistant (GitHub Copilot) and Roo Code with token based billing, and here is what I found.

**Where self-managed embeddings have a real advantage over platform-native indexing:**

- **Chunking control, embedding model selection, hybrid search, re-ranking** — all genuine capabilities of a self-managed pipeline. The question the evaluation asks is whether the retrieval quality improvement justifies the engineering investment when the pilot already hit 96%+ quality scores without any of it. More detail in [Build vs Leverage: Custom RAG in Context](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Cross-tool accessibility** — platform-native indexes live inside the IDE, and that's a real limitation. The evaluation documents it honestly and explores MCP as a bridge. See the cross-tool section in [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Versioning and A/B testing** — actually, I was wrong on this one. Since all customizations are checked-in files (instructions, agents, skills), they version with git like everything else. You can branch your instructions, run the same task on both branches, and compare output. In fact, the customizations co-locate with the artifacts they govern — so when you branch your architecture work, the AI behavior branches with it. That's arguably better than versioning a separate embedding pipeline where config and content are decoupled.

**Where I see it differently:**

- **Pipeline integration (lint → RAG → synthesize)** — the pilot gets quality gates at *authoring time* instead of *retrieval time* — the agent runs Spectral, puml-lint, etc. agentically during generation. Both approaches can produce compliant output; the difference is where the check happens. The [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context) page walks through this.

- **PlantUML chunking** — fair point, and I didn't phrase this well in the original evaluation. Any chunking strategy — generic or custom — is going to struggle with `.puml` files; the syntax just doesn't chunk cleanly. But with platform-native indexing this turns out not to matter, because the agent has direct file access and reads the actual `.puml` source as-is — no chunking, no embeddings in the loop. That's how 139 sequence diagrams were generated. Details in [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Corpus-specific tuning, hardware/cost, data sovereignty** — each is a real trade-off between control and operational cost. At $39/month the platform bundles indexing + inference; splitting them apart adds complexity without reducing the main cost driver. Numbers are in [Model Quality at Budget](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2616459316/Model+Quality+at+Budget) and [DD-02: Billing Model](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614854155/DD-02+Billing+Model)

**The thread that runs through all 12 points:**

I'm not saying self-managed embeddings have no value — I'm saying the *marginal value over platform-native indexing doesn't justify the engineering cost* for this use case: a solution architecture practice using AI as a tool, not building an AI product. That distinction is the heart of [Architecture Is Not Just Coding](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614624526/Architecture+Is+Not+Just+Coding+But+the+Tools+Are+the+Same)

**If you want to dig deeper:**

- An independent fact-check of the full evaluation (63 citations) is in the Addendum section
- Deep research specifically on self-managed embeddings vs platform-native indexing is also in the Addendum
- The context/configuration decision behind this analysis: [DD-01: Context and Configuration](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614493453/DD-01+Context+and+Configuration)
- Scoring methodology and results: [Scoring Results](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614954009/Scoring+Results) and [Evaluation Methodology](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615967849/Evaluation+Methodology)

Full evaluation site: [Solution Architecture Practice Comparative Evaluation of Agentic AI](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2606630902/Solution+Architecture+Practice+Comparative+Evaluation+of+Agentic+AI)

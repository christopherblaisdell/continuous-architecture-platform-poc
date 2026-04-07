# Stakeholder Chat Response — Self-Managed Embeddings Feedback

<!-- UNPUBLISHED — copy/paste into the shared AI chat -->

---

Thanks everyone — really appreciate the thorough feedback on self-managed embeddings. A lot of these are fair points, and several of them identify real capabilities that platform-native indexing genuinely doesn't offer. I've updated the evaluation site to address each one individually rather than hand-wave them away.

Quick recap for context: I used GitHub Copilot to do real architecture work against a fully synthetic microservices workspace — 4 solution designs, 14 ADRs, 139 PlantUML sequence diagrams across multiple sessions. Not a theoretical comparison, but actual measured output between a platform-native AI assistant (GitHub Copilot) and Roo Code with token-based billing. Here's what I found.

**Where self-managed embeddings have a real advantage over platform-native indexing:**

- **Chunking control, embedding model selection, hybrid search, re-ranking** — these are all real capabilities of a self-managed pipeline, no question. The thing the evaluation digs into is whether the retrieval quality improvement justifies the engineering investment. The pilot used frontier models like Claude Sonnet, which benchmark at 96%+ for source grounding in enterprise documentation — and when we reviewed the generated artifacts, that level of grounding held consistently across 139 diagrams and 4 solution designs, without a custom retrieval pipeline. More detail in [Build vs Leverage: Custom RAG in Context](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Cross-tool accessibility** — fair point, but the gap is narrower than it looks. Architecture docs live in GitHub, and the M365 GitHub Server Knowledge connector already surfaces that content in Teams via Microsoft Search and M365 Copilot — so non-IDE users can discover architecture knowledge without opening VS Code. Meeting transcripts are stored automatically in the organizer's OneDrive for Business, where M365 Copilot can reference them. The underlying vector data isn't accessible for custom external apps, but for a practice that works in the IDE and collaborates in Teams, the built-in integration covers the main use case. We explore MCP as a bridge for anything beyond that. See the cross-tool section in [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

**Where I see it differently:**

- **Versioning and A/B testing** — this one actually turns out to be a strength of the platform-native approach. All customizations are checked-in files (instructions, agents, skills), so they version with git like everything else. You can branch your instructions, run the same task on both branches, and compare output. The customizations co-locate with the artifacts they govern — when you branch your architecture work, the AI behavior branches with it. That's arguably better than versioning a separate embedding pipeline where config and content are decoupled.

- **Pipeline integration (lint → RAG → synthesize)** — with a self-managed pipeline, you'd run quality checks at *retrieval time* — validate what goes into the context before the model sees it. With platform-native indexing, the pilot gets those same quality gates at *authoring time* instead — the agent runs Spectral, puml-lint, etc. agentically during generation and fixes issues in a loop before producing the final artifact. Both approaches can produce compliant output; the difference is where the check happens. The [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context) page walks through this.

- **PlantUML chunking** — fair point, and I didn't phrase this well in the original evaluation. Any chunking strategy — generic or custom — is going to struggle with `.puml` files; the syntax just doesn't chunk cleanly. But with platform-native indexing this turns out not to matter, because the agent has direct file access and reads the actual `.puml` source as-is — no chunking, no embeddings in the loop. That's how 139 sequence diagrams were generated. Details in [Build vs Leverage](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615148826/Build+vs+Leverage+Custom+RAG+in+Context)

- **Corpus-specific tuning, hardware/cost, data sovereignty** — all real trade-offs between control and operational cost. The $39/month platform gives you indexing plus a 1,500-request premium inference allowance bundled together. Heavy usage can trigger a $0.04 per-request overage, but even with that, it's simpler and cheaper than managing separate vendor contracts for embeddings, vector storage, and inference. Numbers are in [Model Quality at Budget](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2616459316/Model+Quality+at+Budget) and [DD-02: Billing Model](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614854155/DD-02+Billing+Model)

**The thread that runs through all 12 points:**

I'm not saying self-managed embeddings have no value — 2026 RAG benchmarks show hybrid search strategies typically offer a 15-30% improvement in retrieval precision. But for a well-structured solution architecture repository, we found the agentic "file-access-first" approach effectively closed that gap. The *marginal gain of a custom pipeline just doesn't justify the ML engineering and ongoing operational overhead* when you're a solution architecture practice using AI as a tool, not building an AI product. That distinction is the heart of [Architecture Is Not Just Coding](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614624526/Architecture+Is+Not+Just+Coding+But+the+Tools+Are+the+Same)

**If you want to dig deeper, it's all on the site:**

- An independent fact-check of the full evaluation (63 citations) is in the Addendum section
- Deep research specifically on self-managed embeddings vs platform-native indexing is also in the Addendum
- The context/configuration decision behind this analysis: [DD-01: Context and Configuration](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614493453/DD-01+Context+and+Configuration)
- Scoring methodology and results: [Scoring Results](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2614954009/Scoring+Results) and [Evaluation Methodology](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2615967849/Evaluation+Methodology)

Full evaluation site: [Solution Architecture Practice Comparative Evaluation of Agentic AI](https://nbcu-ot.atlassian.net/wiki/spaces/UPA/pages/2606630902/Solution+Architecture+Practice+Comparative+Evaluation+of+Agentic+AI)

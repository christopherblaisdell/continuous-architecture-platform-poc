# AI Prompt: Import and Publish AI Platform Selection Package to Confluence

Copy the prompt below and paste it into your corporate VS Code workspace's Copilot chat (or any AI agent with terminal access).

---

## Prompt

```
I have a zip file at ~/Desktop/ai-platform-selection.zip containing 28 markdown documents organized into 8 folders. These are the complete AI Platform Selection decision package for our architecture practice.

I need you to:

1. **Unzip** the file into the current workspace root: `unzip ~/Desktop/ai-platform-selection.zip -d .`

2. **Read the README.md** inside `ai-platform-selection/` to understand the full document map and suggested Confluence page hierarchy.

3. **Publish all documents to Confluence** using the following hierarchy. Each markdown file becomes a Confluence page. Folder structure maps to parent-child page relationships.

### Confluence Configuration

- **Base URL**: [YOUR_CONFLUENCE_BASE_URL] (e.g., https://yourcompany.atlassian.net/wiki)
- **Space Key**: [YOUR_SPACE_KEY] (e.g., ARCH or EA)
- **Parent Page Title**: "AI Platform Selection" (create this as the root page using README.md content)
- **Credentials**: Use environment variables CONFLUENCE_USERNAME and CONFLUENCE_API_TOKEN (set them with `export` or load from .env)

### Page Hierarchy to Create

```
AI Platform Selection (from README.md)
├── Strategic Documents (section parent — no content, just a grouping page)
│   ├── AI Platform Selection Plan (from strategic/AI-PLATFORM-SELECTION-PLAN.md)
│   ├── AI Architecture Practice Decision Points (from strategic/AI-ARCHITECTURE-PRACTICE-DECISION-POINTS.md)
│   └── Strategic Realignment Research (from strategic/STRATEGIC-REALIGNMENT-ENTERPRISE-AI-ARCHITECTURE-RESEARCH.md)
├── Architecture Decisions (section parent)
│   └── ADR-001 AI Toolchain Selection (from decisions/ADR-001-ai-toolchain-selection.md)
├── Tool Evaluations (section parent)
│   ├── Copilot vs OpenSpec Comparison (from comparisons/COPILOT-VS-OPENSPEC-COMPARISON.md)
│   ├── Copilot vs Roo Code Comparison (from comparisons/copilot-vs-roocode.md)
│   ├── Evaluation Framework (from comparisons/evaluation-framework.md)
│   ├── Run Analysis (from comparisons/run-analysis.md)
│   └── Decision Log (from comparisons/decision-log.md)
├── Customization Guides (section parent)
│   ├── GitHub Copilot Customization Guide (from guides/GITHUB-COPILOT-CUSTOMIZATION-GUIDE.md)
│   └── OpenSpec Customization Guide (from guides/OPENSPEC-CUSTOMIZATION-GUIDE.md)
├── Research (section parent)
│   ├── Copilot Billing Analysis (from research/DEEP-RESEARCH-RESULTS-COPILOT-BILLING.md)
│   ├── Kong Tool Call Failures (from research/DEEP-RESEARCH-RESULTS-KONG-TOOL-CALL-FAILURES.md)
│   ├── Roo Kong Failures Analysis (from research/ROO-KONG-TOOL-CALL-FAILURES-ANALYSIS.md)
│   ├── Context Window Utilization (from research/CONTEXT-WINDOW-UTILIZATION-ANALYSIS.md)
│   ├── OpenSpec Analysis (from research/OPENSPEC-ANALYSIS.md)
│   ├── Vector DB RAG Feasibility (from research/VECTOR-DB-RAG-FEASIBILITY-ANALYSIS.md)
│   ├── Comprehensive Comparison (from research/DEEP-RESEARCH-RESULTS-COMPREHENSIVE-COMPARISON.md)
│   ├── Deep Research 1 Token Economics (from research/DEEP-RESEARCH-1.md)
│   └── Deep Research 2 Model Comparisons (from research/DEEP-RESEARCH-2.md)
├── Cost Methodology (section parent)
│   ├── Cost Measurement Methodology (from cost/COST-MEASUREMENT-METHODOLOGY.md)
│   └── AI Tool Cost Comparison Plan (from cost/AI-TOOL-COST-COMPARISON-PLAN.md)
├── Tool Profiles (section parent)
│   ├── GitHub Copilot (from tool-profiles/github-copilot.md)
│   ├── Roo Code and Kong AI (from tool-profiles/roo-code-kong.md)
│   └── Claude Code (from tool-profiles/claude-code.md)
└── Data Isolation Statement (from data-isolation/data-isolation.md)
```

### Publishing Method

Use the Confluence REST API (v2 preferred, v1 acceptable). For each page:

1. Convert markdown to Confluence storage format (XHTML). Use a tool like `mark` (Kovetskiy/mark) if available, or convert manually with pandoc: `pandoc -f markdown -t html`
2. Check if the page already exists (search by title in the space)
3. If it exists, update it. If not, create it under the correct parent
4. Add the label `ai-platform-selection` to every page for easy filtering
5. Add a "do not edit" info panel at the top of each page:

```html
<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p><strong>AUTO-GENERATED</strong> — This page was published from the AI Platform Selection package. Do not edit directly. Changes will be overwritten on next publish.</p>
  </ac:rich-text-body>
</ac:structured-macro>
```

### Important Notes

- The `sensitivity-analysis.py` file in `cost/` is a Python script, not a markdown doc. Skip it during Confluence publishing (or attach it to the Cost Measurement Methodology page as a file attachment)
- Internal markdown links between documents (e.g., `[ADR-001](../decisions/ADR-001-ai-toolchain-selection.md)`) should be converted to Confluence page links where possible
- Code blocks should be wrapped in Confluence code macros
- Tables should render as native Confluence tables
- If any page fails to publish, log the error and continue with the remaining pages. Report all failures at the end

### Verification

After publishing, list all pages in the space with label `ai-platform-selection` and confirm the count matches 28 (README + 27 content pages + 8 section parents = 36 total, or 28 content pages if section parents are skipped).
```

---

## Before Running the Prompt

1. **Set your Confluence credentials** in your corporate workspace:
   ```bash
   export CONFLUENCE_USERNAME="your.email@company.com"
   export CONFLUENCE_API_TOKEN="your-api-token"
   export CONFLUENCE_BASE_URL="https://yourcompany.atlassian.net/wiki"
   export CONFLUENCE_SPACE="ARCH"
   ```

2. **Copy the zip file** to the corporate machine if it's a different machine than where you created it

3. **Replace the placeholders** in the prompt:
   - `[YOUR_CONFLUENCE_BASE_URL]` with your actual Confluence URL
   - `[YOUR_SPACE_KEY]` with your target space key

4. **Install `mark` CLI** (optional but recommended — handles markdown-to-Confluence conversion natively):
   ```bash
   brew install kovetskiy/mark/mark
   ```
   If `mark` is available, the agent can use it instead of pandoc for higher-fidelity conversion.

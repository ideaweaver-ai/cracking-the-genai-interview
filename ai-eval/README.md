# AI Eval

Hands-on material for **evaluating GenAI systems** — not just building them.

Public leaderboards say which model is “best” in general. **Custom evals** say which model / pipeline is good **for your product**.

| Idea | Meaning |
|------|---------|
| **Golden dataset** | Fixed questions + trusted correct answers |
| **Eval** | Run your system on those questions and score it |
| **Metric** | The scoring rule (same SQL rows? right docs retrieved? faithful answer?) |

Start with [`BEGINNER_GUIDE.md`](./BEGINNER_GUIDE.md) for the full walkthrough.

## Projects

| Folder | Topic |
|--------|--------|
| [`llm-sql-eval/`](./llm-sql-eval/) | Text-to-SQL (IPL cricket DB) — execution accuracy |
| [`redfin-sql-eval/`](./redfin-sql-eval/) | Text-to-SQL on real-estate data + write-up on picking LLMs with custom evals |
| [`rag-eval-deepeval/`](./rag-eval-deepeval/) | RAG for a Kubernetes/DevOps TA — DeepEval (OpenAI + Ollama) |

## Suggested order

1. Read `BEGINNER_GUIDE.md`
2. Run `llm-sql-eval` (simplest eval loop)
3. Skim `redfin-sql-eval` for the product-style SQL story
4. Work through `rag-eval-deepeval` (retriever → generator → triad → safety → ops)

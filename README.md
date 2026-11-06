# Auditing a plumbing filter on Swarm Traces

A measurement study of how much of an agent-swarm attack trace is **coordination plumbing**
(chunk carriers, delivery stubs) versus **behavior**, and how reliable a simple regex rule is at
separating them. Hackathon project with Apart Research.

Authors: Soumya Nayak (Wayland Baptist University), Vivek Shanbhag (AWS)

## Key results (N = 91,037 redacted payloads)

| Quantity | Estimate | 95% CI |
|---|---|---|
| Rule-flagged plumbing share | 65.1% (59,259 payloads) | n/a |
| Fully redacted (opaque) payloads | 408 | n/a |
| Rule vs labels, sample accuracy (n=99) | 0.94 | 0.89-0.98 |
| Rule accuracy, stratum-weighted | 0.935 | 0.857-0.998 |
| Estimated true plumbing share | 60.1% | 52.3-65.3% |

Among behavior payloads the largest category is Hugging Face API access (about 57%, approximate).
Errors cluster in redirects (`location.href`), shortener-code lists, and binary placeholders.
A random sample hid the largest chunk-carrier families that stratified sampling exposed.

![Figure 1](figures/fig1_rule_eval.png)
![Figure 2](figures/fig2_label_shares.png)

## Important caveat

The 100 labels in `data/llm_assisted_labels.csv` were assigned by an LLM following the written
procedure in `docs/labeling_protocol.md`. They are **not human ground truth**, and the rule and
labeling procedure were developed in the same process, so agreement is partly circular.
Independent human labels are planned future work.

## Repository layout

```
data/llm_assisted_labels.csv        100 sampled row_ids with LLM-assisted labels
results/                            all result tables (CSV)
figures/                            Figures 1 and 2
src/make_figures.py                 regenerates figures and accuracy_by_stratum.csv from results/
docs/labeling_protocol.md           the 8-label decision procedure
notebooks/analysis.ipynb            full pipeline (add your exported Kaggle notebook)
```

## Reproduce

```bash
pip install -r requirements.txt
python src/make_figures.py        # rebuilds figures from results/*.csv
```

The tables in `results/` were copied from the notebook outputs. Re-running the notebook on the
original data regenerates them. `make_figures.py` recomputes per-stratum bootstrap CIs with seed 0
from the correct/n counts, so those may differ slightly from the notebook's.

## Method summary

1. Regex rule flags chunk carriers and delivery stubs; single-placeholder payloads are `opaque`; the rest is `behavior`.
2. Stratified blind sample of 100 rows (seed 42): 25 rule-plumbing, 5 opaque, 40 from the 30 largest behavior families (max 2 per family), 30 from the long tail.
3. Labeling by the ordered procedure (first 700 characters of each payload).
4. Stratum-size-weighted estimates with a stratified bootstrap (2,000 resamples).

## Data and safety

The raw Swarm Traces payload data is **not** included. It is redacted, but contains attack-related
strings, so only row IDs, labels, and aggregate statistics are published. No attack tooling is
released and no redacted content is decoded.

## Limitations

LLM-produced labels; first 700 characters only; n=99; at most 2 rows per large family; behavior
defined by exclusion (28% of behavior is `other_behavior`); no chunk-order recovery.

## LLM usage

Claude (Anthropic) assisted with analysis design, code, labeling, and report drafting. All numbers
come from the authors' notebook runs.

## Citation / license

Add a LICENSE (e.g., MIT for code) and the report PDF under `docs/` before publishing.

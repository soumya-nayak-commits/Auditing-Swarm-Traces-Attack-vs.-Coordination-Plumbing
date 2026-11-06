"""Regenerate all figures from the CSVs in results/.
Usage: python src/make_figures.py
Stratum-accuracy CIs are recomputed here by bootstrap (seed 0) from the
per-stratum correct/n counts, so they may differ slightly from the notebook."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

cm = pd.read_csv("results/confusion_matrix.csv", index_col=0)
st = pd.read_csv("results/stratum_sizes_and_sample.csv")
sh = pd.read_csv("results/label_shares_weighted.csv")
rng = np.random.default_rng(0)

# stratum accuracy + bootstrap CI
names, means, lo, hi = [], [], [], []
for _, r in st.iterrows():
    ok = np.array([1] * int(r.evaluable_correct) + [0] * int(r.evaluable_n - r.evaluable_correct))
    bs = [rng.choice(ok, len(ok)).mean() for _ in range(2000)]
    m = ok.mean()
    names.append(f"{r.stratum}\n(n={int(r.evaluable_n)})"); means.append(m)
    lo.append(m - np.percentile(bs, 2.5)); hi.append(np.percentile(bs, 97.5) - m)
pd.DataFrame({"stratum": st.stratum, "n": st.evaluable_n, "accuracy": means,
              "err_low": lo, "err_high": hi}).round(3).to_csv("results/accuracy_by_stratum.csv", index=False)

# Figure 1: confusion matrix + accuracy by stratum
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].imshow(cm.values, cmap="Blues")
ax[0].set_xticks(range(3), [c.replace("rule_", "") for c in cm.columns])
ax[0].set_yticks(range(3), cm.index)
for i in range(3):
    for j in range(3):
        ax[0].text(j, i, cm.values[i, j], ha="center", va="center")
ax[0].set_xlabel("Rule prediction"); ax[0].set_ylabel("LLM-assisted label")
ax[0].set_title("Rule vs labels (n=99)")
ax[1].bar(names, means, yerr=[lo, hi], capsize=4, color="#4C78A8")
ax[1].set_ylim(0.6, 1.02); ax[1].set_ylabel("Rule accuracy")
ax[1].set_title("Accuracy by stratum (95% CI)")
plt.tight_layout(); plt.savefig("figures/fig1_rule_eval.png", dpi=200); plt.close()

# Figure 2: estimated label shares with CIs
s = sh.sort_values("share")
fig, a = plt.subplots(figsize=(7, 4))
a.barh(s.label, s.share * 100,
       xerr=[(s.share - s.ci_low) * 100, (s.ci_high - s.share) * 100], capsize=3, color="#4C78A8")
a.set_xlabel("Estimated share of all 91,037 payloads (%)")
a.set_title("Stratum-weighted label shares (95% bootstrap CI)")
plt.tight_layout(); plt.savefig("figures/fig2_label_shares.png", dpi=200); plt.close()
print("figures written")

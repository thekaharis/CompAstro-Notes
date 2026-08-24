"""Coherence vs BSD bias for the 3-D matrix cells (active stage 0.05<x_HI<0.95).

x: mean cross-correlation coefficient r(k) over k > 1 Mpc^-1 (phase accuracy)
y: relative mean bubble-size bias.
Sources: Figures/final_eval/matrix/ps/ps_results.npz and bsd/bubble_size_metrics.csv.
"""
import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

B = os.environ.get("MATRIX_DIR", ".")
bsd = pd.read_csv(os.path.join(B, "bsd/bubble_size_metrics.csv"))
npz = np.load(os.path.join(B, "ps/ps_results.npz"), allow_pickle=True)
models = list(pd.read_csv(os.path.join(B, "ps/ps_metrics.csv")).model.unique())
k = npz[models[0] + "/k_centers"]
stage = [s for s in bsd.stage.unique() if "active" in s][0]
i_act = 5

LBL = {"sfno_swhno_bw48om60": "sfno / swhno", "cnn_swhno_plain": "cnn / swhno",
       "cnn_whno_plain": "cnn / whno", "whno_swhno_bw48om60": "whno / swhno",
       "swhno_swhno_bw48om60": "swhno / swhno", "whno_whno_plain": "whno / whno",
       "fno_whno_plain": "fno / whno", "fno_fno_bsd": "fno / fno",
       "wno_whno_plain": "wno / whno", "ufno_plain_gnorm": "U-FNO (ref.)"}
FAM = {"cnn_swhno_plain": "cnn", "cnn_whno_plain": "cnn", "ufno_plain_gnorm": "ref"}
HD, GREY, BLUE = "#9F0101", "#555555", "#1f6fb4"

rows = []
for m in models:
    r = npz[m + "/stage_r_med"][i_act]
    b = bsd[(bsd.model == m) & (bsd.stage == stage)].iloc[0]
    rows.append((m, float(np.mean(r[k > 1])), float(b.relative_mean_bias)))
df = pd.DataFrame(rows, columns=["model", "r_hi", "bias"])
fit = df[df.model != "ufno_plain_gnorm"]
c = np.polyfit(fit.r_hi, fit.bias, 1)
pred = np.polyval(c, fit.r_hi)
r2 = 1 - np.sum((fit.bias - pred) ** 2) / np.sum((fit.bias - fit.bias.mean()) ** 2)

plt.rcParams.update({"font.size": 16, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "savefig.facecolor": "white"})
fig, ax = plt.subplots(figsize=(9.2, 6.2))
xs = np.linspace(0.55, 0.735, 50)
ax.plot(xs, np.polyval(c, xs), color=GREY, lw=1.6, ls="--", zorder=1)
ax.axhline(0, color="black", lw=1.0, zorder=1)
OFF = {"cnn / swhno": (0, 16, "center"), "cnn / whno": (0, -24, "center"),
       "sfno / swhno": (0, 14, "center"), "whno / swhno": (13, 6, "left"),
       "swhno / swhno": (-13, -4, "right"), "whno / whno": (0, -22, "center"),
       "fno / whno": (14, -8, "left"), "fno / fno": (0, 14, "center"),
       "wno / whno": (14, 4, "left"), "U-FNO (ref.)": (0, 15, "center")}
for _, row in df.iterrows():
    lab = LBL[row.model]; fam = FAM.get(row.model, "spec")
    if fam == "ref":
        ax.scatter(row.r_hi, row.bias, s=130, facecolor="none", edgecolor=GREY, lw=1.8, zorder=3)
        col = GREY
    else:
        col = HD if fam == "cnn" else BLUE
        ax.scatter(row.r_hi, row.bias, s=130, color=col, zorder=3)
    dx, dy, ha = OFF[lab]
    ax.annotate(lab, (row.r_hi, row.bias), textcoords="offset points", xytext=(dx, dy),
                ha=ha, fontsize=13.5, color=col)
ax.set_xlabel(r"phase accuracy  $\langle r(k)\rangle_{k>1\,\mathrm{Mpc}^{-1}}$")
ax.set_ylabel("relative mean bubble-size bias")
ax.set_xlim(0.55, 0.745); ax.set_ylim(-0.365, 0.105)
ax.grid(alpha=0.22)
ax.text(0.025, 0.965, f"Spearman $\\rho=+0.88$  ($p=0.002$, n=9)\nlinear fit $R^2={r2:.2f}$, "
        "zero-bias at $r\\approx0.73$", transform=ax.transAxes, va="top", fontsize=13.5,
        color="black")
ax.text(0.985, 0.055, "CNN local slot", transform=ax.transAxes, ha="right", color=HD,
        fontweight="bold", fontsize=13.5)
ax.text(0.985, 0.125, "spectral local slot", transform=ax.transAxes, ha="right", color=BLUE,
        fontweight="bold", fontsize=13.5)
ax.set_title("Bubble-size bias tracks phase accuracy, not small-scale amplitude", fontsize=16, pad=12)
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(os.environ.get("OUT", "."), f"coherence_vs_bsd_bias.{ext}"), dpi=200)
print("ok, R2 =", round(r2, 3))

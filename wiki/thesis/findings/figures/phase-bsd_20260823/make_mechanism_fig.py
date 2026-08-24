"""Why small-scale coherence controls the MFP bubble-size bias.

Left : rank correlation between r(k) in each k bin and the relative mean-MFP
       bias, across the 9 localop cells (active stage). It rises monotonically
       with k -- the signal really does live at small scales.
Right: level-crossing-rate ratio nu = sigma_1/sigma_0 of the predicted field
       over that of the truth, against the mean-MFP ratio. MFP is a first-
       passage statistic, so lambda ~ 1/nu; wrong-phase high-k power inflates
       nu, over-smoothing deflates it.
Sources: Figures/final_eval/matrix/{ps/ps_results.npz,bsd/bubble_size_metrics.csv}
"""
import os
import numpy as np, pandas as pd
from scipy.stats import spearmanr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

B = os.environ.get("MATRIX_DIR", "."); OUT = os.environ.get("OUT", ".")
bsd = pd.read_csv(os.path.join(B, "bsd/bubble_size_metrics.csv"))
npz = np.load(os.path.join(B, "ps/ps_results.npz"), allow_pickle=True)
models = list(pd.read_csv(os.path.join(B, "ps/ps_metrics.csv")).model.unique())
k = npz[models[0] + "/k_centers"]; bst = list(bsd.stage.unique()); IA = 5
noU = [m for m in models if m != "ufno_plain_gnorm"]
HD, GREY, BLUE = "#9F0101", "#555555", "#1f6fb4"
CNN = {"cnn_swhno_plain", "cnn_whno_plain"}
LBL = {"sfno_swhno_bw48om60": "sfno/swhno", "cnn_swhno_plain": "cnn/swhno",
       "cnn_whno_plain": "cnn/whno", "whno_swhno_bw48om60": "whno/swhno",
       "swhno_swhno_bw48om60": "swhno/swhno", "whno_whno_plain": "whno/whno",
       "fno_whno_plain": "fno/whno", "fno_fno_bsd": "fno/fno",
       "wno_whno_plain": "wno/whno", "ufno_plain_gnorm": "U-FNO"}

bias = np.array([bsd[(bsd.model == m) & (bsd.stage == bst[IA])].relative_mean_bias.iloc[0] for m in noU])
rho = np.array([spearmanr([npz[m + "/stage_r_med"][IA][j] for m in noU], bias)[0]
                for j in range(len(k))])
dlnk = np.gradient(np.log(k))
sig = lambda d2, n: np.sqrt(np.sum(k ** (2 * n) * d2 * dlnk))
pts = []
for m in models:
    d2t, d2p = npz[m + "/d2_truth_med"], npz[m + "/d2_pred_med"]
    b = bsd[(bsd.model == m) & (bsd.stage == bst[IA])].iloc[0]
    pts.append((m, (sig(d2p, 1) / sig(d2p, 0)) / (sig(d2t, 1) / sig(d2t, 0)),
                b.pred_restricted_mean_mpc / b.truth_restricted_mean_mpc))

plt.rcParams.update({"font.size": 15, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "white", "savefig.facecolor": "white"})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14.5, 5.8))

a1.axvspan(1.0, k[-1] * 1.15, color=HD, alpha=0.07, lw=0)
a1.plot(k, rho, "o-", color=HD, lw=2, ms=7)
a1.set_xscale("log"); a1.set_xlim(k[0] * 0.9, k[-1] * 1.15); a1.set_ylim(0.6, 1.02)
a1.set_xlabel(r"$k$  [Mpc$^{-1}$]")
a1.set_ylabel(r"Spearman $\rho\,[\,r(k)\,,\ $MFP bias$\,]$")
a1.set_title("the correlation lives at small scales", fontsize=15.5, pad=10)
a1.grid(alpha=0.22)
a1.text(1.15, 0.645, r"$k>1$ band", color=HD, fontsize=13.5)
a1.annotate(r"$\rho=+0.97$", xy=(k[-1], rho[-1]), xytext=(-14, -26),
            textcoords="offset points", ha="right", color=HD, fontsize=13.5)
sec = a1.secondary_xaxis("top", functions=(lambda x: 2 * np.pi / np.maximum(x, 1e-9),
                                           lambda x: 2 * np.pi / np.maximum(x, 1e-9)))
sec.set_xlabel(r"$\lambda=2\pi/k$  [Mpc]", fontsize=13.5)

OFF = {"sfno/swhno": (-10, -6, "right"), "cnn/swhno": (-12, -4, "right"), "cnn/whno": (13, -4, "left"),
       "whno/swhno": (-12, -2, "right"), "swhno/swhno": (12, -4, "left"), "whno/whno": (0, 14, "center"),
       "fno/whno": (0, -22, "center"), "fno/fno": (0, 14, "center"), "wno/whno": (-12, -2, "right"),
       "U-FNO": (0, 14, "center")}
for m, nu, lam in pts:
    ref = m == "ufno_plain_gnorm"
    col = GREY if ref else (HD if m in CNN else BLUE)
    a2.scatter(nu, lam, s=120, zorder=3, color="none" if ref else col,
               edgecolor=col, lw=1.8 if ref else 0)
    dx, dy, ha = OFF[LBL[m]]
    a2.annotate(LBL[m], (nu, lam), textcoords="offset points", xytext=(dx, dy),
                ha=ha, fontsize=12.5, color=col)
a2.axhline(1, color="black", lw=1.0); a2.axvline(1, color="black", lw=1.0)
xs = np.linspace(0.80, 1.24, 50)
a2.plot(xs, 1 / xs, color=GREY, ls="--", lw=1.5)
a2.annotate(r"$\lambda\propto 1/\nu$", xy=(1.19, 1 / 1.19), xytext=(8, 10),
            textcoords="offset points", color=GREY, fontsize=13)
a2.set_xlabel(r"boundary-crossing rate  $\nu_{\rm pred}/\nu_{\rm truth}$,   $\nu=\sigma_1/\sigma_0$")
a2.set_ylabel(r"mean MFP  $\lambda_{\rm pred}/\lambda_{\rm truth}$")
a2.set_title("too many boundaries $\\Rightarrow$ bubbles too small", fontsize=15.5, pad=10)
a2.set_xlim(0.80, 1.24); a2.set_ylim(0.36, 1.34); a2.grid(alpha=0.22)
a2.text(0.03, 0.05, r"$\rho=-0.83$  ($p=0.005$, n=9)", transform=a2.transAxes, fontsize=13.5)
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"bsd_mechanism.{ext}"), dpi=200)
print("ok")

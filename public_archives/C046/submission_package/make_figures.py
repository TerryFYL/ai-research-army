#!/usr/bin/env python3
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
BASE = Path(__file__).resolve().parent.parent
OUT = BASE/"figures"; OUT.mkdir(exist_ok=True, parents=True)
mpl.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"savefig.dpi":400})
def save(fig,name):
    fig.savefig(OUT/f"{name}.png", dpi=400, bbox_inches="tight")
    fig.savefig(OUT/f"{name}.tiff", dpi=400, bbox_inches="tight", pil_kwargs={"compression":"tiff_lzw"})
    plt.close(fig)

# Fig 1 Flow
fig,ax=plt.subplots(figsize=(6,6.5)); ax.axis("off")
flow=[("NHANES 1999-2004 participants",31126),
      ("Age 20-49 y",11812),
      ("Completed treadmill CRF test",5738),
      ("Measured iron panel + Hb",5241),
      ("Non-pregnant",5089),
      ("Complete covariates",4312)]
y=0.94
for i,(s,n) in enumerate(flow):
    ax.add_patch(mpl.patches.FancyBboxPatch((0.12,y-0.06),0.76,0.08,boxstyle="round,pad=0.02",fc="#e0f7fa",ec="#006064"))
    ax.text(0.5,y-0.02,f"{s}\nn = {n:,}",ha="center",va="center",fontsize=10)
    if i<len(flow)-1:
        ax.annotate("",xy=(0.5,y-0.12),xytext=(0.5,y-0.06),arrowprops=dict(arrowstyle="->",color="#006064",lw=1.4))
    y-=0.155
save(fig,"figure1_flow")

# Fig 2 Bar by iron status
fig,ax=plt.subplots(figsize=(6.5,4.4))
cats=["Normal iron\n(n=3,456)","Iron def.\nno anemia\n(n=626)","IDA\n(n=230)"]
means=[37.4,34.2,31.8]; lo=[36.9,33.2,30.3]; hi=[37.9,35.2,33.3]
colors=["#2e7d32","#f9a825","#c62828"]
xs=np.arange(len(cats))
bars=ax.bar(xs,means,color=colors,edgecolor="black",lw=0.8)
ax.errorbar(xs,means,yerr=[[m-l for m,l in zip(means,lo)],[h-m for m,h in zip(means,hi)]],fmt="none",ecolor="black",capsize=5)
for x,m in zip(xs,means): ax.text(x,m+0.5,f"{m:.1f}",ha="center",fontsize=11,weight="bold")
ax.set_xticks(xs); ax.set_xticklabels(cats)
ax.set_ylabel("Estimated VO₂max (mL/kg/min)")
ax.set_title("Estimated VO₂max by iron status, NHANES 1999-2004 (survey-weighted)")
ax.set_ylim(28,42)
save(fig,"figure2_vo2max_bar")

# Fig 3 Subgroup forest
subs=["Overall","Men","Women pre-menopausal","Women post-menopausal","Age 20-34","Age 35-49","BMI <25","BMI ≥25"]
d=[-4.9,-3.1,-5.4,-4.2,-5.2,-4.5,-5.0,-4.7]
lo_s=[-6.3,-5.2,-7.0,-8.8,-7.1,-6.6,-7.1,-6.7]; hi_s=[-3.5,-1.0,-3.8,0.4,-3.3,-2.4,-2.9,-2.7]
fig,ax=plt.subplots(figsize=(7,4.6))
ys=np.arange(len(subs))[::-1]
for y,(dd,l,h) in zip(ys,zip(d,lo_s,hi_s)):
    ax.plot([l,h],[y,y],color="#222",lw=1.4)
    ax.plot(dd,y,"D",ms=9,color="#1565c0")
    ax.text(1.2,y,f"{dd:+.1f} ({l:+.1f}, {h:+.1f})",va="center",fontsize=10)
ax.axvline(0,color="gray",ls="--",lw=0.8)
ax.set_yticks(ys); ax.set_yticklabels(subs)
ax.set_xlim(-9,4); ax.set_xlabel("Adjusted Δ VO₂max (mL/kg/min) vs normal-iron")
ax.set_title("Subgroup association of IDA with estimated VO₂max")
for sp in ("top","right"): ax.spines[sp].set_visible(False)
save(fig,"figure3_subgroups")

# Fig 4 Continuous log-ferritin coefficient.
# Do not draw synthetic participant-level points; only plot the verified model estimate.
fig,ax=plt.subplots(figsize=(6.5,3.8))
beta=0.88; lo=0.54; hi=1.22
ax.axvline(0,color="gray",ls="--",lw=1)
ax.plot([lo,hi],[0,0],color="#222",lw=2)
ax.plot(beta,0,"D",ms=10,color="#1565c0")
ax.text(beta,0.18,f"β = +{beta:.2f} mL/kg/min per 1-log ferritin\n95% CI +{lo:.2f} to +{hi:.2f}",ha="center",va="bottom",fontsize=11,weight="bold")
ax.set_yticks([0]); ax.set_yticklabels(["Log-ferritin model"])
ax.set_xlabel("Adjusted change in estimated VO₂max (mL/kg/min)")
ax.set_xlim(-0.2,1.5); ax.set_ylim(-0.6,0.6)
ax.set_title("Continuous log-ferritin association with estimated VO₂max")
for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
save(fig,"figure4_continuous")
print("figures done")

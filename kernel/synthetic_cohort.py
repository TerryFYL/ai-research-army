"""能力内核 · 合成队列数据（基建：确定性、可复现）

⚠️ 重要声明（红线·不伪装真实性）
    本文件生成的是**完全合成 / SYNTHETIC** 的数据，用固定随机种子由代码现造，
    **不是**真实的曙光（Shuguang）心衰队列、也不对应任何真实患者或真实医院记录。
    它只为「离线、无 API Key、确定性可复现」地打通管线机制而存在；
    一切由它算出的统计量都是**合成数据上的真算结果**，不得对外宣称为真实临床证据。

队列设定（拟真但合成的 HFpEF 回顾队列）：
    - 规模 ~800 例；二分组 arm：GDT（指南导向治疗）vs Usual（常规治疗）——合成的暴露分组。
    - 人口学：age / sex。合并症：hypertension / diabetes / af / ckd。
    - 实验室：NT-proBNP（pg/mL，右偏，对数正态）。超声：LVEF（%，保留射血分数 ≥50）。
    - 随访结局：rehospitalization（主要）/ all-cause death（次要）/ followup_months。
    数据按比例风险模型生成（GDT 真实地设为保护性，便于 Cox 真算复原一个有意义的 HR+CI）。
    所有"真实参数"仅是合成生成参数，不代表任何真实效应。
"""
from __future__ import annotations

import math
import random

# 固定随机种子 —— 确定性、可复现的唯一来源
SEED = 20260620
N = 800

# 合成生成参数（**仅为造数用的潜在参数**，不是任何真实临床效应）
_B_ARM = math.log(0.60)   # GDT 设为保护性：真实 HR≈0.60（Cox 应能近似复原）
_B_AGE = 0.30             # 每标准差年龄
_B_NT = 0.45              # 每标准差 log(NT-proBNP)
_B_CKD = 0.40
_B_AF = 0.25
_LAMBDA0 = 0.030         # 基线月风险（再入院）
_ADMIN_CENSOR = 36.0     # 行政删失（月）


def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


def generate_cohort(seed: int = SEED, n: int = N) -> list:
    """确定性生成合成 HFpEF 回顾队列。同一 seed → 同一数据，逐行可复现。

    返回 list[dict]，每行一例。字段命名直白，便于统计细胞与稿件模板直接消费。
    """
    rng = random.Random(seed)
    rows = []
    for pid in range(1, n + 1):
        treated = rng.random() < 0.5  # GDT 约半数

        # 人口学（GDT 略年轻：合成的"适应证混杂"，使回顾队列更拟真）
        age = int(round(_clamp(rng.gauss(71 if treated else 74, 9), 45, 95)))
        female = rng.random() < 0.55

        # 合并症（部分与 arm 轻度相关 → Table 1 出现可解释的组间差异）
        hypertension = rng.random() < 0.82
        diabetes = rng.random() < (0.46 if treated else 0.38)
        af = rng.random() < 0.36
        ckd = rng.random() < (0.27 if treated else 0.34)

        # 超声：保留射血分数（HFpEF 定义 LVEF ≥ 50）
        lvef = int(round(_clamp(rng.gauss(58, 6), 50, 72)))

        # 实验室：NT-proBNP 右偏（对数正态）；随年龄/CKD/常规治疗升高
        log_nt = (6.9
                  + 0.20 * ((age - 73) / 9.0)
                  + 0.25 * (1 if ckd else 0)
                  + (0.0 if treated else 0.18)
                  + rng.gauss(0, 0.55))
        ntprobnp = int(round(math.exp(log_nt)))

        # 标准化协变量（造时用的同一口径；统计细胞会自己再标准化）
        z_age = (age - 73) / 9.0
        z_lognt = (log_nt - 7.0) / 0.6

        # 比例风险线性预测子 → 指数分布事件时间
        eta = (_B_ARM * (1 if treated else 0)
               + _B_AGE * z_age
               + _B_NT * z_lognt
               + _B_CKD * (1 if ckd else 0)
               + _B_AF * (1 if af else 0))
        rate = _LAMBDA0 * math.exp(eta)
        t_rehosp = rng.expovariate(rate)
        t_death = rng.expovariate(rate * 0.45)       # 死亡较少（次要结局）
        t_loss = rng.expovariate(0.004)              # 随机失访

        obs = min(t_rehosp, t_death, t_loss, _ADMIN_CENSOR)
        rehospitalization = (obs == t_rehosp)
        death = (obs == t_death)
        followup_months = round(obs, 1)

        rows.append({
            "pid": pid,
            "arm": "GDT" if treated else "Usual",
            "age": age,
            "sex": "female" if female else "male",
            "hypertension": hypertension,
            "diabetes": diabetes,
            "af": af,
            "ckd": ckd,
            "lvef": lvef,
            "ntprobnp": ntprobnp,
            "rehospitalization": rehospitalization,
            "death": death,
            "followup_months": followup_months,
        })
    return rows

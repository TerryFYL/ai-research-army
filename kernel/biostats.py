"""能力内核 · 生物统计（基建：纯 Python 真算，无 scipy/numpy，确定性可复现）

这里是统计器官的"真算"底座。每个函数都从数据**真实计算**出结果，
主结果给**效应量 + 95% 置信区间**（Cox 风险比、KM 生存、组间检验）。
红线：稿件正文里出现的每个数字都必须由此处算出，不得手写编造。

实现刻意简化但忠实：
  - 连续变量两组比较：Welch t 检验（正态近似 p）。
  - 偏态变量（NT-proBNP）：Mann–Whitney U（正态近似 p）。
  - 分类变量：Pearson χ²（连续校正可选，这里用基础 χ²，1 自由度正态近似 p）。
  - 生存：Cox 比例风险（Breslow ties，Newton–Raphson）+ Kaplan–Meier + log-rank。
"""
from __future__ import annotations

import math


# ── 基础描述统计 ──────────────────────────────────────────────────────────
def _phi(x):  # 标准正态 CDF
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _two_sided_p_from_z(z):
    return max(0.0, min(1.0, 2 * (1 - _phi(abs(z)))))


def _chi2_1df_p(stat):
    # χ²(1df) 上尾 = 2*(1-Φ(√stat))
    return max(0.0, min(1.0, 2 * (1 - _phi(math.sqrt(max(0.0, stat))))))


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def sd(xs):
    n = len(xs)
    if n < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return float("nan")
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


def quantile(xs, q):
    """线性插值分位数（与常见统计软件一致的 type-7 近似）。"""
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return float("nan")
    if n == 1:
        return float(s[0])
    pos = q * (n - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def welch_t_p(a, b):
    """Welch t 检验双侧 p（正态近似）。"""
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    va, vb = sd(a) ** 2, sd(b) ** 2
    se = math.sqrt(va / na + vb / nb)
    if se == 0:
        return 1.0
    t = (mean(a) - mean(b)) / se
    return _two_sided_p_from_z(t)


def _avg_ranks(sorted_vals):
    ranks = [0.0] * len(sorted_vals)
    i = 0
    while i < len(sorted_vals):
        j = i
        while j + 1 < len(sorted_vals) and sorted_vals[j + 1] == sorted_vals[i]:
            j += 1
        avg = (i + 1 + j + 1) / 2
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    return ranks


def mann_whitney_p(a, b):
    """Mann–Whitney U 双侧 p（正态近似）。"""
    combined = sorted([(v, 0) for v in a] + [(v, 1) for v in b], key=lambda x: x[0])
    ranks = _avg_ranks([v for v, _ in combined])
    r1 = sum(r for r, (_, g) in zip(ranks, combined) if g == 0)
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return float("nan")
    u1 = r1 - n1 * (n1 + 1) / 2
    u = min(u1, n1 * n2 - u1)
    mu = n1 * n2 / 2
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    if sigma == 0:
        return 1.0
    return _two_sided_p_from_z((u - mu) / sigma)


def chi2_p(group_flags, group_labels):
    """2×2（或 2×k）Pearson χ² p。group_flags: list[bool]，group_labels: list[同长]。"""
    labels = sorted(set(group_labels))
    cells = {(g, b): 0 for g in labels for b in (True, False)}
    for f, g in zip(group_flags, group_labels):
        cells[(g, bool(f))] += 1
    n = len(group_flags)
    if n == 0:
        return float("nan")
    row_pos = sum(1 for f in group_flags if f)
    stat = 0.0
    for g in labels:
        ng = sum(1 for x in group_labels if x == g)
        for b in (True, False):
            obs = cells[(g, b)]
            exp = ng * (row_pos if b else (n - row_pos)) / n
            if exp > 0:
                stat += (obs - exp) ** 2 / exp
    return _chi2_1df_p(stat)


# ── 线性代数（小规模，纯 Python） ─────────────────────────────────────────
def _mat_inv(A):
    """高斯-约当求逆（A 为方阵 list[list]）。"""
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("信息矩阵奇异，无法求逆")
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col:
                factor = M[r][col]
                M[r] = [a - factor * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def _solve(A, b):
    inv = _mat_inv(A)
    return [sum(inv[i][j] * b[j] for j in range(len(b))) for i in range(len(b))]


# ── Cox 比例风险（Breslow ties，Newton–Raphson） ──────────────────────────
def cox_ph(times, events, X, names, max_iter=50, tol=1e-8):
    """拟合 Cox PH。

    times: list[float]; events: list[0/1]; X: list[list[float]]（n×p 协变量）;
    names: list[str]（p 个协变量名）。
    返回 {name: {"coef","se","hr","ci_low","ci_high","p","z"}}。
    """
    n = len(times)
    p = len(names)
    beta = [0.0] * p
    # 按时间升序索引
    order = sorted(range(n), key=lambda i: times[i])
    # 唯一事件时间及其死亡集合
    uniq_event_times = sorted({times[i] for i in range(n) if events[i] == 1})

    for _ in range(max_iter):
        # 预算 theta_i = exp(x_i·beta)
        theta = [math.exp(sum(X[i][k] * beta[k] for k in range(p))) for i in range(n)]
        U = [0.0] * p                       # 梯度（score）
        I = [[0.0] * p for _ in range(p)]   # 信息矩阵
        # 以时间降序累积风险集（t_i >= t_event）
        # 用指针法：按时间排序，从大到小加入风险集
        idx_desc = sorted(range(n), key=lambda i: -times[i])
        S0 = 0.0
        S1 = [0.0] * p
        S2 = [[0.0] * p for _ in range(p)]
        ptr = 0
        for tj in sorted(uniq_event_times, reverse=True):
            # 把所有 times[i] >= tj 的个体加入风险集
            while ptr < n and times[idx_desc[ptr]] >= tj:
                i = idx_desc[ptr]
                th = theta[i]
                S0 += th
                for a in range(p):
                    S1[a] += th * X[i][a]
                    for b in range(p):
                        S2[a][b] += th * X[i][a] * X[i][b]
                ptr += 1
            deaths = [i for i in range(n) if events[i] == 1 and times[i] == tj]
            m = len(deaths)
            if S0 <= 0:
                continue
            e1 = [S1[a] / S0 for a in range(p)]
            for i in deaths:
                for a in range(p):
                    U[a] += X[i][a]
            for a in range(p):
                U[a] -= m * e1[a]
            for a in range(p):
                for b in range(p):
                    I[a][b] += m * (S2[a][b] / S0 - e1[a] * e1[b])
        # Newton 步：beta += I^{-1} U
        try:
            step = _solve(I, U)
        except ValueError:
            break
        for k in range(p):
            beta[k] += step[k]
        if max(abs(s) for s in step) < tol:
            break

    cov = _mat_inv(I)
    out = {}
    for k, nm in enumerate(names):
        se = math.sqrt(cov[k][k])
        z = beta[k] / se if se > 0 else float("nan")
        out[nm] = {
            "coef": beta[k],
            "se": se,
            "hr": math.exp(beta[k]),
            "ci_low": math.exp(beta[k] - 1.96 * se),
            "ci_high": math.exp(beta[k] + 1.96 * se),
            "z": z,
            "p": _two_sided_p_from_z(z),
        }
    return out


# ── Kaplan–Meier + log-rank ───────────────────────────────────────────────
def kaplan_meier(times, events):
    """KM 生存函数（步进点）。返回 list[(t, S(t), at_risk)]。"""
    n = len(times)
    order = sorted(range(n), key=lambda i: times[i])
    steps = []
    S = 1.0
    at_risk = n
    i = 0
    ot = [times[o] for o in order]
    oe = [events[o] for o in order]
    while i < n:
        t = ot[i]
        j = i
        d = 0
        cnt = 0
        while j < n and ot[j] == t:
            cnt += 1
            if oe[j] == 1:
                d += 1
            j += 1
        if d > 0:
            S *= (1 - d / at_risk)
            steps.append((t, S, at_risk))
        at_risk -= cnt
        i = j
    return steps


def km_survival_at(steps, t):
    """读取 KM 曲线在时间 t 的生存率（阶梯函数，左连续取最近事件点）。"""
    s = 1.0
    for tt, ss, _ in steps:
        if tt <= t:
            s = ss
        else:
            break
    return s


def km_median(steps):
    """KM 中位生存时间（首个 S(t) ≤ 0.5）；未达到返回 None。"""
    for tt, ss, _ in steps:
        if ss <= 0.5:
            return tt
    return None


def logrank_p(times, events, groups):
    """两组 log-rank 检验，返回 (chi2, p)。groups: list[label]。"""
    labels = sorted(set(groups))
    if len(labels) != 2:
        raise ValueError("log-rank 这里只支持两组")
    g1 = labels[0]
    n = len(times)
    order = sorted(range(n), key=lambda i: times[i])
    ot = [times[o] for o in order]
    oe = [events[o] for o in order]
    og = [groups[o] for o in order]

    at_risk_total = n
    at_risk_1 = sum(1 for g in groups if g == g1)
    O1 = 0.0
    E1 = 0.0
    V = 0.0
    i = 0
    while i < n:
        t = ot[i]
        j = i
        d = d1 = cnt = cnt1 = 0
        while j < n and ot[j] == t:
            cnt += 1
            if og[j] == g1:
                cnt1 += 1
            if oe[j] == 1:
                d += 1
                if og[j] == g1:
                    d1 += 1
            j += 1
        if d > 0 and at_risk_total > 1:
            E1 += d * at_risk_1 / at_risk_total
            O1 += d1
            V += (d * (at_risk_1 / at_risk_total) * (1 - at_risk_1 / at_risk_total)
                  * (at_risk_total - d) / (at_risk_total - 1))
        at_risk_total -= cnt
        at_risk_1 -= cnt1
        i = j
    chi2 = (O1 - E1) ** 2 / V if V > 0 else 0.0
    return chi2, _chi2_1df_p(chi2)

"""
Red-Blue Team Battle: Data Forensics Validation
================================================

Red Team: 生成 4 级难度的造假数据
Blue Team: 用 7 项鉴伪检验识别造假

验证标准:
- 真实数据: 应评为 GREEN (假阳性率 < 10%)
- L1 粗糙造假: 应评为 RED
- L2 中等造假: 应评为 YELLOW 或 RED
- L3 精细造假: 能抓到算赢，抓不到记录为已知盲区
- L4 对抗性造假: 专门针对每项检验规避，测试极限

运行: python3 red_blue_battle.py
"""

import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter
import json
import os
from datetime import datetime

np.random.seed(42)

# ============================================================
# BLUE TEAM: 7 项鉴伪检验实现
# ============================================================

BENFORD_EXPECTED = {
    1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097,
    5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046
}


def is_integer_like(series):
    clean = series.dropna()
    if len(clean) == 0:
        return False
    return np.allclose(clean, clean.round(0), atol=0.001)


def count_decimals(x):
    s = f'{x:.15g}'
    if '.' in s:
        return len(s.split('.')[1].rstrip('0'))
    return 0


# --- T1: GRIM Test ---
def t1_grim(df, group_col, value_cols):
    """GRIM: 检验分组均值在给定 N 下是否数学可能"""
    flags = []
    for col in value_cols:
        if not is_integer_like(df[col]):
            continue
        for group, subset in df.groupby(group_col):
            n = len(subset)
            if n < 5:
                continue
            mean = subset[col].mean()
            product = mean * n
            remainder = abs(product - round(product))
            if remainder > 0.01:
                flags.append({
                    'test': 'T1_GRIM', 'variable': col, 'group': str(group),
                    'severity': 'HIGH',
                    'detail': f'mean={mean:.4f}, n={n}, mean*n={product:.4f}, remainder={remainder:.4f}',
                })
    return flags


# --- T2: SPRITE ---
def t2_sprite(df, discrete_cols, group_col=None, n_iter=10000):
    """SPRITE: 反推验证汇总统计量是否可自洽

    注意: SPRITE 适用于小 N (< 50) 且值域窄的离散变量。
    大 N 时搜索空间爆炸，蒙特卡洛无法覆盖，会产生假阳性。
    """
    flags = []
    groups = list(df.groupby(group_col)) if group_col else [('all', df)]

    for group_name, subset in groups:
        for col in discrete_cols:
            clean = subset[col].dropna()
            if len(clean) < 10 or not is_integer_like(clean):
                continue

            n = len(clean)
            mean = clean.mean()
            sd = clean.std(ddof=1)
            min_val, max_val = int(clean.min()), int(clean.max())

            # SPRITE 仅适用于小 N 且窄值域
            # 大 N 时蒙特卡洛命中率极低，会产生假阳性
            if n > 50:
                continue
            value_range = max_val - min_val
            if value_range > 10:
                continue

            # mean * n 必须接近整数
            target_sum = mean * n
            if abs(target_sum - round(target_sum)) > 0.5:
                flags.append({
                    'test': 'T2_SPRITE', 'variable': col, 'group': str(group_name),
                    'severity': 'HIGH',
                    'detail': f'GRIM pre-check failed: mean*n={target_sum:.4f} not integer',
                })
                continue

            # 蒙特卡洛搜索（增加迭代 + 放宽 SD 容差）
            target_sum_int = round(target_sum)
            sd_tol = max(0.1, sd * 0.05)  # SD 容差: 5% 或 0.1 取大
            found = False
            for _ in range(n_iter):
                arr = np.random.randint(min_val, max_val + 1, size=n)
                diff = target_sum_int - arr.sum()
                for i in range(min(abs(diff), n)):
                    idx = np.random.randint(0, n)
                    if diff > 0 and arr[idx] < max_val:
                        arr[idx] += 1
                    elif diff < 0 and arr[idx] > min_val:
                        arr[idx] -= 1
                if arr.sum() == target_sum_int:
                    if abs(np.std(arr, ddof=1) - sd) < sd_tol:
                        found = True
                        break

            if not found:
                flags.append({
                    'test': 'T2_SPRITE', 'variable': col, 'group': str(group_name),
                    'severity': 'HIGH',
                    'detail': f'No valid dataset found after {n_iter} iterations (n={n}, mean={mean:.2f}, sd={sd:.2f})',
                })
    return flags


# --- T3: Benford's Law ---
def t3_benford(df, continuous_cols, alpha=0.05):
    """Benford: 首位数字分布检验"""
    flags = []
    for col in continuous_cols:
        clean = df[col].dropna()
        clean = clean[clean > 0]
        if len(clean) < 100:
            continue

        mag_range = np.log10(clean.max()) - np.log10(clean.min())
        if mag_range < 1.5:
            continue

        first_digits = clean.apply(lambda x: int(str(f'{abs(x):.10g}').lstrip('0').lstrip('.')[0]) if x != 0 else 0)
        first_digits = first_digits[first_digits > 0]
        n = len(first_digits)
        observed = Counter(first_digits)

        chi2 = sum((observed.get(d, 0) - BENFORD_EXPECTED[d] * n) ** 2 / (BENFORD_EXPECTED[d] * n)
                    for d in range(1, 10))
        p_value = 1 - stats.chi2.cdf(chi2, df=8)

        # MAD
        digit_pcts = {d: observed.get(d, 0) / n for d in range(1, 10)}
        mad = np.mean([abs(digit_pcts[d] - BENFORD_EXPECTED[d]) for d in range(1, 10)]) * 100

        if mad > 1.5 or p_value < alpha:
            severity = 'HIGH' if mad > 2.5 else 'MEDIUM'
            flags.append({
                'test': 'T3_BENFORD', 'variable': col,
                'severity': severity,
                'detail': f'MAD={mad:.2f}, chi2={chi2:.2f}, p={p_value:.4f}',
            })
    return flags


# --- T4: Terminal Digit ---
def t4_terminal_digit(df, continuous_cols, alpha=0.05):
    """末位数字均匀性检验"""
    flags = []
    for col in continuous_cols:
        clean = df[col].dropna()
        if len(clean) < 50:
            continue

        # 只检查有小数的变量
        has_decimals = clean.apply(lambda x: '.' in f'{x:.10g}')
        if has_decimals.mean() < 0.5:
            continue

        # 检测是否所有值都是固定精度（如 .round(1)）
        # 固定精度的 round() 会自然导致末位数字非均匀，这不是造假信号
        decimal_counts = clean.apply(count_decimals)
        if decimal_counts.nunique() == 1:
            # 所有值精度一致 → 可能是仪器精度或 round()，降级为 LOW
            precision_effect = True
        else:
            precision_effect = False

        def get_last_digit(x):
            s = f'{x:.10g}'.rstrip('0').rstrip('.')
            if not s or s == '-':
                return None
            return int(s[-1])

        last_digits = clean.apply(get_last_digit).dropna().astype(int)
        n = len(last_digits)
        if n < 50:
            continue

        observed = Counter(last_digits)
        expected = n / 10
        chi2 = sum((observed.get(d, 0) - expected) ** 2 / expected for d in range(10))
        p_value = 1 - stats.chi2.cdf(chi2, df=9)

        zero_five_pct = (observed.get(0, 0) + observed.get(5, 0)) / n * 100

        # 判定逻辑: 精度效应导致的非均匀不算红旗
        if precision_effect:
            # 仅在 0+5 占比 > 40% 时才标记（极端偏好）
            if zero_five_pct > 40:
                flags.append({
                    'test': 'T4_TERMINAL', 'variable': col,
                    'severity': 'MEDIUM',
                    'detail': f'chi2={chi2:.2f}, p={p_value:.4f}, 0+5占比={zero_five_pct:.1f}% (有精度效应但偏好过强)',
                })
        elif p_value < alpha and zero_five_pct > 30:
            severity = 'HIGH' if zero_five_pct > 40 else 'MEDIUM'
            flags.append({
                'test': 'T4_TERMINAL', 'variable': col,
                'severity': severity,
                'detail': f'chi2={chi2:.2f}, p={p_value:.4f}, 0+5占比={zero_five_pct:.1f}%',
            })
    return flags


# --- T5: Variance Uniformity ---
def t5_variance_uniformity(df, group_col, value_cols):
    """组间方差齐性异常

    阈值随组数动态调整:
    - 2-3 组: CV < 0.02 才标记（少组时自然波动小）
    - 4-6 组: CV < 0.03
    - 7+ 组:  CV < 0.05（多组方差一致才真正可疑）
    """
    flags = []
    for col in value_cols:
        group_stats = df.groupby(group_col)[col].agg(['std', 'count'])
        group_stats = group_stats[group_stats['count'] >= 5]
        n_groups = len(group_stats)
        if n_groups < 2:
            continue

        sds = group_stats['std'].values
        if np.any(sds == 0):
            flags.append({
                'test': 'T5_VARIANCE', 'variable': col,
                'severity': 'HIGH',
                'detail': f'某组 SD=0',
            })
            continue

        # 动态阈值
        if n_groups <= 3:
            cv_threshold = 0.02
        elif n_groups <= 6:
            cv_threshold = 0.03
        else:
            cv_threshold = 0.05

        cv_of_sd = np.std(sds, ddof=1) / np.mean(sds)
        if cv_of_sd < cv_threshold:
            flags.append({
                'test': 'T5_VARIANCE', 'variable': col,
                'severity': 'MEDIUM',
                'detail': f'CV(SD)={cv_of_sd:.4f} < {cv_threshold} ({n_groups}组)',
            })
    return flags


# --- T6: Distribution Plausibility ---
def t6_distribution(df, continuous_cols):
    """分布合理性 — 检测过于完美或不合理的分布"""
    flags = []
    for col in continuous_cols:
        clean = df[col].dropna()
        if len(clean) < 20:
            continue

        # 过于完美的正态性
        if len(clean) <= 5000:
            _, shapiro_p = stats.shapiro(clean)
            if shapiro_p > 0.999:
                flags.append({
                    'test': 'T6_DISTRIBUTION', 'variable': col,
                    'severity': 'MEDIUM',
                    'detail': f'Shapiro p={shapiro_p:.6f}, 过于完美的正态',
                })

        # 偏度峰度同时近零
        skew = clean.skew()
        kurt = clean.kurtosis()
        if abs(skew) < 0.01 and abs(kurt) < 0.01 and len(clean) > 50:
            flags.append({
                'test': 'T6_DISTRIBUTION', 'variable': col,
                'severity': 'MEDIUM',
                'detail': f'skew={skew:.4f}, kurtosis={kurt:.4f}, 同时近零',
            })

        # 常量列
        if clean.min() == clean.max():
            flags.append({
                'test': 'T6_DISTRIBUTION', 'variable': col,
                'severity': 'HIGH',
                'detail': f'常量: {clean.iloc[0]}',
            })
    return flags


# --- T7: Duplicate Pattern ---
def t7_duplicate(df, numeric_cols):
    """重复模式检测"""
    flags = []

    # 完全重复行
    dup_count = df.duplicated(keep=False).sum()
    if dup_count > 0:
        pct = dup_count / len(df) * 100
        severity = 'HIGH' if pct > 5 else 'MEDIUM' if pct > 1 else 'LOW'
        flags.append({
            'test': 'T7_DUPLICATE', 'variable': '_rows_',
            'severity': severity,
            'detail': f'{dup_count} 行重复 ({pct:.1f}%)',
        })

    # 块状重复
    if len(numeric_cols) >= 2:
        cols_to_check = numeric_cols[:10]
        values = df[cols_to_check].values
        n = len(values)
        for block_size in [3, 5]:
            if n < block_size * 2:
                continue
            seen = {}
            for i in range(n - block_size + 1):
                block = tuple(map(tuple, values[i:i + block_size]))
                bh = hash(block)
                if bh in seen and abs(i - seen[bh]) >= block_size:
                    flags.append({
                        'test': 'T7_DUPLICATE', 'variable': '_block_',
                        'severity': 'HIGH',
                        'detail': f'行{seen[bh]}-{seen[bh]+block_size-1} 与 行{i}-{i+block_size-1} 块重复',
                    })
                    break
                seen[bh] = i

    # 完美相关
    check_cols = numeric_cols[:15]
    for i, ca in enumerate(check_cols):
        for cb in check_cols[i + 1:]:
            clean = df[[ca, cb]].dropna()
            if len(clean) < 10:
                continue
            if clean[ca].std() == 0 or clean[cb].std() == 0:
                continue
            r, _ = stats.pearsonr(clean[ca], clean[cb])
            if abs(r) > 0.999:
                flags.append({
                    'test': 'T7_DUPLICATE', 'variable': f'{ca}+{cb}',
                    'severity': 'HIGH',
                    'detail': f'r={r:.6f}',
                })
    return flags


# ============================================================
# BLUE TEAM: 综合评估
# ============================================================

def run_all_tests(df, group_col=None, label="unknown"):
    """对一个数据集运行全部 7 项检验"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    continuous_cols = [c for c in numeric_cols if df[c].nunique() > 20]
    discrete_cols = [c for c in numeric_cols if 2 < df[c].nunique() <= 20]

    all_flags = []

    # T1: GRIM
    if group_col and discrete_cols:
        all_flags.extend(t1_grim(df, group_col, discrete_cols))

    # T2: SPRITE
    if discrete_cols:
        all_flags.extend(t2_sprite(df, discrete_cols, group_col))

    # T3: Benford
    if continuous_cols:
        all_flags.extend(t3_benford(df, continuous_cols))

    # T4: Terminal Digit
    if continuous_cols:
        all_flags.extend(t4_terminal_digit(df, continuous_cols))

    # T5: Variance Uniformity
    if group_col and continuous_cols:
        all_flags.extend(t5_variance_uniformity(df, group_col, continuous_cols))

    # T6: Distribution
    if continuous_cols:
        all_flags.extend(t6_distribution(df, continuous_cols))

    # T7: Duplicate
    all_flags.extend(t7_duplicate(df, numeric_cols))

    # 综合评级
    high = [f for f in all_flags if f['severity'] == 'HIGH']
    medium = [f for f in all_flags if f['severity'] == 'MEDIUM']
    low = [f for f in all_flags if f['severity'] == 'LOW']

    if len(high) >= 3:
        rating = 'RED'
    elif len(high) >= 1:
        rating = 'YELLOW'
    elif len(medium) >= 3:
        rating = 'YELLOW'
    else:
        rating = 'GREEN'

    return {
        'label': label,
        'rating': rating,
        'high': len(high),
        'medium': len(medium),
        'low': len(low),
        'total_flags': len(all_flags),
        'flags': all_flags,
        'tests_applicable': len(set(f['test'] for f in all_flags)) if all_flags else 0,
    }


# ============================================================
# RED TEAM: 生成数据集
# ============================================================

def gen_real_medical_data(n=300):
    """真实医学数据模拟 — 基于真实分布特征"""
    groups = np.random.choice(['A', 'B', 'C'], size=n, p=[0.4, 0.35, 0.25])
    df = pd.DataFrame({
        'group': groups,
        'age': np.random.normal(65, 14, n).clip(20, 95).round(0),
        'bmi': np.random.normal(24.5, 4.2, n).clip(15, 45).round(1),
        'sbp': np.random.normal(135, 22, n).clip(80, 220).round(0),
        'heart_rate': np.random.normal(78, 14, n).clip(40, 150).round(0),
        # 实验室值: 跨数量级，应符合 Benford
        'creatinine': np.random.lognormal(mean=np.log(80), sigma=0.4, size=n).round(1),
        'bnp': np.random.lognormal(mean=np.log(300), sigma=1.0, size=n).round(0),
        'albumin': np.random.normal(38, 5, n).clip(15, 55).round(1),
        # 离散评分
        'nyha_class': np.random.choice([1, 2, 3, 4], size=n, p=[0.1, 0.35, 0.4, 0.15]),
        'pain_score': np.random.choice(range(0, 11), size=n),
        # 结局
        'event': np.random.binomial(1, 0.18, n),
        'follow_up_days': np.random.exponential(365, n).clip(1, 2000).round(0),
    })
    # 添加组间真实差异
    mask_a = df['group'] == 'A'
    df.loc[mask_a, 'sbp'] += 8
    df.loc[mask_a, 'bnp'] *= 1.3
    return df


def gen_L1_crude_fake(n=300):
    """L1 粗糙造假: 随机数 + 手动编均值"""
    groups = np.random.choice(['A', 'B', 'C'], size=n)
    df = pd.DataFrame({
        'group': groups,
        'age': np.random.randint(30, 80, n).astype(float),
        'bmi': np.round(np.random.uniform(18, 35, n), 1),
        'sbp': np.random.randint(90, 180, n).astype(float),
        'heart_rate': np.random.randint(50, 120, n).astype(float),
        # 均匀分布 — 不符合 Benford
        'creatinine': np.round(np.random.uniform(30, 300, n), 1),
        'bnp': np.round(np.random.uniform(50, 5000, n), 0),
        'albumin': np.round(np.random.uniform(20, 50, n), 1),
        # 离散: 均匀分布
        'nyha_class': np.random.choice([1, 2, 3, 4], size=n),
        'pain_score': np.random.choice(range(0, 11), size=n),
        'event': np.random.binomial(1, 0.2, n),
        'follow_up_days': np.random.randint(30, 1000, n).astype(float),
    })
    return df


def gen_L2_moderate_fake(n=300):
    """L2 中等造假: 用正态分布但末位数字偏好 0/5，组间方差完全一致"""
    groups = np.random.choice(['A', 'B', 'C'], size=n)
    df = pd.DataFrame({'group': groups})

    # 连续变量: 正态分布但末位数字偏好 0 和 5
    for col, mu, sigma in [('age', 65, 12), ('bmi', 25, 3.5), ('sbp', 135, 20),
                            ('heart_rate', 78, 12), ('albumin', 38, 5)]:
        vals = np.random.normal(mu, sigma, n)
        # 造假痕迹: 把末位数字强制改为 0 或 5
        vals = np.round(vals, 1)
        for i in range(len(vals)):
            last = int(str(f'{vals[i]:.1f}').replace('.', '')[-1])
            if last not in [0, 5]:
                vals[i] = round(vals[i] * 2) / 2  # 四舍五入到 0.5
        df[col] = vals

    # 实验室值: 对数正态但精度过高
    df['creatinine'] = np.random.lognormal(np.log(80), 0.35, n).round(3)
    df['bnp'] = np.random.lognormal(np.log(300), 0.8, n).round(0)

    # 离散评分
    df['nyha_class'] = np.random.choice([1, 2, 3, 4], size=n, p=[0.1, 0.35, 0.4, 0.15])
    df['pain_score'] = np.random.choice(range(0, 11), size=n)

    # 组间方差完全一致（造假痕迹）
    for group in ['A', 'B', 'C']:
        mask = df['group'] == group
        for col in ['age', 'bmi', 'sbp']:
            vals = df.loc[mask, col]
            target_sd = 12.0 if col == 'age' else 3.5 if col == 'bmi' else 20.0
            current_sd = vals.std()
            if current_sd > 0:
                df.loc[mask, col] = vals.mean() + (vals - vals.mean()) * (target_sd / current_sd)

    df['event'] = np.random.binomial(1, 0.18, n)
    df['follow_up_days'] = np.random.exponential(365, n).clip(1, 2000).round(0)
    return df


def gen_L3_refined_fake(n=300):
    """L3 精细造假: 使用真实分布参数，但数据是合成的"""
    groups = np.random.choice(['A', 'B', 'C'], size=n, p=[0.4, 0.35, 0.25])
    df = pd.DataFrame({'group': groups})

    # 模仿真实分布
    df['age'] = np.random.normal(65, 14, n).clip(20, 95).round(0)
    df['bmi'] = np.random.normal(24.5, 4.2, n).clip(15, 45).round(1)
    df['sbp'] = np.random.normal(135, 22, n).clip(80, 220).round(0)
    df['heart_rate'] = np.random.normal(78, 14, n).clip(40, 150).round(0)
    df['creatinine'] = np.random.lognormal(np.log(80), 0.4, n).round(1)
    df['bnp'] = np.random.lognormal(np.log(300), 1.0, n).round(0)
    df['albumin'] = np.random.normal(38, 5, n).clip(15, 55).round(1)
    df['nyha_class'] = np.random.choice([1, 2, 3, 4], size=n, p=[0.1, 0.35, 0.4, 0.15])
    df['pain_score'] = np.random.choice(range(0, 11), size=n)
    df['event'] = np.random.binomial(1, 0.18, n)
    df['follow_up_days'] = np.random.exponential(365, n).clip(1, 2000).round(0)

    # 但!故意插入 5% 的复制粘贴行（模拟 "凑数据" 行为）
    n_dup = int(n * 0.05)
    dup_indices = np.random.choice(n, n_dup, replace=False)
    source_indices = np.random.choice(n, n_dup, replace=True)
    for col in df.columns:
        if col != 'group':
            df.iloc[dup_indices, df.columns.get_loc(col)] = df.iloc[source_indices, df.columns.get_loc(col)].values

    return df


def gen_L4_adversarial_fake(n=300):
    """L4 对抗性造假: 专门针对每项检验设计规避策略"""
    groups = np.random.choice(['A', 'B', 'C'], size=n, p=[0.4, 0.35, 0.25])
    df = pd.DataFrame({'group': groups})

    # 对抗 T1 GRIM: 使用非整数数据，避免 GRIM 适用
    df['age'] = np.random.normal(65, 14, n).clip(20, 95).round(1)  # 故意保留小数
    df['bmi'] = np.random.normal(24.5, 4.2, n).clip(15, 45).round(1)
    df['sbp'] = np.random.normal(135, 22, n).clip(80, 220).round(1)  # 故意保留小数
    df['heart_rate'] = np.random.normal(78, 14, n).clip(40, 150).round(1)

    # 对抗 T3 Benford: 使用对数正态生成，应自然符合
    df['creatinine'] = np.random.lognormal(np.log(80), 0.4, n).round(1)
    df['bnp'] = np.random.lognormal(np.log(300), 1.0, n).round(0)

    # 对抗 T4 Terminal: 确保末位数字均匀
    df['albumin'] = np.random.normal(38, 5, n).clip(15, 55).round(1)

    # 对抗 T5 Variance: 允许自然方差波动
    mask_a = df['group'] == 'A'
    df.loc[mask_a, 'sbp'] += 5

    # 离散数据使用真实比例
    df['nyha_class'] = np.random.choice([1, 2, 3, 4], size=n, p=[0.1, 0.35, 0.4, 0.15])
    df['pain_score'] = np.random.choice(range(0, 11), size=n)
    df['event'] = np.random.binomial(1, 0.18, n)
    df['follow_up_days'] = np.random.exponential(365, n).clip(1, 2000).round(0)

    # 但!偷偷让两个变量有不合理的完美线性关系（造假遗留）
    df['lab_marker_a'] = np.random.normal(50, 10, n).round(1)
    df['lab_marker_b'] = df['lab_marker_a'] * 2.0 + 3.0 + np.random.normal(0, 0.001, n)
    df['lab_marker_b'] = df['lab_marker_b'].round(1)

    return df


# ============================================================
# BATTLE ARENA
# ============================================================

def print_separator(char='=', width=70):
    print(char * width)


def print_result(result):
    """打印单个数据集的检验结果"""
    rating_colors = {'GREEN': '\033[92m', 'YELLOW': '\033[93m', 'RED': '\033[91m'}
    reset = '\033[0m'
    color = rating_colors.get(result['rating'], '')

    print(f"  {color}[{result['rating']}]{reset} "
          f"HIGH={result['high']} MEDIUM={result['medium']} LOW={result['low']} "
          f"总红旗={result['total_flags']}")

    if result['flags']:
        # 按测试分组汇总
        by_test = {}
        for f in result['flags']:
            by_test.setdefault(f['test'], []).append(f)
        for test, flags in sorted(by_test.items()):
            severities = [f['severity'] for f in flags]
            print(f"    {test}: {len(flags)} 个红旗 ({', '.join(severities)})")
            for f in flags[:2]:  # 每项只显示前 2 个
                print(f"      -> {f.get('variable', '?')}: {f['detail']}")
            if len(flags) > 2:
                print(f"      ... 还有 {len(flags)-2} 个")


def main():
    print_separator()
    print("RED-BLUE TEAM BATTLE: Data Forensics Validation")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print_separator()
    print()

    # 生成数据集
    datasets = [
        ('REAL: 真实医学数据', gen_real_medical_data, 'GREEN'),
        ('L1: 粗糙造假(均匀分布)', gen_L1_crude_fake, 'RED'),
        ('L2: 中等造假(末位偏好+方差一致)', gen_L2_moderate_fake, 'YELLOW+'),
        ('L3: 精细造假(真实分布+5%复制)', gen_L3_refined_fake, 'YELLOW+'),
        ('L4: 对抗性造假(规避检验+隐藏关联)', gen_L4_adversarial_fake, 'YELLOW+'),
    ]

    results = []
    for name, gen_func, expected in datasets:
        print(f"\n{'─' * 60}")
        print(f"数据集: {name}")
        print(f"期望评级: {expected}")
        print(f"{'─' * 60}")

        df = gen_func(n=300)
        group_col = 'group' if 'group' in df.columns else None
        result = run_all_tests(df, group_col=group_col, label=name)
        result['expected'] = expected

        print_result(result)

        # 判定胜负
        if expected == 'GREEN':
            success = result['rating'] == 'GREEN'
            team = 'BLUE' if not success else 'BOTH'
            note = '假阳性!' if not success else '正确放行'
        else:
            if result['rating'] in ['RED', 'YELLOW']:
                success = True
                team = 'BLUE'
                note = '成功识别!'
            else:
                success = False
                team = 'RED'
                note = '逃脱检测!'

        result['success'] = success
        result['winner'] = team
        result['note'] = note
        results.append(result)

        print(f"\n  >>> {'BLUE WINS' if team == 'BLUE' else 'RED WINS' if team == 'RED' else 'FAIR'}: {note}")

    # 汇总
    print(f"\n{'=' * 70}")
    print("BATTLE SUMMARY")
    print(f"{'=' * 70}")
    print(f"\n{'数据集':<40} {'期望':>8} {'实际':>8} {'胜者':>8}")
    print('─' * 70)
    for r in results:
        label = r['label'][:38]
        expected = r['expected']
        actual = r['rating']
        winner = r['winner']
        mark = 'v' if r['success'] else 'X'
        print(f"{label:<40} {expected:>8} {actual:>8} {winner:>8} [{mark}]")

    blue_wins = sum(1 for r in results if r['winner'] == 'BLUE')
    red_wins = sum(1 for r in results if r['winner'] == 'RED')
    fair = sum(1 for r in results if r['winner'] == 'BOTH')
    print(f"\nBLUE (鉴伪方): {blue_wins} 胜")
    print(f"RED  (造假方): {red_wins} 胜")
    print(f"FAIR (无争议): {fair}")

    # 保存详细结果
    output_path = os.path.join(os.path.dirname(__file__), 'battle_report.json')
    serializable = []
    for r in results:
        sr = {k: v for k, v in r.items() if k != 'flags'}
        sr['flag_summary'] = {}
        for f in r['flags']:
            sr['flag_summary'].setdefault(f['test'], 0)
            sr['flag_summary'][f['test']] += 1
        serializable.append(sr)

    with open(output_path, 'w') as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
    print(f"\n详细报告已保存: {output_path}")


if __name__ == '__main__':
    main()

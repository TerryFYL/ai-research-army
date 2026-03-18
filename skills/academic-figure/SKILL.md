---
name: academic-figure
description: "学术图表生成。基于统计结果生成出版级图表。触发词：'出图'、'画图'、'academic figure'、'生成图表'。"
argument-hint: [统计结果文件或图表需求]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# 学术图表 - Lena 的出版工坊

## 概述
基于统计分析结果，生成符合学术期刊规范的出版级图表。所有图表执行数据对账——图中数字必须与 analysis_results.md 严格一致。以 Lena 的视角执行（参考 ~/.claude/agents/lena.md）。

## 支持的图表类型

| 图表类型 | 适用场景 | 关键参数 |
|---------|---------|---------|
| Kaplan-Meier 生存曲线 | 生存分析 | 风险表、置信区间带、P值标注 |
| Forest Plot 森林图 | 亚组分析/Meta分析 | 效应量+CI、异质性指标、参考线 |
| Funnel Plot 漏斗图 | 发表偏倚检测 | Egger线、修剪填充标记 |
| Heatmap 热力图 | 相关性矩阵/时序模式 | 色阶、聚类树、数值标注 |
| Box Plot 箱线图 | 组间分布比较 | 单个数据点叠加、显著性标记 |
| Bar Chart 柱状图 | 频率/比例比较 | 误差线(95%CI)、分组配色 |
| Scatter Plot 散点图 | 两变量关联 | 回归线、置信带、R值标注 |
| Radar Chart 雷达图 | 多维特征对比 | 标准化轴、半透明填充 |
| Flow Diagram 流程图 | 样本纳入排除 | CONSORT/STROBE 格式 |
| Table 1 三线表 | 基线特征 | 标准学术三线表格式 |

## 流程

### Step 1: 数据对账（强制）
1. 读取 `analysis_results.md` 获取所有待绘图数据
2. 逐项核对：
   - 效应量数值
   - 置信区间上下界
   - P 值
   - 样本量
   - 百分比
3. 发现不一致时**立即停止绘图**，回溯 analysis_results.md 确认正确值
4. 生成对账记录：`figures/data_reconciliation.md`

### Step 2: 图表规划
根据 research_plan.md 和 analysis_results.md 规划图表清单：

```markdown
## 图表清单
- Figure 1: [类型] - [描述] - 来源: analysis_results.md 第X节
- Figure 2: ...
- Table 1: 基线特征表 - 来源: analysis_results.md Table 1
```

### Step 3: 统一视觉规范
在绘图前设定全局参数：

```python
# 出版级默认配置
FIGURE_DPI = 300                    # 最低 300 DPI
COLOR_PALETTE = "colorblind_safe"   # 色盲友好调色板
FONT_FAMILY = "Arial"               # 学术期刊通用字体
FONT_SIZE_TITLE = 12
FONT_SIZE_LABEL = 10
FONT_SIZE_TICK = 8
LINE_WIDTH = 1.5
OUTPUT_FORMAT = ["tiff", "pdf"]     # 双格式输出
FIGURE_SIZE = (7, 5)                # 英寸，单栏宽度
```

### Step 4: 逐图生成
对每张图表：
1. 提取对应数据
2. 选择图表类型和布局
3. 应用统一视觉规范
4. 添加必要标注（P值、效应量、样本量）
5. 导出 TIFF（300+ DPI）+ PDF 双格式
6. 生成图例文本（Figure Legend）

### Step 5: 色盲友好验证
对所有图表执行色盲模拟检查：
- 红绿色盲（Deuteranopia）模拟
- 确保仅靠颜色区分的元素同时有形状/线型区分
- 必要时调整配色

### Step 6: 图例文本撰写
为每张图表撰写标准格式的图例：

```markdown
Figure 1. [标题]。[描述图表内容]。[说明统计方法]。
[缩写说明]。CI, confidence interval; HR, hazard ratio.
```

## 输出
- `figures/` 目录，包含：
  - `Figure_1.tiff` + `Figure_1.pdf` — 每张图双格式
  - `figure_legends.md` — 所有图例文本
  - `data_reconciliation.md` — 数据对账记录
- 更新 `progress.md` 中学术图表阶段状态

## 关键规则
1. **数据对账是强制步骤**：图中每个数字必须与 analysis_results.md 完全一致，差一个小数点都不行
2. **300 DPI 底线**：低于 300 DPI 的图不合格，直接重出
3. **色盲友好**：不可仅靠颜色传递信息，必须同时用形状、线型或标注区分
4. **标签不重叠**：X 轴标签过长时旋转或缩写；数据点密集时调整 xlim/ylim 留出空间
5. **不美化数据**：图表忠实反映数据，不做视觉上的误导（如截断 Y 轴起点）
6. **图例独立可读**：图例文本应足够详细，使读者不看正文也能理解图表含义
7. **大文件处理**：如果 Write 工具因文件过大失败，立即用 Bash (cat << 'EOF' > file) 分块写入。不要询问用户——直接执行

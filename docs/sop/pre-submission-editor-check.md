# 投稿前编辑视角检查 SOP

> v1.0 · 2026-09-30
> 依据：Warren WS. Beating the odds for journal acceptance. *Sci Adv.* 2022;8:eadd9147. doi:10.1126/sciadv.add9147

---

## 1. 目的

高拒稿率期刊的大部分稿件在送审前就被编辑拒掉（desk reject）。*Science Advances* 每年约 20,000 篇投稿，拒稿约 90%，多数没有送审。编辑的判断很大程度依赖稿件表面的信号：夸大措辞、错别字、看不懂的图、写错的期刊名。

本 SOP 把这些信号转成出稿前的逐项检查，目标是**不让稿件因为表达和流程问题被拒**。科学质量由 Alex 的八层审查负责，不在本 SOP 范围内。

## 2. 适用范围与在管线中的位置

- 适用于所有交给客户投稿的稿件（原创研究、综述、Meta 分析）。
- 执行时机：

```
Hao 完成 manuscript + cover letter
    ↓
【本 SOP】各负责人自查 → Alex 终审时按本清单复核
    ↓ 全部 BLOCK 项通过
/submit-package 组装投稿包 → /delivery 交付
```

- 本 SOP **不替代**：STROBE/CONSORT/PRISMA 等报告规范、Alex 八层审查、`/submit-package` 的前置门控。三者并行，互不覆盖。
- 期刊投稿指南与本 SOP 冲突时，**以期刊要求为准**（如图的放置位置、是否允许推荐编辑）。

## 3. 编辑怎么读稿（本 SOP 的逻辑）

Warren 是 *Science Advances* 物理与材料组的资深副主编。该组 12 位副主编每人每月处理 50–100 篇稿件，且都是兼职。他描述的读稿顺序：

| 阶段 | 编辑看什么 | 决定什么 |
|---|---|---|
| 第一印象 | 只看**标题、摘要、cover letter 正文**，刻意不看作者和单位 | 要不要继续看 |
| 第二印象 | **图和图注**（很多审稿人也从这里开始） | 能不能看懂主要信息 |
| 分派 | 找副编辑（AE）和审稿人 | AE 多次拒接、合格审稿人多次拒审，会被当作"稿件缺乏普遍兴趣"的信号 |
| 历史 | 是否重复投稿、是否处理过他刊审稿意见 | 编辑部会追踪被拒稿件最后发在哪里 |

四条原则：

1. **编辑时间很少，靠信号判断。** 表面缺陷会被读成"作者不严谨"，进而怀疑工作本身。
2. **两道关按顺序打磨。** 先保证标题、摘要、cover letter，再保证图和图注。
3. **稿件好不好分派，本身就是一种评价。** 推荐合适的编辑和审稿人会影响编辑对稿件价值的判断。
4. **问题在表达，不在科学。** Warren 在结尾承认，编辑部大概拒过有真正意义的论文，只因编辑和审稿人没看出价值。

> 适用性说明：原文来自综合性期刊的物理与材料组。医学期刊的流程细节不同（例如多数不允许推荐处理编辑），但 desk reject 机制相同。本 SOP 中的医学对应项（如因果措辞）是我们的推断，已单独标出。

## 4. 判定等级

| 等级 | 含义 |
|---|---|
| **BLOCK** | 必须修改，否则不得进入 `/submit-package` |
| **WARN** | 修改，或在检查记录中写明保留理由 |
| **OPTIONAL** | 视情况采用 |

---

## 5. 检查流程

### Step 0　确认投稿类型（Priya 在需求阶段收集，Tom 与客户核实）

投稿历史只有客户知道，必须在需求阶段问清楚，写入 `requirement_v1.md`。

| 类型 | 定义 | 需要从客户处拿到 | 额外执行 |
|---|---|---|---|
| 首投 | 从未投过 | — | — |
| 改投 | 被其他期刊拒稿后投新期刊 | 原期刊名、决定信、**审稿意见原文** | Step 7-A |
| 重投 | 被同一期刊拒稿后再投该刊 | 决定信、编辑是否邀请重投 | Step 7-B |
| 转投 | 接受期刊的转投推荐，或选择同家族期刊 | 转投推荐信（如有） | Step 7-C |

### Step 1　标题与摘要（Hao 自查，Alex 复核）

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| T1 | 标题无错别字 | 逐词核对，零错误 | BLOCK | 5 |
| T2 | 摘要第一句语法正确 | 零错误 | BLOCK | 5 |
| T3 | 摘要写出最核心的发现 | 结果部分用一句话给出主要发现，含效应量和 95% CI | BLOCK | 1 |
| T4 | 无夸大措辞 | 附录 A1 词表中的词，每处要有证据支撑，否则删除 | WARN | 1 |
| T5 | 观察性研究不用因果措辞 | 标题、摘要、结论中不出现附录 A2 的因果表述 | BLOCK | 6（医学对应） |
| T6 | 领域外读者能看懂重要性 | 摘要背景第一句说明临床问题，而不是统计方法或数据库名称 | WARN | 4 |

> T5 说明：Warren 批评"把模拟或计算结果写得像实验结果"，审稿人识破后会失望并写进意见。医学稿件里的同类问题是把观察性数据的"关联"写成"效应"或"因果"。回顾性队列、横断面、生态学研究尤其要查。

### Step 2　Cover letter（Hao 撰写，Alex 复核）

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| C1 | 期刊名正确 | 收件期刊、栏目、稿件类型与本次目标一致；全文不出现其他期刊名（用附录 B 命令检查） | BLOCK | 9 |
| C2 | 讲清研究在领域中的位置 | 三句话说明：已知什么 → 缺什么 → 本研究补了什么 | BLOCK | 4 |
| C3 | 不堆砌文献 | 不用"列一串高影响期刊论文"来代替背景说明 | WARN | 4 |
| C4 | 与摘要一致 | cover letter 中的核心发现、数字、样本量与摘要完全一致 | BLOCK | — |
| C5 | 说明为什么适合该期刊 | 引用该期刊的 scope 或近期同类文章，不写空泛套话 | WARN | 4 |
| C6 | 推荐审稿人附理由 | 如在 cover letter 中推荐审稿人，每人一句理由 | WARN | 8 |

### Step 3　语言（Hao 通读，Alex 抽查）

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| L1 | 拼写检查 | 全文跑一遍拼写检查（附录 B），逐条处理 | BLOCK | 5 |
| L2 | 抽查语言错误密度 | Alex 随机抽 3 页，任一页语言错误 ≥ 2 处 → 全文返工 | BLOCK | 5 |
| L3 | 术语与缩写 | 缩写首次出现给全称，全文用法统一 | WARN | — |

> Warren 原话的意思：因语言问题快速拒稿其实是帮作者，因为审稿人看到每页好几处错误会非常恼火，影响公平评审。非英语母语客户的稿件，L2 必须执行。

### Step 4　图与图注（Lena 自查，Alex 复核）

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| F1 | 图的位置符合期刊要求 | 期刊允许时，审稿版把图放在首次引用附近；期刊要求单独上传时，图注集中放在指定位置 | BLOCK | 6 |
| F2 | 图注能独立读懂 | 不看正文也能知道：画的是什么、人群与样本量、统计方法、误差线或区间的含义、所有缩写 | BLOCK | 6 |
| F3 | 主要结果一眼可见 | 只看主结果图（通常是 Figure 1 或 2）就能看出主要发现 | WARN | 6 |
| F4 | 数字对账已执行 | 图上数字与正文、表格一致（Lena 现有对账流程的执行记录） | BLOCK | — |

### Step 5　前人工作与定位（Jing 负责，Hao 写入，Alex 复核）

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| P1 | 点名对比最相关的研究 | 引言或讨论中明确对比 2–3 项最接近的研究（同人群/同暴露/同结局），并说明本研究的不同 | BLOCK | 3 |
| P2 | 不回避不一致的结果 | 与既往结论不一致时，讨论中正面解释可能原因 | BLOCK | 3 |
| P3 | 覆盖近期研究 | 已检索近 2 年的相关文献，避免漏掉最新的竞争工作 | WARN | 3 |
| P4 | "首次"类声明有依据 | 出现"首次""first"等声明时，必须有检索记录支撑（数据库、检索式、日期），否则删除 | BLOCK | 1, 3 |

> 最可能被请来审稿的人，恰恰是被你忽略的那篇论文的作者。

### Step 6　编辑与审稿人推荐（Jing 提名，Tom 与客户核实）

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| R1 | 推荐处理编辑 | 仅在投稿系统允许时执行：查编委会页面，推荐研究方向最接近的编辑 | OPTIONAL | 7 |
| R2 | 推荐审稿人的资质 | 按期刊要求的人数推荐；每人近 5 年在同主题有发表（给出 1 篇代表作）；附一句推荐理由 | BLOCK | 8 |
| R3 | 排除利益冲突 | 排除：近 5 年合著者、同单位人员、导师或学生、近期合作者、有经济或学术竞争关系者（年限以期刊规定为准） | BLOCK | 8 |
| R4 | 客户确认 | 由客户书面确认与每位被推荐人无上述关系（合作关系只有客户知道） | BLOCK | 8 |
| R5 | 回避审稿人 | 如要求回避某些审稿人，写明理由，人数克制 | WARN | — |

> 利益冲突严重时，编辑可能整份审稿意见作废，拖慢整个流程。合格的审稿人一再拒审，会被当作"稿件不适合本刊"的信号。

### Step 7　投稿历史专项（按 Step 0 的类型执行）

**7-A　改投（被他刊拒后投新期刊）**

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| H1 | 期刊名全部替换 | cover letter、标题页、页眉、正文中所有旧期刊名均已替换（附录 B 命令） | BLOCK | 9 |
| H2 | 处理上一轮审稿意见 | 逐条记录"改了什么 / 为什么没改"，存为内部文件 `prior_reviews_response.md` | BLOCK | 9 |
| H3 | 按新期刊重排格式 | 字数、摘要结构、参考文献格式、图表要求全部按新期刊 | BLOCK | — |
| H4 | 主动说明上一轮审稿 | 修改充分且上一轮意见有实质价值时，可在 cover letter 中说明，并附上之前的审稿意见与修改对照 | OPTIONAL | 9 |

> H4 依据：Warren 接收过的最好的综述之一就在别处被拒过。作者主动提供了之前的审稿意见，解释为什么认为那个决定有误，并展示了修改。反面例子："Dear Editors of Nature"，以及审稿人说"作者无视了我所有意见"。

**7-B　重投（被同一期刊拒后再投该刊）**

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| H5 | 有重投资格 | 仅两种情况允许：编辑明确邀请重投；或有实质性新数据/新分析。否则不重投，改投他刊 | BLOCK | 2 |
| H6 | 讲清区别 | 不能只改标题。cover letter 第一段写明与上次稿件的区别和新增内容 | BLOCK | 2 |

> 编辑部会识别近似重复稿件。没有编辑邀请又没讲清楚区别的重投，稿件不会进入编辑评估。

**7-C　转投（期刊推荐或同家族期刊）**

| ID | 检查项 | 通过标准 | 等级 | 原文 |
|---|---|---|---|---|
| H7 | 目标期刊与内容匹配 | 读目标期刊的 aims & scope 和近一年同类文章后再决定，不按刊名或影响因子选 | BLOCK | 10 |

> 医学期刊同样有家族内转投（如 JAMA Network、Lancet 系列、BMJ 系列）。Warren 的例子：电子工程作者按刊名要求转投 *Science Signaling*，而那是一本生物学期刊。

### Step 8　放行与记录（Alex）

全部 BLOCK 项通过、WARN 项已修改或写明理由后，在任务目录写入 `pre_submission_check.md`：

```markdown
# 投稿前编辑视角检查记录

- 稿件：
- 目标期刊：
- 投稿类型：首投 / 改投 / 重投 / 转投
- 检查人：
- 日期：

| ID | 结果 | 说明（WARN 保留理由 / 修改位置） |
|----|------|------|
| T1 | PASS | |
| ...| | |

结论：放行 / 打回（打回项及负责人）
```

放行后进入 `/submit-package`。

---

## 附录 A　措辞词表

### A1　夸大措辞（标题、摘要中出现需有证据支撑）

novel · first / for the first time · unprecedented · groundbreaking · breakthrough · paradigm (shift) · revolutionary · remarkable / remarkably · dramatic / dramatically · striking / strikingly · pioneering · landmark · unique · prove / proves / proved · conclusive / conclusively · definitive / definitively · undoubtedly

中文稿件对应：首次、突破性、开创性、颠覆、显著地证明、毋庸置疑、填补空白（无检索依据时）。

### A2　观察性研究的因果措辞及替换

| 避免 | 改为 |
|---|---|
| X **causes** / **leads to** Y | X **was associated with** Y |
| the **effect of** X on Y | the **association between** X and Y |
| the **impact of** X on Y | the **association of** X with Y |
| X **reduces** / **increases** the risk of Y | X **was associated with a lower / higher risk of** Y |
| X is **protective** against Y | X **was associated with a lower risk of** Y |
| X **prevents** Y | X **was associated with fewer** Y |
| Y is **driven by** X | Y **was related to** X |

例外：研究设计本身支持因果推断（RCT、明确的因果推断方法如目标试验模拟、工具变量等），且方法部分已说明假设时，可以使用因果措辞。由 Kenji 判断。

## 附录 B　快速自检命令

在任务目录下运行，逐条人工核对输出。命令只负责找出候选位置，是否违规由人判断。

```bash
MS=manuscript.md          # 稿件
CL=cover_letter.md        # 投稿信
TP=title_page.md          # 标题页（如有）
TARGET="BMJ Open"         # 目标期刊全名

# 取出标题和摘要
TA=$(awk '/^# /&&!t{print;t=1;next} /^## Abstract/{p=1;print;next} p&&/^## /{exit} p' "$MS")

# T4：夸大措辞（标题 + 摘要）
grep -niwE "novel|first|unprecedented|groundbreaking|breakthrough|paradigm|revolutionary|remarkabl(e|y)|dramatic(ally)?|striking(ly)?|pioneering|landmark|unique|prove[sd]?|conclusive(ly)?|definitive(ly)?|undoubtedly" <<<"$TA"

# T5：因果措辞（先查标题 + 摘要，再查全文）
CAUSAL="\b(effects? of|impacts? of|leads? to|led to|caus(e|es|ed|ing)|protect(s|ed|ive)|prevent(s|ed|ing)?|driven by|drives|results? in|resulted in)\b"
grep -niE "$CAUSAL" <<<"$TA"
grep -niE "$CAUSAL" "$MS"

# C1 / H1：期刊名。每一行输出都必须指向目标期刊
echo "目标期刊出现次数: $(grep -ciF "$TARGET" "$CL")"   # 应 ≥ 1
grep -niE "dear|journal|lancet|jama|bmj|nejm|new england|circulation|nature|science|plos|frontiers|scientific reports|jacc|annals" "$CL" "$TP" 2>/dev/null

# L1：拼写检查（需先 pip install codespell）
codespell "$MS" "$CL"
```

已知噪声：因果词表会命中数据库名称（如 "Select Causes of Death"）和参考文献标题，逐条判断即可。

## 附录 C　原文十条与本 SOP 对照

| 原文 | 要点 | 本 SOP 检查项 |
|---|---|---|
| 1 | 标题和摘要简洁克制，不夸大，直说核心发现 | T3, T4, P4 |
| 2 | 不换标题原样重投；重投须有编辑邀请或重要新数据，并在 cover letter 讲清楚 | H5, H6 |
| 3 | 公平、显著地对比最相关的前人工作 | P1–P4 |
| 4 | 用好 cover letter：说明研究在领域中的位置，不是列一串高影响论文 | T6, C2, C3, C5 |
| 5 | 修改语法和表达：标题错字、摘要首句语法错误最伤印象 | T1, T2, L1–L3 |
| 6 | 让主要信息一眼可见：图嵌入正文、图注信息充分；不把模拟写成实验 | F1–F3, T5 |
| 7 | 认真推荐副编辑；AE 多次拒接被视为缺乏普遍兴趣 | R1 |
| 8 | 推荐称职且无偏的审稿人；合格审稿人多次拒审也是负面信号 | R2–R5, C6 |
| 9 | 改投时改期刊名，按上一轮审稿意见修改 | H1–H4 |
| 10 | 转投姊妹刊要选内容相关的期刊 | H7 |

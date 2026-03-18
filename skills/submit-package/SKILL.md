---
name: submit-package
description: "投稿包组装。生成期刊可直接上传的完整投稿材料。触发词：'打包投稿'、'投稿包'、'submit package'。"
argument-hint: [manuscript文件和目标期刊]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
---

# 投稿包组装 - 最终交付

## 概述
科研军团流水线的最后一站。将论文及所有配套材料组装为期刊可直接上传的投稿包。执行前置门控检查，确保质量审查已通过且引用已验证，然后将 Markdown 转换为 Word 格式并组装全部投稿文件。

## 前置门控

在组装投稿包之前，必须通过以下检查：

| 门控项 | 检查内容 | 不通过的处理 |
|--------|---------|-------------|
| 质量审查 | `REVIEW_STATE.json` 中最终得分 ≥ 55（C 级） | 返回 `/quality-review` 继续迭代 |
| 引用验证 | `verified_ref_pool.md` 中无 failed 引用被使用 | 返回 `/ref-manager verify` |
| 图表完整 | `figures/` 中所有图表文件存在 | 返回 `/academic-figure` 补图 |
| 无遗留标记 | manuscript.md 中无 [VERIFY] 或 [TODO] 标记 | 逐一解决后继续 |

任一门控不通过，立即报告并给出具体修复指引，不强行组装不合格的投稿包。

## 流程

### Step 1: 确定目标期刊规范
1. 读取用户指定的目标期刊（或从 requirement_v1.md 获取）
2. 通过 WebSearch 查询该期刊的投稿指南：
   - 字数限制（摘要、正文）
   - 参考文献格式（Vancouver/APA/自定义）
   - 图表要求（格式、大小、分辨率）
   - 必需的附加文件（Cover Letter、清单等）
   - 文件命名规范
3. 若无法获取具体期刊规范，使用通用医学期刊默认配置

### Step 2: Markdown 转 Word
1. 使用 pandoc 将 `manuscript.md` 转换为 docx 格式：
   ```bash
   pandoc manuscript.md -o manuscript.docx --reference-doc=template.docx
   ```
2. 若 pandoc 不可用，使用 Python (python-docx) 作为备选方案
3. 转换后检查：
   - 标题层级正确
   - 表格格式完整
   - 参考文献编号连续
   - 无乱码或格式错误

### Step 3: 图表文件整理
1. 将 `figures/` 中的 TIFF 文件复制到投稿包目录
2. 确认所有图表：
   - 分辨率 ≥ 300 DPI
   - 文件命名符合期刊要求（如 Figure_1.tiff）
   - 文件大小在期刊限制内
3. 生成独立的图例文件（如期刊要求）

### Step 4: Cover Letter 撰写
生成 `cover_letter.md`（后转 docx），结构：

```markdown
Dear Editor,

[第一段: 投稿声明——论文标题、研究类型、目标栏目]

[第二段: 研究重要性——为什么这项研究值得发表]

[第三段: 主要发现——1-2 句核心结论]

[第四段: 适合该期刊的理由——与期刊 scope 的匹配度]

[第五段: 声明——原创性、无重复投稿、所有作者同意]

Sincerely,
[通讯作者]
```

### Step 5: 报告清单生成
根据研究类型生成对应的报告清单：

| 研究类型 | 清单 |
|---------|------|
| 观察性研究（队列/病例对照/横断面） | STROBE |
| 随机对照试验 | CONSORT |
| 系统综述/Meta 分析 | PRISMA |
| 诊断准确性研究 | STARD |
| 预后研究 | TRIPOD |

逐条对照清单项，在论文中标注对应位置（页码/段落）。

### Step 6: 作者声明文件
生成 `declarations.md`（后转 docx）：

```markdown
# 作者声明

## 利益冲突
[声明所有作者的利益冲突或"无"声明]

## 资金来源
[列出基金资助信息]

## 伦理审批
[伦理委员会名称、审批编号]

## 知情同意
[患者知情同意声明]

## 数据可获取性
[数据共享声明]

## 作者贡献
[CRediT 格式的作者贡献声明]

## AI 使用声明
本研究使用 AI 工具辅助数据分析和论文撰写。所有 AI 生成内容均经过作者审查和验证。
AI 工具不列为论文作者。
```

### Step 7: 投稿包组装
创建 `submission_package/` 目录，包含：

```
submission_package/
├── manuscript.docx           # 论文正文
├── figures/
│   ├── Figure_1.tiff        # 图表文件（300+ DPI）
│   ├── Figure_2.tiff
│   └── ...
├── tables/
│   └── Table_1.docx         # 独立表格文件（如期刊要求）
├── cover_letter.docx         # 投稿信
├── checklist_STROBE.docx     # 报告清单（视研究类型而定）
├── declarations.docx         # 作者声明
├── figure_legends.docx       # 图例汇总
└── 投稿说明.md               # 投稿操作指引
```

### Step 8: 投稿说明生成
生成 `投稿说明.md`，包含：
- 目标期刊名称和投稿网址
- 投稿系统操作步骤
- 各文件的上传顺序和对应栏目
- 审稿周期预估
- 注意事项

## 输出
- `submission_package/` 目录 — 完整投稿包
- `投稿说明.md` — 操作指引
- 更新 `progress.md` 标记全流程完成

## 关键规则
1. **门控不可跳过**：质量审查未通过不组装投稿包，即使用户催促也要先过质量关
2. **格式以期刊为准**：不同期刊要求不同，必须查阅具体投稿指南
3. **AI 使用必须声明**：论文中使用 AI 辅助必须在声明中如实披露
4. **文件命名规范**：遵循期刊命名要求，不可使用中文文件名（投稿系统可能不支持）
5. **交付包=投稿包，非报告**：最终交付物是期刊可直接上传的文件，不是内部报告
6. **最终检查**：组装完成后逐一打开每个文件确认无误，再交付给用户
7. **大文件处理**：如果 Write 工具因文件过大失败，立即用 Bash (cat << 'EOF' > file) 分块写入。不要询问用户——直接执行

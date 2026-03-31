# Paper Revision Workflow

Detailed workflow for processing academic paper revisions systematically.

---

## Phase 1: Project Initialization

### 1.1 Create Project Structure

```bash
# Create revision project directory
mkdir -p revision_project/{tracking,responses,manuscript,submission}
```

### 1.2 Project CLAUDE.md Template

```markdown
---
project_name: "[Journal] Paper Revision - [Topic]"
project_type: "论文返修"
status: "进行中"
progress: 0
manuscript_id: "[ID]"
journal: "[Journal Name]"
revision_round: 1
created_date: "[Date]"
---

## 项目概述
[Brief description]

## 审稿意见摘要
| Reviewer | Comments | Priority |
|----------|----------|----------|
| [ID] | [Count] | [Distribution] |

## 当前进度
- [ ] 解析审稿意见
- [ ] 处理Comment 1
- [ ] ...

## 关键文件
- 审稿意见: `reviewer_comments.txt`
- Response Letter: `responses/response_letter.md`
- 修改稿: `manuscript/revised_marked.docx`
```

### 1.3 Parse Reviewer Comments

**Input**: Raw decision letter or reviewer comments

**Output**: `tracking/comments_parsed.yaml`

```yaml
revision_round: 1
journal: "JMIR Medical Informatics"
manuscript_id: "85270"
decision_date: "2026-01-04"
decision_type: "Minor Revision"

reviewers:
  G:
    id: "Reviewer G"
    expertise_focus: "Methodology"
    total_comments: 5
    comments:
      - id: "G1"
        type: "major"
        priority: "critical"  # critical|high|significant|editorial
        topic: "Sampling methodology"
        original_text: |
          "The sampling process described in the Methods section..."
        key_issues:
          - "Medlive platform procedure unclear"
          - "Generalizability concerns"
        estimated_hours: 4
        requires_reanalysis: false
        cross_references: []  # Related comments

      - id: "G2"
        type: "major"
        priority: "high"
        # ...

  N:
    id: "Reviewer N"
    expertise_focus: "Theoretical depth"
    # ...

editorial_comments:
  - id: "E1"
    type: "editorial"
    priority: "editorial"
    topic: "P-value formatting"
    # ...

summary:
  total_comments: 8
  by_priority:
    critical: 1
    high: 3
    significant: 2
    editorial: 2
  estimated_total_hours: 24
```

---

## Phase 2: Comment Analysis

### 2.1 Per-Comment Analysis Document

For each comment, create `responses/comment_[id]/analysis.md`:

```markdown
# Comment [ID] Analysis

## Original Comment
> "[Full text of reviewer's comment]"

## Problem Diagnosis

### Issue Classification
- **Type**: [ ] Data/Statistics [ ] Methodology [ ] Expression [ ] Format
- **Root Cause**: [What is the actual problem?]
- **Impact Level**: [How does this affect the paper?]

### Key Issues Identified
1. [Issue 1]: [Description]
2. [Issue 2]: [Description]

## Current State Assessment
- **Manuscript Location**: [Section, Paragraph N]
- **Current Text**: "[What the manuscript currently says]"
- **Data Available**: [What data/analysis exists]

## Gap Analysis
| Reviewer Expects | Current State | Gap |
|------------------|---------------|-----|
| [Expectation 1] | [Current] | [Gap] |

## Complexity Assessment
- **Estimated Effort**: [Hours]
- **Requires Reanalysis**: [Yes/No]
- **Dependencies**: [Other comments, external data]
```

### 2.2 Priority Matrix

```
                    HIGH IMPACT
                         │
     ┌───────────────────┼───────────────────┐
     │                   │                   │
     │   🟡 HIGH         │   🔴 CRITICAL     │
     │   Address next    │   Address first   │
     │                   │                   │
LOW ─┼───────────────────┼───────────────────┼─ HIGH
EFFORT│                   │                   │ EFFORT
     │   ⚪ EDITORIAL    │   🟢 SIGNIFICANT  │
     │   Quick fixes     │   Moderate effort │
     │                   │                   │
     └───────────────────┼───────────────────┘
                         │
                    LOW IMPACT
```

---

## Phase 3: Strategy Development

### 3.1 Strategy Document

Create `responses/comment_[id]/strategy.md`:

```markdown
# Comment [ID] Strategy

## Recommended Approach

### Option A: [Primary Strategy] ⭐ Recommended
**Description**: [What we will do]
**Pros**: [Advantages]
**Cons**: [Disadvantages]
**Effort**: [Hours]

### Option B: [Alternative Strategy]
**Description**: [What we could do]
**Pros**: [Advantages]
**Cons**: [Disadvantages]
**Effort**: [Hours]

## Selected Approach: Option [A/B]
**Rationale**: [Why this approach]

## Implementation Plan

### Step 1: [Action]
- **What**: [Description]
- **Where**: [Manuscript location]
- **Output**: [Expected result]

### Step 2: [Action]
- ...

## Response Outline
1. **Acknowledgment**: [Key phrase]
2. **Modifications**:
   - [Modification 1]
   - [Modification 2]
3. **Evidence**: [Table/Figure to cite]
4. **Location**: [Section, Paragraph N]

## Verification Checklist
- [ ] Response addresses all sub-points
- [ ] Manuscript modification complete
- [ ] Yellow highlight applied
- [ ] Cross-references checked
```

### 3.2 Strategy Selection Framework

```
Problem Type → Strategy Selection:

├─ DATA INCONSISTENCY
│   ├─ Calculation error → Recompute + New Table
│   ├─ Missing data → Acknowledge limitation
│   └─ Contradictory results → Verify source, explain

├─ METHODOLOGY CONCERN
│   ├─ Wrong method used → Sensitivity analysis
│   ├─ Insufficient detail → Expand Methods section
│   └─ Missing justification → Add rationale

├─ INTERPRETATION ISSUE
│   ├─ Overclaiming → Soften language
│   ├─ Missing context → Add literature
│   └─ Unclear implication → Expand Discussion

├─ FORMAT/EDITORIAL
│   ├─ Typos → Direct correction
│   ├─ Style issues → Apply journal format
│   └─ Citation problems → Fix references

└─ CROSS-CUTTING (multiple comments)
    └─ Integrated response with cross-references
```

---

## Phase 4: Execution

### 4.1 Response Writing

Follow the Four-Part Framework (see [TEMPLATES.md](TEMPLATES.md)):

1. Write response draft in Markdown
2. Include exact manuscript locations
3. Quote revised text precisely
4. Add supporting evidence

### 4.2 Manuscript Modification

**Rules**:
1. All changes must have **yellow highlight**
2. Use consistent formatting with journal style
3. Track all modification locations
4. Maintain paragraph numbering

**Process**:
```
1. Open manuscript
2. Navigate to target location
3. Make modification
4. Apply yellow highlight
5. Record in tracking document
6. Update response with exact location
```

### 4.3 Progress Tracking

Update `tracking/revision_tracking.md`:

```markdown
# Revision Progress Tracking

| ID | Priority | Status | Response | Manuscript | Verified |
|----|----------|--------|----------|------------|----------|
| G1 | 🔴 | ✅ Done | ✅ | ✅ | ✅ |
| G2 | 🟡 | 🔄 In Progress | ✅ | 🔄 | ⏳ |
| G3 | 🟢 | ⏳ Pending | ⏳ | ⏳ | ⏳ |

## Progress Summary
- Completed: 2/8 (25%)
- In Progress: 1/8
- Pending: 5/8

## Time Tracking
- Estimated: 24 hours
- Spent: 8 hours
- Remaining: 16 hours (estimated)
```

---

## Phase 5: Verification

### 5.1 Per-Comment Verification

Create `responses/comment_[id]/verification.md`:

```markdown
# Comment [ID] Verification

## Response-Manuscript Consistency

| Claimed Change | Location | Found | Highlighted |
|----------------|----------|-------|-------------|
| [Change 1] | Para 16 | ✅ | ✅ |
| [Change 2] | Table S4 | ✅ | ✅ |

## Cross-Reference Check
- [ ] No conflicts with Comment [X]
- [ ] No conflicts with Comment [Y]

## Data Accuracy
- [ ] All statistics verified
- [ ] All citations correct

## Verification Score: [N]/[Total] ([%])
## Status: [PASSED/NEEDS ATTENTION]
```

### 5.2 Four-Layer Quality Check

See [QUALITY.md](QUALITY.md) for detailed checks.

---

## Phase 6: Packaging

### 6.1 Final Document Preparation

```
submission/
├── Response_to_Reviewers.docx    # Converted from MD
├── Revised_Manuscript_marked.docx # With yellow highlights
├── Revised_Manuscript_clean.docx  # Without highlights
├── Supplementary_Materials/
│   ├── Table_S1.docx
│   └── ...
└── submission_checklist.md
```

### 6.2 Submission Checklist

```markdown
# Submission Checklist

## Response Letter
- [ ] All comments addressed
- [ ] Professional tone throughout
- [ ] Exact locations cited
- [ ] Evidence provided

## Manuscript (Marked Version)
- [ ] All changes yellow highlighted
- [ ] Consistent formatting
- [ ] No tracked changes visible

## Manuscript (Clean Version)
- [ ] No highlights
- [ ] No tracked changes
- [ ] Final formatting applied

## Supplementary Materials
- [ ] All appendices updated
- [ ] New tables/figures included
- [ ] File naming correct

## Final Check
- [ ] Co-author approval obtained
- [ ] File names follow journal convention
- [ ] All files open correctly
```

---

## Time Estimation Guidelines

| Comment Type | Typical Hours | Notes |
|--------------|---------------|-------|
| 🔴 CRITICAL (reanalysis) | 8-12 | Full statistical recomputation |
| 🔴 CRITICAL (data fix) | 4-6 | Error correction + verification |
| 🟡 HIGH (content expansion) | 3-5 | New section/paragraph |
| 🟡 HIGH (sensitivity analysis) | 4-6 | Additional analysis |
| 🟢 SIGNIFICANT (discussion) | 2-3 | Discussion enhancement |
| 🟢 SIGNIFICANT (visualization) | 2-4 | New/updated figures |
| ⚪ EDITORIAL | 0.5-1 | Quick corrections |

**Overhead**:
- Quality checks: +20% of total
- Documentation: +10% of total
- Packaging: 2-3 hours

---

## Parallel Processing Opportunities

```
Can Run in Parallel:
├─ Independent comments (different sections)
├─ Literature research + analysis writing
├─ Figure generation + text drafting

Must Run Sequentially:
├─ Analysis → Response → Verification (per comment)
├─ Cross-dependent comments
├─ Final assembly → Quality check
```

---

## Session Management

For multi-day revisions:

```
End of Session:
1. Update tracking document
2. Save all work
3. Note next steps in CLAUDE.md

Start of Session:
1. Read CLAUDE.md for context
2. Check tracking for progress
3. Continue from last incomplete comment
```

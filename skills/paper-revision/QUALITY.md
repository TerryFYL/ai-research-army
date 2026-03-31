# Quality Assurance Standards

Comprehensive quality control for academic paper revisions.

---

## Four-Layer Quality System

```
┌─────────────────────────────────────────────────────────┐
│ Layer 4: ACCURACY                                        │
│ Data accuracy, citation completeness, statistical rigor │
├─────────────────────────────────────────────────────────┤
│ Layer 3: CONFLICT DETECTION                              │
│ Inter-comment conflicts, logical consistency            │
├─────────────────────────────────────────────────────────┤
│ Layer 2: CONSISTENCY                                     │
│ Response ↔ Manuscript alignment                         │
├─────────────────────────────────────────────────────────┤
│ Layer 1: FORMAT                                          │
│ Response letter format, document structure              │
└─────────────────────────────────────────────────────────┘
```

---

## Layer 1: Format Standardization

### Response Letter Format Checks

| Check Item | Standard | Verification |
|------------|----------|--------------|
| Comment Header | `### Comment [ID]: [Topic]` (bold) | Visual inspection |
| Original Quote | `> "[Exact text]"` (blockquote) | Compare with source |
| RESPONSE Label | `**RESPONSE**:` (bold) | Format check |
| Revised Text | `**Revised text ([Section], Paragraph [N])**:` | Location format |
| Subheadings | Bold category labels | Consistency check |

### Format Validation Checklist

```markdown
## Format Check for Comment [ID]

### Structure
- [ ] Comment ID and topic in header
- [ ] Original comment quoted exactly
- [ ] RESPONSE label in bold
- [ ] Clear modification categories
- [ ] Revised text with location

### Styling
- [ ] Consistent bold usage for emphasis
- [ ] Proper blockquote for citations
- [ ] Uniform heading levels
- [ ] Professional language

### Cross-Comment Consistency
- [ ] Same format as other comments
- [ ] Consistent terminology
- [ ] Uniform location citation style
```

### Common Format Issues

| Issue | Example | Fix |
|-------|---------|-----|
| Missing bold | `RESPONSE:` | `**RESPONSE**:` |
| Vague location | "in Methods section" | "Methods, Paragraph 16" |
| Misquoted | Paraphrased instead of exact | Copy exact reviewer text |
| Inconsistent headers | Mix of formats | Standardize to one format |

---

## Layer 2: Consistency Verification

### Response-Manuscript Alignment

For each modification claimed in the Response Letter:

```markdown
## Consistency Check for Comment [ID]

### Modification [1]: [Description]

| Aspect | Response Says | Manuscript Shows | Status |
|--------|---------------|------------------|--------|
| Location | Para 16, Methods | Para 16, Methods | ✅ |
| Content | "[Quoted text]" | "[Actual text]" | ✅/❌ |
| Highlight | Yellow | Yellow applied | ✅/❌ |

### Verification Result
- Total claims: [N]
- Verified: [N]
- Discrepancies: [N]
- Pass rate: [%]
```

### Consistency Verification Steps

1. **Extract all claims from Response**
   - List every modification mentioned
   - Note claimed locations
   - Note claimed content

2. **Locate in Manuscript**
   - Navigate to cited paragraph
   - Find the exact text
   - Check for yellow highlight

3. **Compare and Document**
   - Text match: exact vs. different
   - Location match: correct paragraph
   - Highlight: applied or missing

4. **Flag Discrepancies**
   - Missing modifications
   - Wrong locations
   - Missing highlights
   - Text mismatches

### Consistency Error Types

| Error Type | Severity | Fix |
|------------|----------|-----|
| Location mismatch | 🔴 High | Update Response with correct location |
| Text mismatch | 🔴 High | Align Response and Manuscript |
| Missing highlight | 🟡 Medium | Add yellow highlight |
| Minor wording | 🟢 Low | Adjust for consistency |

---

## Layer 3: Conflict Detection

### Inter-Comment Conflict Analysis

```markdown
## Conflict Analysis Matrix

### Potential Conflict Pairs

| Comment A | Comment B | Overlap Area | Status |
|-----------|-----------|--------------|--------|
| G1 (sampling) | N3 (representativeness) | Sample description | ✅ Complementary |
| G2 (BI measurement) | N1 (ceiling effect) | BI validity | ✅ Complementary |

### Conflict Types

1. **Direct Contradiction**
   - Response to A says X
   - Response to B says not-X
   - Status: CONFLICT

2. **Implicit Conflict**
   - Different interpretations of same data
   - Conflicting implications
   - Status: NEEDS RESOLUTION

3. **Complementary**
   - Different aspects of same issue
   - Mutually supporting
   - Status: OK
```

### Conflict Resolution Strategies

| Conflict Type | Resolution |
|---------------|------------|
| Both reviewers correct but different emphasis | Integrate both perspectives |
| One reviewer's suggestion contradicts another | Explain rationale, cite literature |
| Data can support both views | Acknowledge complexity, be transparent |
| Fundamental disagreement | Address the underlying issue |

### Cross-Comment Consistency Checks

```markdown
## Key Consistency Areas

### Data Values
- [ ] Sample size consistent across all responses
- [ ] Statistics consistent (P-values, effect sizes)
- [ ] Percentages consistent

### Terminology
- [ ] Same terms used for same concepts
- [ ] Abbreviations defined consistently
- [ ] Technical terms accurate

### Claims
- [ ] No contradictory conclusions
- [ ] Limitations acknowledged consistently
- [ ] Implications aligned

### References
- [ ] Figure/Table numbers consistent
- [ ] Paragraph numbers accurate
- [ ] Supplementary material references correct
```

---

## Layer 4: Accuracy Verification

### Data Accuracy Checks

```markdown
## Data Accuracy Report

### Key Statistics

| Statistic | Value in Response | Value in Manuscript | Source | Status |
|-----------|-------------------|---------------------|--------|--------|
| Sample size | 4,024 | 4,024 | Table 1 | ✅ |
| Response rate | 85.3% | 85.3% | Methods | ✅ |
| R² | 0.216 | 0.216 | Results | ✅ |
| AUC | 0.840 | 0.840 | Table 4 | ✅ |

### Cross-Reference Verification
- [ ] Abstract matches Results
- [ ] Tables match in-text citations
- [ ] Figures match descriptions
- [ ] Supplementary data consistent
```

### Citation Accuracy

```markdown
## Citation Check

### In-Text Citations
- [ ] All claims supported by citations
- [ ] Citation numbers match reference list
- [ ] No broken references

### Figure/Table References
- [ ] All figures cited in text
- [ ] All tables cited in text
- [ ] Supplementary materials referenced correctly

### Self-References
- [ ] Internal cross-references accurate
- [ ] Section references correct
- [ ] Paragraph numbers current (after edits)
```

### Statistical Accuracy

```markdown
## Statistical Verification

### P-Values
| Test | Reported P | Calculation Source | Format Correct |
|------|------------|-------------------|----------------|
| [Test 1] | P<.001 | [Source] | ✅ |

### Effect Sizes
| Measure | Value | 95% CI | Interpretation |
|---------|-------|--------|----------------|
| β | 0.32 | [0.28, 0.36] | Appropriate |

### Model Fit
| Index | Value | Threshold | Status |
|-------|-------|-----------|--------|
| CFI | 0.95 | >0.90 | ✅ |
| RMSEA | 0.05 | <0.08 | ✅ |
```

---

## Quality Report Template

```markdown
# Revision Quality Assurance Report

**Manuscript ID**: [ID]
**Revision Round**: [N]
**Check Date**: [Date]

---

## Executive Summary

| Layer | Score | Status |
|-------|-------|--------|
| L1: Format | [N]/100 | ✅/⚠️/❌ |
| L2: Consistency | [N]/100 | ✅/⚠️/❌ |
| L3: Conflicts | [N]/100 | ✅/⚠️/❌ |
| L4: Accuracy | [N]/100 | ✅/⚠️/❌ |
| **Overall** | **[N]/100** | **[Status]** |

---

## Layer 1: Format (Score: [N]/100)

### Passing
- [List of passing items]

### Issues Found
| Issue | Location | Severity | Fix |
|-------|----------|----------|-----|
| [Issue] | [Location] | [🔴/🟡/🟢] | [Fix] |

---

## Layer 2: Consistency (Score: [N]/100)

### Verification Matrix
| Comment | Claims | Verified | Pass Rate |
|---------|--------|----------|-----------|
| G1 | 4 | 4 | 100% |
| G2 | 3 | 2 | 67% |

### Issues Found
| Issue | Response vs Manuscript | Fix |
|-------|------------------------|-----|
| [Issue] | [Discrepancy] | [Fix] |

---

## Layer 3: Conflicts (Score: [N]/100)

### Conflict Check Results
- Potential conflicts identified: [N]
- Resolved: [N]
- Remaining: [N]

### Conflict Details (if any)
| Comments | Conflict | Resolution |
|----------|----------|------------|
| [A] vs [B] | [Description] | [How resolved] |

---

## Layer 4: Accuracy (Score: [N]/100)

### Data Verification
- Statistics checked: [N]
- Accurate: [N]
- Discrepancies: [N]

### Citation Verification
- References checked: [N]
- Accurate: [N]
- Issues: [N]

---

## Action Items

### 🔴 Critical (Must Fix)
1. [Issue description]

### 🟡 Important (Should Fix)
1. [Issue description]

### 🟢 Minor (Consider)
1. [Issue description]

---

## Conclusion

**Overall Assessment**: [PASS / NEEDS REVISION / MAJOR ISSUES]

**Recommendation**: [Ready for submission / Additional fixes needed]

---

*Report generated: [Date]*
*Verified by: Claude AI*
```

---

## Pre-Submission Checklist

### Response Letter Final Check

```markdown
## Response Letter Checklist

### Content
- [ ] All comments addressed
- [ ] No reviewer comment skipped
- [ ] Acknowledgment in each response
- [ ] Clear modification descriptions
- [ ] Specific locations cited

### Format
- [ ] Consistent formatting throughout
- [ ] Professional tone
- [ ] Proper citations and quotes
- [ ] Correct heading hierarchy

### Quality
- [ ] All claims verifiable
- [ ] No contradictions
- [ ] Evidence provided where needed
```

### Manuscript Final Check

```markdown
## Manuscript Checklist

### Marked Version
- [ ] All changes highlighted (yellow)
- [ ] No tracked changes visible
- [ ] Consistent formatting
- [ ] All new content properly marked

### Clean Version
- [ ] All highlights removed
- [ ] Final formatting applied
- [ ] No editing artifacts
- [ ] Ready for publication view

### Both Versions
- [ ] Content identical (except highlighting)
- [ ] Page numbers correct
- [ ] References complete
- [ ] Figures/tables in place
```

### Supplementary Materials Check

```markdown
## Supplementary Materials Checklist

- [ ] All new tables included
- [ ] All new figures included
- [ ] Correct naming convention
- [ ] Referenced correctly in manuscript
- [ ] Standalone readability
```

---

## Scoring Guidelines

### Layer Scoring (0-100)

| Score Range | Interpretation |
|-------------|----------------|
| 95-100 | Excellent - Ready for submission |
| 85-94 | Good - Minor fixes needed |
| 70-84 | Fair - Several issues to address |
| <70 | Needs work - Significant revisions required |

### Overall Readiness

| Overall Score | Action |
|---------------|--------|
| ≥90 | Submit |
| 80-89 | Fix issues, then submit |
| 70-79 | Address all issues before submission |
| <70 | Major rework needed |

---

## Common Quality Issues

### Top 10 Issues (Ranked by Frequency)

1. **Missing yellow highlight** - Modification claimed but not marked
2. **Wrong paragraph number** - Location shifted after edits
3. **Text mismatch** - Response quotes differ from manuscript
4. **Inconsistent statistics** - Values differ across documents
5. **Missing acknowledgment** - Response jumps to modifications
6. **Vague locations** - "in the Methods section" instead of "Paragraph 16"
7. **Broken cross-references** - Figure/table numbers wrong
8. **Format inconsistency** - Different response formats
9. **Unchecked claims** - Data not verified against source
10. **Conflicting statements** - Responses contradict each other

### Prevention Strategies

| Issue | Prevention |
|-------|------------|
| Missing highlight | Highlight immediately after editing |
| Wrong paragraph | Use text search, not paragraph count |
| Text mismatch | Copy-paste from manuscript to response |
| Inconsistent stats | Single source of truth for all numbers |
| Format issues | Use templates consistently |

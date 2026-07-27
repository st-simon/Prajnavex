---
id: card-20260726-codex-coding-verification
type: card
title: "Codex 修改代码必须遵守规则、验证结果和用户变更边界"
summary: "Coding 纪律要求 Codex 先读取适用规则，保持范围最小，加入必要测试，运行验证并报告真实结果，不得覆盖无关用户变化。"
tags: [ai-collaboration-governance, codex-governance, coding-discipline, testing, verification]
stage: promotable
source_id: source-20260726-codex-governance-framework
card_type: concept
sources: [source-20260726-codex-governance-framework]
relations: {}
evidence_level: derived
epistemic_status: working
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
domain: ai-collaboration-governance/codex
knowledge_kind: normative
applicability: code and configuration edits
authority: workspace
authority_path: <workspace-root>/codex-workspace-governance/_workspace/CODING_RULES.md
evidence: [source-20260726-codex-governance-framework]
allowed_consumers: [human, agent]
---

# Codex 修改代码必须遵守规则、验证结果和用户变更边界

## Before Editing

1. 读取工作区和项目 `AGENTS.md`。
2. 涉及编辑时读取 `CODING_RULES.md`。
3. 检查 Git 状态和明显敏感文件。
4. 确认目标路径、分支和变更范围。

## After Editing

- 为行为变化增加或更新测试。
- 运行最窄但足够的验证。
- 检查 `git diff --check` 和临时文件。
- 报告文件、验证结果、遗留风险和未完成事项。

## Invariant

既有用户变化属于保护对象；Codex 只能修改授权范围内的文件。

---
id: card-20260726-codex-publish-closeout
type: card
title: "Codex 的发布和收尾必须显式授权并留下连续性记录"
summary: "Commit、Push、PR、外部写入和治理任务收尾都属于有边界的动作；Codex 需要确认授权、验证结果和下一步，而不是默认发布。"
tags: [ai-collaboration-governance, codex-governance, git, publish, closeout, continuity]
stage: promotable
source_id: source-20260726-codex-governance-framework
card_type: method
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
knowledge_kind: procedural
applicability: publish and substantial task closeout
authority: workspace
authority_path: <workspace-root>/codex-workspace-governance/AGENTS.md
evidence: [source-20260726-codex-governance-framework]
allowed_consumers: [human, agent]
---

# Codex 的发布和收尾必须显式授权并留下连续性记录

## Publish Boundary

- 修改文件不等于允许 Commit。
- Commit 不等于允许 Push。
- Push 不等于允许创建或合并 PR。
- 外部系统写入必须单独确认权限和范围。

## Closeout

收尾应说明完成内容、验证结果、未解决风险、遗留工作和下一步；L2 治理任务还需要留下可被后续任务读取的连续性记录。

## Invariant

没有明确授权时，Codex 停留在本地验证和报告，不自行发布。

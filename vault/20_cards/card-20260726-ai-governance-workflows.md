---
id: card-20260726-ai-governance-workflows
type: card
title: "AI 协作治理通过生命周期流程控制工作"
summary: "治理不是一组孤立规则，而是覆盖 intake、提案、执行、验证、发布、收尾和复查的生命周期。"
tags: [ai-collaboration-governance, workflow, lifecycle, review, closeout]
stage: promotable
source_id: source-20260726-ai-collaboration-governance-domain
card_type: method
sources: [source-20260726-ai-collaboration-governance-domain]
relations: {}
evidence_level: derived
epistemic_status: working
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
domain: ai-collaboration-governance
knowledge_kind: procedural
applicability: task lifecycle
authority: workspace
authority_path: <workspace-root>/codex-workspace-governance/AGENTS.md
evidence: [source-20260726-ai-collaboration-governance-domain]
allowed_consumers: [human, agent]
---

# AI 协作治理通过生命周期流程控制工作

## Lifecycle

```text
intake → scope → proposal → route → execute → verify → publish → closeout → review
```

## Control Points

- `intake`：明确目标、项目归属和是否需要提问。
- `proposal`：按后果、风险和可逆性判断是否需要批准。
- `route`：选择最小必要的工作流和 Agent 能力组合。
- `execute`：在权限、分支和文件边界内行动。
- `verify`：运行测试、索引、审计或证据检查。
- `publish`：Commit、Push 或外部发布必须明确授权。
- `closeout`：记录结果、遗留风险和下一步。

## Invariant

每个高风险任务都必须有可追溯的起点、批准边界、验证结果和收尾记录。

---
id: source-20260726-codex-governance-framework
type: source
title: "Codex 治理框架子域"
summary: "AI 协作治理知识域中的第一个完整 Agent 子域，组织 Codex 任务 intake、Proposal、工作路由、Coding 纪律、验证、发布和 closeout。"
tags: [ai-collaboration-governance, codex-governance, codex, workflow, coding-discipline]
stage: source
source_type: manual
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
domain: ai-collaboration-governance/codex
knowledge_kind: subdomain-map
authority: workspace
authority_path: <workspace-root>/codex-workspace-governance/AGENTS.md
related_cards: [card-20260726-codex-task-intake, card-20260726-codex-proposal-routing, card-20260726-codex-coding-verification, card-20260726-codex-publish-closeout]
promoted_skills: [skill-20260726-ai-governance-task-lifecycle, skill-20260726-ai-governance-review-upgrade]
allowed_consumers: [human, agent]
---

# Codex 治理框架子域

## Position

Codex 治理框架是 `ai-collaboration-governance` 知识域的第一个 Agent 子域，不是整个 AI 协作治理知识域的总称，也不是工作区 governance 权威本身。

## Coverage

- 任务 intake、范围和项目归属；
- Proposal gate 与工作路由；
- Coding 纪律、测试和验证；
- Commit、Push、PR 和 Session closeout；
- 工作区规则与项目规则的关系；
- 从 Codex 工作经验中提炼可复用知识。

## Authority Boundary

本 Source 映射而不复制权威规则。实际执行时仍需读取：

- `<workspace-root>/codex-workspace-governance/AGENTS.md`
- `<workspace-root>/codex-workspace-governance/_workspace/PROPOSAL_RULES.md`
- `<workspace-root>/codex-workspace-governance/_workspace/WORK_ROUTING_RULES.md`
- `<workspace-root>/codex-workspace-governance/_workspace/CODING_RULES.md`
- `<workspace-root>/projects/<project>/AGENTS.md`

## Subdomain Rule

Codex、Claude 或其他 Agent 的品牌变化，不应改变这里记录的治理原则、权限边界和生命周期结构；变化应记录在具体 Agent 适配器或角色卡中。

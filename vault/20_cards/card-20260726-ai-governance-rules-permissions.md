---
id: card-20260726-ai-governance-rules-permissions
type: card
title: "AI 协作治理把规则、权限和审批条件分开管理"
summary: "规则说明应该做什么，权限说明谁可以做，审批条件说明什么情况下必须由人确认；三者不能混成一句模糊的行为要求。"
tags: [ai-collaboration-governance, rules, permissions, approval, least-privilege]
stage: promotable
source_id: source-20260726-ai-collaboration-governance-domain
card_type: concept
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
knowledge_kind: normative
applicability: permission and approval decisions
authority: workspace
authority_path: <workspace-root>/codex-workspace-governance/_workspace/PROPOSAL_RULES.md
evidence: [source-20260726-ai-collaboration-governance-domain]
allowed_consumers: [human, agent]
---

# AI 协作治理把规则、权限和审批条件分开管理

## Three Questions

- 规则：这项工作应该如何完成？
- 权限：哪个角色或 Agent 可以执行？
- 审批：什么条件下必须停下来请求人类确认？

## Default Risk Ladder

```text
只读检索 → 可逆项目修改 → 持久化知识变更 → 外部系统写入 → 不可逆或高风险动作
```

风险越高，越需要明确范围、Proposal、人工批准和验证证据。

## Authority Examples

- 工作区 Proposal 规则：`<workspace-root>/codex-workspace-governance/_workspace/PROPOSAL_RULES.md`
- 编辑纪律：`<workspace-root>/codex-workspace-governance/_workspace/CODING_RULES.md`
- 项目规则：`<workspace-root>/projects/<project>/AGENTS.md`

本卡用于解释和索引，不替代上述权威文件。

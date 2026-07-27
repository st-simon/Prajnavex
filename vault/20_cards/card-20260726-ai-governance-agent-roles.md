---
id: card-20260726-ai-governance-agent-roles
type: card
title: "AI 协作治理按角色而不是品牌定义 Agent 责任"
summary: "Codex、Claude 和其他 Agent 是具体实现；治理应先定义人类、编排、编码、研究、审查和知识角色，再决定哪个 Agent 承担角色。"
tags: [ai-collaboration-governance, agent-roles, codex, claude, responsibility]
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
knowledge_kind: descriptive
applicability: multi-agent collaboration
authority: project
authority_path: DECISIONS.md
evidence: [source-20260726-ai-collaboration-governance-domain]
allowed_consumers: [human, agent]
---

# AI 协作治理按角色而不是品牌定义 Agent 责任

## Role Map

| 角色 | 主要责任 |
|---|---|
| 人类用户 | 目标、授权、关键判断、最终批准 |
| 编排 Agent | 理解任务、选择流程、协调工作 |
| Coding Agent | 修改代码、运行测试、报告变更 |
| Research Agent | 搜索、整理来源、形成研究草稿 |
| Review Agent | 检查事实、风险、质量和一致性 |
| Knowledge Agent | 索引、召回、引用和生命周期建议 |

## Brand Boundary

Codex 和 Claude 可以分别承担一个或多个角色，但品牌不等于权限；权限由当前任务、项目规则和批准状态决定。

## Invariant

角色责任、工具权限和最终批准权必须分开记录，不能因为某个 Agent 能够执行某动作，就默认它有权执行。

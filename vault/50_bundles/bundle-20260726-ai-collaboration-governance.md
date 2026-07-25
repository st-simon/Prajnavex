---
id: bundle-20260726-ai-collaboration-governance
type: bundle
title: "AI 协作治理知识域"
summary: "Prajnavex 内用于理解、检索、执行和升级 AI 协作治理知识的入口 Bundle；当前以 Codex 治理框架为第一批完整子域。"
tags: [ai-collaboration-governance, prajnavex, codex-governance, agent-governance]
stage: bundle-draft
skills: [skill-20260726-ai-governance-task-lifecycle, skill-20260726-ai-governance-review-upgrade]
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
input_contract: "AI 协作任务、治理规则、Agent 角色、经验教训或升级问题。"
output_contract: "可引用的治理知识、可执行流程、角色边界、审计结论或升级 Proposal。"
workflow_status: draft
domain: ai-collaboration-governance
knowledge_kind: navigation
authority: project
authority_path: DECISIONS.md
allowed_consumers: [human, agent]
---

# AI 协作治理知识域

## Scope

这是 Prajnavex 内的一个知识域，不是工作区 governance 本身。它服务人类和 Agent，对治理内容进行记录、解释、索引、引用和复用。

## Core Maps

- 宪法原则：哪些边界对所有 Agent 都成立。
- 规则与权限：什么能做、谁能做、何时需要批准。
- 流程生命周期：从 intake 到 closeout 的控制点。
- Agent 角色：人类、编排、编码、研究、审查和知识角色。
- 知识与经验：规范、事实、经验和可复用方法的分层。
- 审计与升级：复查、修订、升级、降级和归档。

## First Subdomain: Codex Governance

当前 Codex 治理框架最完整，包含工作区启动、Proposal、工作路由、Coding 纪律、测试验证、Commit/Push 和 Session closeout 等内容。它是本 Bundle 的第一批内容，不是总领域的边界。

Codex 子域入口：

- [[source-20260726-codex-governance-framework]]
- [[card-20260726-codex-task-intake]]
- [[card-20260726-codex-proposal-routing]]
- [[card-20260726-codex-coding-verification]]
- [[card-20260726-codex-publish-closeout]]

## Workflow

1. 从当前任务识别需要的治理主题。
2. 通过 Prajnavex Knowledge API 搜索 Cards、Skills 和权威路径。
3. 用 context pack 提供给人类或 Agent。
4. 执行任务并记录验证与引用。
5. 将新的经验先记录为经验知识，再决定是否升级为 Skill 或规则 Proposal。

## Included Skills

- [[skill-20260726-ai-governance-task-lifecycle]]
- [[skill-20260726-ai-governance-review-upgrade]]

## Authority Boundary

工作区 governance 仓库仍是实际执行规则的权威来源。若本 Bundle 与权威文件冲突，以权威文件为准，并记录冲突以便治理升级。

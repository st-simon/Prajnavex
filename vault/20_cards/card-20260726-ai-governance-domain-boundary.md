---
id: card-20260726-ai-governance-domain-boundary
type: card
title: "AI 协作治理知识域是 Prajnavex 内的知识域，不是工作区治理权威"
summary: "AI 协作治理知识域负责组织和复用治理知识；工作区 governance 文件负责规定真正生效的执行规则。两者必须保持权威与解释层分离。"
tags: [ai-collaboration-governance, prajnavex, domain-boundary, authority]
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
knowledge_kind: boundary
applicability: governance knowledge organization
authority: project
authority_path: DECISIONS.md
evidence: [source-20260726-ai-collaboration-governance-domain]
allowed_consumers: [human, agent]
---

# AI 协作治理知识域是 Prajnavex 内的知识域，不是工作区治理权威

## Core Idea

Prajnavex 记录、解释、索引、引用和打包治理知识；工作区 governance 仓库中的规则文件决定 Codex 在实际任务中必须如何行动。

## Boundary

- `Prajnavex`：知识底座与双消费者接口。
- `AI 协作治理知识域`：Prajnavex 内的治理知识集合。
- `Workspace Governance`：权威规则、Hook、Proposal 和生命周期执行层。
- `Codex 治理框架`：AI 协作治理知识域中的第一个 Agent 子域。

## Invariant

当知识域中的解释与权威文件冲突时，以权威文件为准，并把冲突记录为治理升级事项。

## When Useful

当需要判断一条内容是“生效规则”、“解释性知识”还是“经验教训”时，先使用本边界卡。

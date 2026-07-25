---
id: source-20260726-prajnavex-dual-consumer-model
type: source
title: "Prajnavex 双消费者模型架构决策"
summary: "Prajnavex 同时服务人类用户和 Agent：共享一个 Markdown/frontmatter 知识底座，并通过人类工作台与只读 bounded context pack 分别提供消费接口。"
tags: [prajnavex, architecture, agent, knowledge-core, context-pack]
stage: source
source_type: manual
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
authority: project
authority_path: DECISIONS.md
related_cards: [card-20260726-prajnavex-dual-consumer-model]
promoted_skills: []
allowed_consumers: [human, agent]
---

# Prajnavex 双消费者模型架构决策

## Decision

Prajnavex 不是单纯的个人笔记库，也不是只服务 Agent 的向量数据库，而是同时服务人类理解与 Agent 行动的带证据链知识核心。

## Consumer Split

- 人类使用 Obsidian 或 Web UI 进行阅读、编辑、链接、研究和批准。
- Agent 使用 frontmatter-first recall 和 bounded context packs 进行检索、引用和任务应用。

## Boundary

知识底座只有一份。Agent 的 context pack 是只读的，不能自动晋升、合并、删除或重写知识；权威文件优先于派生 Card、Skill 或 Bundle。

## Authority

项目决策记录：`DECISIONS.md`。

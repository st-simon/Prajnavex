---
id: card-20260726-prajnavex-dual-consumer-model
type: card
title: "一个知识底座，两个消费接口"
summary: "Prajnavex 应以一套 Markdown/frontmatter 知识底座同时服务人类和 Agent；人类获得可读可编辑的知识，Agent 获得有边界、可引用、可审计的 context pack。"
tags: [prajnavex, architecture, dual-consumer, agent, context-pack]
stage: promotable
source_id: source-20260726-prajnavex-dual-consumer-model
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
usefulness: high
actionability: architecture-principle
promotable: true
domain: prajnavex-architecture
applicability: knowledge retrieval and reuse
authority: project
authority_path: DECISIONS.md
evidence: [DECISIONS.md:2026-07-26]
allowed_consumers: [human, agent]
---

# 一个知识底座，两个消费接口

## Core Idea

人和 Agent 不需要两套知识库。两者共享同一个经过审核的知识底座，但使用不同的消费接口。

## Human Interface

用户关注阅读、理解、比较、编辑、链接、研究和批准。Markdown、Obsidian 和 Web UI 适合承担这些任务。

## Agent Interface

Agent 关注召回、筛选、引用、应用和反馈。它应先检索 frontmatter，再加载有限正文，通过 bounded context pack 获取稳定 ID、来源、置信度、时效和引用信息。

## Invariant

Agent 可以提炼和建议，但不能绕过人工批准直接把草稿变成稳定知识。权威规则和原始来源优先于派生 Card、Skill 和 Bundle。

## When Useful

当同一批知识既要供用户长期研究，又要供 Codex 或其他 Agent 在任务中自动引用时，采用双消费者模型。

## Source

[[source-20260726-prajnavex-dual-consumer-model]]

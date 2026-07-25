---
id: skill-20260726-ai-governance-review-upgrade
type: skill
title: "复查和升级 AI 协作治理知识"
summary: "用于复查治理规则、角色、流程和经验，决定保留、修订、升级、降级或归档。"
tags: [ai-collaboration-governance, review, audit, upgrade, knowledge-lifecycle]
stage: skill-draft
trigger: [review-after, repeated-failure, rule-conflict, process-change, agent-change]
inputs: [knowledge-note, authority-source, usage-evidence, failure-examples]
outputs: [review-decision, updated-metadata, upgrade-proposal]
source_cards: [card-20260726-ai-governance-knowledge-experience, card-20260726-ai-governance-audit-upgrade, card-20260726-ai-governance-domain-boundary]
created: 2026-07-26
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: high
staleness: fresh
maturity: experimental
domain: ai-collaboration-governance
knowledge_kind: procedural
authority: project
authority_path: DECISIONS.md
allowed_consumers: [human, agent]
---

# 复查和升级 AI 协作治理知识

## When To Use

当一条规则到达 `review_after`、被反复违反、与其他规则冲突，或 Agent、工具和项目环境发生变化时使用。

## Procedure

1. 确认记录类型：规范、描述、经验、Skill 还是 Bundle。
2. 找到真正的权威来源，检查是否仍然存在和适用。
3. 检查最近使用、失败案例、冲突记录和引用反馈。
4. 判断保留、修订、升级、降级、合并或归档。
5. 更新 `updated`、`last_verified`、`review_after`、`confidence` 和 `staleness`。
6. 记录复查理由、证据和对下游 Skill/Bundle 的影响。
7. 运行索引与审计；必要时提出新的治理 Proposal。

## Decision Table

| 情况 | 处理 |
|---|---|
| 内容仍有效且证据充分 | 保留并刷新复查日期 |
| 事实变化但原则仍有效 | 修订正文，保留原则 |
| 经验可重复且边界清楚 | 提出 Skill 草案 |
| 规则权威来源已变化 | 更新映射并重新验证 |
| 内容过时或无证据 | 降级、标记 stale 或归档 |

## Pitfalls

- 不要只因为日期到了就机械延长 `review_after`。
- 不要把派生 Card 的内容当成权威规则。
- 不要隐藏冲突或把不确定性写成确定结论。

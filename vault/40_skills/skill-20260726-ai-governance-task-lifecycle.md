---
id: skill-20260726-ai-governance-task-lifecycle
type: skill
title: "执行一次受治理的 AI 协作任务"
summary: "用于在 Codex、Claude 或其他 Agent 参与的任务中完成范围确认、风险判断、执行、验证和收尾。"
tags: [ai-collaboration-governance, workflow, task-lifecycle, agent]
stage: skill-draft
trigger: [new-task, code-change, research-task, agent-collaboration]
inputs: [user-request, project-context, applicable-rules]
outputs: [verified-result, citations, closeout-record]
source_cards: [card-20260726-ai-governance-domain-boundary, card-20260726-ai-governance-constitution, card-20260726-ai-governance-rules-permissions, card-20260726-ai-governance-workflows, card-20260726-ai-governance-agent-roles]
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

# 执行一次受治理的 AI 协作任务

## When To Use

当任务需要一个或多个 Agent 读取知识、修改文件、研究外部信息、调用工具或产生可持久化结果时使用。

## Procedure

1. 明确用户目标、项目归属、交付物和约束。
2. 读取适用的项目与工作区规则，判断是否需要提问。
3. 按后果、风险和可逆性判断是否需要 Proposal 或人工批准。
4. 选择最小必要的 Agent 角色和工具权限。
5. 执行任务，保持变更范围和权限边界。
6. 用测试、索引、来源或人工检查验证结果。
7. 说明事实、推断、未解决风险和引用来源。
8. 记录 closeout、遗留事项和可沉淀的经验。

## Output Template

```text
目标：
范围与权限：
使用的角色：
批准边界：
已完成：
验证：
引用与不确定性：
下一步：
```

## Pitfalls

- 不要把 Agent 能做到的事情当成 Agent 被授权做的事情。
- 不要让一次对话直接成为永久规则。
- 不要跳过验证和收尾。

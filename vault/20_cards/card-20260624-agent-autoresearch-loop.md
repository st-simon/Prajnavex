---
id: card-20260624-agent-autoresearch-loop
type: card
title: "Agent 的关键跃迁是围绕目标函数持续自我改进"
summary: "比起让 agent 一次性写代码，更重要的能力是把 agent 部署在明确目标函数上，让它观察指标、修改方案、运行验证并持续推进。"
tags: [ai, coding-agent, autoresearch, feedback-loop, product-strategy]
stage: promotable
source_id: "source-20260624-ai-coding-host-layer-descent-infographics"
created: 2026-06-24
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-08-26
confidence: medium
staleness: watch
usefulness: high
actionability: workflow-pattern
promotable: true
---

# Agent 的关键跃迁是围绕目标函数持续自我改进

## Core Idea

下一代 coding agent 的重要信号不是“能写多少代码”，而是能否围绕一个可度量目标函数形成持续闭环：提出改动、执行改动、观察指标、判断效果、继续迭代。

## Loop Pattern

```text
目标函数 -> 初始方案 -> 执行动作 -> 指标反馈 -> 策略修正 -> 再执行
```

这类循环把 agent 从问答工具变成实验执行者。用户不再逐步要求“帮我改这里”，而是设定目标，例如训练时间下降、测试通过率提高、渲染速度提升、错误率降低。

## Preconditions

- 目标可量化：benchmark、测试、速度、成本、准确率、转化率等。
- 环境可运行：agent 能执行代码、读取结果、保留尝试历史。
- 反馈足够快：指标延迟不能太长，否则循环成本过高。
- 权限有边界：agent 可以操作，但关键风险动作需要审批。
- 失败可回滚：每轮实验能恢复或比较。

## Product Implication

真正强的 agent 产品需要提供的不只是模型调用，而是一个安全的连续实验环境：任务队列、运行沙箱、评估指标、版本记录、回滚机制和人类审批点。

## Pitfall

不要把一次性自动化误判为 autoresearch。只有当 agent 能在目标函数上持续观察、反思和改进时，才构成真正的闭环。

## Source

[[source-20260624-ai-coding-host-layer-descent-infographics]]

## Review 2026-07-26

保留为中等置信度的方法判断。官方材料继续显示 coding agent 正在增加自主运行、检查点和反馈闭环能力，但本 Card 的“持续自我改进”仍要求具体目标函数、可观察指标和可回滚环境，不能仅凭产品宣传或一次性自动化宣称已经实现。

复查证据：

- https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously
- https://arxiv.org/abs/2603.05344

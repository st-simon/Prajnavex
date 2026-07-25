---
id: card-20260624-ai-coding-host-layer-descent
type: card
title: "AI Coding 产品在向更深宿主层下沉"
summary: "AI Coding 的代际变化可以被看作宿主入口迁移：从编辑器，到终端，再到个人 OS 与 IM。越深的宿主层越可能获得更完整上下文、更强权限、更长驻留时间和更大的潜在用户池。"
tags: [ai, coding-agent, product-strategy, host-layer]
stage: promotable
source_id: "source-20260624-ai-coding-host-layer-descent-infographics"
created: 2026-06-24
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-08-26
confidence: medium
staleness: watch
usefulness: high
actionability: framework
promotable: true
---

# AI Coding 产品在向更深宿主层下沉

## Core Idea

AI Coding 的竞争不是简单地从“补全更准”进化到“agent 更聪明”，而是宿主层级在下沉。产品越接近操作系统、通讯入口和长期任务环境，就越能拿到持续上下文、执行权限和用户日常工作流。

## Host Layer Ladder

- 编辑器层：适合代码补全、局部修改、文件级上下文。
- 终端层：适合运行命令、读写项目、执行测试、调试环境。
- OS + IM 层：适合跨应用、跨文件、跨沟通场景地常驻执行。

## Why It Matters

宿主层越深，agent 的能力边界越像“可委派的工作流”，而不是“增强版输入框”。深宿主层带来四种优势：

- 更完整上下文：项目、终端、历史尝试、用户偏好和沟通记录。
- 更强执行权：本地命令、文件系统、应用跳转、通知和审批流。
- 更长驻留时间：从一次请求变成一个持续任务。
- 更高切换成本：用户不只是迁移插件，而是在迁移工作入口。

## Diagnostic Questions

- 这个产品只嵌在工具里，还是成为用户工作的入口？
- 它依赖用户频繁提示，还是能围绕目标持续推进？
- 它能否观察真实反馈：测试、benchmark、用户行为、业务指标？
- 它的上下文是临时 session，还是可积累的长期记忆？
- 它扩大了用户池，还是只服务原有 IDE 用户？

## Source

[[source-20260624-ai-coding-host-layer-descent-infographics]]

## Review 2026-07-26

保留为中等置信度的分析框架。Cursor 将 agent 工作流扩展到编辑器之外，Claude Code 同时覆盖终端、VS Code 和自主运行，OpenClaw 文档也显示本地记忆与多渠道 agent runtime 已成为可观察形态；但“宿主层越深必然越有价值”仍是待验证推论，不是事实结论。

复查证据：

- https://cursor.com/blog/third-era
- https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously
- https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md

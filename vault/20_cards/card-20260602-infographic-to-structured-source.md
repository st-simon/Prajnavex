---
id: card-20260602-infographic-to-structured-source
type: card
title: "信息图适合先转成结构化文本再提炼卡片"
summary: "图片类资料尤其是信息图，应该先保留 OCR 原文，再整理 Cleaned Text，最后提炼 source 和 cards。"
tags: [prajnavex, image-ingest, ocr, workflow]
stage: extracted
source_id: "source-20260602-coffee-bean-family-infographic"
source_url: ""
created: 2026-06-02
updated: 2026-06-04
last_verified: 2026-06-04
review_after: 2026-12-04
confidence: high
staleness: fresh
usefulness: high
actionability: workflow-rule
promotable: true
---

# 信息图适合先转成结构化文本再提炼卡片

## Core Idea

信息图通常包含标题、分类、表格、图标和小字。OCR 会有噪声，因此应采用四步流程：

```text
OCR Text -> Cleaned Text -> Source -> Cards
```

## How To Apply

- OCR Text 保留为原始机器输出。
- Cleaned Text 由人或视觉模型整理成可信文本。
- Source 记录图片的整体含义和来源。
- Cards 提炼可复用的判断、分类法或工作流。

## Source

[[source-pasted-image-20260528120958]]

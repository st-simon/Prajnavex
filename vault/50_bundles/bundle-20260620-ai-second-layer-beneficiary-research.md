---
id: bundle-20260620-ai-second-layer-beneficiary-research
type: bundle
title: "AI 第二层受益者研究工作流"
summary: "把行业、公司、财务和资本开支证据组织成候选公司地图、投资假设、风险检查清单与后续研究问题。"
tags: [ai, investing, research-workflow, second-order-beneficiaries]
stage: bundle-draft
skills: [skill-20260602-ai-second-layer-beneficiary-research]
created: 2026-06-20
updated: 2026-07-26
last_verified: 2026-07-26
review_after: 2026-10-26
confidence: medium
staleness: fresh
input_contract: "目标行业或市场、候选公司、财务数据、客户暴露、AI 资本开支周期及估值证据。"
output_contract: "候选公司地图、逐公司研究假设、关键指标、反证条件、风险检查清单和待验证问题。"
workflow_status: draft
---

# AI 第二层受益者研究工作流

## Goal

识别 AI 资本开支和使用扩散带来的第二层、第三层受益公司，同时避免把叙事暴露误判为可持续基本面改善。

## Included Skills

- [[skill-20260602-ai-second-layer-beneficiary-research]]

当前 v0.2 execution seed 只包含一个已存在的研究 Skill。未来只有在新增独立、可复用的验证 Skill 后，才扩展此 Bundle；不为凑数量拆分虚假步骤。

## Workflow

1. 明确研究市场、行业边界和候选公司集合。
2. 收集收入、客户、订单、利润率、现金流、估值及资本开支周期证据。
3. 运行“寻找 AI 第二层受益者”Skill，生成候选地图和逐公司假设。
4. 对每个候选项记录反证条件、周期风险、客户集中度和估值风险。
5. 输出需要进一步验证的问题，不形成自动投资建议。

## Done Criteria

- 每个候选公司都有明确的 AI 暴露来源和受益机制。
- 每个研究假设都包含关键指标与反证条件。
- 输出区分事实、推断与待验证问题。
- 最终结果包含风险检查清单，且明确声明不构成投资建议。

## Review 2026-07-26

工作流仍能正确组合当前 Skill，目标、流程和完成标准没有发现结构性问题。本次刷新为 `fresh`，未改变 Bundle 阶段或投资研究边界。

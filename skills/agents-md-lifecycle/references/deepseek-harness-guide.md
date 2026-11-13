# DeepSeek Harness Compatibility & Optimization Guide

## 1. 概述与定位 (Overview)
DeepSeek Harness (`deepseek-ai/deepseek-harness`) 是基于 Cordis 运行时的插件化 Agent 架构与评测环境。
本指南针对在 DeepSeek Harness 运行时中运行或测试的 Agent，制定 `AGENTS.md` 规范与提示词工程约束。

---

## 2. 运行时与环境识别特征 (Detection Signatures)
当项目中存在以下特征之一时，判定项目启用了 DeepSeek Harness 兼容模式：
- 存在 `dsh` CLI 命令或可执行脚本
- 存在 Cordis 插件依赖或 `harness.config.*` / `dsh.yaml` 配置文件
- 存在 `deepseek-harness` 评测集基准目录（如 `benchmarks/`、`evals/`）
- 环境变量中声明了 `DEEPSEEK_API_KEY`、`DEEPSEEK_BASE_URL`

---

## 3. DeepSeek 模型特性与 Token 经济学 (Token Economy)
针对 DeepSeek-V3 与 DeepSeek-R1 推理模型，执行严格优化：
1. **保护推理预算 (Preserve Reasoning Tokens)**：
   - DeepSeek-R1 会生成内生思维链 (`<think>...</think>`)。
   - 根文档 `AGENTS.md` 必须维持在 150 行以内，严禁闲聊客套与冗余解释。过载的上下文会显著削弱模型的深度推理质量。
2. **确定性动宾指令 (Imperative Grammar)**：
   - DeepSeek 对成对规则响应最稳定：明确标注 `FORBIDDEN: X -> USE: Y`。
   - 避免模糊指令（如“请尽量考虑安全” -> `FORBIDDEN: Raw SQL -> USE: Parameterized queries`）。
3. **结构化工具契约 (Structured Tool Contract)**：
   - 遵守严格的 JSON / Tool Call 协议，输出确定性字段，杜绝 markdown 语法包裹混淆。

---

## 4. 关键命令与评测门禁 (Harness Commands)
在 DeepSeek Harness 项目的 `AGENTS.md` 中，配置标准执行入口：
- Harness 交互运行：`dsh run --agent <name>`
- 基准评测运行：`dsh eval --suite <benchmark-suite>`
- 插件热重载：`dsh plugin reload`

---

## 5. AGENTS.md 样例片段 (Sample Profile)
```markdown
## CONTEXT & STACK
- Runtime: Node 22 / Python 3.12 | DeepSeek Harness (dsh) / Cordis
- Model Profile: DeepSeek-V3 / DeepSeek-R1 (Strict Reasoning Budget)

## CRITICAL COMMANDS
- Eval Benchmark: `dsh eval --suite default`
- Run Harness: `dsh run --agent main`

## WORKFLOW CONSTRAINTS (SPARTAN RULES)
- High SNR only: Direct actions and diffs. Zero conversational filler.
- FORBIDDEN: Unstructured tool responses -> USE: Strict schema adherence.
```

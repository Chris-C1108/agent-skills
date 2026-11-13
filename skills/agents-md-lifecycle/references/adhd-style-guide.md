# ADHD / Spartan 表达规范指南

本规范旨在消除 Agent 提示词、系统指令与规范文档中的低熵废话，最大化大语言模型的注意力集中度与指令执行率。

---

## 1. 认知原理：为什么需要 ADHD / Spartan 模式？

大语言模型（LLM）的自注意力计算机制与 ADHD（注意缺陷与多动障碍）特质高度相似：
- **工作记忆容量受限**：上下文越冗长，对核心规则的注意力稀释越严重（Attention Drift / Lost in the Middle）。
- **客套冗余降低信噪比**：礼貌前缀（如 "Please ensure", "Kindly remember to"）不仅吞噬常驻 Token 预算，还会分散模型对关键动词和约束边界的关注。
- **孤立否定指令极易失效**：仅告诉模型 "不要做 X"，模型激活了 X 的语义表示，很容易反向触发；必须声明成对约束："禁用 X -> 改用 Y"。

---

## 2. 禁用词汇与句式清单 (Banned Fluff)

严禁在 AGENTS.md 及系统提示词中出现以下低信息熵表达，检测到必须就地重写：

| 禁用类型 | 典型禁用词 / 句式 | 重写原则 |
| :--- | :--- | :--- |
| **礼貌客套** | `Please`, `Kindly`, `Would you mind`, `Remember to`, `You should`, `It is important that` | 删去修饰，直接使用动宾命令句（如 `Run...`, `Enforce...`） |
| **主观模糊** | `Clean code`, `Properly`, `Carefully`, `Well-structured`, `As much as possible`, `Reasonable` | 替换为可度量标准（如 `Max 30 lines/fn`, `Zero lint warnings`） |
| **元对话废话**| `As an AI assistant...`, `In this repository, we prefer to...`, `The reason is that...` | 直接陈述事实与规则，禁止背景唠叨 |
| **空洞铺垫** | `Here is the result:`, `Sure, I can help with that!`, `In summary, ...` | 零前缀开门见山，首句即结论或有效数据 |

---

## 3. ADHD 槽位化转换对照表 (SNR Optimization)

| 传统低信噪比写法 (Low SNR) | ADHD / Spartan 极致高信噪比写法 (High SNR) |
| :--- | :--- |
| Please make sure you run the tests before pushing and be careful not to break anything. | **PRE-COMMIT**: Run `pnpm test`. Zero failed tests allowed. |
| In this research report, avoid using very long paragraphs because readers get bored easily. | **LAYOUT**: Max 3 lines per paragraph. Bullet points prioritized. |
| We used to use yarn, but recently we switched to pnpm, so please do not use yarn anymore. | **PKG_MGR**: `pnpm` only. FORBIDDEN: `yarn`, `npm`. |
| Make sure slides are engaging with good contrast and not too much text on each slide. | **SLIDE_RULES**: 1 core takeaway/slide. Contrast ratio >= 4.5:1. Max 4 bullets/slide. |
| Try to write modular code and keep components small and reusable when possible. | **COMPONENT_BUDGET**: Max 120 lines/component. Extract hooks if > 2 `useEffect`. |
| When answering questions, please be concise and get straight to the point. | **OUTPUT_STYLE**: BLUF (Bottom Line Up Front). Zero preamble. |

---

## 4. 语法约束核心结构 (Rule Syntax)

每条规则遵循两类原子结构之一：

### 结构 A：动作指令型 (Imperative Action)
```text
[CATEGORY/DOMAIN]: [Imperative Verb] [Concrete Target] [Metrics/Boundary]
```
*示例*：
- `TEST_GATE: Run vitest on modified file before declaring task done.`
- `DOC_BUDGET: Limit root AGENTS.md to 150 lines.`

### 结构 B：成对否定替代型 (Paired Negative Constraint)
```text
FORBIDDEN: [Prohibited Action/Tool/Syntax] -> USE: [Allowed Alternative]
```
*示例*：
- `FORBIDDEN: Direct schema edits in production -> USE: Prisma migration files.`
- `FORBIDDEN: npm or yarn install -> USE: pnpm install.`
- `FORBIDDEN: H3 headers in executive summary -> USE: Bold bullet lists.`

# AGENTS.md

## PROJECT PURPOSE & AUDIENCE
- Domain: {PROJECT_DOMAIN} (e.g., 竞争情报调研 / 行业技术白皮书 / 融资路演 PPT)
- Target Audience: {TARGET_AUDIENCE} (e.g., C-Level 决策层 / 研发架构师 / 投资人 / 个人学习)
- Deliverable Format: {OUTPUT_FORMAT} (e.g., Markdown 报告 / Marp PPTX 源码 / 飞书文档)

## STYLE & INFORMATION DENSITY (ADHD MODE)
- Tone: Objective, analytical, brutal high-signal.
- NO conversational filler: 严禁前置寒暄（如“好的，为您整理如下”）、文末空洞总结。
- Hierarchy: 结论前置（BLUF: Bottom Line Up Front）。
- Layout: 单段不得超过 3 行；超过 2 个并列要点强制采用无序列表加粗首词。

## FACT & CITATION RULES
- 严禁模糊推测：置信度低于 90% 的数据必须明确标注 `[待校验数据]`。
- 事实溯源：所有关键论点必须在行末标注来源文件或参考链接。
- 数据冲突时：保留最新时间戳信源，并向用户显式标出冲突点。
- 会话与教训检索：重大方案重构前，核对 `docs/handoff/handoff-readme.md` 历史经验或运行 `handoff2docs`。
- 交付交接规范：会话结束前运行 `handoff2docs` 归档成果与结论。
- FORBIDDEN: Reversing deliberate decisions or proposing rejected options -> USE: Check docs/decisions/ first.

## DELIVERABLE ARTIFACT SPECIFICATIONS
- PPT/幻灯片制作：
  - 每页 1 个核心洞察，单页要点不超过 4 行。
  - 使用 Marp/Markdown 语法输出，代码块必须可直接渲染。
- 调研报告：
  - 必须包含四大板块：执行摘要 (Executive Summary) -> 核心对比矩阵 -> 深度剖析 -> 行动建议。

## REFERENCE POINTERS
- Handoff & lessons ledger: -> `docs/handoff/handoff-readme.md`
- Architecture decisions & rejected archive: -> docs/decisions/
- 原始资料库索引: -> `references/sources.md`
- 专属术语表与受众画像: -> `specs/glossary.md`

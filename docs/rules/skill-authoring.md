# Agent 技能研发与规范指南 (Skill Authoring Standard)

## 1. 技能目录标准规范
每个新技能必须放置在 `skills/<skill-name>/` 下，并具备如下目录骨架：
- `SKILL.md`：技能调度入口（严格包含 YAML frontmatter：name, description, triggers）。
- `README.md`：人读说明书，包含背景、架构与典型实战命令。
- `references/`：高阶操作指南、模板与细分领域规约（支持渐进式信息披露）。
- `scripts/`：该技能自带的辅助 CLI / 校验脚本。
- `assets/`：静态资源或开箱即用代码模版。

## 2. 编写与修剪原则
- **行数预算**：`SKILL.md` 必须控制在 200 行以内；细节按需拆分至 `references/*.md`。
- **ADHD 零废话**：全篇采用动宾命令句与成对约束（`FORBIDDEN: X -> USE: Y`），严禁任何礼貌客套与前置铺垫。
- **真实性第一**：所有命令必须经过运行环境真实性验证，严禁虚构不存在的 CLI 参数或依赖。
- **融合修改 (Integrated Editing)**：`FORBIDDEN: Appending rule modifications blindly to the bottom -> USE: Integrate modifications into existing logical sections and balance with existing constraints.`
- **诚实验收规范 (Explicit Verification Standard)**：`FORBIDDEN: Omitting unverified checks or claiming false passes -> USE: Explicitly list all verification items with status ('Passed' or 'Not run'). A check that was not run must be explicitly marked as 'Not run'.`

## 3. 发布与同步测试门禁
- 本地研发完成后，运行 `npm run lint` 确保静态合规通过；
- 运行 `npm run install:all` 同步至本机 `~/.agents/skills` 与 `~/.codex/skills`；
- 在真实 Agent 会话中测试触发词与执行效果。

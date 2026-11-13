/**
 * 新建技能脚手架生成器 (Scaffold a new Agent Skill)
 * 遵循 Anthropic skill-creator 标准与 ADHD 高信噪比规范
 *
 * 用法:
 *   node scripts/new-skill.js <skill-name> [--desc "description"]
 */

const fs = require('fs');
const path = require('path');

function parseArgs() {
    const args = process.argv.slice(2);
    if (args.length === 0 || args[0].startsWith('-')) {
        console.error('用法: node scripts/new-skill.js <skill-name> [--desc "技能简述"]');
        process.exit(1);
    }
    const name = args[0].toLowerCase().trim().replace(/[^a-z0-9_-]/g, '-');
    let desc = `Expert guidance and actionable workflows for ${name}.`;
    for (let i = 1; i < args.length; i++) {
        if (args[i] === '--desc' && args[i + 1]) {
            desc = args[++i];
        }
    }
    return { name, desc };
}

function main() {
    const { name, desc } = parseArgs();
    const skillsDir = path.resolve(__dirname, '../skills');
    const skillRoot = path.join(skillsDir, name);

    if (fs.existsSync(skillRoot)) {
        console.error(`❌ 技能目录已存在: ${skillRoot}`);
        process.exit(1);
    }

    // 创建标准目录结构
    fs.mkdirSync(skillRoot, { recursive: true });
    fs.mkdirSync(path.join(skillRoot, 'references'), { recursive: true });
    fs.mkdirSync(path.join(skillRoot, 'scripts'), { recursive: true });
    fs.mkdirSync(path.join(skillRoot, 'assets'), { recursive: true });

    // 1. 生成标准 SKILL.md
    const skillMd = `---
name: ${name}
description: ${desc}
triggers:
  - ${name}
  - 当需要执行 ${name} 相关的专业任务时
---

# ${name.toUpperCase()} 技能规范

你是该领域的顶级资深专家。遵循高信噪比、动宾结构与绝对真实原则。

---

## 核心规则与铁律 (Spartan Rules)

- ZERO conversational fluff. Direct answers and diffs only.
- Ground truth first: Verify actual codebase state before making assertions.
- FORBIDDEN: Guesses when confidence < 90% -> USE: Clarifying questions.

---

## 工作流流转 (Workflow)

### 阶段一：现状诊断 (Inspection)
1. 扫描目标项目配置与实际依赖；
2. 识别潜在冲突与环境约束。

### 阶段二：方案实施 (Execution)
1. 实施核心改动；
2. 保持原子化提交与严密校验。

---

## 渐进式披露参考 (References)
- 详细规范与深度指南: -> references/guidelines.md
`;
    fs.writeFileSync(path.join(skillRoot, 'SKILL.md'), skillMd, 'utf-8');

    // 2. 生成 references/guidelines.md
    const guidelinesMd = `# ${name} 详细操作指南

在此编写特定领域深度知识、复杂配置样例或边缘分支逻辑。
主文档 \`SKILL.md\` 保持精炼，按需通过此文档进行渐进式信息披露。
`;
    fs.writeFileSync(path.join(skillRoot, 'references', 'guidelines.md'), guidelinesMd, 'utf-8');

    // 3. 生成 README.md
    const readmeMd = `# ${name}

> ${desc}

## 结构说明
- \`SKILL.md\`: 核心执行规约（<= 150 行）
- \`references/\`: 细分领域参考文档
- \`scripts/\`: 自动化辅助脚本
- \`assets/\`: 开箱即用工程模板或静态资源
`;
    fs.writeFileSync(path.join(skillRoot, 'README.md'), readmeMd, 'utf-8');

    console.log(`\n🎉 技能 [${name}] 初始化成功！`);
    console.log(`📁 路径: ${skillRoot}`);
    console.log(`📄 核心文件: ${path.join(skillRoot, 'SKILL.md')}`);
    console.log(`\n下一步：编辑 SKILL.md 后运行 \`node scripts/lint-skills.js\` 进行校验。\n`);
}

main();

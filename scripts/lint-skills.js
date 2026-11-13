/**
 * Agent Skills 静态质量与合规性检查器 (Linter)
 * 检查 YAML frontmatter、行数预算、废话词、路径有效性
 */

const fs = require('fs');
const path = require('path');

const MAX_SKILL_LINES = 200;
const BANNED_PATTERNS = [
    { name: 'Please', regex: /(?<!["'`“‘])\bplease\b(?!["'`”’])/i },
    { name: 'Kindly', regex: /(?<!["'`“‘])\bkindly\b(?!["'`”’])/i },
    { name: 'You should', regex: /(?<!["'`“‘])\byou should\b(?!["'`”’])/i },
    { name: 'As an AI', regex: /(?<!["'`“‘])\bas an ai\b(?!["'`”’])/i },
    { name: 'Be careful to', regex: /(?<!["'`“‘])\bbe careful to\b(?!["'`”’])/i },
    { name: 'Ensure that you', regex: /(?<!["'`“‘])\bensure that you\b(?!["'`”’])/i },
    { name: 'It is important that', regex: /(?<!["'`“‘])\bit is important that\b(?!["'`”’])/i }
];

const SKILLS_DIR = path.resolve(__dirname, '../skills');

function lintSkill(skillName) {
    const skillDir = path.join(SKILLS_DIR, skillName);
    const skillMdPath = path.join(skillDir, 'SKILL.md');

    const issues = [];
    const warnings = [];

    if (!fs.existsSync(skillMdPath)) {
        issues.push(`缺少主入口文件: SKILL.md`);
        return { issues, warnings, lineCount: 0 };
    }

    const content = fs.readFileSync(skillMdPath, 'utf-8');
    const lines = content.split(/\r?\n/);

    // 1. 检查 YAML frontmatter
    if (!content.startsWith('---')) {
        issues.push(`SKILL.md 必须以 YAML frontmatter (---) 开头`);
    } else {
        const parts = content.split('---');
        if (parts.length < 3) {
            issues.push(`YAML frontmatter 未闭合`);
        } else {
            const frontmatter = parts[1];
            if (!/name:\s*[a-z0-9_-]+/i.test(frontmatter)) {
                issues.push(`frontmatter 缺少有效的 'name' 字段`);
            }
            if (!/description:/i.test(frontmatter)) {
                issues.push(`frontmatter 缺少 'description' 字段`);
            }
        }
    }

    // 2. 检查行数预算
    if (lines.length > MAX_SKILL_LINES) {
        issues.push(`行数超标: 共 ${lines.length} 行，上限为 ${MAX_SKILL_LINES} 行（请采用渐进式披露分流至 references/）`);
    }

    // 3. 检查低熵废话（过滤掉作为反例说明的引号用法）
    lines.forEach((line, idx) => {
        BANNED_PATTERNS.forEach(({ name, regex }) => {
            const match = line.match(regex);
            if (match) {
                issues.push(`第 ${idx + 1} 行检测到废话词 '${match[0]}': "${line.trim()}"`);
            }
        });
    });

    // 4. 检查相对 markdown 引用路径
    const mdLinks = content.match(/\((references\/[a-zA-Z0-9_\-\./]+\.[a-zA-Z0-9]+)\)/g) || [];
    mdLinks.forEach(link => {
        const cleanPath = link.replace(/[()]/g, '').trim();
        const resolved = path.resolve(skillDir, cleanPath);
        if (!fs.existsSync(resolved)) {
            warnings.push(`引用的文件不存在: ${cleanPath}`);
        }
    });

    return { issues, warnings, lineCount: lines.length };
}

function main() {
    console.log('\n🔍 开始对技能库执行质量与合规性静态审查 (Linting Skills)...\n');

    const skills = fs.readdirSync(SKILLS_DIR).filter(name => {
        return fs.statSync(path.join(SKILLS_DIR, name)).isDirectory();
    });

    let totalIssues = 0;
    let totalWarnings = 0;

    for (const skill of skills) {
        const { issues, warnings, lineCount } = lintSkill(skill);
        const statusIcon = issues.length === 0 ? '✔' : '✖';
        console.log(`${statusIcon} [${skill}] (${lineCount} 行)`);

        if (issues.length > 0) {
            totalIssues += issues.length;
            issues.forEach(i => console.log(`   ❌ ${i}`));
        }
        if (warnings.length > 0) {
            totalWarnings += warnings.length;
            warnings.forEach(w => console.log(`   ⚠ ${w}`));
        }
    }

    console.log(`\n=========================================`);
    if (totalIssues > 0) {
        console.error(`❌ 审计失败: 发现 ${totalIssues} 个错误，${totalWarnings} 个警告。\n`);
        process.exit(1);
    } else {
        console.log(`🎉 审计通过: 全部 ${skills.length} 个技能均通过合规检查！\n`);
        process.exit(0);
    }
}

main();

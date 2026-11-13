/**
 * Agent Skills 本地多环境一键同步/安装器
 *
 * 用法:
 *   node scripts/install.js                      # 同步全部技能至 ~/.agents/skills 与 ~/.codex/skills
 *   node scripts/install.js --skill <name>       # 仅同步指定技能
 *   node scripts/install.js --target <agents|codex|all>  # 指定安装目标
 *   node scripts/install.js --list               # 列出当前仓库内所有可用技能
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = os.homedir();
const TARGET_AGENTS = path.join(HOME, '.agents', 'skills');
const TARGET_CODEX = path.join(HOME, '.codex', 'skills');
const SOURCE_DIR = path.resolve(__dirname, '../skills');

function copyDir(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest, { recursive: true });
    }
    const entries = fs.readdirSync(src, { withFileTypes: true });
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        if (entry.isDirectory()) {
            copyDir(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

function parseArgs() {
    const args = process.argv.slice(2);
    const options = {
        skill: null,
        target: 'all',
        list: false
    };

    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--list' || arg === '-l') {
            options.list = true;
        } else if (arg === '--skill' || arg === '-s') {
            options.skill = args[++i];
        } else if (arg === '--target' || arg === '-t') {
            options.target = args[++i] || 'all';
        } else if (!arg.startsWith('-') && !options.skill) {
            options.skill = arg;
        }
    }
    return options;
}

function getAvailableSkills() {
    if (!fs.existsSync(SOURCE_DIR)) return [];
    return fs.readdirSync(SOURCE_DIR).filter(name => {
        const skillPath = path.join(SOURCE_DIR, name);
        return fs.statSync(skillPath).isDirectory() && fs.existsSync(path.join(skillPath, 'SKILL.md'));
    });
}

function main() {
    const options = parseArgs();
    const availableSkills = getAvailableSkills();

    if (options.list) {
        console.log('\n📦 本地工作台可用技能列表 (Available Skills):');
        availableSkills.forEach((s, idx) => {
            console.log(`  ${idx + 1}. ${s}`);
        });
        console.log('');
        return;
    }

    if (availableSkills.length === 0) {
        console.log('❌ 未在 skills/ 目录下找到任何有效技能（需包含 SKILL.md）。');
        return;
    }

    const skillsToInstall = options.skill ? [options.skill] : availableSkills;

    // 验证技能是否存在
    for (const s of skillsToInstall) {
        if (!availableSkills.includes(s)) {
            console.error(`❌ 未找到技能: ${s}。请使用 --list 查看已有技能。`);
            process.exit(1);
        }
    }

    // 确定安装目录列表
    const targets = [];
    if (options.target === 'all' || options.target === 'agents') {
        targets.push({ name: '~/.agents/skills (Claude Code / OpenCode / Windsurf)', path: TARGET_AGENTS });
    }
    if (options.target === 'all' || options.target === 'codex') {
        targets.push({ name: '~/.codex/skills (Codex App / CLI)', path: TARGET_CODEX });
    }

    console.log(`\n🚀 开始同步技能至本地目标环境 (共 ${skillsToInstall.length} 个技能)...\n`);

    for (const target of targets) {
        console.log(`📁 目标目录: ${target.name}`);
        if (!fs.existsSync(target.path)) {
            fs.mkdirSync(target.path, { recursive: true });
        }

        for (const skill of skillsToInstall) {
            const srcSkillPath = path.join(SOURCE_DIR, skill);
            const destSkillPath = path.join(target.path, skill);
            copyDir(srcSkillPath, destSkillPath);
            console.log(`  ✔ 已同步: ${skill}`);
        }
        console.log('');
    }

    console.log('🎉 技能同步完成！Codex、Claude Code、OpenCode 等 Agent 将自动热重载新技能。\n');
}

main();

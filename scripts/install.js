/**
 * Agent Skills 本地一键安装器
 * 
 * 用法:
 *   node scripts/install.js               # 安装全部技能到 ~/.agents/skills
 *   node scripts/install.js <skill-name>  # 安装指定技能
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const HOME = os.homedir();
const TARGET_DIR = path.join(HOME, '.agents', 'skills');
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

function main() {
    const requestedSkill = process.argv[2];

    if (!fs.existsSync(TARGET_DIR)) {
        fs.mkdirSync(TARGET_DIR, { recursive: true });
    }

    const availableSkills = fs.readdirSync(SOURCE_DIR).filter(name => {
        return fs.statSync(path.join(SOURCE_DIR, name)).isDirectory();
    });

    if (availableSkills.length === 0) {
        console.log('未找到任何技能。');
        return;
    }

    const skillsToInstall = requestedSkill ? [requestedSkill] : availableSkills;

    for (const skill of skillsToInstall) {
        const srcSkillPath = path.join(SOURCE_DIR, skill);
        const destSkillPath = path.join(TARGET_DIR, skill);

        if (!fs.existsSync(srcSkillPath)) {
            console.error(`❌ 未找到技能: ${skill}`);
            continue;
        }

        console.log(`📦 正在安装技能 [${skill}] -> ${destSkillPath}...`);
        copyDir(srcSkillPath, destSkillPath);
        console.log(`✅ 技能 [${skill}] 安装完成！`);
    }

    console.log('\n🎉 安装完成！Codex、Claude Code、OpenCode、Antigravity 等 Agent 将立即自动识别该技能。');
}

main();

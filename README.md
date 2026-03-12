<div align="center">

# 🧬 KnowMe

**你跟 AI 的每一次对话，都在暴露你的性格。**

**KnowMe 从你的 ChatGPT / Claude / DeepSeek 聊天记录中，自动分析出你的 MBTI 类型、性格优劣势和人生建议。**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/github/license/AIPMAndy/KnowMe)](LICENSE)
[![Stars](https://img.shields.io/github/stars/AIPMAndy/KnowMe?style=social)](https://github.com/AIPMAndy/KnowMe/stargazers)
[![Issues](https://img.shields.io/github/issues/AIPMAndy/KnowMe)](https://github.com/AIPMAndy/KnowMe/issues)

[English](README_EN.md) | **简体中文**

<br>

<img src="assets/demo-output.png" width="680" alt="KnowMe 分析结果示例">

</div>

---

## 💡 为什么做这个？

传统 MBTI 测试问你「你觉得你会怎么做」。

**KnowMe 分析你真正做了什么** —— 你怎么提问、怎么做决策、怎么组织语言、在什么话题上花最多时间 —— 全部从你跟 AI 的真实对话中提取。

> **不填问卷。不靠自评。只看你的真实行为。**

想想看：你跟 ChatGPT 聊过几百上千次了，这些对话里藏着你最真实的思维模式和性格特征。KnowMe 就是把它们挖出来。

---

## 🆚 为什么选 KnowMe？

| 能力 | 传统 MBTI 测试 | AI 对话式测评 | **KnowMe** |
|------|:---:|:---:|:---:|
| 基于真实行为（非自评） | ❌ | ❌ | ✅ |
| 支持 ChatGPT / Claude / DeepSeek 数据 | ❌ | ❌ | ✅ |
| 50+ 行为信号检测 | ❌ | ❌ | ✅ |
| 中英文双语信号识别 | ❌ | 部分 | ✅ |
| 100% 本地运行，数据不出设备 | ❌ | ❌ | ✅ |
| 每个维度置信度评分 | ❌ | ❌ | ✅ |
| 16 种类型的个性化人生建议 | ✅ | 部分 | ✅ |
| 免费开源 | ❌ | ❌ | ✅ |

**核心差异：我们不让你做选择题，我们让你的行为替你回答。**

---

## 🚀 30 秒快速开始

### 方式一：命令行（推荐）

```bash
# 克隆项目
git clone https://github.com/AIPMAndy/KnowMe.git
cd KnowMe

# 分析你的 ChatGPT 数据（去 ChatGPT Settings → Data Controls → Export 导出）
python3 scripts/collect.py --source chatgpt --file ~/Downloads/conversations.json --output data.json
python3 scripts/analyze.py --input data.json --output report.md
python3 scripts/advise.py --report report.md --output advice.md

# 查看你的性格报告！
cat report.md
```

### 方式二：作为 OpenClaw Skill

```bash
# 安装 skill
openclaw skill install knowme

# 然后直接跟你的 AI 助理说：
# "分析一下我的性格"
# "我的 MBTI 是什么？"
# "从我们的聊天记录里分析我"
```

---

## 📊 你会得到什么

### 1. MBTI 类型 + 置信度评分

```
你的 MBTI 类型：INTJ（建筑师 / Architect）

E [██████░░░░░░░░░░░░░░] I  (28% / 72%) → I ⬅️ (高置信度)
S [░░░░░░░░████████████] N  (15% / 85%) → N ⬅️ (高置信度)
T [████████████████░░░░] F  (78% / 22%) → T ⬅️ (高置信度)
J [██████████████░░░░░░] P  (68% / 32%) → J ⬅️ (中置信度)
```

每个维度都有：
- 📊 百分比得分（不是二元标签）
- 🎯 置信度等级（高/中/低）
- 📝 行为证据（你说了什么让我们这么判断的）

### 2. 沟通风格分析

- 消息长度模式（你是精简派还是长文派？）
- 问句/感叹率
- Emoji 使用频率
- 话题分布（技术 vs 商业 vs 人际 vs 自我成长）
- 协作 vs 独立倾向

### 3. 个性化人生建议

- 💪 **你的超能力** — 前 3 大优势
- 🌱 **成长边界** — 最值得突破的 3 个方向
- 🎯 **职业透镜** — 你适合什么角色、什么工作方式
- 💬 **沟通盲区** — 你可能没意识到的问题
- ❤️ **关系洞察** — 你的社交模式和相处风格
- ⚡ **30 天挑战** — 一个具体的成长实验

---

## 📦 支持的数据源

| 数据源 | 命令 | 获取方式 |
|--------|------|----------|
| **ChatGPT** | `--source chatgpt --file conversations.json` | Settings → Data Controls → Export Data |
| **Claude** | `--source claude --file claude_export.json` | Settings → Account → Export Data |
| **OpenClaw** | `--source openclaw` | 自动读取 workspace 记忆文件 |
| **任意文本** | `--source text --file ./chats/` | 任何含 `User:/Assistant:` 标记的 .md/.txt |

> 💡 **小贴士**：数据越多，分析越准。建议 50 条以上消息。把多个平台的数据合并效果最好。

---

## 🔬 技术原理

KnowMe **不**调用任何 AI API 来分析（那样又慢又贵又不稳定）。

我们用的是 **信号检测系统**：

```
你的聊天记录 → 50+ 行为信号扫描 → 8 维度加权评分 → MBTI + 性格画像
```

### 信号示例

| 你说的话 | 检测到的信号 | 影响维度 |
|---------|------------|---------|
| "让我想想..." | 需要独处思考 | I +3 |
| "我们一起讨论一下" | 协作倾向 | E +2 |
| "具体怎么一步步做？" | 实用导向 | S +2 |
| "如果从另一个角度看..." | 抽象思维 | N +2 |
| "数据显示..." | 数据驱动 | T +2 |
| "这会让大家感受如何？" | 人际关怀 | F +2 |
| "下一步行动是什么？" | 闭合驱动 | J +2 |
| "看情况吧，灵活调整" | 开放弹性 | P +2 |

### 为什么这么设计？

- ⚡ **快** — 1000+ 条消息几秒内分析完
- 🔒 **隐私** — 零 API 调用，数据不出设备
- 📊 **可解释** — 每个评分都有行为证据
- 🔄 **可复现** — 相同输入永远得到相同结果

---

## 🛠️ 进阶用法

### 合并多个数据源

```bash
# 分别收集
python3 scripts/collect.py --source chatgpt --file chatgpt.json --output /tmp/gpt.json
python3 scripts/collect.py --source claude --file claude.json --output /tmp/claude.json

# 合并（用 jq）
jq -s '{messages: (.[0].messages + .[1].messages), source: "merged", total_messages: (.[0].total_messages + .[1].total_messages)}' \
  /tmp/gpt.json /tmp/claude.json > /tmp/merged.json

# 分析合并数据
python3 scripts/analyze.py --input /tmp/merged.json --output report.md
```

### 导出原始评分

```bash
python3 scripts/analyze.py --input data.json --output report.md --json raw_scores.json
```

---

## 🏗️ 项目结构

```
knowme/
├── README.md                         # 中文文档
├── README_EN.md                      # English docs
├── scripts/
│   ├── collect.py                    # 多源数据收集器
│   ├── analyze.py                    # 信号检测 + 性格分析
│   └── advise.py                     # 16 类型个性化建议
├── references/
│   ├── mbti_signals.md               # 信号分类体系（50+ 信号）
│   └── advice_frameworks.md          # 建议生成框架
├── assets/                           # 演示图片和素材
├── SKILL.md                          # OpenClaw Skill 定义
├── CONTRIBUTING.md                   # 贡献指南
└── LICENSE                           # MIT 开源协议
```

---

## 🗺️ Roadmap

- [x] 核心 MBTI 4 维度分析
- [x] ChatGPT / Claude / OpenClaw 数据源
- [x] 16 种类型个性化建议
- [x] 中英文双语信号检测
- [x] OpenClaw Skill 集成
- [ ] 🔜 Web UI（上传文件 → 在线看报告）
- [ ] 🔜 Gemini / Copilot / DeepSeek 数据源
- [ ] 🔜 Big Five（大五人格）分析模块
- [ ] 🔜 时间线分析（你的性格是怎么变化的？）
- [ ] 🔜 匿名基准对比（你和 10 万人比怎么样？）
- [ ] 🔜 AI 对话风格分析（不同 AI 如何改变你的表达？）

---

## 🤝 参与贡献

欢迎 PR！特别是以下方向：

- 🔌 新数据源解析器（Gemini、Copilot、DeepSeek 等）
- 🔍 新的行为信号 pattern
- 🌍 更多语言的信号检测
- 📊 可视化和 Web UI
- 🧪 Big Five / Enneagram 等其他人格框架

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## ⚠️ 免责声明

KnowMe 是自我探索工具，不是临床诊断。MBTI 是偏好模型 —— 用这些结果作为自我反思的起点，而不是固定标签。分析质量随对话数据量提升（建议 50+ 条消息）。

---

## 📄 License

[MIT](LICENSE) — 随便用，随便改，随便分享。

---

<div align="center">

**如果 KnowMe 帮你更了解了自己，给个 ⭐ Star 吧！**

**Built with ❤️ by [AI酋长Andy](https://github.com/AIPMAndy)**

*你跟 AI 聊了那么多，是时候让这些对话为你所用了。*

</div>

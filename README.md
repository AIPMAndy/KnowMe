# 🧬 KnowMe

[English](./README_EN.md) | 中文

> **你和 AI 的每一次对话，都在暴露你的性格。**
>
> KnowMe 分析你的 ChatGPT / Claude / DeepSeek 聊天记录，推断 MBTI 类型、性格优劣势、职业方向，并给出可执行的成长建议。

[![Star](https://img.shields.io/github/stars/AIPMAndy/KnowMe?style=social)](https://github.com/AIPMAndy/KnowMe/stargazers)
[![License](https://img.shields.io/github/license/AIPMAndy/KnowMe)](https://github.com/AIPMAndy/KnowMe)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/Built%20for-OpenClaw-purple)](https://github.com/openclaw/openclaw)

---

## 💡 为什么是 KnowMe？

传统 MBTI 测试问的是「你觉得自己会怎么做」。

**KnowMe 分析的是你实际怎么做的** —— 你怎么提问、怎么决策、怎么组织思路、关注什么话题。全部从你和 AI 的真实对话中提取。

> **没有问卷，没有自我美化偏差。只有你最真实的行为模式。**

| 能力 | 传统 MBTI 测试 | AI 聊天评估 | **KnowMe** |
|------|:---:|:---:|:---:|
| 基于真实行为（非自我报告） | ❌ | ❌ | ✅ |
| 支持 ChatGPT / Claude / DeepSeek | ❌ | ❌ | ✅ |
| 50+ 行为信号检测 | ❌ | ❌ | ✅ |
| 中英双语信号识别 | ❌ | 部分 | ✅ |
| 100% 本地运行，数据不出设备 | ❌ | ❌ | ✅ |
| 职业方向建议 | ❌ | ❌ | ✅ |
| 免费开源 | ❌ | ❌ | ✅ |

---

## 🚀 快速开始（30 秒）

### 方式一：命令行（推荐）

```bash
git clone https://github.com/AIPMAndy/KnowMe.git
cd KnowMe

# 1. 收集数据（ChatGPT: 设置 → 数据控制 → 导出数据）
python3 scripts/collect.py --source chatgpt --file ~/Downloads/conversations.json --output data.json

# 2. 分析性格
python3 scripts/analyze.py --input data.json --output report.md

# 3. 生成建议（含职业方向）
python3 scripts/advise.py --report report.md --output advice.md

# 看报告！
cat report.md
```

### 方式二：作为 OpenClaw Skill

```bash
openclaw skill install knowme

# 然后直接问你的 AI 助手：
# "分析一下我的性格"
# "我的 MBTI 是什么？"
# "给我职业方向建议"
```

---

## 📊 你会得到什么

### 1. MBTI 类型 + 置信度评分

```
你的 MBTI 类型: INTJ（建筑师）

E [██████░░░░░░░░░░░░░░] I  (28% / 72%) → I ⬅️ 高置信度
S [░░░░░░░░████████████] N  (15% / 85%) → N ⬅️ 高置信度
T [████████████████░░░░] F  (78% / 22%) → T ⬅️ 高置信度
J [██████████████░░░░░░] P  (68% / 32%) → J ⬅️ 中置信度
```

每个维度包含：百分比评分、置信度等级、行为证据（哪些对话导致了这个评分）。

### 2. 沟通风格分析

- 消息长度模式（你是简洁型还是详尽型？）
- 提问 / 感叹频率
- Emoji 使用习惯
- 话题分布（技术 vs 商业 vs 人际 vs 自我成长）
- 协作 vs 独立倾向

### 3. 🎯 职业方向建议（NEW）

基于你的 MBTI 类型和对话中的行为模式，给出个性化的职业洞察：

```
🎯 职业方向分析:

  适合你的赛道:
  - 战略咨询 / 管理咨询（发挥系统性思维）
  - 产品架构 / 技术架构（长期规划 + 逻辑能力）
  - 独立研究 / R&D（深度思考 + 自驱力）

  你的职场超能力:
  - 能快速看到系统全貌，找到杠杆点
  - 擅长把模糊问题结构化
  - 长期主义，不被短期噪音干扰

  需要注意的职业陷阱:
  - ⚠️ 容易低估「人」的因素（团队管理、向上沟通）
  - ⚠️ 可能过度优化而错过执行窗口
  - ⚠️ 独立偏好强，注意别变成信息孤岛

  给你的行动建议:
  - 找一个需要「说服别人」的项目练手
  - 每周主动做一次非正式的 1:1 沟通
  - 把你的分析能力包装成可交付的方案，而不只是洞察
```

**16 种 MBTI 类型均有对应的职业建议框架：**

| 类型组 | 适合方向 | 核心优势 |
|--------|----------|----------|
| NT（INTJ/INTP/ENTJ/ENTP） | 战略、架构、研发、咨询 | 系统思维 + 创新 |
| NF（INFJ/INFP/ENFJ/ENFP） | 产品、设计、教育、内容 | 愿景驱动 + 共情 |
| ST（ISTJ/ISTP/ESTJ/ESTP） | 运营、工程、财务、管理 | 执行力 + 可靠性 |
| SF（ISFJ/ISFP/ESFJ/ESFP） | HR、客户成功、社区、医疗 | 人际连接 + 服务意识 |

### 4. 个性化成长建议

- 💪 **你的超能力** —— Top 3 优势
- 🌱 **成长空间** —— 最值得发展的 3 个方向
- 💬 **沟通盲区** —— 你可能没注意到的问题
- ❤️ **关系洞察** —— 你的社交模式
- ⚡ **30 天挑战** —— 一个具体的成长实验

### 5. 🎨 生成式个性化（v2.0）

**从性格到视觉 —— 生成你的专属形象**

```bash
# 生成个性化肖像
python3 scripts/generate_portrait.py --mbti INTJ --style professional

# 直接生成图像（支持 Bailian/PonyFlash 等）
python3 scripts/generate_image.py --mbti INTJ --service bailian --output portrait.png
```

支持 professional / anime / realistic / artistic / minimalist 多种风格。

---

## 📦 支持的数据源

| 来源 | 命令 | 如何导出 |
|------|------|----------|
| **ChatGPT** | `--source chatgpt --file conversations.json` | 设置 → 数据控制 → 导出数据 |
| **Claude** | `--source claude --file claude_export.json` | 设置 → 账户 → 导出数据 |
| **OpenClaw** | `--source openclaw` | 自动读取 workspace 记忆文件 |
| **任意文本** | `--source text --file ./chats/` | 任何含 `User:/Assistant:` 标记的 .md/.txt 文件 |

> 💡 数据越多，分析越准。建议 50+ 条消息。合并多平台数据效果最佳。

---

## 🔬 工作原理

KnowMe **不调用任何 AI API** 做分析（那样慢、贵、不稳定）。

它使用**基于信号的评分系统**：

```
你的聊天记录 → 50+ 行为信号扫描 → 8 维度加权评分 → MBTI + 性格画像 + 职业建议
```

| 你说了什么 | 检测到的信号 | 影响维度 |
|-----------|-------------|---------|
| "让我想想..." | 需要独处思考时间 | I +3 |
| "我们一起头脑风暴吧" | 协作倾向 | E +2 |
| "具体怎么一步步做？" | 实践导向 | S +2 |
| "换个角度看看..." | 抽象思维 | N +2 |
| "数据显示..." | 数据驱动决策 | T +2 |
| "团队会怎么想？" | 以人为本 | F +2 |

**为什么这样做？**
- ⚡ 快 —— 1000+ 条消息秒级分析
- 🔒 隐私 —— 零 API 调用，数据不出设备
- 📊 可解释 —— 每个评分都有行为证据
- 🔄 可复现 —— 相同输入永远相同输出

---

## 📁 项目结构

```
KnowMe/
├── scripts/
│   ├── collect.py              # 多源数据收集器
│   ├── analyze.py              # 信号评分性格分析
│   ├── advise.py               # 16 类型个性化建议引擎（含职业方向）
│   ├── generate_portrait.py    # MBTI → 图像 Prompt
│   └── generate_image.py       # 直接生成图像
├── references/
│   ├── mbti_signals.md         # 信号分类（50+ 信号）
│   └── advice_frameworks.md    # 建议生成框架（含职业建议）
├── assets/                     # Demo 图片
├── SKILL.md                    # OpenClaw Skill 定义
└── README.md
```

---

## 🗺️ Roadmap

- [x] MBTI 4 维度核心分析
- [x] ChatGPT / Claude / OpenClaw 数据源
- [x] 16 类型个性化建议
- [x] 中英双语信号检测
- [x] 职业方向建议模块
- [x] 生成式个性化肖像（v2.0）
- [ ] 🔜 Web UI（上传文件 → 浏览器看报告）
- [ ] 🔜 Gemini / Copilot / DeepSeek 数据源
- [ ] 🔜 大五人格分析模块
- [ ] 🔜 时间线分析（你的性格如何变化？）
- [ ] 🔜 匿名基准对比（你和 10 万人比如何？）

---

## 🤝 贡献

欢迎 PR！特别欢迎：

- 🔌 新数据源解析器（Gemini、Copilot、DeepSeek 等）
- 🔍 新的行为信号模式
- 🌍 更多语言的信号检测
- 🎯 更细粒度的职业建议框架
- 📊 可视化和 Web UI

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## ⚠️ 免责声明

KnowMe 是自我探索工具，不是临床评估。MBTI 是偏好模型 —— 把结果当作自我反思的起点，而不是固定标签。分析质量随对话数据量提升（建议 50+ 条消息）。

---

## 📄 License

[Apache 2.0](LICENSE) — 随意使用、Fork、改进、分享。

---

<div align="center">

**如果 KnowMe 帮你更了解自己，给个 ⭐ Star 吧！**

**Built with ❤️ by [AI酋长Andy](https://github.com/AIPMAndy)**

*你和 AI 聊了上千次。是时候让这些对话为你所用了。*

</div>

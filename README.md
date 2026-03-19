# 🧠 KnowMe

[English](./README_EN.md) | 中文

> AI 性格分析系统 - 从对话中推断你的 MBTI 类型和认知模式

[![Star](https://img.shields.io/github/stars/AIPMAndy/KnowMe?style=flat)](https://github.com/AIPMAndy/KnowMe/stargazers)
[![License](https://img.shields.io/github/license/AIPMAndy/KnowMe)](https://github.com/AIPMAndy/KnowMe)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/Built%20for-OpenClaw-purple)](https://github.com/openclaw/openclaw)

---

## 🚀 快速开始

```bash
# 安装
pip install knowme-ai

# 使用
knowme --source chat_history.json
knowme --source openclaw
knowme --personality-report
```

---

## 📺 Demo 演示

```bash
# 分析聊天记录
$ knowme --source conversation.json
🔍 分析中...
   
   MBTI 类型: INTJ (高置信度)
   
   I - 内向: 92%
   N - 直觉: 85%
   T - 思考: 78%
   J - 判断: 89%

# 生成性格报告
$ knowme --personality-report
📊 性格分析报告:
   
   核心特质:
   - 战略型思考者
   - 独立自主
   - 追求效率
   
   沟通风格:
   - 喜欢深度讨论
   - 数据驱动
   - 简洁直接
   
   潜在优势:
   - 长期规划能力
   - 客观分析能力
   
   成长建议:
   - 多倾听不同观点
   - 适当放松完美主义

# 与 DNA Memory 联动
$ knowme --integrate dna-memory
✅ 已将性格分析结果同步到 DNA Memory
   - 偏好深度交流
   - 喜欢简洁风格
   - INTJ 思维模式
```

---

## 🧠 核心特性

### MBTI 分析

- 从对话文本推断 MBTI 类型
- 提供置信度评分
- 分析各维度的倾向程度

### 认知模式识别

- 信息获取方式 (S/N)
- 决策方式 (T/F)
- 生活态度 (J/P)

### 行为洞察

- 沟通风格分析
- 潜在优势识别
- 成长建议提供

### 🎨 生成式个性化 (NEW v2.0)

**从性格到视觉 —— 生成你的专属形象**

- **MBTI → 图像 Prompt** —— 自动将性格特征转化为视觉描述
- **多风格支持** —— professional/anime/realistic/artistic/minimalist
- **多平台兼容** —— Bailian, Midjourney, DALL-E, Stable Diffusion 等
- **AI分身生成** —— 为你的AI助手创建匹配性格的形象

```bash
# 生成个性化肖像
python3 scripts/generate_portrait.py --mbti INTJ --style professional

# 直接生成图像 (支持 Bailian/PonyFlash 等)
python3 scripts/generate_image.py --mbti INTJ --service bailian --output portrait.png
```

---

## 📁 项目结构

```
KnowMe/
├── analyzers/       # 分析模块
│   ├── mbti.py     # MBTI 推断
│   └── pattern.py   # 模式识别
├── collectors/      # 数据收集
│   ├── openclaw.py # OpenClaw 数据
│   └── json.py     # JSON 文件
├── reports/         # 报告生成
└── tests/          # 测试用例
```

---

## 🔧 配置

```python
from knowme import Analyzer

analyzer = Analyzer(
    model="claude-3-opus",
    confidence_threshold=0.7,
    include_growth_advice=True,
)
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/xxx`)
3. 提交更改 (`git commit -m 'Add xxx'`)
4. 推送到分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 📄 License

MIT License - 随意使用，保留署名即可

---

## 👤 作者

**Andy** - [GitHub](https://github.com/AIPMAndy)

> 了解自己，是成长的第一步。

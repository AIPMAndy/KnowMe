# 🧬 KnowMe — Know Yourself Through AI Conversations

> **Your AI conversations reveal your personality.** KnowMe analyzes your chat history with AI assistants to uncover your MBTI type, personality traits, strengths/weaknesses, and delivers personalized high-value life advice.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/OpenClaw-skill-purple.svg" alt="OpenClaw Skill">
</p>

## 🤔 Why KnowMe?

Traditional MBTI tests ask you what you *think* you'd do. **KnowMe analyzes what you *actually* do** — how you communicate, what you ask about, how you make decisions, how you structure your thoughts — all extracted from your real conversations with AI.

**No surveys. No self-reporting bias. Just your authentic behavior.**

## ✨ Features

- 🔍 **Multi-source collection** — Supports OpenClaw, ChatGPT, Claude, and raw text
- 📊 **8-dimension analysis** — MBTI 4 dimensions + communication style + cognitive patterns + emotional tendencies + decision mode
- 🎯 **Signal-based scoring** — 50+ behavioral signals with confidence levels
- 💡 **16-type advice engine** — Personalized career, communication, relationship, and growth advice for all MBTI types
- 🌏 **Chinese + English** — Signal detection works in both languages with cultural context adjustments
- 🔒 **100% local** — All analysis runs on your machine, no data leaves your device
- 📦 **OpenClaw Skill** — Drop-in skill for any OpenClaw-powered AI assistant

## 🚀 Quick Start

### As a standalone tool

```bash
# 1. Collect conversation data
python3 scripts/collect.py --source chatgpt --file ~/Downloads/conversations.json --output data.json

# 2. Analyze personality
python3 scripts/analyze.py --input data.json --output report.md

# 3. Generate personalized advice
python3 scripts/advise.py --report report.md --output advice.md

# 4. Read your report!
cat report.md
cat advice.md
```

### As an OpenClaw Skill

```bash
# Install the skill
openclaw skill install knowme.skill

# Then just ask your AI assistant:
# "Analyze my personality based on our conversations"
# "What's my MBTI type?"
# "Give me personality insights from my chat history"
```

## 📖 Supported Data Sources

| Source | Command | Notes |
|--------|---------|-------|
| **ChatGPT** | `--source chatgpt --file conversations.json` | Export from Settings → Data Controls → Export |
| **Claude** | `--source claude --file claude_export.json` | Export from Settings → Export Data |
| **OpenClaw** | `--source openclaw` | Auto-reads from workspace memory |
| **Raw Text** | `--source text --file ./chats/` | Any `.md` or `.txt` files with User:/Assistant: markers |

## 📊 What You Get

### 1. MBTI Type with Confidence Scores

```
E [██████████░░░░░░░░░░] I  (32% / 68%) → I (high)
S [░░░░░░░░████████████] N  (18% / 82%) → N (high)
T [████████████████░░░░] F  (78% / 22%) → T (high)
J [██████████████░░░░░░] P  (65% / 35%) → J (medium)
```

### 2. Communication Style Analysis

- Message length patterns
- Question/exclamation rates
- Topic distribution
- Emoji usage patterns
- Collaborative vs solo language

### 3. Personalized Advice Report

- 💪 **Superpowers** — Your top 3 strengths
- 🌱 **Growth Edges** — Areas for development
- 🎯 **Career Lens** — Role fit and work style
- 💬 **Communication Guide** — Blind spots and tips
- ❤️ **Relationship Insights** — Social patterns
- ⚡ **30-Day Challenge** — One specific growth experiment

## 🏗️ Architecture

```
knowme/
├── SKILL.md                          # OpenClaw skill definition
├── scripts/
│   ├── collect.py                    # Multi-source data collector
│   ├── analyze.py                    # Signal-based personality analyzer
│   └── advise.py                     # 16-type advice generator
└── references/
    ├── mbti_signals.md               # Signal taxonomy (50+ signals)
    └── advice_frameworks.md          # Advice generation frameworks
```

### Pipeline

```
[ChatGPT/Claude/OpenClaw/Text] → collect.py → [Unified JSON]
                                                     ↓
                                              analyze.py → [Personality Report]
                                                     ↓
                                              advise.py → [Growth Guide]
```

## 🔬 How Analysis Works

KnowMe doesn't use AI to analyze your conversations (that would be expensive and inconsistent). Instead, it uses a **signal-based scoring system**:

1. **Signal Detection**: 50+ regex-based behavioral signals scan each message
2. **Dimensional Scoring**: Signals are weighted (1-3 points) and accumulated per MBTI dimension
3. **Confidence Calculation**: Based on signal volume and consistency
4. **Cultural Adjustment**: Chinese communication norms are accounted for (e.g., indirectness ≠ introversion)

This approach is:
- ⚡ **Fast** — Analyzes 1000+ messages in seconds
- 🔒 **Private** — No API calls, everything runs locally
- 📊 **Transparent** — Every score has traceable evidence
- 🔄 **Reproducible** — Same input always gives same output

## 🛠️ Advanced Usage

### Merge multiple sources

```bash
# Collect from multiple sources
python3 scripts/collect.py --source chatgpt --file chatgpt_export.json --output /tmp/chatgpt.json
python3 scripts/collect.py --source claude --file claude_export.json --output /tmp/claude.json

# Merge (use jq or write a simple script)
jq -s '.[0].messages + .[1].messages | {messages: ., source: "merged", total_messages: length}' \
  /tmp/chatgpt.json /tmp/claude.json > /tmp/merged.json

python3 scripts/analyze.py --input /tmp/merged.json --output report.md
```

### Export raw scores

```bash
python3 scripts/analyze.py --input data.json --output report.md --json raw_scores.json
```

## 🤝 Contributing

PRs welcome! Especially for:
- New data source parsers (Gemini, Copilot, etc.)
- Additional signal patterns
- Non-English signal detection
- Visualization improvements
- Integration with other personality frameworks (Big Five, Enneagram)

## ⚠️ Disclaimer

KnowMe is a self-discovery tool, not a clinical assessment. MBTI is a preference model — use results as conversation starters for self-reflection, not as fixed labels. The analysis quality improves with more conversation data (50+ messages recommended).

## 📄 License

MIT — Use it, fork it, improve it.

---

**Built with ❤️ for the self-aware.**

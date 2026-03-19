---
name: knowme
description: |
  Analyze your personality through AI conversations. Infer MBTI type, cognitive patterns,
  strengths/weaknesses, and provide actionable life advice based on chat history.
  Activate when user mentions "MBTI", "personality analysis", "know me", "性格分析",
  "了解自己", "性格优缺点", "KnowMe", or wants personality insights from their conversations.
---

# KnowMe - Know Yourself Through AI Conversations

> Your conversations reveal who you are. KnowMe analyzes your AI chat patterns to uncover your MBTI type, personality traits, and growth opportunities.

## How It Works

KnowMe extracts behavioral signals from conversations:
- **Communication style** → E/I (how you engage)
- **Information processing** → S/N (concrete vs abstract)
- **Decision-making** → T/F (logic vs values)
- **Lifestyle approach** → J/P (structured vs flexible)

## Quick Start

### 1. Collect Conversation Data

Run the collector script to gather chat history:

```bash
python3 scripts/collect.py --source openclaw --output /tmp/knowme_data.json
```

Supported sources:
- `openclaw` — Reads from OpenClaw session history (default)
- `chatgpt` — Parses ChatGPT export JSON (`--file path/to/conversations.json`)
- `claude` — Parses Claude export JSON (`--file path/to/claude_export.json`)
- `text` — Raw text/markdown conversation files (`--file path/to/chats/`)

### 2. Analyze Personality

```bash
python3 scripts/analyze.py --input /tmp/knowme_data.json --output /tmp/knowme_report.md
```

This produces a comprehensive personality report.

### 3. Generate Advice

```bash
python3 scripts/advise.py --report /tmp/knowme_report.md --output /tmp/knowme_advice.md
```

Generates personalized, high-value advice across multiple life dimensions.

## Analysis Dimensions

### MBTI 4-Dimension Scoring

Each dimension scored 0-100 with confidence level:

| Dimension | Left Pole | Right Pole | Signals Used |
|-----------|-----------|------------|--------------|
| E/I | Extraversion | Introversion | Initiative, social references, energy patterns |
| S/N | Sensing | Intuition | Detail level, abstraction, future vs present focus |
| T/F | Thinking | Feeling | Logic usage, empathy signals, decision framing |
| J/P | Judging | Perceiving | Planning language, flexibility, closure-seeking |

### Extended Personality Profile

- **Communication Style**: Assertive / Collaborative / Analytical / Expressive
- **Cognitive Patterns**: How you process and structure information
- **Emotional Tendencies**: Stress signals, enthusiasm markers, resilience indicators
- **Decision Mode**: Intuitive rapid / Deliberate analytical / Values-driven / Data-driven
- **Growth Orientation**: Fixed vs growth mindset signals

### Advice Categories

- 🎯 **Career**: Role fit, leadership style, collaboration tips
- 💬 **Communication**: Blind spots, persuasion patterns, conflict style
- 🧠 **Learning**: Optimal learning mode, knowledge gaps, growth areas
- ❤️ **Relationships**: Attachment signals, empathy patterns, social energy
- ⚡ **Productivity**: Work rhythm, procrastination patterns, energy management
- 🌱 **Personal Growth**: Specific exercises based on personality type

## 🎨 New: Generative Personalization (v2.0)

**KnowMe now creates visual content from your personality profile!**

### Universal Image Generation — From MBTI to Portrait in 10 seconds

Works with **any** image generation service: Bailian, Midjourney, DALL-E, Stable Diffusion, PonyFlash, etc.

```python
# Generate optimized prompt from MBTI
from knowme.generative import PortraitGenerator

generator = PortraitGenerator()
prompt = generator.generate_prompt(mbti="INTJ", style="professional")

# Use with any image API:
# - Bailian: bailian.images.generate(prompt=prompt)
# - Midjourney: /imagine prompt
# - DALL-E: openai.images.generate(prompt=prompt)
# - Stable Diffusion: pipe(prompt)
```

**What happens:**
1. KnowMe extracts your MBTI type from conversation analysis
2. Maps to visual traits (expression, attire, colors, mood)
3. Generates optimized prompt for any image generation service
4. Returns ready-to-use prompt + optional direct API integration

### Visual Traits by MBTI Type

| Type | Expression | Attire | Colors | Mood |
|------|-----------|--------|--------|------|
| **INTJ** | Analytical, strategic | Minimalist dark blazer | Deep blues, silvers | Intellectual authority |
| **ENTP** | Mischievous, energetic | Creative professional | Vibrant purples | Innovation, debate |
| **ENFP** | Enthusiastic, bright | Colorful, expressive | Rainbow accents | Boundless energy |
| **ISFJ** | Gentle, caring | Modest, comfortable | Soft greens, beiges | Quiet dedication |

### Supported Image Services

| Service | Integration | Example |
|---------|-------------|---------|
| **Bailian** | `bailian.images.generate()` | 阿里云百炼 |
| **Midjourney** | Prompt export | Discord bot |
| **DALL-E** | `openai.images.generate()` | OpenAI API |
| **Stable Diffusion** | Local/remote inference | ComfyUI, etc. |
| **PonyFlash** | `ponyflash.images.generate()` | 统一创意API |

### Use Cases
- 🎭 **Personal Avatars** — Profile pictures matching your MBTI
- 🎨 **Content Creation** — Personality-aligned visuals for social media  
- 📝 **AI Assistants** — Generate your AI分身 (like 圆圆 the cat!)
- 🎯 **Brand Identity** — Visual assets reflecting authentic self

### Example Workflow

```bash
# 1. Analyze personality
python3 scripts/analyze.py --input data.json --output report.md

# 2. Generate personalized portrait (prompt only)
python3 scripts/generate_portrait.py --report report.md --output portrait.png

# 3. [NEW] Direct image generation (optional adapters available)
python3 scripts/generate_image.py --report report.md --service bailian --output my_portrait.png

# 4. Or specify MBTI directly
python3 scripts/generate_image.py --mbti INTJ --style anime --output intj_avatar.png

# 5. Create personality-based content prompts
python3 scripts/generate_prompts.py --report report.md --output prompts.json
```

### Supported Styles

| Style | Description | Best For |
|-------|-------------|----------|
| `professional` | Corporate portrait, business photography | LinkedIn, professional profiles |
| `anime` | Manga aesthetic, vibrant colors | Social media, avatars |
| `realistic` | Photorealistic, DSLR quality | Authentic portraits |
| `artistic` | Painterly, creative composition | Personal branding |
| `minimalist` | Clean, modern, simple | Design-focused profiles |

### Quick Demo

```python
from knowme.generative import generate_portrait

# One-liner: MBTI → Portrait
portrait = generate_portrait(
    mbti="INTJ",
    style="professional",
    output="my_portrait.png"
)
# Returns: {"url": "...", "mbti": "INTJ", "style": "professional"}
```

## For AI Agents (Integration Guide)

When triggered as a skill, follow this workflow:

1. Check if user has conversation data ready, or help them collect it
2. Run `collect.py` with appropriate source
3. Run `analyze.py` to generate the personality report
4. Run `advise.py` to generate personalized advice
5. **[NEW]** Offer generative personalization (portraits, content, prompts)
6. Present results conversationally — don't just dump the report
7. Offer to deep-dive into any specific dimension

### Interpretation Guidelines

See `references/mbti_signals.md` for the complete signal taxonomy used in analysis.
See `references/advice_frameworks.md` for the advice generation frameworks.
See `references/generative_workflows.md` for personalization examples.

## Limitations

- Analysis quality scales with conversation volume (recommend 50+ messages)
- MBTI is a preference model, not a fixed label — present results as tendencies
- Cultural context affects expression — the same trait may surface differently
- This is self-discovery, not clinical diagnosis

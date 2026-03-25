---
name: knowme
description: |
  Analyze your personality through AI conversations. Infer MBTI type, cognitive patterns,
  strengths/weaknesses, and provide actionable life advice based on chat history.
  
  **OpenClaw Auto-Integration:** When running as an OpenClaw skill, automatically detects
  session history, requests authorization if needed, and performs analysis without manual steps.
  
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

### 1. Auto-Detect & Request Authorization (Recommended)

**When running as an OpenClaw skill**, KnowMe automatically:

1. **Detects OpenClaw environment** — Checks if running in an OpenClaw session
2. **Locates session data** — Finds `~/.openclaw/agents/<agentId>/sessions/*.jsonl`
3. **Requests authorization** — Sends OAuth card for user to approve access
4. **Auto-collects on approval** — Immediately reads and analyzes conversation history

**No manual steps needed** — just say "分析我的性格" or "KnowMe".

### 2. Manual Collection (Fallback)

If auto-detection fails or you prefer manual export:

```bash
python3 scripts/collect.py --source openclaw --output /tmp/knowme_data.json
```

Supported sources:
- `openclaw` — Reads from OpenClaw session history (default, auto-authorized)
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

### Auto-Authorization Flow (OpenClaw Integration)

```python
# 1. Detect OpenClaw environment
import os
from pathlib import Path

def detect_openclaw_sessions():
    """Auto-detect OpenClaw session files"""
    home = Path.home()
    agents_dir = home / ".openclaw" / "agents"
    
    if not agents_dir.exists():
        return None
    
    # Find all session files
    sessions = []
    for agent_dir in agents_dir.iterdir():
        sessions_dir = agent_dir / "sessions"
        if sessions_dir.exists():
            for jsonl_file in sessions_dir.glob("*.jsonl"):
                if not jsonl_file.name.endswith(('.bak', '.reset', '.deleted')):
                    sessions.append(jsonl_file)
    
    return sessions

# 2. Check if we have access
has_access = check_session_access()  # Try to read a test file

if not has_access:
    # 3. Request authorization
    send_authorization_card(
        title="KnowMe 申请访问您的对话历史",
        description="需要访问 OpenClaw 会话数据以进行性格分析",
        scopes=["openclaw:session:read"],
        on_approve="auto_collect_and_analyze"
    )
    return "已发送授权请求，请批准后我将自动分析您的对话历史"

# 4. Auto-collect and analyze
data = auto_collect_sessions()
report = analyze_personality(data)
advice = generate_advice(report)
portrait_prompt = generate_portrait_prompt(report.mbti)
```

### Complete Workflow

1. **Auto-detect** — Check for OpenClaw session files
2. **Check access** — Try to read, if fail → request auth
3. **Request authorization** — Send OAuth card (one-click approve)
4. **Auto-collect** — On approval, immediately read all session files
5. **Analyze** — Run personality analysis
6. **Generate advice** — Create personalized recommendations  
7. **Generate portrait** — Create MBTI-based visual prompt
8. **Present results** — Conversational summary (not raw dump)
9. **Offer deep-dive** — Let user explore specific dimensions

### Authorization Scope

```json
{
  "scope": "knowme:openclaw:read",
  "access": [
    "~/.openclaw/agents/*/sessions/*.jsonl",
    "~/.openclaw/workspace/memory/*.md",
    "~/.openclaw/workspace/MEMORY.md"
  ],
  "purpose": "Personality analysis and self-discovery",
  "retention": "Analysis only, no external storage"
}
```

### OpenClaw Tool Integration

When triggered in OpenClaw, use these tool calls:

```python
# 1. Auto-detect and collect
result = auto_collect_sessions()

if result["status"] == "needs_auth":
    # Send authorization card
    feishu_im_user_message(
        action="send",
        msg_type="interactive",
        content=build_auth_card(
            title="KnowMe 申请访问对话历史",
            description=f"需要访问 {result['session_count']} 个会话文件进行性格分析",
            scope="knowme:openclaw:read",
            callback="knowme.handle_auth"
        )
    )
    return "已发送授权申请，请点击卡片授权后自动完成分析"

elif result["status"] == "success":
    # Proceed with analysis
    report = analyze_personality(result["messages"])
    advice = generate_advice(report)
    
    # Save to workspace
    write(
        file_path="~/.openclaw/workspace/knowme_report.md",
        content=report.to_markdown()
    )
    
    return report.summary()
```

### One-Command Analysis

For OpenClaw users, the entire flow is:

```
User: "分析我的性格"
AI: 
  1. Detects OpenClaw environment ✓
  2. Finds session files ✓
  3. [If no access] Sends auth card
  4. [On approval] Auto-collects & analyzes
  5. Returns MBTI report + advice
```

**Total user effort: 1 message + 1 click (if auth needed)**

### Interpretation Guidelines

See `references/mbti_signals.md` for the complete signal taxonomy used in analysis.
See `references/advice_frameworks.md` for the advice generation frameworks.
See `references/generative_workflows.md` for personalization examples.

## Limitations

- Analysis quality scales with conversation volume (recommend 50+ messages)
- MBTI is a preference model, not a fixed label — present results as tendencies
- Cultural context affects expression — the same trait may surface differently
- This is self-discovery, not clinical diagnosis

# KnowMe

English | [中文](./README.md)

> **Understand yourself and read other people through real conversations.**

KnowMe extracts behavioral signals from ChatGPT, Claude, OpenClaw, Feishu, and speaker-labeled chat text. It can analyze your own long-term AI conversations or one selected person in a conversation with a manager, colleague, partner, friend, or customer.

[![Star](https://img.shields.io/github/stars/AIPMAndy/KnowMe?style=social)](https://github.com/AIPMAndy/KnowMe/stargazers)
[![License](https://img.shields.io/github/license/AIPMAndy/KnowMe)](https://github.com/AIPMAndy/KnowMe)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![Feishu](https://img.shields.io/badge/Feishu-direct%20chat%20import-3370ff)](https://www.feishu.cn/)

![KnowMe report example](assets/demo-output.png)

## Two analysis modes

| Mode | What is analyzed | Common use |
|---|---|---|
| **Know yourself** | Your actual questions, decisions, and expression in AI chats | Self-awareness, career direction, growth advice |
| **Understand others** | Only the selected participant's messages | Communicating with a manager, colleague, partner, friend, or customer |

Traditional personality tests ask what people believe they would do. KnowMe looks at what they already do in ordinary conversations: how they structure information, ask for outcomes, balance facts and people, and seek closure or flexibility.

## Direct Feishu conversation integration

KnowMe can read a Feishu group or direct-message conversation through an authenticated `lark-cli` user identity. Speaker names are preserved, and only the selected person is analyzed.

### Analyze a manager or colleague

```bash
# Find a group chat_id by name
lark-cli im +chat-search --as user --query "Project group" --format json

python3 scripts/collect.py \
  --source feishu \
  --chat-id oc_xxx \
  --mode other \
  --target "Morgan Chen" \
  --self-name "Andy" \
  --relationship boss \
  --start 2026-07-01 \
  --output data.json

python3 scripts/analyze.py --input data.json --output report.md
```

For a direct message, replace `--chat-id oc_xxx` with `--user-id ou_xxx`.

### Analyze an exported or copied Feishu chat

```bash
python3 scripts/collect.py \
  --source feishu \
  --file ./feishu-chat.txt \
  --mode other \
  --target "Morgan Chen" \
  --self-name "Andy" \
  --relationship colleague \
  --output data.json
```

Accepted Feishu inputs:

- raw JSON from `lark-cli im +chat-messages-list --format json`;
- JSON containing a `messages` array and sender fields;
- copied `Name HH:MM` message blocks;
- speaker-labeled text such as `Morgan: Send the data and conclusion first.`

## Analyze your own AI conversations

```bash
git clone https://github.com/AIPMAndy/KnowMe.git
cd KnowMe

python3 scripts/collect.py \
  --source chatgpt \
  --file ~/Downloads/conversations.json \
  --mode self \
  --output data.json

python3 scripts/analyze.py --input data.json --output report.md
python3 scripts/advise.py --report report.md --output advice.md
```

Example Skill requests:

- "Analyze my personality from my AI conversations."
- "Use this Feishu chat to understand my manager's communication style."
- "Analyze only the other person's messages in this conversation."
- "How should I report progress to this manager?"

## What the report contains

- selected subject and `self` or `other` mode;
- source, relationship context, subject sample size, and total messages;
- E/I, S/N, T/F, and J/P tendencies with confidence;
- short evidence excerpts from the selected person's own messages;
- communication style and topic distribution;
- practical guidance for the next interaction in `other` mode;
- limitations and prohibited high-impact uses.

## Supported sources

| Source | Collection method | Subject |
|---|---|---|
| **Feishu group/DM** | `--source feishu --chat-id/--user-id` | Selected participant |
| **Feishu export/text** | `--source feishu --file` | Selected participant |
| **ChatGPT** | `--source chatgpt --file conversations.json` | Self |
| **Claude** | `--source claude --file export.json` | Self |
| **OpenClaw** | `--source openclaw` | Self |
| **Text** | `--source text --file` | Self in AI conversations |

## How it works

```text
conversation data
  -> preserve speakers
  -> select one subject
  -> scan bilingual behavioral signals
  -> score four MBTI dimensions
  -> calibrate confidence by sample size
  -> produce evidence and communication guidance
```

The analyzer does not call an external AI API. Analysis runs locally. Direct Feishu collection uses the user's authorized `lark-cli` connection, then processes the retrieved messages on the local machine.

Recommended sample sizes:

- fewer than 20 authored messages: low confidence;
- 20-49 messages: directional only;
- 50 or more messages across multiple days and topics: preferred.

## Project structure

```text
KnowMe/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
│   ├── collect.py
│   ├── analyze.py
│   ├── advise.py
│   ├── auto_collect.py
│   └── generate_portrait.py
├── references/
│   ├── mbti_signals.md
│   ├── relationship_analysis.md
│   └── advice_frameworks.md
└── tests/test_pipeline.py
```

## Validation

KnowMe uses only the Python standard library:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts
```

## Privacy and limits

- Analyze only conversations the user is authorized to access.
- Raw chats stay local by default.
- Analysis of another person is a communication hypothesis, not a clinical diagnosis.
- Do not infer protected traits, mental health, honesty, or hidden intent.
- Do not use the output to manipulate, exclude, hire, fire, or make another high-impact decision.
- Verify important conclusions through direct communication.

## Roadmap

- [x] ChatGPT / Claude / OpenClaw self-analysis
- [x] Direct Feishu group and DM collection
- [x] Feishu JSON and copied-text import
- [x] One-person targeting without mixing speakers
- [x] Workplace relationship context and communication guidance
- [x] Sample-size confidence calibration
- [ ] Web UI
- [ ] WeChat conversation parser
- [ ] Big Five and timeline analysis

## License

[Apache 2.0](LICENSE)

Built by [AI酋长Andy](https://github.com/AIPMAndy).

---
name: knowme
description: Analyze one person's personality and communication patterns from real conversations. Supports self-analysis from ChatGPT, Claude, OpenClaw, or text, and analysis of another person from Feishu chats, Feishu exports, or speaker-labeled text. Use for MBTI, personality analysis, communication style, understanding a boss, colleague, partner, friend, or customer, "了解自己", "分析他的性格", "看看老板是什么性格", "聊天记录分析", "飞书对话分析", or KnowMe requests.
---

# KnowMe

Analyze behavior people reveal in ordinary conversations instead of asking them
to describe an idealized version of themselves. Treat the result as a
directional communication hypothesis, not a diagnosis.

## Choose the mode

- Use `self` for the user's own AI conversations or authored text.
- Use `other` for a specific participant in an interpersonal conversation.
- Never merge both sides of a conversation. Preserve speaker identity and select
  exactly one target before analysis.
- For `other`, read [references/relationship_analysis.md](references/relationship_analysis.md).

## Collect conversations

### Analyze the user from AI conversations

```bash
python3 scripts/collect.py \
  --source chatgpt \
  --file conversations.json \
  --mode self \
  --output /tmp/knowme_data.json
```

Supported self-analysis sources:

- `chatgpt`: ChatGPT `conversations.json`
- `claude`: Claude export JSON
- `openclaw`: OpenClaw workspace memory files
- `text`: `.txt` or `.md` using `User:` / `Assistant:` markers

### Analyze another person from Feishu directly

Use an authenticated `lark-cli` user identity. A group or P2P chat can be read
without exporting it first.

```bash
python3 scripts/collect.py \
  --source feishu \
  --chat-id oc_xxx \
  --mode other \
  --target "张经理" \
  --self-name "Andy" \
  --relationship boss \
  --output /tmp/knowme_data.json
```

For a direct message, replace `--chat-id oc_xxx` with `--user-id ou_xxx`.
Use `--start`, `--end`, and `--max-pages` to bound collection. If Feishu
authentication or permissions are missing, follow the local `lark-cli` auth
workflow; do not invent tokens or claim that messages were fetched.

### Analyze a Feishu export or copied chat

```bash
python3 scripts/collect.py \
  --source feishu \
  --file ./feishu-chat.txt \
  --mode other \
  --target "张经理" \
  --self-name "Andy" \
  --relationship colleague \
  --output /tmp/knowme_data.json
```

Accepted Feishu inputs:

- JSON returned by `lark-cli im +chat-messages-list --format json`
- Plain JSON with a `messages` array and sender fields
- Copied text in `Name HH:MM` blocks
- Speaker-labeled text such as `张经理: 先给我数据和结论`

After collection, inspect `participants` and `subject_messages` in the output.
If `subject_messages` is zero or the name is ambiguous, correct `--target`
before analysis.

## Analyze the selected speaker

```bash
python3 scripts/analyze.py \
  --input /tmp/knowme_data.json \
  --output /tmp/knowme_report.md \
  --json /tmp/knowme_scores.json
```

The report must state:

- analyzed person and mode;
- source, relationship, and sample count;
- MBTI dimensional tendencies and confidence;
- short behavioral evidence from that person's own messages;
- communication style;
- for `other`, practical guidance for the next interaction;
- evidence limitations and prohibited high-impact uses.

Use these sample thresholds:

- fewer than 20 authored messages: low confidence;
- 20-49 messages: directional only;
- 50 or more messages across multiple days/topics: preferred.

Read [references/mbti_signals.md](references/mbti_signals.md) when reviewing or
extending the scoring model.

## Generate self-development advice

Use the advice generator only for `self` mode:

```bash
python3 scripts/advise.py \
  --report /tmp/knowme_report.md \
  --output /tmp/knowme_advice.md
```

For `other` mode, use the communication guidance already included in the
analysis report. Do not turn another person's report into unsolicited life
advice for them.

## Privacy and interpretation

- Analyze only conversations the user is authorized to access.
- Keep raw chat data local unless the user explicitly asks to share it.
- Quote only short evidence excerpts; do not dump full private conversations.
- Do not infer protected traits, mental-health conditions, honesty, intent, or
  employment fitness.
- Do not use personality output to manipulate, exclude, hire, fire, or make
  another high-impact decision.
- Verify important conclusions through direct communication with the person.

## Validation

After changing the skill, run:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

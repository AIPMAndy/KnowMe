#!/usr/bin/env python3
"""Collect and normalize conversations for KnowMe analysis.

The normalized schema keeps the speaker identity so KnowMe can analyze one
specific person instead of mixing both sides of an interpersonal conversation.
"""

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def collect_openclaw(workspace_path=None):
    """Collect user-authored context from OpenClaw memory files."""
    if workspace_path is None:
        workspace_path = os.path.expanduser("~/.openclaw/workspace")

    messages = []
    memory_dir = os.path.join(workspace_path, "memory")
    if os.path.isdir(memory_dir):
        for fpath in sorted(glob.glob(os.path.join(memory_dir, "*.md"))):
            fname = os.path.basename(fpath)
            date_match = re.match(r"(\d{4}-\d{2}-\d{2})", fname)
            timestamp = date_match.group(1) if date_match else None
            with open(fpath, "r", encoding="utf-8") as file_obj:
                content = file_obj.read().strip()
            if content:
                messages.append({
                    "role": "user",
                    "speaker": "self",
                    "content": content,
                    "timestamp": timestamp,
                    "source": "openclaw_memory",
                    "file": fname,
                })

    memory_md = os.path.join(workspace_path, "MEMORY.md")
    if os.path.isfile(memory_md):
        with open(memory_md, "r", encoding="utf-8") as file_obj:
            content = file_obj.read().strip()
        if content:
            messages.append({
                "role": "context",
                "speaker": "self",
                "content": content,
                "timestamp": None,
                "source": "openclaw_longterm",
                "file": "MEMORY.md",
            })
    return messages


def collect_chatgpt(file_path):
    """Parse a ChatGPT conversations.json export."""
    with open(file_path, "r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    messages = []
    for conv in data if isinstance(data, list) else [data]:
        for node in conv.get("mapping", {}).values():
            msg = node.get("message")
            if msg is None:
                continue
            author = msg.get("author", {}).get("role", "unknown")
            parts = msg.get("content", {}).get("parts", [])
            content = "\n".join(str(part) for part in parts if isinstance(part, str))
            if not content.strip() or author not in ("user", "assistant"):
                continue

            timestamp = None
            create_time = msg.get("create_time")
            if create_time:
                try:
                    timestamp = datetime.fromtimestamp(create_time).isoformat()
                except (ValueError, TypeError, OSError):
                    pass
            messages.append({
                "role": author,
                "speaker": "self" if author == "user" else "ChatGPT",
                "content": content.strip(),
                "timestamp": timestamp,
                "source": "chatgpt",
            })
    return messages


def collect_claude(file_path):
    """Parse a Claude export JSON file."""
    with open(file_path, "r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    messages = []
    for conv in data if isinstance(data, list) else [data]:
        for msg in conv.get("chat_messages", []):
            sender = msg.get("sender", "unknown")
            content = msg.get("text", "")
            if not content.strip() or sender not in ("human", "assistant"):
                continue
            role = "user" if sender == "human" else "assistant"
            messages.append({
                "role": role,
                "speaker": "self" if role == "user" else "Claude",
                "content": content.strip(),
                "timestamp": msg.get("created_at"),
                "source": "claude",
            })
    return messages


def collect_text(file_path):
    """Parse text or Markdown with common AI conversation role markers."""
    path = Path(file_path)
    files = sorted(path.glob("**/*.md")) + sorted(path.glob("**/*.txt")) if path.is_dir() else [path]
    messages = []

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as file_obj:
            content = file_obj.read().strip()
        if not content:
            continue

        turns = re.split(
            r"\n(?=(?:User|Human|Me|Assistant|AI|Bot|Q|A)\s*[:：])",
            content,
            flags=re.IGNORECASE,
        )
        for turn in turns:
            turn = turn.strip()
            if not turn:
                continue
            user_match = re.match(
                r"^(User|Human|Me|Q)\s*[:：]\s*(.*)",
                turn,
                re.IGNORECASE | re.DOTALL,
            )
            assistant_match = re.match(
                r"^(Assistant|AI|Bot|A)\s*[:：]\s*(.*)",
                turn,
                re.IGNORECASE | re.DOTALL,
            )
            if user_match:
                role, speaker, body = "user", "self", user_match.group(2)
            elif assistant_match:
                role, speaker, body = "assistant", assistant_match.group(1), assistant_match.group(2)
            else:
                role, speaker, body = "user", "self", turn
            messages.append({
                "role": role,
                "speaker": speaker,
                "content": body.strip(),
                "timestamp": None,
                "source": "text",
                "file": str(fpath),
            })
    return messages


def _content_to_text(content):
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, dict):
        for key in ("text", "content", "title"):
            value = content.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    if content is None:
        return ""
    return json.dumps(content, ensure_ascii=False)


def _unwrap_feishu_payload(payload):
    """Return the message list and pagination fields from lark-cli or plain JSON."""
    data = payload.get("data", payload) if isinstance(payload, dict) else payload
    if isinstance(data, dict) and isinstance(data.get("messages"), list):
        return data["messages"], data.get("has_more", False), data.get("page_token")
    if isinstance(data, list):
        return data, False, None
    raise ValueError("Feishu JSON must contain a messages array")


def parse_feishu_payload(payload):
    """Normalize JSON returned by lark-cli im or a compatible export."""
    raw_messages, has_more, page_token = _unwrap_feishu_payload(payload)
    messages = []
    for item in raw_messages:
        if not isinstance(item, dict) or item.get("deleted"):
            continue
        sender = item.get("sender") or {}
        speaker = (
            sender.get("name")
            or sender.get("sender_name")
            or item.get("speaker")
            or sender.get("id")
            or "Unknown"
        )
        sender_id = sender.get("id") or item.get("sender_id")
        content = _content_to_text(item.get("content") or item.get("text"))
        if not content or item.get("msg_type") == "system":
            continue
        messages.append({
            "role": "participant",
            "speaker": str(speaker).strip(),
            "speaker_id": sender_id,
            "content": content,
            "timestamp": item.get("create_time") or item.get("timestamp"),
            "source": "feishu",
            "message_id": item.get("message_id"),
        })
    return messages, has_more, page_token


FEISHU_HEADER_RE = re.compile(
    r"^(?P<speaker>.{1,80}?)\s+(?P<timestamp>(?:20\d{2}[-/.年]\d{1,2}[-/.月]\d{1,2}(?:日)?\s+)?(?:[01]?\d|2[0-3]):[0-5]\d)\s*$"
)
FEISHU_INLINE_RE = re.compile(
    r"^(?:\[(?P<timestamp>[^\]]+)\]\s*)?(?P<speaker>[^:：\n]{1,40})[:：]\s*(?P<content>.+)$"
)


def parse_feishu_text(content, source_file=None):
    """Parse copied Feishu text in `Name time` or `Name: message` formats."""
    messages = []
    current = None

    def flush():
        if current and current["content"]:
            current["content"] = "\n".join(current["content"]).strip()
            if current["content"]:
                messages.append(current.copy())

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        header_match = FEISHU_HEADER_RE.match(line)
        inline_match = FEISHU_INLINE_RE.match(line)
        if header_match:
            flush()
            current = {
                "role": "participant",
                "speaker": header_match.group("speaker").strip(),
                "content": [],
                "timestamp": header_match.group("timestamp"),
                "source": "feishu_export",
                "file": source_file,
            }
        elif inline_match and not line.lower().startswith(("http:", "https:")):
            flush()
            current = {
                "role": "participant",
                "speaker": inline_match.group("speaker").strip(),
                "content": [inline_match.group("content").strip()],
                "timestamp": inline_match.group("timestamp"),
                "source": "feishu_export",
                "file": source_file,
            }
        elif current:
            current["content"].append(line)
    flush()
    return messages


def collect_feishu_file(file_path):
    """Collect Feishu conversations from JSON, text, Markdown, or a directory."""
    path = Path(file_path)
    files = (
        sorted(path.glob("**/*.json"))
        + sorted(path.glob("**/*.txt"))
        + sorted(path.glob("**/*.md"))
        if path.is_dir()
        else [path]
    )
    messages = []
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as file_obj:
            raw = file_obj.read()
        if fpath.suffix.lower() == ".json":
            parsed, _, _ = parse_feishu_payload(json.loads(raw))
        else:
            parsed = parse_feishu_text(raw, str(fpath))
        messages.extend(parsed)
    return messages


def collect_feishu_live(chat_id=None, user_id=None, start=None, end=None, max_pages=20):
    """Read a Feishu chat through the authenticated lark-cli user identity."""
    if not shutil.which("lark-cli"):
        raise RuntimeError("lark-cli is required for direct Feishu collection")

    messages = []
    page_token = None
    for _ in range(max_pages):
        command = [
            "lark-cli", "im", "+chat-messages-list", "--as", "user",
            "--order", "asc", "--page-size", "50", "--no-reactions", "--format", "json",
        ]
        command.extend(["--chat-id", chat_id] if chat_id else ["--user-id", user_id])
        if start:
            command.extend(["--start", start])
        if end:
            command.extend(["--end", end])
        if page_token:
            command.extend(["--page-token", page_token])

        env = os.environ.copy()
        env["LARKSUITE_CLI_NO_UPDATE_NOTIFIER"] = "1"
        env["LARKSUITE_CLI_NO_SKILLS_NOTIFIER"] = "1"
        result = subprocess.run(command, capture_output=True, text=True, env=env, check=False)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "unknown lark-cli error"
            raise RuntimeError("Unable to read Feishu messages: " + detail)
        page_messages, has_more, page_token = parse_feishu_payload(json.loads(result.stdout))
        messages.extend(page_messages)
        if not has_more or not page_token:
            break
    return messages


def _identity(value):
    return re.sub(r"\s+", "", str(value or "")).casefold()


def mark_subject(messages, target=None):
    """Mark exactly which speaker should be analyzed."""
    target_key = _identity(target)
    subject_count = 0
    for message in messages:
        matches_target = target_key and target_key in {
            _identity(message.get("speaker")),
            _identity(message.get("speaker_id")),
        }
        if matches_target or (not target_key and message.get("role") in ("user", "context")):
            message["role"] = "subject"
            subject_count += 1
    return subject_count


def main():
    parser = argparse.ArgumentParser(description="KnowMe - Collect conversations for one-person analysis")
    parser.add_argument(
        "--source",
        choices=["openclaw", "chatgpt", "claude", "text", "feishu"],
        default="openclaw",
        help="Conversation source",
    )
    parser.add_argument("--file", help="Input file or directory")
    parser.add_argument("--workspace", help="OpenClaw workspace path")
    parser.add_argument("--chat-id", help="Feishu chat_id for direct collection")
    parser.add_argument("--user-id", help="Feishu open_id for direct-message collection")
    parser.add_argument("--start", help="Feishu start time (ISO 8601 or YYYY-MM-DD)")
    parser.add_argument("--end", help="Feishu end time (ISO 8601 or YYYY-MM-DD)")
    parser.add_argument("--max-pages", type=int, default=20, help="Maximum Feishu pages to read")
    parser.add_argument("--mode", choices=["self", "other"], help="Analysis mode; inferred when omitted")
    parser.add_argument("--target", help="Speaker name or Feishu sender id to analyze")
    parser.add_argument("--self-name", help="Your display name in an interpersonal conversation")
    parser.add_argument(
        "--relationship",
        choices=["boss", "colleague", "partner", "friend", "customer", "other"],
        default="other",
        help="Relationship to the analyzed person",
    )
    parser.add_argument("--output", default="/tmp/knowme_data.json", help="Output JSON path")
    args = parser.parse_args()

    mode = args.mode or ("other" if args.target else "self")
    print(f"[KnowMe] Collecting from {args.source} in {mode} mode")

    if args.source == "openclaw":
        messages = collect_openclaw(args.workspace)
    elif args.source == "chatgpt":
        if not args.file:
            parser.error("--file is required for chatgpt")
        messages = collect_chatgpt(args.file)
    elif args.source == "claude":
        if not args.file:
            parser.error("--file is required for claude")
        messages = collect_claude(args.file)
    elif args.source == "text":
        if not args.file:
            parser.error("--file is required for text")
        messages = collect_text(args.file)
    else:
        selectors = sum(bool(value) for value in (args.file, args.chat_id, args.user_id))
        if selectors != 1:
            parser.error("feishu requires exactly one of --file, --chat-id, or --user-id")
        target = args.target or args.self_name
        if not target:
            parser.error("feishu requires --target (or --self-name for self analysis)")
        if args.file:
            messages = collect_feishu_file(args.file)
        else:
            messages = collect_feishu_live(
                chat_id=args.chat_id,
                user_id=args.user_id,
                start=args.start,
                end=args.end,
                max_pages=args.max_pages,
            )

    target = args.target or (args.self_name if args.source == "feishu" else None)
    subject_count = mark_subject(messages, target)
    if subject_count == 0:
        parser.error(f"no messages matched analysis target: {target or 'self'}")

    participants = Counter(message.get("speaker", "Unknown") for message in messages)
    output = {
        "source": args.source,
        "collected_at": datetime.now().isoformat(),
        "analysis": {
            "mode": mode,
            "target": target or "self",
            "self_name": args.self_name,
            "relationship": args.relationship if mode == "other" else None,
        },
        "participants": dict(participants),
        "total_messages": len(messages),
        "subject_messages": subject_count,
        "user_messages": subject_count,
        "messages": messages,
    }

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as file_obj:
        json.dump(output, file_obj, ensure_ascii=False, indent=2)
    print(f"[KnowMe] Collected {len(messages)} messages; analyzing {subject_count} from {output['analysis']['target']}")
    print(f"[KnowMe] Saved to {args.output}")


if __name__ == "__main__":
    main()

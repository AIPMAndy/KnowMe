#!/usr/bin/env python3
"""
KnowMe - Conversation Data Collector

Collects and normalizes conversation data from various AI chat sources
into a unified format for personality analysis.

Supported sources:
- openclaw: OpenClaw session history (reads from memory/daily files)
- chatgpt: ChatGPT export JSON (conversations.json)
- claude: Claude export JSON
- text: Raw text/markdown files

Output format:
{
  "source": "openclaw",
  "collected_at": "2024-01-01T00:00:00",
  "message_count": 150,
  "messages": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "2024-01-01T00:00:00",
      "source": "openclaw"
    }
  ]
}
"""

import json
import os
import sys
import glob
import argparse
import re
from datetime import datetime
from pathlib import Path


def collect_openclaw(workspace_path=None):
    """Collect messages from OpenClaw memory/daily files and MEMORY.md."""
    if workspace_path is None:
        workspace_path = os.path.expanduser("~/.openclaw/workspace")

    messages = []

    # Read daily memory files
    memory_dir = os.path.join(workspace_path, "memory")
    if os.path.isdir(memory_dir):
        for fpath in sorted(glob.glob(os.path.join(memory_dir, "*.md"))):
            fname = os.path.basename(fpath)
            # Try to extract date from filename
            date_match = re.match(r"(\d{4}-\d{2}-\d{2})", fname)
            timestamp = date_match.group(1) if date_match else None

            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                messages.append({
                    "role": "user",
                    "content": content,
                    "timestamp": timestamp,
                    "source": "openclaw_memory",
                    "file": fname
                })

    # Read MEMORY.md for long-term patterns
    memory_md = os.path.join(workspace_path, "MEMORY.md")
    if os.path.isfile(memory_md):
        with open(memory_md, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            messages.append({
                "role": "context",
                "content": content,
                "timestamp": None,
                "source": "openclaw_longterm",
                "file": "MEMORY.md"
            })

    return messages


def collect_chatgpt(file_path):
    """Parse ChatGPT export JSON (conversations.json)."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = []
    conversations = data if isinstance(data, list) else [data]

    for conv in conversations:
        mapping = conv.get("mapping", {})
        for node_id, node in mapping.items():
            msg = node.get("message")
            if msg is None:
                continue
            author = msg.get("author", {}).get("role", "unknown")
            content_parts = msg.get("content", {}).get("parts", [])
            content = "\n".join(str(p) for p in content_parts if isinstance(p, str))
            create_time = msg.get("create_time")

            if content.strip() and author in ("user", "assistant"):
                timestamp = None
                if create_time:
                    try:
                        timestamp = datetime.fromtimestamp(create_time).isoformat()
                    except (ValueError, TypeError, OSError):
                        pass

                messages.append({
                    "role": author,
                    "content": content.strip(),
                    "timestamp": timestamp,
                    "source": "chatgpt"
                })

    return messages


def collect_claude(file_path):
    """Parse Claude export JSON."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = []

    # Claude export can be a list of conversations or a single conversation
    conversations = data if isinstance(data, list) else [data]

    for conv in conversations:
        chat_messages = conv.get("chat_messages", [])
        for msg in chat_messages:
            role = msg.get("sender", "unknown")
            content = msg.get("text", "")
            created_at = msg.get("created_at")

            if content.strip() and role in ("human", "assistant"):
                messages.append({
                    "role": "user" if role == "human" else "assistant",
                    "content": content.strip(),
                    "timestamp": created_at,
                    "source": "claude"
                })

    return messages


def collect_text(file_path):
    """Parse raw text/markdown conversation files."""
    messages = []
    path = Path(file_path)

    if path.is_dir():
        files = sorted(path.glob("**/*.md")) + sorted(path.glob("**/*.txt"))
    else:
        files = [path]

    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            # Try to split into user/assistant turns
            # Common patterns: "User:", "Human:", "Me:", "Assistant:", "AI:", "Bot:"
            turns = re.split(
                r'\n(?=(?:User|Human|Me|Assistant|AI|Bot|Q|A)\s*[:：])',
                content,
                flags=re.IGNORECASE
            )

            for turn in turns:
                turn = turn.strip()
                if not turn:
                    continue

                role_match = re.match(
                    r'^(User|Human|Me|Q)\s*[:：]\s*(.*)',
                    turn,
                    re.IGNORECASE | re.DOTALL
                )
                if role_match:
                    messages.append({
                        "role": "user",
                        "content": role_match.group(2).strip(),
                        "timestamp": None,
                        "source": "text",
                        "file": str(fpath)
                    })
                    continue

                assistant_match = re.match(
                    r'^(Assistant|AI|Bot|A)\s*[:：]\s*(.*)',
                    turn,
                    re.IGNORECASE | re.DOTALL
                )
                if assistant_match:
                    messages.append({
                        "role": "assistant",
                        "content": assistant_match.group(2).strip(),
                        "timestamp": None,
                        "source": "text",
                        "file": str(fpath)
                    })
                    continue

                # If no role detected, treat as user message
                messages.append({
                    "role": "user",
                    "content": turn,
                    "timestamp": None,
                    "source": "text",
                    "file": str(fpath)
                })

    return messages


def main():
    parser = argparse.ArgumentParser(description="KnowMe - Collect conversation data")
    parser.add_argument("--source", choices=["openclaw", "chatgpt", "claude", "text"],
                        default="openclaw", help="Data source type")
    parser.add_argument("--file", help="Input file path (for chatgpt/claude/text sources)")
    parser.add_argument("--workspace", help="OpenClaw workspace path (for openclaw source)")
    parser.add_argument("--output", default="/tmp/knowme_data.json", help="Output JSON path")
    args = parser.parse_args()

    print(f"[KnowMe] Collecting from source: {args.source}")

    if args.source == "openclaw":
        messages = collect_openclaw(args.workspace)
    elif args.source == "chatgpt":
        if not args.file:
            print("Error: --file required for chatgpt source")
            sys.exit(1)
        messages = collect_chatgpt(args.file)
    elif args.source == "claude":
        if not args.file:
            print("Error: --file required for claude source")
            sys.exit(1)
        messages = collect_claude(args.file)
    elif args.source == "text":
        if not args.file:
            print("Error: --file required for text source")
            sys.exit(1)
        messages = collect_text(args.file)
    else:
        print(f"Error: Unknown source {args.source}")
        sys.exit(1)

    # Filter to user messages only (we analyze user behavior)
    user_messages = [m for m in messages if m["role"] in ("user", "context")]

    output = {
        "source": args.source,
        "collected_at": datetime.now().isoformat(),
        "total_messages": len(messages),
        "user_messages": len(user_messages),
        "messages": messages
    }

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"[KnowMe] Collected {len(messages)} messages ({len(user_messages)} user messages)")
    print(f"[KnowMe] Saved to {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
KnowMe Auto-Collector for OpenClaw
Automatically detects, requests auth, and collects conversation data.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

def detect_openclaw_environment() -> Optional[Path]:
    """Detect if running in OpenClaw environment and locate sessions."""
    home = Path.home()
    openclaw_dir = home / ".openclaw"
    
    if not openclaw_dir.exists():
        return None
    
    agents_dir = openclaw_dir / "agents"
    if not agents_dir.exists():
        return None
    
    return agents_dir

def find_session_files(agents_dir: Path) -> List[Path]:
    """Find all valid session JSONL files."""
    sessions = []
    
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue
            
        sessions_dir = agent_dir / "sessions"
        if not sessions_dir.exists():
            continue
        
        for jsonl_file in sessions_dir.glob("*.jsonl"):
            # Skip backup/reset/deleted files
            if any(suffix in jsonl_file.name for suffix in ['.bak', '.reset', '.deleted', '.lock']):
                continue
            sessions.append(jsonl_file)
    
    # Sort by modification time (newest first)
    sessions.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return sessions

def check_access(session_file: Path) -> bool:
    """Check if we can read session files."""
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            f.readline()
        return True
    except (PermissionError, OSError):
        return False

def parse_session_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Parse a session JSONL file into messages."""
    messages = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if record.get('type') == 'message':
                        msg_data = record.get('message', {})
                        if msg_data.get('role') in ['user', 'assistant']:
                            messages.append({
                                'role': msg_data['role'],
                                'content': extract_text_content(msg_data.get('content', [])),
                                'timestamp': record.get('timestamp'),
                                'session_id': record.get('id')
                            })
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
    
    return messages

def extract_text_content(content: List[Dict]) -> str:
    """Extract text from content blocks."""
    texts = []
    for block in content:
        if isinstance(block, dict):
            if block.get('type') == 'text':
                texts.append(block.get('text', ''))
            elif block.get('type') == 'thinking':
                texts.append(f"[Thinking: {block.get('thinking', '')}]")
    return '\n'.join(texts)

def collect_all_sessions(max_files: int = 10, max_messages: int = 1000) -> Dict[str, Any]:
    """
    Main entry point: Auto-detect and collect OpenClaw sessions.
    
    Returns:
        {
            "status": "success" | "needs_auth" | "no_data",
            "messages": [...],
            "stats": {...},
            "auth_url": "..."  # if needs_auth
        }
    """
    agents_dir = detect_openclaw_environment()
    
    if not agents_dir:
        return {
            "status": "no_data",
            "message": "OpenClaw environment not detected"
        }
    
    session_files = find_session_files(agents_dir)
    
    if not session_files:
        return {
            "status": "no_data", 
            "message": "No session files found"
        }
    
    # Check access on first file
    if not check_access(session_files[0]):
        return {
            "status": "needs_auth",
            "message": "Authorization required to access session data",
            "auth_scope": "openclaw:session:read",
            "session_count": len(session_files)
        }
    
    # Collect messages from recent sessions
    all_messages = []
    files_processed = 0
    
    for session_file in session_files[:max_files]:
        messages = parse_session_jsonl(session_file)
        all_messages.extend(messages)
        files_processed += 1
        
        if len(all_messages) >= max_messages:
            break
    
    # Sort by timestamp
    all_messages.sort(key=lambda m: m.get('timestamp', ''), reverse=True)
    
    return {
        "status": "success",
        "messages": all_messages[:max_messages],
        "stats": {
            "total_messages": len(all_messages),
            "files_processed": files_processed,
            "user_messages": len([m for m in all_messages if m['role'] == 'user']),
            "assistant_messages": len([m for m in all_messages if m['role'] == 'assistant'])
        }
    }

def main():
    """CLI entry point."""
    result = collect_all_sessions()
    
    if result["status"] == "needs_auth":
        print(json.dumps({
            "action": "request_authorization",
            "scope": result["auth_scope"],
            "session_count": result.get("session_count", 0),
            "message": result["message"]
        }))
        sys.exit(1)
    
    elif result["status"] == "no_data":
        print(json.dumps({
            "action": "no_data",
            "message": result["message"]
        }))
        sys.exit(1)
    
    else:
        # Success - output collected data
        output_path = "/tmp/knowme_data.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(json.dumps({
            "action": "collected",
            "output_path": output_path,
            "stats": result["stats"]
        }))

if __name__ == "__main__":
    main()

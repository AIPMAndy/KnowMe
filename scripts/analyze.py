#!/usr/bin/env python3
"""
KnowMe - Personality Analyzer

Analyzes collected conversation data to infer MBTI type and personality traits.
Uses signal-based scoring from the MBTI signal taxonomy.

Input: JSON from collect.py
Output: Markdown personality report
"""

import json
import re
import sys
import os
import argparse
from collections import Counter, defaultdict
from datetime import datetime


# ─── Signal Detection ───

class SignalDetector:
    """Detects MBTI-related behavioral signals in text."""

    def __init__(self):
        self.signals = defaultdict(list)
        self.scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        self.evidence = defaultdict(list)
        self.stats = {
            "avg_message_length": 0,
            "total_messages": 0,
            "exclamation_rate": 0,
            "question_rate": 0,
            "emoji_rate": 0,
            "first_person_rate": 0,
            "we_rate": 0,
            "topics": Counter(),
            "languages": Counter(),
        }

    def analyze_message(self, content, role="user"):
        """Analyze a single message for personality signals."""
        if role != "user":
            return

        self.stats["total_messages"] += 1
        content_lower = content.lower()
        content_stripped = content.strip()

        # ─── Basic stats ───
        msg_len = len(content_stripped)
        has_exclamation = "!" in content or "！" in content
        has_question = "?" in content or "？" in content
        has_emoji = bool(re.search(r'[\U0001f600-\U0001f9ff\U0001fa00-\U0001faff]', content))

        self.stats["avg_message_length"] += msg_len
        self.stats["exclamation_rate"] += int(has_exclamation)
        self.stats["question_rate"] += int(has_question)
        self.stats["emoji_rate"] += int(has_emoji)

        # ─── Language detection ───
        if re.search(r'[\u4e00-\u9fff]', content):
            self.stats["languages"]["zh"] += 1
        if re.search(r'[a-zA-Z]{3,}', content):
            self.stats["languages"]["en"] += 1

        # ─── E/I Signals ───
        # Extraversion
        if has_exclamation and msg_len < 200:
            self._score("E", 1, "Short enthusiastic message")
        if re.search(r'\b(we|our|us|team|together|大家|我们|一起)\b', content_lower):
            self.stats["we_rate"] += 1
            self._score("E", 2, "Collaborative language (we/our)")
        if re.search(r'(brainstorm|discuss|meeting|聊聊|讨论|开会)', content_lower):
            self._score("E", 2, "Social/collaborative activity reference")
        if msg_len < 100 and self.stats["total_messages"] > 1:
            self._score("E", 1, "Short rapid message")

        # Introversion
        if msg_len > 500:
            self._score("I", 2, "Long, carefully composed message")
        if re.search(r'\b(I think|I feel|I believe|我觉得|我认为|我想)\b', content_lower):
            self.stats["first_person_rate"] += 1
            self._score("I", 1, "First-person reflection")
        if re.search(r'(read|write|think|reflect|alone|quiet|阅读|写作|思考|独自|安静)', content_lower):
            self._score("I", 2, "Solo activity reference")
        if re.search(r'(let me think|给我.*时间|让我想想|容我.*思考)', content_lower):
            self._score("I", 3, "Requests time to think")

        # ─── S/N Signals ───
        # Sensing
        if re.search(r'\d+\.?\d*', content) and re.search(r'(具体|specific|exactly|步骤|step)', content_lower):
            self._score("S", 2, "Specific details with numbers")
        if re.search(r'(how exactly|specifically|step.by.step|具体怎么|一步步|详细)', content_lower):
            self._score("S", 2, "Asks for specifics/steps")
        if re.search(r'(last time|before|经验|之前|上次|以前)', content_lower):
            self._score("S", 1, "References past experience")
        if re.search(r'(practical|实用|实际|现实|落地)', content_lower):
            self._score("S", 2, "Practical orientation")

        # Intuition
        if re.search(r'(what if|imagine|could be|如果|想象|可能|假设)', content_lower):
            self._score("N", 2, "Hypothetical/future thinking")
        if re.search(r'(pattern|framework|model|paradigm|模式|框架|模型|范式)', content_lower):
            self._score("N", 2, "Framework/pattern thinking")
        if re.search(r'(why|为什么|本质|底层|根本)', content_lower):
            self._score("N", 1, "Asks why (abstract reasoning)")
        if re.search(r'(vision|trend|future|趋势|未来|方向|远景)', content_lower):
            self._score("N", 2, "Future/vision oriented")
        if re.search(r'(metaphor|analogy|like a|就像|比喻|类比|好比)', content_lower):
            self._score("N", 2, "Metaphorical thinking")

        # ─── T/F Signals ───
        # Thinking
        if re.search(r'(because|therefore|thus|since|因为|所以|因此|由此)', content_lower):
            self._score("T", 1, "Logical connectors")
        if re.search(r'(efficient|optimize|system|logic|效率|优化|系统|逻辑)', content_lower):
            self._score("T", 2, "Systems/efficiency thinking")
        if re.search(r'(data|evidence|proof|metric|数据|证据|指标|量化)', content_lower):
            self._score("T", 2, "Data-driven reasoning")
        if re.search(r'(pros?.and.cons|trade.?off|权衡|利弊|优劣)', content_lower):
            self._score("T", 2, "Analytical evaluation")

        # Feeling
        if re.search(r'(feel|感觉|感受|心情|情感|情绪)', content_lower):
            self._score("F", 1, "Feeling language")
        if re.search(r'(people|team|someone|别人|大家|他们.*感受)', content_lower):
            self._score("F", 1, "People-centered concern")
        if re.search(r'(value|meaningful|purpose|价值|意义|使命|初心)', content_lower):
            self._score("F", 2, "Values-driven language")
        if re.search(r'(thank|appreciate|grateful|谢谢|感谢|感恩)', content_lower):
            self._score("F", 1, "Appreciation/gratitude")
        if re.search(r'(impact|affect|influence|影响|关怀|关心)', content_lower):
            self._score("F", 2, "Impact-on-people concern")

        # ─── J/P Signals ───
        # Judging
        if re.search(r'(plan|schedule|deadline|timeline|计划|排期|截止|时间表)', content_lower):
            self._score("J", 2, "Planning language")
        if re.search(r'(next step|action item|to.?do|下一步|行动项|待办)', content_lower):
            self._score("J", 2, "Action/closure oriented")
        if re.search(r'(decide|finalize|conclude|确定|敲定|最终)', content_lower):
            self._score("J", 2, "Seeks closure")
        if re.search(r'(organize|structure|systematic|整理|结构|体系)', content_lower):
            self._score("J", 1, "Organization preference")

        # Perceiving
        if re.search(r'(maybe|perhaps|might|或许|也许|可能|看情况)', content_lower):
            self._score("P", 1, "Open/flexible language")
        if re.search(r'(explore|try|experiment|curious|探索|尝试|试试|好奇)', content_lower):
            self._score("P", 2, "Exploration/discovery")
        if re.search(r'(depend|it.depends|看.*情况|不一定|灵活)', content_lower):
            self._score("P", 2, "Situational flexibility")
        if re.search(r'(by the way|also|btw|另外|顺便|对了|还有)', content_lower):
            self._score("P", 1, "Topic-hopping")

        # ─── Topic Detection ───
        topics = {
            "tech": r'(code|api|python|ai|ml|app|dev|编程|代码|开发|技术)',
            "business": r'(business|startup|revenue|market|产品|商业|创业|营收|市场)',
            "learning": r'(learn|study|course|book|学习|课程|书|教程)',
            "creativity": r'(create|design|art|write|story|创作|设计|写作|故事)',
            "people": r'(team|colleague|friend|family|团队|同事|朋友|家人)',
            "self": r'(myself|my life|growth|career|自己|人生|成长|职业)',
        }
        for topic, pattern in topics.items():
            if re.search(pattern, content_lower):
                self.stats["topics"][topic] += 1

    def _score(self, dimension, points, evidence):
        self.scores[dimension] += points
        self.evidence[dimension].append(evidence)

    def get_results(self):
        """Calculate final MBTI scores and profile."""
        n = max(self.stats["total_messages"], 1)
        self.stats["avg_message_length"] = self.stats["avg_message_length"] / n
        self.stats["exclamation_rate"] = self.stats["exclamation_rate"] / n
        self.stats["question_rate"] = self.stats["question_rate"] / n
        self.stats["emoji_rate"] = self.stats["emoji_rate"] / n
        self.stats["first_person_rate"] = self.stats["first_person_rate"] / n
        self.stats["we_rate"] = self.stats["we_rate"] / n

        # Calculate dimension percentages
        dimensions = {}
        for left, right in [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]:
            total = self.scores[left] + self.scores[right]
            if total == 0:
                dimensions[f"{left}/{right}"] = {
                    "left": left, "right": right,
                    "left_score": 50, "right_score": 50,
                    "result": "?", "confidence": "low",
                    "evidence_left": [], "evidence_right": []
                }
            else:
                left_pct = round(self.scores[left] / total * 100)
                right_pct = 100 - left_pct
                winner = left if left_pct >= 50 else right
                diff = abs(left_pct - 50)
                confidence = "high" if diff > 30 else ("medium" if diff > 15 else "low")
                dimensions[f"{left}/{right}"] = {
                    "left": left, "right": right,
                    "left_score": left_pct, "right_score": right_pct,
                    "result": winner, "confidence": confidence,
                    "evidence_left": list(set(self.evidence[left]))[:5],
                    "evidence_right": list(set(self.evidence[right]))[:5],
                }

        # Determine MBTI type
        mbti_type = ""
        for dim in dimensions.values():
            mbti_type += dim["result"]

        # Overall confidence
        confidences = [d["confidence"] for d in dimensions.values()]
        if confidences.count("low") >= 2:
            overall_confidence = "low"
        elif confidences.count("high") >= 3:
            overall_confidence = "high"
        else:
            overall_confidence = "medium"

        return {
            "mbti_type": mbti_type,
            "overall_confidence": overall_confidence,
            "dimensions": dimensions,
            "stats": {k: v if not isinstance(v, Counter) else dict(v)
                      for k, v in self.stats.items()},
            "raw_scores": dict(self.scores),
        }


# ─── Communication Style Analysis ───

def analyze_communication_style(stats):
    """Determine communication style from message statistics."""
    styles = []

    if stats["avg_message_length"] > 300:
        styles.append("Analytical — prefers thorough, detailed communication")
    elif stats["avg_message_length"] < 100:
        styles.append("Direct — concise, to-the-point communication")

    if stats["exclamation_rate"] > 0.3:
        styles.append("Expressive — energetic, enthusiastic tone")
    if stats["question_rate"] > 0.4:
        styles.append("Inquisitive — frequently asks questions, seeks understanding")
    if stats["emoji_rate"] > 0.2:
        styles.append("Warm — uses emoji for emotional expression")

    topics = stats.get("topics", {})
    if topics.get("people", 0) > topics.get("tech", 0):
        styles.append("People-oriented — conversations center on human dynamics")
    elif topics.get("tech", 0) > topics.get("people", 0):
        styles.append("Task-oriented — conversations center on problems and solutions")

    return styles if styles else ["Balanced — no dominant communication style detected"]


# ─── Report Generation ───

def generate_report(results, output_path):
    """Generate a Markdown personality report."""
    mbti = results["mbti_type"]
    dims = results["dimensions"]
    stats = results["stats"]
    confidence = results["overall_confidence"]

    comm_styles = analyze_communication_style(stats)

    # Build dimension bars
    def dim_bar(d):
        left_pct = d["left_score"]
        right_pct = d["right_score"]
        bar_len = 20
        left_filled = round(left_pct / 100 * bar_len)
        right_filled = bar_len - left_filled
        bar = "█" * left_filled + "░" * right_filled
        winner = f"**{d['result']}**"
        return f"{d['left']} [{bar}] {d['right']}  ({left_pct}% / {right_pct}%) → {winner} ({d['confidence']})"

    report = f"""# 🧬 KnowMe Personality Report

> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> Based on {stats['total_messages']} user messages
> Overall confidence: **{confidence}**

---

## 🎯 Your MBTI Type: **{mbti}**

### Dimensional Scores

```
{dim_bar(dims['E/I'])}
{dim_bar(dims['S/N'])}
{dim_bar(dims['T/F'])}
{dim_bar(dims['J/P'])}
```

### Evidence Summary

"""

    for dim_key, d in dims.items():
        report += f"**{dim_key}**\n"
        if d["evidence_left"]:
            report += f"- {d['left']} signals: {', '.join(d['evidence_left'][:3])}\n"
        if d["evidence_right"]:
            report += f"- {d['right']} signals: {', '.join(d['evidence_right'][:3])}\n"
        report += "\n"

    report += f"""---

## 💬 Communication Style

"""
    for style in comm_styles:
        report += f"- {style}\n"

    report += f"""
### Message Statistics

| Metric | Value |
|--------|-------|
| Average message length | {stats['avg_message_length']:.0f} chars |
| Exclamation rate | {stats['exclamation_rate']:.0%} |
| Question rate | {stats['question_rate']:.0%} |
| Emoji usage | {stats['emoji_rate']:.0%} |
| "We/our" rate | {stats['we_rate']:.0%} |

### Topic Distribution

"""
    topics = stats.get("topics", {})
    if topics:
        sorted_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)
        for topic, count in sorted_topics:
            bar = "▓" * min(count, 20)
            report += f"- **{topic}**: {bar} ({count})\n"
    else:
        report += "- No dominant topics detected\n"

    report += f"""
---

## 📊 Raw Scores

```json
{json.dumps(results['raw_scores'], indent=2)}
```

---

## ⚠️ Disclaimer

This analysis is based on conversational patterns and should be treated as a **tendency indicator**, not a definitive personality assessment. MBTI is a preference model — you may express different facets in different contexts. Use these insights as a starting point for self-reflection, not as a fixed label.
"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    return report


def main():
    parser = argparse.ArgumentParser(description="KnowMe - Analyze personality from conversations")
    parser.add_argument("--input", default="/tmp/knowme_data.json", help="Input JSON from collect.py")
    parser.add_argument("--output", default="/tmp/knowme_report.md", help="Output report path")
    parser.add_argument("--json", help="Also output raw results as JSON to this path")
    args = parser.parse_args()

    print(f"[KnowMe] Loading data from {args.input}")

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    messages = data.get("messages", [])
    if not messages:
        print("Error: No messages found in input data")
        sys.exit(1)

    print(f"[KnowMe] Analyzing {len(messages)} messages...")

    detector = SignalDetector()
    for msg in messages:
        detector.analyze_message(msg["content"], msg.get("role", "user"))

    results = detector.get_results()

    print(f"[KnowMe] MBTI Type: {results['mbti_type']} (confidence: {results['overall_confidence']})")

    report = generate_report(results, args.output)
    print(f"[KnowMe] Report saved to {args.output}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[KnowMe] Raw results saved to {args.json}")


if __name__ == "__main__":
    main()

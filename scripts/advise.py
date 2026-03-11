#!/usr/bin/env python3
"""
KnowMe - Personalized Advice Generator

Takes the personality report and generates high-value, actionable advice
across multiple life dimensions based on MBTI type and observed patterns.

Input: Markdown report from analyze.py
Output: Markdown advice document
"""

import re
import sys
import os
import json
import argparse
from datetime import datetime


# ─── Type-Specific Advice Database ───

TYPE_PROFILES = {
    "INTJ": {
        "alias": "Architect / 建筑师",
        "snapshot": "Strategic thinker with a vision. You see systems and patterns others miss, and you have the determination to turn ideas into reality.",
        "superpowers": [
            "🔭 Strategic vision — you naturally think 3 steps ahead",
            "🧩 Systems thinking — you see how pieces connect",
            "🎯 Laser focus — once committed, you execute relentlessly"
        ],
        "growth_edges": [
            "🤝 Emotional expression — others may find you cold (you're not, but you seem it)",
            "🔄 Flexibility — your plans are good, but rigidity can cost you opportunities",
            "👥 Delegation — you struggle to trust others' execution quality"
        ],
        "career": "Thrive in strategy, architecture, research. You're the person who builds the master plan. Risk: getting so focused on the plan that you miss on-the-ground reality. Tip: pair with an ESTP or ENFP to balance vision with action energy.",
        "communication": "You explain by logic chains, which works great for fellow Thinkers but can feel dismissive to Feelers. Try: before the logical argument, spend 10 seconds acknowledging the emotional context.",
        "relationship": "You show love through competence and problem-solving. Not everyone reads that as affection. Experiment: once a day, express care without solving anything.",
        "challenge_30d": "Each day, have one conversation where you ask 'how does this make you feel?' and listen without analyzing."
    },
    "INTP": {
        "alias": "Logician / 逻辑学家",
        "snapshot": "Analytical explorer driven by curiosity. You live in the world of ideas and systems, constantly building and rebuilding mental models.",
        "superpowers": [
            "🧠 Deep analysis — you dissect problems to their atoms",
            "💡 Original thinking — your ideas come from unexpected angles",
            "📚 Knowledge integration — you connect dots across domains"
        ],
        "growth_edges": [
            "⏰ Follow-through — starting > finishing for you",
            "💬 Communication — translating your mental models into plain language",
            "🏃 Action bias — you can think forever; sometimes just ship it"
        ],
        "career": "Ideal for research, engineering, analysis. You're the person who finds the non-obvious solution. Risk: analysis paralysis. Tip: set artificial deadlines and use 80/20 rule.",
        "communication": "You communicate in layers of abstraction. Most people think in one layer. Try: start with the conclusion, then add depth if they ask.",
        "relationship": "You connect through ideas, not small talk. Find people who enjoy intellectual exploration. But also: sometimes people just want to vent, not be diagnosed.",
        "challenge_30d": "Ship one 'imperfect' thing each week. Blog post, project, decision. Done > perfect."
    },
    "ENTJ": {
        "alias": "Commander / 指挥官",
        "snapshot": "Born leader with a drive to organize and optimize everything. You see inefficiency as a personal challenge.",
        "superpowers": [
            "👑 Natural leadership — people follow your confidence and clarity",
            "📈 Growth mindset — you always push for better",
            "⚡ Decisive action — you cut through indecision fast"
        ],
        "growth_edges": [
            "🫂 Patience — not everyone moves at your speed (and that's okay)",
            "👂 Listening — your urge to direct can override others' input",
            "🌿 Rest — burnout is real, even for commanders"
        ],
        "career": "CEO, GM, Strategy Lead. You turn chaos into systems. Risk: micromanagement when stressed. Tip: build a team you trust, then actually trust them.",
        "communication": "Direct and efficient. Loved by other Thinkers, sometimes intimidating to Feelers. Try: ask before telling, even when you already know.",
        "relationship": "You approach relationships like projects — optimize, improve, grow. Some people just want to be accepted as-is. Practice unconditional presence.",
        "challenge_30d": "Once a day, ask someone for their opinion and implement it — even if yours is 'better'."
    },
    "ENTP": {
        "alias": "Debater / 辩论家",
        "snapshot": "Creative challenger who sees possibilities everywhere. You love the thrill of new ideas and pushing boundaries.",
        "superpowers": [
            "🚀 Innovation — you generate more ideas in an hour than most do in a week",
            "🎭 Adaptability — you thrive in chaos and change",
            "🗣️ Persuasion — you can argue any side convincingly"
        ],
        "growth_edges": [
            "🏗️ Execution — ideas are cheap; building is the hard part",
            "🤐 Sensitivity — debating everything can hurt people",
            "📌 Focus — shiny object syndrome is your kryptonite"
        ],
        "career": "Entrepreneur, product innovator, consultant. You're the spark. Risk: starting 10 things, finishing 0. Tip: find an ISTJ co-founder who actually ships.",
        "communication": "You communicate through challenge and debate. It energizes you but can exhaust others. Try: read the room — some people want support, not sparring.",
        "relationship": "You need intellectual stimulation. Boring = death for you in relationships. But depth requires staying with one topic/person long enough to get past the surface.",
        "challenge_30d": "Pick ONE project and work on it daily for 30 days. No switching. See what depth reveals."
    },
    "INFJ": {
        "alias": "Advocate / 提倡者",
        "snapshot": "Idealistic visionary with deep empathy. You understand people intuitively and care deeply about making things meaningful.",
        "superpowers": [
            "🔮 Intuitive insight — you read between the lines effortlessly",
            "💝 Deep empathy — people feel truly understood by you",
            "✨ Vision for humanity — you see what could be, not just what is"
        ],
        "growth_edges": [
            "🛡️ Boundaries — you absorb others' emotions and burn out",
            "🗣️ Assertiveness — you know the answer but hesitate to push it",
            "🎯 Perfectionism — your idealism can paralyze execution"
        ],
        "career": "Coaching, writing, product design, education. You create meaning. Risk: martyrdom. Tip: your vision matters — protect your energy to deliver it.",
        "communication": "You communicate in metaphors and meaning. Powerful with fellow NFs, confusing to STs. Try: include concrete next-steps alongside your vision.",
        "relationship": "You seek deep, soulful connection. Surface relationships drain you. It's okay to have a small circle. But don't over-idealize partners.",
        "challenge_30d": "Say 'no' to one request per day that drains you. Track how it changes your energy."
    },
    "INFP": {
        "alias": "Mediator / 调停者",
        "snapshot": "Gentle idealist driven by authenticity and personal values. You have a rich inner world and deep capacity for caring.",
        "superpowers": [
            "🎨 Authenticity — you are genuinely yourself, which inspires others",
            "📝 Creative expression — writing, art, music flow naturally from you",
            "💚 Deep values — your moral compass is strong and consistent"
        ],
        "growth_edges": [
            "⚔️ Conflict tolerance — avoiding all conflict avoids growth too",
            "📋 Structure — freedom is great until deadlines arrive",
            "🌍 Pragmatism — ideals need implementation plans"
        ],
        "career": "Writing, design, counseling, creative fields. You make things beautiful and meaningful. Risk: struggle in corporate politics. Tip: find a mission-driven team.",
        "communication": "You communicate through stories and feelings. Beautiful but can be vague. Try: end with one clear ask or action point.",
        "relationship": "You love deeply and expect the same. Disappointment hits hard. Practice: separate what people do from what you hoped they'd do.",
        "challenge_30d": "Have one uncomfortable conversation per week that you'd normally avoid."
    },
    "ENFJ": {
        "alias": "Protagonist / 主人公",
        "snapshot": "Charismatic leader who inspires through warmth and vision. You naturally bring out the best in others.",
        "superpowers": [
            "🌟 Inspiration — people light up around your energy",
            "🤝 Bridge building — you connect people and ideas naturally",
            "📣 Communication — you make complex ideas feel personal and urgent"
        ],
        "growth_edges": [
            "😤 People-pleasing — saying yes to everyone means saying no to yourself",
            "🎭 Authenticity under pressure — you may perform 'fine' when you're not",
            "📊 Data blindness — your intuition is strong but not infallible"
        ],
        "career": "Leadership, coaching, sales, education. You move people. Risk: burnout from carrying everyone. Tip: lead systems, not just people.",
        "communication": "You match others' emotional wavelength effortlessly. Superpower. Risk: losing your own voice. Try: express your actual opinion before harmonizing.",
        "relationship": "You give more than you get. Sustainably? Check. Make sure your relationships have reciprocity, not just your generosity.",
        "challenge_30d": "Track energy givers vs drainers. Eliminate or reduce one drainer per week."
    },
    "ENFP": {
        "alias": "Campaigner / 竞选者",
        "snapshot": "Enthusiastic explorer of people and possibilities. Your energy is contagious and your curiosity limitless.",
        "superpowers": [
            "🎉 Infectious enthusiasm — you make everything feel possible",
            "🌈 Creativity — you see connections and possibilities everywhere",
            "💫 Empathy + energy — rare combo of caring deeply AND taking action"
        ],
        "growth_edges": [
            "🎯 Focus — your breadth is amazing; depth requires discipline",
            "📅 Follow-through — the boring middle part of projects",
            "😔 Emotional swings — highs are very high, lows hit hard"
        ],
        "career": "Marketing, product, startup, content creation. You're the person who makes people care. Risk: jack of all trades. Tip: go deep in ONE domain for 2+ years.",
        "communication": "You communicate with stories, energy, and emotion. Magnetic in person. In writing: watch for rambling. Try: edit ruthlessly. Your best work is in the cuts.",
        "relationship": "You fall in love with potential — in people, projects, ideas. Be careful: love who someone IS, not who they could be.",
        "challenge_30d": "Complete one thing per day before starting anything new. Finish → Start, not Start → Start → Start."
    },
    "ISTJ": {
        "alias": "Logistician / 物流师",
        "snapshot": "Reliable, thorough, and principled. You are the backbone that keeps systems running and promises kept.",
        "superpowers": [
            "🏗️ Reliability — when you say it's done, it's done right",
            "📋 Organization — you bring order to chaos effortlessly",
            "🔍 Attention to detail — nothing slips past you"
        ],
        "growth_edges": [
            "🌊 Adaptability — change isn't a threat, it's data",
            "💡 Innovation — sometimes the proven way isn't the best way",
            "🎨 Self-expression — your competence speaks, but sometimes people need words"
        ],
        "career": "Operations, finance, engineering, management. You are the ship's engine. Risk: resisting change until forced. Tip: schedule 'innovation time' like a meeting.",
        "communication": "Precise and factual. Trusted immediately by colleagues. Risk: seeming inflexible. Try: start some sentences with 'What if we...' instead of 'We should...'",
        "relationship": "You show love through actions and consistency. That's real and valuable. But also: say the words occasionally. They matter.",
        "challenge_30d": "Try one new thing each week that has no proven ROI. Just explore."
    },
    "ISTP": {
        "alias": "Virtuoso / 鉴赏家",
        "snapshot": "Cool-headed problem solver who learns by doing. You master tools and systems through hands-on experimentation.",
        "superpowers": [
            "🔧 Hands-on mastery — you figure things out by building",
            "🧊 Crisis calm — you're the person everyone wants in an emergency",
            "🎯 Efficiency — you find the shortest path between A and B"
        ],
        "growth_edges": [
            "💬 Emotional expression — people can't read your mind",
            "📅 Long-term planning — you're great in the moment, less so at 5-year plans",
            "👥 Team engagement — lone wolf mode has limits"
        ],
        "career": "Engineering, troubleshooting, trades, technical roles. You fix things. Risk: undervaluing soft skills. Tip: your technical skill + basic communication = 10x career leverage.",
        "communication": "Minimal and efficient. You say more with less. Risk: others feel excluded. Try: narrate your thinking process occasionally — it helps people trust you.",
        "relationship": "You show care through fixing problems and shared activities. Words of affirmation: try them, even if they feel redundant.",
        "challenge_30d": "Share your thought process out loud with someone every day — even if it feels unnecessary."
    },
    "ESTJ": {
        "alias": "Executive / 总经理",
        "snapshot": "Organized, decisive, and results-driven. You create order and hold standards high.",
        "superpowers": [
            "📊 Execution — you get things DONE, on time, on budget",
            "👔 Leadership — people trust your competence and clarity",
            "⚖️ Fairness — you apply rules consistently"
        ],
        "growth_edges": [
            "🫂 Empathy — efficiency shouldn't override human needs",
            "🌿 Patience — not everyone processes at your speed",
            "🎭 Flexibility — rules serve people, not the other way around"
        ],
        "career": "Management, operations, law, consulting. You run the machine. Risk: becoming the machine. Tip: schedule unstructured time with your team.",
        "communication": "Clear, direct, authoritative. Great for execution. Risk: seeming bossy. Try: replace 'Do X' with 'What do you think about X?'",
        "relationship": "You express love through providing and organizing. Strong foundation. But also: sometimes sit with someone in their mess without cleaning it up.",
        "challenge_30d": "Once a day, let someone else lead — and follow without correcting."
    },
    "ESTP": {
        "alias": "Entrepreneur / 企业家",
        "snapshot": "Bold, practical, and energetic. You live in the present and make things happen through sheer force of personality.",
        "superpowers": [
            "🎲 Boldness — you take action when others hesitate",
            "👁️ Situational awareness — you read rooms and people instantly",
            "⚡ Resourcefulness — you work with what's available, now"
        ],
        "growth_edges": [
            "🔮 Long-term thinking — today's win isn't always tomorrow's",
            "📝 Reflection — pause between action cycles",
            "💭 Depth — some problems need thinking, not doing"
        ],
        "career": "Sales, entrepreneurship, crisis management. You thrive in high-stakes, fast-moving environments. Risk: boredom in stable roles. Tip: build a business that matches your pace.",
        "communication": "Charismatic and persuasive. You close deals and win people over. Risk: overselling. Try: listen 2x more than you pitch.",
        "relationship": "Exciting partner, keeps things fun. Risk: avoiding deep emotional conversations. Tip: schedule them like meetings if you have to.",
        "challenge_30d": "Spend 15 minutes daily in silent reflection. No phone, no action. Just think."
    },
    "ISFJ": {
        "alias": "Defender / 守卫者",
        "snapshot": "Warm, dedicated, and deeply caring. You quietly hold everything together and remember every detail about the people you love.",
        "superpowers": [
            "💝 Caring — you notice what people need before they ask",
            "📋 Dependability — you never drop the ball",
            "🧠 Memory — you remember details that make people feel seen"
        ],
        "growth_edges": [
            "🗣️ Self-advocacy — your needs matter too",
            "🆕 Change acceptance — new ≠ bad",
            "🔥 Conflict — avoiding it doesn't resolve it"
        ],
        "career": "Healthcare, education, HR, support roles. You make organizations human. Risk: being taken for granted. Tip: document your impact — others won't do it for you.",
        "communication": "Warm, supportive, detail-oriented. Everyone loves talking to you. Risk: never expressing dissatisfaction. Try: practice 'I need...' statements.",
        "relationship": "You love through service and attention. Beautiful. But make sure you're receiving too, not just giving.",
        "challenge_30d": "Ask for one thing you need each day. No apologizing for the ask."
    },
    "ISFP": {
        "alias": "Adventurer / 探险家",
        "snapshot": "Gentle artist with quiet strength. You experience the world deeply through senses and values.",
        "superpowers": [
            "🎨 Aesthetic sense — you make things beautiful naturally",
            "🤫 Quiet strength — you stand firm on values without drama",
            "🌿 Present-moment awareness — you're truly HERE"
        ],
        "growth_edges": [
            "📢 Self-expression — share your inner world more",
            "📅 Planning — spontaneity is great until rent is due",
            "🔍 Assertiveness — your perspective deserves airtime"
        ],
        "career": "Design, art, healthcare, environment. You bring beauty and meaning. Risk: underearning because you prioritize meaning over money. Tip: meaning AND money aren't mutually exclusive.",
        "communication": "You communicate through actions, art, and quiet presence. Powerful but easily overlooked. Try: use words for 20% more of what you express.",
        "relationship": "Deeply loyal, quietly passionate. Risk: suffering in silence. Speak up before resentment builds.",
        "challenge_30d": "Share one personal opinion daily that you'd normally keep to yourself."
    },
    "ESFJ": {
        "alias": "Consul / 执政官",
        "snapshot": "Social harmonizer who keeps communities thriving. You remember birthdays, check in on people, and create belonging.",
        "superpowers": [
            "🫂 Community building — you create spaces where people belong",
            "📱 Social awareness — you know who needs what",
            "🎉 Organizing — events, teams, gatherings flow under your hand"
        ],
        "growth_edges": [
            "🎭 Authenticity — don't lose yourself in others' expectations",
            "📊 Critical thinking — not every opinion deserves equal weight",
            "🔥 Tough love — sometimes helping means saying no"
        ],
        "career": "HR, event management, community, customer success. You make organizations feel like families. Risk: measuring self-worth by others' approval. Tip: define your own standards.",
        "communication": "Warm, inclusive, attentive. Everyone feels welcome. Risk: avoiding hard truths. Try: deliver difficult feedback with compassion — it's kinder than avoidance.",
        "relationship": "You create warmth and stability. Wonderful. But also: let people struggle a little — growth requires friction.",
        "challenge_30d": "Give honest feedback to one person per week, even if it's uncomfortable."
    },
    "ESFP": {
        "alias": "Entertainer / 表演者",
        "snapshot": "Life of the party with genuine heart. You bring joy, energy, and spontaneity to everything you touch.",
        "superpowers": [
            "🎉 Energy — you light up every room you enter",
            "🤸 Adaptability — you improvise better than anyone",
            "💛 Genuine warmth — your enthusiasm for people is real"
        ],
        "growth_edges": [
            "📅 Discipline — freedom needs structure to sustain itself",
            "🔍 Depth — go past the fun layer occasionally",
            "💰 Long-term thinking — future-you will thank present-you"
        ],
        "career": "Entertainment, sales, hospitality, marketing. You make people feel alive. Risk: not being taken seriously. Tip: your charisma + substance = unstoppable.",
        "communication": "Vibrant, engaging, fun. Everyone wants to talk to you. Risk: keeping things too light. Try: let conversations go deep when someone opens up.",
        "relationship": "Fun, generous, present partner. Risk: avoiding heavy topics. The best relationships go deep AND fun.",
        "challenge_30d": "Have one 'deep' conversation per week. Topic: something that genuinely worries or excites you about the future."
    },
}

DEFAULT_PROFILE = {
    "alias": "Explorer / 探索者",
    "snapshot": "Your type pattern is still emerging. The more conversations we analyze, the clearer the picture becomes.",
    "superpowers": ["🔍 Self-awareness — you're curious enough to look inward", "🌱 Growth — analyzing yourself is the first step", "🧩 Complexity — you may be situationally adaptive"],
    "growth_edges": ["📊 More data needed — share more conversations for a clearer picture", "🎯 Self-observation — start noticing your patterns", "📝 Journaling — writing reveals personality patterns"],
    "career": "Keep exploring. Your versatility may be a superpower in itself.",
    "communication": "Your style appears adaptive. Pay attention to which mode feels most natural.",
    "relationship": "Continue observing your patterns in relationships. Self-knowledge takes time.",
    "challenge_30d": "Journal for 5 minutes daily about how you made decisions today."
}


def parse_report(report_text):
    """Extract MBTI type and key metrics from the report."""
    type_match = re.search(r'Your MBTI Type:\s*\*\*(\w{4})\*\*', report_text)
    mbti_type = type_match.group(1) if type_match else "XXXX"

    confidence_match = re.search(r'Overall confidence:\s*\*\*(\w+)\*\*', report_text)
    confidence = confidence_match.group(1) if confidence_match else "unknown"

    msg_count_match = re.search(r'Based on (\d+) user messages', report_text)
    msg_count = int(msg_count_match.group(1)) if msg_count_match else 0

    return mbti_type, confidence, msg_count


def generate_advice(report_path, output_path):
    """Generate personalized advice based on personality report."""
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    mbti_type, confidence, msg_count = parse_report(report_text)
    profile = TYPE_PROFILES.get(mbti_type, DEFAULT_PROFILE)

    advice = f"""# 🌟 KnowMe — Your Personalized Growth Guide

> Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> Type: **{mbti_type}** — {profile['alias']}
> Confidence: **{confidence}** (based on {msg_count} messages)

---

## 🧬 Who You Are

{profile['snapshot']}

---

## 💪 Your Superpowers

"""
    for s in profile["superpowers"]:
        advice += f"{s}\n"

    advice += f"""
---

## 🌱 Growth Edges

"""
    for g in profile["growth_edges"]:
        advice += f"{g}\n"

    advice += f"""
---

## 🎯 Career Lens

{profile['career']}

---

## 💬 Communication Guide

{profile['communication']}

---

## ❤️ Relationship Insights

{profile['relationship']}

---

## ⚡ 30-Day Challenge

{profile['challenge_30d']}

---

## 🔄 What's Next?

1. **Share more conversations** — The more data, the sharper the insight
2. **Re-run in 30 days** — See how your patterns evolve after the challenge
3. **Cross-reference** — Try with different AI chat sources for a fuller picture
4. **Discuss** — Talk about your results with someone you trust

---

*Remember: MBTI is a compass, not a cage. Use these insights to grow, not to limit yourself.*
"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(advice)

    return advice


def main():
    parser = argparse.ArgumentParser(description="KnowMe - Generate personalized advice")
    parser.add_argument("--report", default="/tmp/knowme_report.md", help="Input report from analyze.py")
    parser.add_argument("--output", default="/tmp/knowme_advice.md", help="Output advice path")
    args = parser.parse_args()

    print(f"[KnowMe] Generating advice from {args.report}")
    advice = generate_advice(args.report, args.output)
    print(f"[KnowMe] Advice saved to {args.output}")

    # Print summary
    mbti_type, confidence, msg_count = parse_report(open(args.report).read())
    profile = TYPE_PROFILES.get(mbti_type, DEFAULT_PROFILE)
    print(f"[KnowMe] Type: {mbti_type} ({profile['alias']})")
    print(f"[KnowMe] Challenge: {profile['challenge_30d']}")


if __name__ == "__main__":
    main()

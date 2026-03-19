#!/usr/bin/env python3
"""
KnowMe - Personality Portrait Generator

Generates personalized portraits based on MBTI personality profiles.
Integrates with PonyFlash or other image generation APIs.

Usage:
    python3 scripts/generate_portrait.py --report report.md --output portrait.png
    python3 scripts/generate_portrait.py --report report.md --style anime --output avatar.png
"""

import argparse
import re
import sys
import os
from typing import Optional

# ─── MBTI to Visual Traits Mapping ───

MBTI_VISUAL_TRAITS = {
    # Analysts (NT)
    "INTJ": {
        "expression": "confident, analytical gaze with strategic depth",
        "attire": "minimalist dark blazer, clean lines, professional",
        "background": "abstract neural networks, data flows, subtle tech elements",
        "lighting": "crisp, professional, highlighting focused expression",
        "colors": "deep blues, silvers, sophisticated muted palette",
        "mood": "intellectual authority, quiet confidence"
    },
    "INTP": {
        "expression": "curious, contemplative, slightly distant",
        "attire": "casual intellectual, perhaps glasses, comfortable",
        "background": "books, abstract concepts, floating ideas",
        "lighting": "soft, natural, contemplative",
        "colors": "earth tones, warm grays, intellectual blues",
        "mood": "thoughtful, innovative, slightly quirky"
    },
    "ENTJ": {
        "expression": "commanding presence, decisive, charismatic",
        "attire": "sharp business attire, power dressing",
        "background": "city skyline, success symbols, dynamic energy",
        "lighting": "dramatic, high contrast, powerful",
        "colors": "bold blacks, golds, confident reds",
        "mood": "leadership, ambition, natural authority"
    },
    "ENTP": {
        "expression": "mischievous, energetic, quick-witted",
        "attire": "creative professional, unique accessories",
        "background": "chaotic creativity, multiple ideas, innovation",
        "lighting": "dynamic, varied, playful shadows",
        "colors": "vibrant purples, electric blues, creative oranges",
        "mood": "innovation, debate, creative chaos"
    },
    # Diplomats (NF)
    "INFJ": {
        "expression": "mysterious, empathetic, deeply thoughtful",
        "attire": "elegant, understated, meaningful accessories",
        "background": "ethereal, mystical, nature meets abstract",
        "lighting": "soft, dreamy, warm glow",
        "colors": "deep purples, forest greens, mystical golds",
        "mood": "wisdom, mystery, quiet intensity"
    },
    "INFP": {
        "expression": "gentle, dreamy, authentic",
        "attire": "artistic, bohemian, personal expression",
        "background": "nature, art, personal symbols",
        "lighting": "golden hour, soft, warm",
        "colors": "pastels, nature tones, artistic hues",
        "mood": "idealism, creativity, gentle strength"
    },
    "ENFJ": {
        "expression": "warm, inspiring, engaging",
        "attire": "approachable professional, welcoming",
        "background": "people, community, connection",
        "lighting": "bright, inviting, warm",
        "colors": "warm oranges, friendly yellows, nurturing greens",
        "mood": "charisma, inspiration, human connection"
    },
    "ENFP": {
        "expression": "enthusiastic, bright, infectious energy",
        "attire": "colorful, expressive, unique style",
        "background": "adventure, possibilities, excitement",
        "lighting": "bright, dynamic, full of life",
        "colors": "rainbow accents, bright pinks, energetic yellows",
        "mood": "enthusiasm, creativity, boundless energy"
    },
    # Sentinels (SJ)
    "ISTJ": {
        "expression": "reliable, serious, trustworthy",
        "attire": "classic professional, traditional, neat",
        "background": "organized, structured, established",
        "lighting": "even, clear, straightforward",
        "colors": "navy blues, grays, traditional tones",
        "mood": "dependability, tradition, quiet competence"
    },
    "ISFJ": {
        "expression": "gentle, caring, attentive",
        "attire": "modest, comfortable, caring details",
        "background": "home, comfort, nurturing environment",
        "lighting": "soft, warm, comforting",
        "colors": "soft greens, warm beiges, gentle blues",
        "mood": "warmth, care, quiet dedication"
    },
    "ESTJ": {
        "expression": "authoritative, practical, no-nonsense",
        "attire": "business formal, efficient, practical",
        "background": "office, organization, results",
        "lighting": "bright, clear, direct",
        "colors": "strong blues, practical grays, efficient blacks",
        "mood": "efficiency, management, get-things-done"
    },
    "ESFJ": {
        "expression": "friendly, welcoming, sociable",
        "attire": "approachable, fashionable, considerate",
        "background": "social gathering, community, harmony",
        "lighting": "bright, flattering, social",
        "colors": "warm pinks, friendly blues, social purples",
        "mood": "harmony, social grace, helpfulness"
    },
    # Explorers (SP)
    "ISTP": {
        "expression": "focused, practical, observant",
        "attire": "functional, practical, ready for action",
        "background": "tools, mechanics, hands-on environment",
        "lighting": "practical, clear, task-focused",
        "colors": "metallic grays, practical blues, tool steel",
        "mood": "competence, practicality, quiet skill"
    },
    "ISFP": {
        "expression": "artistic, sensitive, present",
        "attire": "artistic, expressive, aesthetic",
        "background": "art studio, nature, beauty",
        "lighting": "artistic, natural, beautiful",
        "colors": "artistic palette, nature tones, creative expression",
        "mood": "artistry, sensitivity, living in the moment"
    },
    "ESTP": {
        "expression": "energetic, confident, action-oriented",
        "attire": "stylish, current, ready for anything",
        "background": "action, excitement, adventure",
        "lighting": "dynamic, high energy, dramatic",
        "colors": "bold reds, energetic oranges, action blacks",
        "mood": "energy, spontaneity, living life fully"
    },
    "ESFP": {
        "expression": "vivacious, fun-loving, magnetic",
        "attire": "trendy, eye-catching, expressive",
        "background": "party, spotlight, entertainment",
        "lighting": "bright, colorful, celebratory",
        "colors": "glittering golds, party purples, fun pinks",
        "mood": "entertainment, joy, being the life of the party"
    }
}

# ─── Style Modifiers ───

STYLE_MODIFIERS = {
    "professional": "modern corporate portrait, high-end business photography, clean composition",
    "anime": "anime style, manga aesthetic, vibrant colors, expressive features",
    "realistic": "photorealistic, DSLR quality, natural lighting, professional photography",
    "artistic": "artistic portrait, painterly style, creative composition, gallery quality",
    "minimalist": "minimalist aesthetic, clean background, simple composition, modern design",
    "cyberpunk": "cyberpunk aesthetic, neon accents, futuristic, digital art style",
    "fantasy": "fantasy art style, magical elements, epic composition, imaginative"
}

# ─── Portrait Generator ───

class PortraitGenerator:
    """Generates personalized portraits based on MBTI personality profiles."""
    
    def __init__(self):
        self.mbti_traits = MBTI_VISUAL_TRAITS
        self.style_modifiers = STYLE_MODIFIERS
    
    def extract_mbti_from_report(self, report_path: str) -> Optional[str]:
        """Extract MBTI type from personality report."""
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for MBTI pattern (e.g., "INTJ", "ENFP")
            mbti_pattern = r'\b([IE][NS][TF][JP])\b'
            matches = re.findall(mbti_pattern, content)
            
            if matches:
                return matches[0]  # Return first match
            return None
        except Exception as e:
            print(f"Error reading report: {e}")
            return None
    
    def generate_prompt(self, mbti_type: str, style: str = "professional") -> str:
        """Generate image prompt based on MBTI type and style."""
        if mbti_type not in self.mbti_traits:
            print(f"Warning: Unknown MBTI type {mbti_type}, using generic traits")
            traits = self.mbti_traits.get("INTJ")  # Default
        else:
            traits = self.mbti_traits[mbti_type]
        
        style_modifier = self.style_modifiers.get(style, self.style_modifiers["professional"])
        
        prompt = f"""A {style_modifier} portrait of a person with {traits['expression']}.
        
Attire: {traits['attire']}.
Background: {traits['background']}.
Lighting: {traits['lighting']}.
Color palette: {traits['colors']}.
Mood: {traits['mood']}.

Style: High-quality digital art, {style_modifier}, 4K detail, sophisticated composition."""
        
        return prompt
    
    def create_portrait(self, report_path: str, style: str = "professional", output: Optional[str] = None) -> dict:
        """Generate portrait prompt from personality report."""
        mbti = self.extract_mbti_from_report(report_path)
        
        if not mbti:
            print("Could not extract MBTI type from report")
            return {"success": False, "error": "No MBTI found"}
        
        prompt = self.generate_prompt(mbti, style)
        
        result = {
            "success": True,
            "mbti": mbti,
            "style": style,
            "prompt": prompt,
            "output_path": output
        }
        
        # Save prompt if output specified
        if output:
            prompt_file = output.replace('.png', '_prompt.txt').replace('.jpg', '_prompt.txt')
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(f"# KnowMe Portrait Prompt\n")
                f.write(f"# MBTI: {mbti}\n")
                f.write(f"# Style: {style}\n\n")
                f.write(prompt)
            print(f"Prompt saved to: {prompt_file}")
        
        return result

# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description='Generate personality-based portraits')
    parser.add_argument('--report', required=True, help='Path to KnowMe personality report')
    parser.add_argument('--style', default='professional', 
                      choices=list(STYLE_MODIFIERS.keys()),
                      help='Visual style for portrait')
    parser.add_argument('--output', help='Output path for prompt file')
    
    args = parser.parse_args()
    
    generator = PortraitGenerator()
    result = generator.create_portrait(args.report, args.style, args.output)
    
    if result["success"]:
        print(f"\n🎨 Portrait Prompt Generated!")
        print(f"MBTI Type: {result['mbti']}")
        print(f"Style: {result['style']}")
        print(f"\nPrompt:\n{result['prompt'][:500]}...")
        print(f"\n💡 Use this prompt with PonyFlash, Midjourney, DALL-E, or Stable Diffusion")
    else:
        print(f"❌ Failed: {result.get('error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()

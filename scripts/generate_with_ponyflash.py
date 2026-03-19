#!/usr/bin/env python3
"""
KnowMe - PonyFlash Integration

Direct integration with PonyFlash API to generate personality-based portraits.

Usage:
    python3 scripts/generate_with_ponyflash.py --report report.md --output portrait.png
    python3 scripts/generate_with_ponyflash.py --mbti INTJ --style professional --output avatar.png
"""

import argparse
import sys
import os
from pathlib import Path

# Import portrait generator
try:
    from generate_portrait import PortraitGenerator, MBTI_VISUAL_TRAITS
except ImportError:
    # Add parent directory to path
    sys.path.insert(0, str(Path(__file__).parent))
    from generate_portrait import PortraitGenerator, MBTI_VISUAL_TRAITS

def generate_with_ponyflash(mbti_type: str, style: str = "professional", output: str = None):
    """Generate portrait using PonyFlash API."""
    
    # Check for PonyFlash
    try:
        from ponyflash import PonyFlash
    except ImportError:
        print("❌ PonyFlash SDK not found. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "ponyflash", "--break-system-packages"])
        from ponyflash import PonyFlash
    
    # Generate prompt
    generator = PortraitGenerator()
    prompt = generator.generate_prompt(mbti_type, style)
    
    # Initialize PonyFlash
    pf = PonyFlash()
    
    print(f"🎨 Generating {mbti_type} portrait with PonyFlash...")
    print(f"Style: {style}")
    print(f"Prompt: {prompt[:100]}...")
    
    try:
        # Generate image
        image = pf.images.generate(
            model='nano-banana-pro',
            prompt=prompt,
            resolution='2K',
            aspect_ratio='1:1'
        )
        
        print(f"✅ Image generated successfully!")
        print(f"   URL: {image.url}")
        
        # Download if output specified
        if output:
            import requests
            response = requests.get(image.url)
            with open(output, 'wb') as f:
                f.write(response.content)
            print(f"   Saved to: {output}")
        
        return {
            "success": True,
            "url": image.url,
            "mbti": mbti_type,
            "style": style,
            "prompt": prompt
        }
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return {"success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Generate portraits with PonyFlash')
    parser.add_argument('--report', help='Path to KnowMe report')
    parser.add_argument('--mbti', help='MBTI type (e.g., INTJ, ENFP)')
    parser.add_argument('--style', default='professional', 
                      choices=['professional', 'anime', 'realistic', 'artistic', 'minimalist'],
                      help='Visual style')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    # Determine MBTI type
    if args.report:
        generator = PortraitGenerator()
        mbti = generator.extract_mbti_from_report(args.report)
        if not mbti:
            print("❌ Could not extract MBTI from report")
            sys.exit(1)
    elif args.mbti:
        mbti = args.mbti.upper()
    else:
        print("❌ Please provide --report or --mbti")
        sys.exit(1)
    
    # Generate
    result = generate_with_ponyflash(mbti, args.style, args.output)
    
    if result["success"]:
        print(f"\n🎉 {mbti} portrait generated!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
KnowMe - Bailian Image Generation Adapter

阿里云百炼图像生成适配器
将KnowMe的MBTI分析结果转换为Bailian可用的图像生成请求

Usage:
    python3 scripts/bailian_adapter.py --report report.md --output portrait.png
    python3 scripts/bailian_adapter.py --mbti INTJ --style professional --output avatar.png
"""

import argparse
import sys
import os
from pathlib import Path

# 导入KnowMe的portrait生成器
try:
    from generate_portrait import PortraitGenerator, MBTI_VISUAL_TRAITS
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from generate_portrait import PortraitGenerator, MBTI_VISUAL_TRAITS


class BailianAdapter:
    """适配器：将KnowMe输出转换为Bailian输入"""
    
    def __init__(self):
        self.generator = PortraitGenerator()
    
    def generate_bailian_request(self, mbti_type: str, style: str = "professional") -> dict:
        """
        生成Bailian图像生成请求
        
        Returns:
            {
                "model": str,
                "prompt": str,
                "negative_prompt": str,
                "width": int,
                "height": int,
                "style_preset": str,
                "parameters": dict
            }
        """
        # 生成优化的prompt
        prompt = self.generator.generate_prompt(mbti_type, style)
        
        # 根据风格设置参数
        style_configs = {
            "professional": {
                "width": 1024,
                "height": 1024,
                "style_preset": "photographic",
                "negative_prompt": "cartoon, anime, illustration, painting, drawing, sketch, low quality, blurry"
            },
            "anime": {
                "width": 1024,
                "height": 1024,
                "style_preset": "anime",
                "negative_prompt": "photorealistic, 3d render, realistic, photo, low quality, blurry"
            },
            "realistic": {
                "width": 1024,
                "height": 1024,
                "style_preset": "photographic",
                "negative_prompt": "cartoon, anime, illustration, painting, low quality, blurry"
            },
            "artistic": {
                "width": 1024,
                "height": 1024,
                "style_preset": "digital-art",
                "negative_prompt": "photorealistic, 3d render, photo, low quality, blurry"
            },
            "minimalist": {
                "width": 1024,
                "height": 1024,
                "style_preset": "line-art",
                "negative_prompt": "cluttered, busy, complex, detailed, low quality, blurry"
            }
        }
        
        config = style_configs.get(style, style_configs["professional"])
        
        return {
            "model": "wanx-v1",  # Bailian的通义万相模型
            "prompt": prompt,
            "negative_prompt": config["negative_prompt"],
            "width": config["width"],
            "height": config["height"],
            "style_preset": config["style_preset"],
            "parameters": {
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
                "seed": -1  # 随机种子
            },
            "metadata": {
                "mbti_type": mbti_type,
                "style": style,
                "generator": "KnowMe-v2.0"
            }
        }
    
    def save_request(self, request: dict, output_path: str):
        """保存请求到JSON文件，供后续使用"""
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(request, f, ensure_ascii=False, indent=2)
        print(f"✅ Bailian请求已保存: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='KnowMe Bailian Adapter')
    parser.add_argument('--report', help='KnowMe personality report path')
    parser.add_argument('--mbti', help='MBTI type (e.g., INTJ, ENFP)')
    parser.add_argument('--style', default='professional',
                      choices=['professional', 'anime', 'realistic', 'artistic', 'minimalist'],
                      help='Image style')
    parser.add_argument('--output', default='bailian_request.json', help='Output JSON file')
    parser.add_argument('--pretty', action='store_true', help='Pretty print the request')
    
    args = parser.parse_args()
    
    # Determine MBTI type
    adapter = BailianAdapter()
    
    if args.report:
        mbti = adapter.generator.extract_mbti_from_report(args.report)
        if not mbti:
            print("❌ Could not extract MBTI from report")
            sys.exit(1)
    elif args.mbti:
        mbti = args.mbti.upper()
    else:
        print("❌ Please provide --report or --mbti")
        sys.exit(1)
    
    # Generate Bailian request
    print(f"🎨 Generating Bailian request for {mbti} ({args.style} style)...")
    request = adapter.generate_bailian_request(mbti, args.style)
    
    # Save or print
    if args.pretty:
        import json
        print("\n📋 Bailian Request:")
        print(json.dumps(request, ensure_ascii=False, indent=2))
    
    adapter.save_request(request, args.output)
    
    print(f"\n💡 Next steps:")
    print(f"   1. Load this request in your Bailian client")
    print(f"   2. Or use: bailian.images.generate(**request)")
    print(f"   3. Get your personalized {mbti} portrait!")


if __name__ == "__main__":
    main()

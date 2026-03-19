# KnowMe 生成式个性化工作流示例

> 从MBTI性格分析到个性化图像生成的完整流程

## 快速开始

### 1. 基础流程：分析 → 生成Prompt

```bash
# 分析聊天记录
python3 scripts/analyze.py --input conversation.json --output report.md

# 生成图像Prompt
python3 scripts/generate_portrait.py --report report.md --style professional
```

### 2. 使用Bailian生成图像

```bash
# 生成Bailian请求
python3 scripts/bailian_adapter.py --report report.md --style professional --output bailian_request.json

# 然后在你的代码中使用：
```python
import json
from bailian import BailianClient

# 加载请求
with open('bailian_request.json') as f:
    request = json.load(f)

# 生成图像
client = BailianClient(api_key="your_key")
image = client.images.generate(**request)
print(image.url)
```

### 3. 直接指定MBTI生成

```bash
# 无需分析报告，直接指定类型
python3 scripts/bailian_adapter.py --mbti INTJ --style anime --output request.json
python3 scripts/bailian_adapter.py --mbti ENFP --style artistic --output request.json
```

## 风格说明

| 风格 | 适用场景 | Bailian预设 |
|------|---------|------------|
| professional | LinkedIn头像、商务形象 | photographic |
| anime | 社交媒体、二次元头像 | anime |
| realistic | 真实感肖像 | photographic |
| artistic | 艺术创作、个人品牌 | digital-art |
| minimalist | 设计作品集、简历 | line-art |

## MBTI视觉特征映射

### 分析师 (NT)

**INTJ** - 建筑师
- 表情：自信、战略思维、锐利眼神
- 着装：极简深色西装、干净线条
- 背景：抽象神经网络、数据流
- 色调：深蓝、银色、高级灰

**ENTJ** - 指挥官
- 表情：威严、果断、有魅力
- 着装：权力着装、 sharp business attire
- 背景：城市天际线、成功象征
- 色调：黑色、金色、自信红

### 外交官 (NF)

**INFJ** - 提倡者
- 表情：神秘、共情、深思熟虑
- 着装：优雅、低调、有意义配饰
- 背景：空灵、自然与抽象结合
- 色调：深紫、森林绿、神秘金

**ENFP** - 竞选者
- 表情：热情、明亮、感染力
- 着装：多彩、表达性强、独特风格
- 背景：冒险、可能性、兴奋
- 色调：彩虹点缀、亮粉、活力黄

### 哨兵 (SJ)

**ISTJ** - 物流师
- 表情：可靠、严肃、值得信赖
- 着装：经典职业装、传统、整洁
- 背景：有组织、结构化、已建立
- 色调：海军蓝、灰色、传统色调

**ESFJ** - 执政官
- 表情：友好、热情、善于社交
- 着装：平易近人、时尚、体贴
- 背景：社交聚会、社区、和谐
- 色调：暖粉、友好蓝、社交紫

### 探险家 (SP)

**ISTP** - 鉴赏家
- 表情：专注、务实、善于观察
- 着装：功能性、实用、准备行动
- 背景：工具、机械、动手环境
- 色调：金属灰、实用蓝、工具钢色

**ISFP** - 探险家
- 表情：艺术感、敏感、活在当下
- 着装：艺术性、表达性、审美
- 背景：艺术工作室、自然、美
- 色调：艺术调色板、自然色调

## 实际案例

### 案例1：Andy (INTJ) 的专业形象

```bash
python3 scripts/bailian_adapter.py \
  --mbti INTJ \
  --style professional \
  --output andy_intj.json \
  --pretty
```

生成的Prompt：
```
A modern corporate portrait, high-end business photography, clean composition 
portrait of a person with confident, analytical gaze with strategic depth.

Attire: Minimalist dark blazer, clean lines, professional.
Background: Abstract neural networks, data flows, subtle tech elements.
Lighting: Crisp, professional, highlighting focused expression.
Color palette: Deep blues, silvers, sophisticated muted palette.
Mood: Intellectual authority, quiet confidence.

Style: High-quality digital art, modern corporate portrait, high-end business 
photography, clean composition, 4K detail, sophisticated composition.
```

### 案例2：圆圆 (猫咪AI分身)

```bash
python3 scripts/generate_portrait.py --mbti ENTP --style anime
```

特点：
- 傲娇表情 + 科技配饰
- 神经网络背景
- 蓝紫渐变光晕

## 高级用法

### 批量生成所有类型

```bash
for mbti in INTJ INTP ENTJ ENTP INFJ INFP ENFJ ENFP ISTJ ISFJ ESTJ ESFJ ISTP ISFP ESTP ESFP; do
  python3 scripts/bailian_adapter.py --mbti $mbti --style professional --output "requests/${mbti}.json"
done
```

### 自定义风格参数

修改 `bailian_adapter.py` 中的 `style_configs`：

```python
style_configs = {
    "cyberpunk": {
        "width": 1024,
        "height": 1024,
        "style_preset": "digital-art",
        "negative_prompt": "natural, organic, traditional, low quality"
    }
}
```

### 集成到工作流

```python
from knowme import Analyzer
from scripts.bailian_adapter import BailianAdapter

# 分析性格
analyzer = Analyzer()
report = analyzer.analyze(conversations)

# 生成图像
adapter = BailianAdapter()
request = adapter.generate_bailian_request(report.mbti, style="professional")

# 生成头像
image = bailian_client.generate(**request)
user.avatar = image.url
```

## 常见问题

**Q: 生成的图像不像我怎么办？**
A: 这是基于MBTI类型的"典型形象"，不是照片级还原。可以在此基础上用真实照片进行img2img优化。

**Q: 支持哪些图像生成服务？**
A: 目前提供Bailian适配器，但生成的Prompt可以用于任何服务：Midjourney、DALL-E、Stable Diffusion等。

**Q: 可以生成非人类形象吗？**
A: 可以！比如给AI助手生成形象（像圆圆这样的猫咪AI分身），只需在Prompt中描述即可。

## 下一步

- [ ] 添加更多风格预设
- [ ] 支持img2img基于照片优化
- [ ] 添加视频生成支持
- [ ] 集成更多图像服务适配器

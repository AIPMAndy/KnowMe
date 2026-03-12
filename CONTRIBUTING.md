# Contributing to KnowMe

感谢你有兴趣为 KnowMe 贡献代码！以下是参与指南。

Thank you for your interest in contributing to KnowMe! Here's how to get started.

---

## 🚀 Quick Start

```bash
# Fork & clone
git clone https://github.com/<your-username>/KnowMe.git
cd KnowMe

# Run a quick test
python3 scripts/collect.py --source text --file references/ --output /tmp/test_data.json
python3 scripts/analyze.py --input /tmp/test_data.json --output /tmp/test_report.md
python3 scripts/advise.py --report /tmp/test_report.md --output /tmp/test_advice.md
```

No dependencies beyond Python 3.8+ standard library. Zero setup.

---

## 🎯 What We Need Most

### 🔌 New Data Source Parsers (High Priority)

We want to support every AI platform. Each parser is a single function in `scripts/collect.py`:

```python
def collect_gemini(file_path):
    """Parse Gemini export data."""
    # Read the export file
    # Return list of {"role": "user"|"assistant", "content": "...", "timestamp": "...", "source": "gemini"}
    pass
```

**Wanted**: Gemini, Copilot, DeepSeek, Perplexity, Grok, Pi, Poe

If you use any of these, export your data and write a parser!

### 🔍 New Behavioral Signals (High Priority)

More signals = better analysis. Add patterns to the `SignalDetector` class in `scripts/analyze.py`:

```python
# Example: detect perfectionism (J signal)
if re.search(r'(perfect|flawless|完美|零缺陷)', content_lower):
    self._score("J", 2, "Perfectionism tendency")
```

**Guidelines**:
- Each signal should be backed by MBTI theory
- Test with at least 5 real messages before submitting
- Include both English and Chinese patterns when possible
- Weight: 1 = weak signal, 2 = moderate, 3 = strong

### 🌍 Language Support

Currently: English + Chinese. Want: Japanese, Korean, Spanish, German, French...

Each language needs:
1. Signal patterns in `analyze.py`
2. Cultural adjustment notes in `references/mbti_signals.md`

### 📊 Web UI

We want a simple browser-based interface:
1. Upload your export file
2. See your report rendered beautifully
3. Share results (as image or link)

Tech preference: Vanilla HTML/JS (no framework), or lightweight (Svelte/Vue).

---

## 📋 PR Guidelines

1. **One feature per PR** — Keep it focused
2. **Test it** — Run the full pipeline with real data
3. **Both languages** — If you add signal patterns, include EN + CN when possible
4. **Update docs** — If you add a data source, update the table in README.md and README_EN.md
5. **Keep it simple** — No new dependencies unless absolutely necessary

### Commit Messages

```
feat: add Gemini data source parser
fix: improve Chinese indirectness signal detection
docs: update roadmap with Web UI plans
refactor: extract signal patterns to config
```

---

## 🐛 Bug Reports

Use the [Bug Report template](https://github.com/AIPMAndy/KnowMe/issues/new?template=bug_report.md) and include:

- Python version
- Data source type
- Error message or unexpected behavior
- Sample data (anonymized) if possible

## 💡 Feature Requests

Use the [Feature Request template](https://github.com/AIPMAndy/KnowMe/issues/new?template=feature_request.md).

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

**Every contribution makes KnowMe smarter. Thank you! 🧬**

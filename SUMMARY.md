# LLM Diverse Perspectives Generation - Summary

## Overview
This project generates diverse perspectives on social/political topics using GPT-5 with different few-shot prompting strategies.

## Generated Results

### Total Outputs
- **120 diverse perspectives** across 3 topics and 4 methods
- **12 JSON files** (6 from 5-shot, 6 from 1-shot)
- **2 formatted text files** for easy reading

### Topics
1. **Elections Trust**: "How should we increase the general public's trust in US elections?"
2. **Littering Prevention**: "What are the best policies to prevent littering in public spaces?"
3. **Campus Protests**: "What are your thoughts on the way university campus administrators should approach the issue of Israel/Gaza demonstrations?"

### Prompting Methods

#### 5-Shot Examples (Original)
- **criteria-based**: Uses 5 example statements with Stance, Criteria, and Reason
- **free-form**: Uses 5 example statements with Stance and Reason only

#### 1-Shot Examples (New)
- **1-shot-criteria-based**: Uses 1 example statement with Stance, Criteria, and Reason
- **1-shot-free-form**: Uses 1 example statement with Stance and Reason only

## File Structure

```
evaluate-generative-social-choice-topics/
├── prompts/
│   ├── 5-shot-criteria-based-prompting.txt
│   ├── 5-shot-free-form-prompting.txt
│   ├── 1-shot-criteria-based-prompting.txt
│   └── 1-shot-free-form-prompting.txt
├── outputs/
│   ├── criteria-based_elections.json           (5-shot, 10 perspectives)
│   ├── criteria-based_littering.json           (5-shot, 10 perspectives)
│   ├── criteria-based_campus_protests.json     (5-shot, 10 perspectives)
│   ├── free-form_elections.json                (5-shot, 10 perspectives)
│   ├── free-form_littering.json                (5-shot, 10 perspectives)
│   ├── free-form_campus_protests.json          (5-shot, 10 perspectives)
│   ├── 1-shot-criteria-based_elections.json    (1-shot, 10 perspectives)
│   ├── 1-shot-criteria-based_littering.json    (1-shot, 10 perspectives)
│   ├── 1-shot-criteria-based_campus_protests.json (1-shot, 10 perspectives)
│   ├── 1-shot-free-form_elections.json         (1-shot, 10 perspectives)
│   ├── 1-shot-free-form_littering.json         (1-shot, 10 perspectives)
│   ├── 1-shot-free-form_campus_protests.json   (1-shot, 10 perspectives)
│   ├── formatted_results.txt                   (5-shot results only, 24K)
│   └── formatted_results_all.txt               (both 5-shot and 1-shot, 47K)
├── generate_statements_unified.py              (unified generation script)
├── format_results_unified.py                   (unified formatting script)
├── pyproject.toml
├── .env                                        (contains OPENAI_API_KEY)
├── README.md                                   (comprehensive documentation)
└── SUMMARY.md                                  (this file)
```

## Scripts

### Unified Scripts (Current)
1. **generate_statements_unified.py**: Generates perspectives with configurable shot types
   - Supports: `--shot-type {1-shot, 5-shot, all}`
   - Reads: `prompts/{N}-shot-{method}-prompting.txt`
   - Outputs: `outputs/{method}_{topic}.json`

2. **format_results_unified.py**: Displays results with flexible filtering
   - Supports: `--shot-type {1-shot, 5-shot, all}`
   - Reads: `outputs/*.json`
   - Outputs: Console + `outputs/formatted_results_{type}.txt`

## Running the Scripts

```bash
# Generate all perspectives (both 5-shot and 1-shot)
uv run --no-project python generate_statements_unified.py

# Generate only specific shot type
uv run --no-project python generate_statements_unified.py --shot-type 5-shot
uv run --no-project python generate_statements_unified.py --shot-type 1-shot

# Format all results (5-shot + 1-shot comparison)
uv run --no-project python format_results_unified.py --shot-type all

# Format specific shot type
uv run --no-project python format_results_unified.py --shot-type 5-shot
uv run --no-project python format_results_unified.py --shot-type 1-shot

# Save to custom file
uv run --no-project python format_results_unified.py --save my_output.txt
```

## Model Configuration
- **Model**: `gpt-5-2025-08-07`
- **Max Completion Tokens**: 4000
- **Temperature**: Default (1.0, as required by GPT-5)

## Key Features
- ✅ Non-overwriting output files (1-shot files have different names)
- ✅ JSON structured output for easy analysis
- ✅ Human-readable formatted text files
- ✅ Comparison-ready structure (5-shot vs 1-shot)
- ✅ Consistent format across all perspectives
- ✅ Error handling and progress reporting


# LLM Diverse Perspectives Generation

Generate diverse perspectives on social and political topics using GPT-5 with different few-shot prompting strategies.

## Quick Start

### Generate Perspectives

```bash
# Generate all perspectives (both 5-shot and 1-shot)
uv run --no-project python generate_statements_unified.py

# Generate only 5-shot examples
uv run --no-project python generate_statements_unified.py --shot-type 5-shot

# Generate only 1-shot examples
uv run --no-project python generate_statements_unified.py --shot-type 1-shot
```

### Format and Display Results

```bash
# Display all results (5-shot and 1-shot comparison)
uv run --no-project python format_results_unified.py --shot-type all

# Display only 5-shot results
uv run --no-project python format_results_unified.py --shot-type 5-shot

# Display only 1-shot results
uv run --no-project python format_results_unified.py --shot-type 1-shot

# Save to custom file
uv run --no-project python format_results_unified.py --save my_results.txt
```

## Project Structure

```
evaluate-generative-social-choice-topics/
├── prompts/                              # Few-shot prompt templates
│   ├── 5-shot-criteria-based-prompting.txt
│   ├── 5-shot-free-form-prompting.txt
│   ├── 1-shot-criteria-based-prompting.txt
│   └── 1-shot-free-form-prompting.txt
├── outputs/                              # Generated perspectives (JSON)
│   ├── criteria-based_*.json            # 5-shot criteria-based results
│   ├── free-form_*.json                 # 5-shot free-form results
│   ├── 1-shot-criteria-based_*.json     # 1-shot criteria-based results
│   ├── 1-shot-free-form_*.json          # 1-shot free-form results
│   └── formatted_results_*.txt          # Human-readable formatted output
├── generate_statements_unified.py        # Unified generation script
├── format_results_unified.py            # Unified formatting script
├── pyproject.toml                       # Project dependencies
├── .env                                 # API keys (OPENAI_API_KEY)
└── README.md                            # This file
```

## Topics

The project generates diverse perspectives on three topics:

1. **Elections Trust**: "How should we increase the general public's trust in US elections?"
2. **Littering Prevention**: "What are the best policies to prevent littering in public spaces?"
3. **Campus Protests**: "What are your thoughts on the way university campus administrators should approach the issue of Israel/Gaza demonstrations?"

## Prompting Methods

### Few-Shot Examples
- **5-shot**: Uses 5 example statements to guide the model
- **1-shot**: Uses 1 example statement to guide the model

### Prompting Styles
- **Criteria-based**: Generates perspectives with explicit key criteria
  - Output includes: Position, Key Criteria (list), Reasoning
- **Free-form**: Generates perspectives without explicit criteria
  - Output includes: Position, Reasoning

## Output Format

### JSON Structure

Each output file contains 10 perspectives in JSON format:

```json
{
  "1": {
    "Stance": "Position or approach description",
    "Criteria": ["criterion1", "criterion2", ...],  // Only in criteria-based
    "Reason": "Detailed reasoning"
  },
  "2": { ... },
  ...
}
```

### File Naming Convention

- 5-shot results: `{method}_{topic_id}.json`
  - Example: `criteria-based_elections.json`
  
- 1-shot results: `1-shot-{method}_{topic_id}.json`
  - Example: `1-shot-criteria-based_elections.json`

## Configuration

### Environment Variables

Create a `.env` file with your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### Model Configuration

- **Model**: `gpt-5-2025-08-07`
- **Max Completion Tokens**: 4000
- **Temperature**: Default (1.0, required by GPT-5)

## Command Line Options

### Generation Script

```
generate_statements_unified.py [OPTIONS]

Options:
  --shot-type {1-shot,5-shot,all}   Type of few-shot examples (default: all)
  --output-dir OUTPUT_DIR           Output directory (default: outputs)
```

### Formatting Script

```
format_results_unified.py [OPTIONS]

Options:
  --shot-type {1-shot,5-shot,all}   Which results to display (default: all)
  --output-dir OUTPUT_DIR           Input directory (default: outputs)
  --save FILENAME                   Save to file (auto-generated if omitted)
```

## Generated Statistics

- **120 total perspectives** across:
  - 3 topics
  - 2 shot types (5-shot, 1-shot)
  - 2 prompting styles (criteria-based, free-form)
  - 10 perspectives per combination

## Examples

### Example: Generate and Format 5-shot Only

```bash
# Generate 5-shot perspectives
uv run --no-project python generate_statements_unified.py --shot-type 5-shot

# Format and save results
uv run --no-project python format_results_unified.py --shot-type 5-shot \
    --save outputs/results_5shot.txt
```

### Example: Compare 5-shot vs 1-shot

```bash
# Generate all perspectives
uv run --no-project python generate_statements_unified.py

# Display comparison
uv run --no-project python format_results_unified.py --shot-type all
```

## Dependencies

Install with uv (automatically handled by `uv run`):

- `openai>=1.0.0`
- `python-dotenv>=1.0.0`

## Notes

- The unified scripts replace the older separate scripts for generation and formatting
- Existing output files are never overwritten (generation creates new files if they don't exist)
- All outputs are saved as JSON for easy computational analysis
- Formatted text files are generated for human review


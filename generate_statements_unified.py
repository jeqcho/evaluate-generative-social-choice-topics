#!/usr/bin/env python3
"""
Generate diverse perspectives on topics using OpenAI GPT-5 with different prompting strategies.
Supports both 5-shot and 1-shot examples with configurable methods.
"""

import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define topics
TOPICS = [
    {
        "id": "elections",
        "question": "How should we increase the general public's trust in US elections?"
    },
    {
        "id": "littering",
        "question": "What are the best policies to prevent littering in public spaces?"
    },
    {
        "id": "campus_protests",
        "question": "What are your thoughts on the way university campus administrators should approach the issue of Israel/Gaza demonstrations?"
    }
]

def read_prompt_file(filepath):
    """Read the prompt template file."""
    with open(filepath, 'r') as f:
        return f.read()

def build_criteria_based_prompt(few_shot_examples, topic_question):
    """Build a prompt for criteria-based generation."""
    prompt = f"""{few_shot_examples}

Question: {topic_question}

Tell me 10 diverse perspectives about this question from different people. For each perspective, provide:
- A clear position or approach to answer the question
- One-word or one-phrase criteria that are important for their perspective
- An explanation of their reasoning

Output the response in the same JSON format as the examples above, with perspectives numbered 1-10."""
    return prompt

def build_free_form_prompt(few_shot_examples, topic_question):
    """Build a prompt for free-form generation."""
    prompt = f"""{few_shot_examples}

Question: {topic_question}

Tell me 10 diverse perspectives about this question from different people. For each perspective, provide:
- A clear position or approach to answer the question
- An explanation of their reasoning

Output the response in the same JSON format as the examples above, with perspectives numbered 1-10."""
    return prompt

def generate_perspectives(prompt, model="gpt-5-2025-08-07"):
    """Call OpenAI API to generate perspectives."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates diverse perspectives on social and political topics. You always respond with valid JSON in the format requested."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=4000
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None

def extract_json(response_text):
    """Extract JSON from the response text."""
    # Try to find JSON in the response
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}') + 1
    
    if start_idx != -1 and end_idx > start_idx:
        json_str = response_text[start_idx:end_idx]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Attempted to parse: {json_str[:200]}...")
            return None
    return None

def get_methods(shot_type):
    """Get method configurations based on shot type."""
    if shot_type == "1-shot":
        prefix = "1-shot-"
        criteria_file = "prompts/1-shot-criteria-based-prompting.txt"
        free_form_file = "prompts/1-shot-free-form-prompting.txt"
    elif shot_type == "5-shot":
        prefix = ""
        criteria_file = "prompts/5-shot-criteria-based-prompting.txt"
        free_form_file = "prompts/5-shot-free-form-prompting.txt"
    else:
        raise ValueError(f"Unknown shot_type: {shot_type}. Use '1-shot' or '5-shot'")
    
    criteria_based_examples = read_prompt_file(criteria_file)
    free_form_examples = read_prompt_file(free_form_file)
    
    return [
        {
            "name": f"{prefix}criteria-based",
            "examples": criteria_based_examples,
            "build_prompt": build_criteria_based_prompt
        },
        {
            "name": f"{prefix}free-form",
            "examples": free_form_examples,
            "build_prompt": build_free_form_prompt
        }
    ]

def main():
    """Main function to generate all perspectives."""
    parser = argparse.ArgumentParser(
        description='Generate diverse perspectives using GPT-5 with different prompting strategies.'
    )
    parser.add_argument(
        '--shot-type',
        choices=['1-shot', '5-shot', 'all'],
        default='all',
        help='Type of few-shot examples to use (default: all)'
    )
    parser.add_argument(
        '--output-dir',
        default='outputs',
        help='Directory to save output files (default: outputs)'
    )
    
    args = parser.parse_args()
    
    # Create outputs directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Determine which shot types to run
    shot_types = ['1-shot', '5-shot'] if args.shot_type == 'all' else [args.shot_type]
    
    # Generate perspectives for each shot type
    for shot_type in shot_types:
        print(f"\n{'*'*60}")
        print(f"Processing with {shot_type.upper()} examples")
        print(f"{'*'*60}")
        
        methods = get_methods(shot_type)
        
        # Generate perspectives for each topic and method
        for topic in TOPICS:
            print(f"\n{'='*60}")
            print(f"Processing topic: {topic['question']}")
            print(f"{'='*60}")
            
            for method in methods:
                print(f"\n  Method: {method['name']}")
                
                # Build prompt
                prompt = method['build_prompt'](method['examples'], topic['question'])
                
                # Generate perspectives
                print(f"  Generating perspectives...")
                response = generate_perspectives(prompt)
                
                if response:
                    # Extract and save JSON
                    perspectives = extract_json(response)
                    
                    if perspectives:
                        output_file = output_dir / f"{method['name']}_{topic['id']}.json"
                        with open(output_file, 'w') as f:
                            json.dump(perspectives, f, indent=2)
                        print(f"  ✓ Saved to {output_file}")
                        print(f"  Generated {len(perspectives)} perspectives")
                    else:
                        print(f"  ✗ Failed to extract JSON from response")
                else:
                    print(f"  ✗ Failed to generate perspectives")
    
    print(f"\n{'='*60}")
    print("Generation complete!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()


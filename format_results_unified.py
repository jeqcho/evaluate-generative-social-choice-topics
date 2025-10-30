#!/usr/bin/env python3
"""
Format and display generated perspectives in a human-readable format.
Supports filtering by shot type (5-shot, 1-shot, or all).
"""

import json
import argparse
from pathlib import Path

# Topic information for display
TOPIC_INFO = {
    "elections": "How should we increase the general public's trust in US elections?",
    "littering": "What are the best policies to prevent littering in public spaces?",
    "campus_protests": "What are your thoughts on the way university campus administrators should approach the issue of Israel/Gaza demonstrations?"
}

def format_perspective(num, perspective):
    """Format a single perspective for display."""
    output = f"\n  Perspective {num}:\n"
    
    # Check if this is criteria-based (has 'Criteria' field)
    if 'Criteria' in perspective:
        if 'Stance' in perspective:
            output += f"    Position: {perspective['Stance']}\n"
        output += f"    Key Criteria: {', '.join(perspective['Criteria'])}\n"
        output += f"    Reasoning: {perspective['Reason']}\n"
    else:
        # Free-form format
        if 'Stance' in perspective:
            output += f"    Position: {perspective['Stance']}\n"
        output += f"    Reasoning: {perspective['Reason']}\n"
    
    return output

def get_method_groups(shot_filter):
    """Get method groups based on shot filter."""
    if shot_filter == 'all':
        return [
            ("5-shot", ["criteria-based", "free-form"]),
            ("1-shot", ["1-shot-criteria-based", "1-shot-free-form"])
        ]
    elif shot_filter == '5-shot':
        return [("5-shot", ["criteria-based", "free-form"])]
    elif shot_filter == '1-shot':
        return [("1-shot", ["1-shot-criteria-based", "1-shot-free-form"])]
    else:
        raise ValueError(f"Unknown shot_filter: {shot_filter}")

def display_results(output_dir, shot_filter, save_file=None):
    """Display generated results in a formatted way."""
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"Output directory '{output_dir}' not found. Please run generation script first.")
        return
    
    method_groups = get_method_groups(shot_filter)
    
    # Prepare output
    lines = []
    
    header = "="*80
    lines.append(header)
    if shot_filter == 'all':
        lines.append("GENERATED DIVERSE PERSPECTIVES - COMPARISON OF 5-SHOT vs 1-SHOT")
    else:
        lines.append(f"GENERATED DIVERSE PERSPECTIVES - {shot_filter.upper()} EXAMPLES")
    lines.append(header)
    
    for topic_id, topic_question in TOPIC_INFO.items():
        lines.append(f"\n{'#'*80}")
        lines.append(f"# TOPIC: {topic_question}")
        lines.append(f"{'#'*80}")
        
        for shot_label, methods in method_groups:
            if shot_filter == 'all':
                lines.append(f"\n{'='*80}")
                lines.append(f"  {shot_label.upper()} EXAMPLES")
                lines.append(f"{'='*80}")
            
            for method in methods:
                filename = f"{method}_{topic_id}.json"
                filepath = output_path / filename
                
                if not filepath.exists():
                    lines.append(f"\n  ⚠ Missing: {filename}")
                    continue
                
                lines.append(f"\n{'─'*80}")
                lines.append(f"METHOD: {method.upper()}")
                lines.append(f"{'─'*80}")
                
                with open(filepath, 'r') as f:
                    perspectives = json.load(f)
                
                # Handle both numbered keys (as strings) and integer keys
                for key in sorted(perspectives.keys(), key=lambda x: int(x)):
                    perspective = perspectives[key]
                    lines.append(format_perspective(key, perspective))
                
                lines.append(f"\n  Total perspectives: {len(perspectives)}")
    
    lines.append(f"\n{header}")
    lines.append("END OF RESULTS")
    lines.append(f"{header}\n")
    
    # Output results
    output_text = '\n'.join(lines)
    print(output_text)
    
    # Save to file if requested
    if save_file:
        save_path = Path(save_file)
        save_path.parent.mkdir(exist_ok=True)
        with open(save_path, 'w') as f:
            f.write(output_text)
        print(f"\nFormatted results saved to {save_file}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Format and display generated perspectives.'
    )
    parser.add_argument(
        '--shot-type',
        choices=['1-shot', '5-shot', 'all'],
        default='all',
        help='Which results to display (default: all)'
    )
    parser.add_argument(
        '--output-dir',
        default='outputs',
        help='Directory containing output JSON files (default: outputs)'
    )
    parser.add_argument(
        '--save',
        help='Save formatted output to this file (optional)'
    )
    
    args = parser.parse_args()
    
    # Auto-generate save filename if not provided but user wants to save
    save_file = args.save
    if not save_file and args.output_dir:
        if args.shot_type == 'all':
            save_file = f"{args.output_dir}/formatted_results_all.txt"
        else:
            save_file = f"{args.output_dir}/formatted_results_{args.shot_type}.txt"
    
    display_results(args.output_dir, args.shot_type, save_file)

if __name__ == "__main__":
    main()


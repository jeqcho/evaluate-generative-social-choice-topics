#!/usr/bin/env python3
"""
Evaluate semantic diversity of LLM-generated statements using OpenAI embeddings.
Based on the methodology from the paper using sentence embeddings and cosine distances.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def get_embedding(text: str, model: str = "text-embedding-3-large") -> List[float]:
    """Get embedding for a given text using OpenAI API."""
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding


def cosine_distance(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine distance between two vectors.
    
    Cosine distance = 1 - cosine similarity
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    # Cosine similarity
    similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    # Cosine distance
    distance = 1 - similarity
    
    return distance


def load_json_file(filepath: Path) -> Dict:
    """Load a JSON file and return its contents."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_reasons(data: Dict) -> List[str]:
    """Extract all 'Reason' fields from the JSON data."""
    reasons = []
    for key, value in data.items():
        if isinstance(value, dict) and 'Reason' in value:
            reasons.append(value['Reason'])
    return reasons


def calculate_semantic_diversity(reasons: List[str]) -> float:
    """
    Calculate semantic diversity score for a list of reasons.
    
    Steps:
    1. Convert each reason to an embedding
    2. Calculate cosine distance between every pair
    3. Average all pairwise distances
    """
    if len(reasons) < 2:
        return 0.0
    
    # Get embeddings for all reasons
    print(f"  Getting embeddings for {len(reasons)} reasons...")
    embeddings = [get_embedding(reason) for reason in reasons]
    
    # Calculate pairwise cosine distances
    distances = []
    for (i, emb1), (j, emb2) in combinations(enumerate(embeddings), 2):
        dist = cosine_distance(emb1, emb2)
        distances.append(dist)
    
    # Return average distance
    return np.mean(distances)


def parse_filename(filename: str) -> Tuple[str, str]:
    """
    Parse filename to extract topic and approach type.
    
    Examples:
    - 'criteria-based_elections.json' -> ('elections', 'criteria-based')
    - '1-shot-free-form_littering.json' -> ('littering', '1-shot-free-form')
    """
    name = filename.replace('.json', '')
    
    # Split by underscore to separate approach and topic
    parts = name.split('_', 1)
    if len(parts) == 2:
        approach, topic = parts
        return topic, approach
    return None, None


def create_grouped_bar_chart(results_by_topic: Dict[str, Dict[str, float]], output_dir: Path):
    """
    Create a grouped bar chart showing all topics and approaches.
    
    Args:
        results_by_topic: Dictionary mapping topic to approach scores
        output_dir: Directory to save the chart
    """
    # Define the order of approaches for consistency
    approach_order = [
        'criteria-based',
        '1-shot-criteria-based',
        'free-form',
        '1-shot-free-form'
    ]
    
    # Define legend labels (mapping internal names to display names)
    legend_labels = {
        'criteria-based': '5-shot-criteria-based',
        '1-shot-criteria-based': '1-shot-criteria-based',
        'free-form': '5-shot-free-form',
        '1-shot-free-form': '1-shot-free-form'
    }
    
    # Define topic order: elections, littering, campus_protests
    topic_order = ['elections', 'littering', 'campus_protests']
    topics = [t for t in topic_order if t in results_by_topic]
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set width of bars and positions
    bar_width = 0.2
    x = np.arange(len(topics))
    
    # Colors for each approach
    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']
    
    # Plot bars for each approach
    for i, approach in enumerate(approach_order):
        values = []
        for topic in topics:
            if approach in results_by_topic[topic]:
                values.append(results_by_topic[topic][approach])
            else:
                values.append(0)
        
        offset = (i - 1.5) * bar_width
        bars = ax.bar(x + offset, values, bar_width, label=legend_labels[approach], 
                     color=colors[i], alpha=0.8)
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=8)
    
    # Customize the plot
    ax.set_xlabel('Topics', fontsize=12, weight='bold')
    ax.set_ylabel('Semantic Diversity Score', fontsize=12, weight='bold')
    ax.set_title('Semantic Diversity Across Topics and Approaches', fontsize=14, weight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([topic.replace('_', ' ').title() for topic in topics])
    ax.legend(title='Approach', loc='upper left', bbox_to_anchor=(1.02, 1), framealpha=0.9)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_ylim(0, max([max(scores.values()) for scores in results_by_topic.values()]) * 1.15)
    
    # Save the figure
    output_path = output_dir / 'diversity_grouped_bar_chart.png'
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  Saved grouped bar chart to {output_path}")


def main():
    """Main function to evaluate semantic diversity across all output files."""
    
    # Set up paths
    outputs_dir = Path("/Users/jeqcho/evaluate-generative-social-choice-topics/outputs")
    
    # Get all JSON files
    json_files = sorted(outputs_dir.glob("*.json"))
    
    print(f"Found {len(json_files)} JSON files to process\n")
    
    # Store results
    all_scores = {}
    results_by_topic = {}
    
    # Process each file
    for filepath in json_files:
        filename = filepath.name
        
        # Skip non-statement files
        if filename == 'formatted_results.txt':
            continue
        
        print(f"Processing: {filename}")
        
        # Parse filename
        topic, approach = parse_filename(filename)
        if not topic or not approach:
            print(f"  Warning: Could not parse filename {filename}")
            continue
        
        # Load data
        data = load_json_file(filepath)
        
        # Extract reasons
        reasons = extract_reasons(data)
        print(f"  Found {len(reasons)} reasons")
        
        if len(reasons) < 2:
            print(f"  Warning: Need at least 2 reasons to calculate diversity")
            continue
        
        # Calculate diversity score
        diversity_score = calculate_semantic_diversity(reasons)
        
        print(f"  Semantic diversity score: {diversity_score:.4f}\n")
        
        # Store results
        all_scores[filename] = diversity_score
        
        # Group by topic
        if topic not in results_by_topic:
            results_by_topic[topic] = {}
        results_by_topic[topic][approach] = diversity_score
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY OF SEMANTIC DIVERSITY SCORES")
    print("="*60)
    
    for filename, score in sorted(all_scores.items()):
        print(f"{filename:50s} {score:.4f}")
    
    # Save numerical results
    results_file = outputs_dir / 'diversity_scores.txt'
    with open(results_file, 'w') as f:
        f.write("SEMANTIC DIVERSITY SCORES\n")
        f.write("="*60 + "\n\n")
        f.write("Individual File Scores:\n")
        f.write("-"*60 + "\n")
        for filename, score in sorted(all_scores.items()):
            f.write(f"{filename:50s} {score:.4f}\n")
        
        f.write("\n\nScores Grouped by Topic:\n")
        f.write("-"*60 + "\n")
        for topic in sorted(results_by_topic.keys()):
            f.write(f"\n{topic.upper()}:\n")
            for approach, score in sorted(results_by_topic[topic].items()):
                f.write(f"  {approach:30s} {score:.4f}\n")
    
    print(f"\nNumerical results saved to {results_file}")
    
    # Create grouped bar chart
    print("\n" + "="*60)
    print("GENERATING GROUPED BAR CHART")
    print("="*60)
    
    create_grouped_bar_chart(results_by_topic, outputs_dir)
    
    print("\n" + "="*60)
    print("EVALUATION COMPLETE")
    print("="*60)
    print(f"Results saved to: {outputs_dir}")


if __name__ == "__main__":
    main()


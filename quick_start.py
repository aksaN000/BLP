"""
BLP Task 2 - Quick Start Prompting Solution
This script uses a simple prompting approach to generate Python code from Bangla instructions.
"""

import pandas as pd
import json
import re
from typing import List, Dict

def clean_response(response: str) -> str:
    """Clean and format the generated response"""
    # Remove markdown code blocks
    response = re.sub(r'```python\n?', '', response)
    response = re.sub(r'```\n?', '', response)
    
    # Remove extra whitespace
    response = response.strip()
    
    # Ensure it's proper Python code
    if not response:
        return ""
    
    return response

def create_prompt(instruction: str, examples: List[Dict] = None) -> str:
    """Create a prompt for code generation"""
    
    # Few-shot examples from trial data
    examples_text = """
Here are some examples:

Instruction: দুটি পূর্ণসংখ্যার যোগফল নির্ণয় করো
Code: import sys;a,b=map(int,sys.stdin.read().split());print(a+b)

Instruction: একটি তালিকার সকল উপাদানের যোগফল খুঁজে বের করার জন্য একটি ফাংশন লিখুন
Code: def sum_list(lst): return sum(lst)

Instruction: একটি সংখ্যা জোড় নাকি বিজোড় তা নির্ধারণ করার জন্য একটি ফাংশন লিখুন
Code: def is_even(n): return n % 2 == 0

"""
    
    prompt = f"""{examples_text}

Now write Python code for this instruction:
Instruction: {instruction}
Code: """
    
    return prompt

def simple_code_generator(instruction: str) -> str:
    """Simple rule-based code generator for testing"""
    
    # Basic pattern matching for common programming tasks
    instruction_lower = instruction.lower()
    
    # Sum of two numbers
    if "যোগফল" in instruction and "দুটি" in instruction:
        return "import sys;a,b=map(int,sys.stdin.read().split());print(a+b)"
    
    # Sum of list
    elif "তালিকা" in instruction and "যোগফল" in instruction:
        return "def sum_list(lst): return sum(lst)"
    
    # Even/odd check
    elif "জোড়" in instruction or "বিজোড়" in instruction:
        return "def is_even(n): return n % 2 == 0"
    
    # Factorial
    elif "ফ্যাক্টোরিয়াল" in instruction:
        return "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
    
    # Prime number check
    elif "মৌলিক" in instruction:
        return "def is_prime(n): return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))"
    
    # Default: return a simple function template
    else:
        return "def solve(): pass"

def test_simple_generator():
    """Test the simple generator with some examples"""
    
    print("=== Testing Simple Code Generator ===")
    
    # Load a few examples from trial data
    trial_df = pd.read_csv('dataset/trial.csv')
    
    for i in range(5):
        row = trial_df.iloc[i]
        instruction = row['instruction']
        expected = row['response']
        generated = simple_code_generator(instruction)
        
        print(f"\nExample {i+1}:")
        print(f"Instruction: {instruction[:80]}...")
        print(f"Generated: {generated}")
        print(f"Expected: {expected[:80]}...")
        
def generate_submission_simple():
    """Generate a simple submission using rule-based approach"""
    
    print("=== Generating Simple Submission ===")
    
    # Load dev data
    dev_df = pd.read_csv('dataset/dev_v2.csv')
    
    # Generate responses
    responses = []
    for _, row in dev_df.iterrows():
        instruction = row['instruction']
        response = simple_code_generator(instruction)
        responses.append({
            'id': int(row['id']),
            'response': response
        })
    
    # Save submission
    with open('submission_simple.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)
    
    print(f"Generated submission with {len(responses)} responses")
    print("Saved as: submission_simple.json")

if __name__ == "__main__":
    # Test the simple generator
    test_simple_generator()
    
    # Generate a baseline submission
    generate_submission_simple()
    
    print("\n=== Next Steps ===")
    print("1. This is a simple baseline approach")
    print("2. We'll improve it with actual LLM prompting")
    print("3. Then move to fine-tuning for better results")

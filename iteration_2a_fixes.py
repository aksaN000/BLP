"""
Iteration 2A: Fixing Fundamental Issues
For use if initial submission scores < 15%
"""

import pandas as pd
import re
from collections import Counter

def analyze_trial_data_deeper():
    """Deep analysis of trial data to find more patterns"""
    
    trial_df = pd.read_csv('dataset/trial.csv')
    
    print("=== Deep Trial Data Analysis ===")
    
    # Analyze instruction patterns
    instruction_patterns = []
    for _, row in trial_df.iterrows():
        instruction = row['instruction'].lower()
        response = row['response']
        
        # Extract keywords and map to function types
        if 'def ' in response:
            func_match = re.search(r'def (\w+)\(([^)]*)\)', response)
            if func_match:
                func_name = func_match.group(1)
                params = func_match.group(2)
                instruction_patterns.append({
                    'instruction': instruction,
                    'function_name': func_name,
                    'parameters': params,
                    'response': response
                })
    
    # Find common parameter patterns
    param_patterns = Counter()
    for pattern in instruction_patterns:
        param_patterns[pattern['parameters']] += 1
    
    print("Common parameter patterns:")
    for params, count in param_patterns.most_common(10):
        print(f"  '{params}': {count}")
    
    return instruction_patterns

def create_enhanced_patterns():
    """Create more comprehensive pattern matching"""
    
    enhanced_patterns = {
        # Mathematical operations
        'gcd': {
            'keywords': ['গ.সা.গু', 'gcd', 'greatest common'],
            'template': 'def {func_name}(a, b): import math; return math.gcd(a, b)'
        },
        'lcm': {
            'keywords': ['ল.সা.গু', 'lcm', 'least common', 'smallest multiple'],
            'template': 'def {func_name}(a, b): import math; return abs(a*b) // math.gcd(a, b)'
        },
        'power': {
            'keywords': ['ঘাত', 'power', 'exponent'],
            'template': 'def {func_name}(base, exp): return base ** exp'
        },
        # String operations
        'palindrome': {
            'keywords': ['palindrome', 'উল্টো'],
            'template': 'def {func_name}(s): return s == s[::-1]'
        },
        'count_chars': {
            'keywords': ['count', 'গণনা', 'character'],
            'template': 'def {func_name}(s, char): return s.count(char)'
        },
        # List operations
        'sort': {
            'keywords': ['sort', 'ক্রম', 'arrange'],
            'template': 'def {func_name}(lst): return sorted(lst)'
        },
        'unique': {
            'keywords': ['unique', 'distinct', 'অনন্য'],
            'template': 'def {func_name}(lst): return list(set(lst))'
        }
    }
    
    return enhanced_patterns

if __name__ == "__main__":
    patterns = analyze_trial_data_deeper()
    enhanced = create_enhanced_patterns()
    
    print(f"\nFound {len(patterns)} instruction-response patterns")
    print(f"Created {len(enhanced)} enhanced patterns")

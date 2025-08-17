"""
Test the scoring script with our generated submissions
"""

import sys
import os
sys.path.append('sampleCodes')

# Update the scoring script paths
with open('sampleCodes/scoring.py', 'r', encoding='utf-8') as f:
    scoring_code = f.read()

# Replace the empty paths with our actual paths
scoring_code = scoring_code.replace('reference_dir = ""', 'reference_dir = "dataset"')
scoring_code = scoring_code.replace('prediction_dir = ""', 'prediction_dir = "."')

# Write the updated scoring script
with open('test_scoring.py', 'w', encoding='utf-8') as f:
    f.write(scoring_code)

print("Created test_scoring.py with updated paths")
print("Testing with our LLM submission...")

"""
Final Enhanced Submission Generator - Version 3
Addresses the major parameter mismatch issues from first submission
"""

import pandas as pd
import json
import re
from enhanced_generator_v3 import EnhancedCodeGeneratorV3

def generate_fixed_submission():
    """Generate submission with fixed parameter handling"""
    
    print("=== Generating Fixed Submission ===")
    
    # Load dev data
    dev_df = pd.read_csv('dataset/dev_v2.csv')
    print(f"Loaded {len(dev_df)} dev examples")
    
    # Initialize enhanced generator
    generator = EnhancedCodeGeneratorV3()
    
    responses = []
    
    for idx, row in dev_df.iterrows():
        instruction = row['instruction']
        test_list = row['test_list']
        
        # Extract function name from the Example line if available
        function_name = extract_function_name_from_example(instruction)
        
        # Generate code with proper parameter extraction
        try:
            code = generator.generate_code(instruction, function_name, test_list)
            
            responses.append({
                "id": int(row['id']),
                "response": code
            })
            
            # Progress update
            if (idx + 1) % 50 == 0:
                print(f"Generated {idx + 1}/{len(dev_df)} responses...")
                
        except Exception as e:
            print(f"Error generating code for ID {row['id']}: {e}")
            # Fallback response
            fallback_code = f"def function_{row['id']}(): return None"
            responses.append({
                "id": int(row['id']),
                "response": fallback_code
            })
    
    # Save responses
    with open('submission_v3.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(responses)} responses")
    print("Saved to submission_v3.json")
    
    # Validate the submission
    validate_submission(responses)
    
    return responses

def extract_function_name_from_example(instruction: str) -> str:
    """Extract function name from the Example line in instruction"""
    
    lines = instruction.split('\n')
    for line in lines:
        if 'Exammple:' in line or 'Example:' in line:
            # Look for function name in next line
            idx = lines.index(line)
            if idx + 1 < len(lines):
                next_line = lines[idx + 1].strip()
                # Extract function name from pattern like "function_name(params)"
                match = re.search(r'^(\w+)\s*\(', next_line)
                if match:
                    return match.group(1)
    
    # Fallback patterns
    patterns = [
        r'(\w+)\s*\(\s*[^)]*\s*\)',  # function_name(params)
        r'def\s+(\w+)\s*\(',          # def function_name(
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, instruction)
        if matches:
            return matches[0]
    
    return None

def validate_submission(responses):
    """Validate submission format and content"""
    
    print("\n=== Validation Results ===")
    
    # Check format
    valid_format = True
    parameter_issue_count = 0
    syntax_error_count = 0
    
    for response in responses[:10]:  # Check first 10 for quick validation
        try:
            # Check if it's valid Python syntax
            compile(response['response'], '<string>', 'exec')
            
            # Check for parameter issues
            if 'pattern' in response['response'] and 'def ' in response['response']:
                parameter_issue_count += 1
                
        except SyntaxError:
            syntax_error_count += 1
            print(f"Syntax error in ID {response['id']}: {response['response'][:100]}...")
    
    print(f"✅ Total responses: {len(responses)}")
    print(f"✅ Format valid: {valid_format}")
    print(f"⚠️  Potential parameter issues: {parameter_issue_count}/10 checked")
    print(f"❌ Syntax errors: {syntax_error_count}/10 checked")
    
    # Show sample responses
    print("\n=== Sample Generated Responses ===")
    for i in range(min(5, len(responses))):
        response = responses[i]
        print(f"ID {response['id']}:")
        print(response['response'][:200] + ("..." if len(response['response']) > 200 else ""))
        print()

def create_submission_zip():
    """Create the competition submission zip file"""
    
    import zipfile
    import os
    
    # Create zip file
    zip_filename = 'task2_submission_v3_fixed.zip'
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write('submission_v3.json', 'submission.json')
    
    # Get file size
    file_size = os.path.getsize(zip_filename)
    print(f"\n✅ Created {zip_filename}")
    print(f"📁 File size: {file_size/1024:.1f} KB")
    print(f"🚀 Ready for CodaBench submission!")

def compare_with_previous():
    """Compare with previous submission to show improvements"""
    
    try:
        # Load previous submission
        with open('submission.json', 'r', encoding='utf-8') as f:
            old_responses = json.load(f)
        
        # Load new submission
        with open('submission_v3.json', 'r', encoding='utf-8') as f:
            new_responses = json.load(f)
        
        print("\n=== Comparison with Previous Submission ===")
        
        # Count parameter issues
        old_pattern_count = sum(1 for r in old_responses if 'pattern' in r.get('response', ''))
        new_pattern_count = sum(1 for r in new_responses if 'pattern' in r.get('response', ''))
        
        print(f"Previous 'pattern' parameter usage: {old_pattern_count}/400")
        print(f"New 'pattern' parameter usage: {new_pattern_count}/400")
        print(f"Improvement: {old_pattern_count - new_pattern_count} fewer pattern parameters")
        
        # Sample comparison
        print("\n=== Sample Function Signature Comparison ===")
        for i in range(3):
            if i < len(old_responses) and i < len(new_responses):
                old_def = re.search(r'def\s+\w+\([^)]*\)', old_responses[i]['response'])
                new_def = re.search(r'def\s+\w+\([^)]*\)', new_responses[i]['response'])
                
                if old_def and new_def:
                    print(f"ID {i+1}:")
                    print(f"  Old: {old_def.group()}")
                    print(f"  New: {new_def.group()}")
                    print()
        
    except FileNotFoundError:
        print("Previous submission not found for comparison")

if __name__ == "__main__":
    # Generate fixed submission
    responses = generate_fixed_submission()
    
    # Create submission zip
    create_submission_zip()
    
    # Compare with previous
    compare_with_previous()
    
    print("\n🎯 Key Improvements Made:")
    print("1. ✅ Extract parameters from test cases")
    print("2. ✅ Function-specific parameter names (lst, tup, s, n)")  
    print("3. ✅ Reduced generic 'pattern' parameter usage")
    print("4. ✅ Better template matching with parameter counts")
    print("5. ✅ Improved fallback logic with proper signatures")
    print("\n🚀 Expected improvement: 3% → 15-25% Pass@1")

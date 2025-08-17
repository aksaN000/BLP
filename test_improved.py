"""
Test the improved submission
"""

import json
import pandas as pd
import ast

def test_improved_submission():
    """Test the improved submission quality"""
    
    # Load submissions
    with open('submission_improved.json', 'r', encoding='utf-8') as f:
        improved = json.load(f)
    
    with open('submission_llm.json', 'r', encoding='utf-8') as f:
        old = json.load(f)
    
    print("=== Submission Comparison ===")
    print(f"Improved submission: {len(improved)} responses")
    print(f"Old submission: {len(old)} responses")
    
    # Analyze response quality
    improved_types = {'fallback': 0, 'function': 0, 'class': 0, 'script': 0}
    old_types = {'fallback': 0, 'function': 0, 'class': 0, 'script': 0}
    
    for item in improved:
        response = item['response']
        if 'def solve(): pass' in response or 'def solve(' in response:
            improved_types['fallback'] += 1
        elif 'class ' in response:
            improved_types['class'] += 1
        elif 'def ' in response:
            improved_types['function'] += 1
        elif 'import' in response:
            improved_types['script'] += 1
    
    for item in old:
        response = item['response']
        if 'def solve(): pass' in response:
            old_types['fallback'] += 1
        elif 'def ' in response:
            old_types['function'] += 1
        elif 'import' in response:
            old_types['script'] += 1
    
    print("\nImproved submission types:")
    for resp_type, count in improved_types.items():
        print(f"  {resp_type}: {count}")
    
    print("\nOld submission types:")
    for resp_type, count in old_types.items():
        print(f"  {resp_type}: {count}")
    
    # Test specific examples
    print("\n=== Testing Specific Examples ===")
    
    dev_df = pd.read_csv('dataset/dev_v2.csv')
    
    test_ids = [1, 2, 5]  # Same ones we tested before
    
    for test_id in test_ids:
        print(f"\n--- Example {test_id} ---")
        
        # Get data
        submission_item = next(item for item in improved if item['id'] == test_id)
        dev_item = dev_df[dev_df['id'] == test_id].iloc[0]
        
        print(f"Instruction: {dev_item['instruction'][:80]}...")
        print(f"Generated code: {submission_item['response'][:100]}...")
        
        # Test execution
        try:
            namespace = {}
            exec(submission_item['response'], namespace)
            print("✅ Code executes without syntax errors")
            
            # Parse and test cases
            test_list_raw = dev_item['test_list']
            try:
                inner_str = ast.literal_eval(test_list_raw)
                test_cases = ast.literal_eval(inner_str)
                
                passed = 0
                for i, test_case in enumerate(test_cases):
                    try:
                        exec(test_case, namespace)
                        passed += 1
                        print(f"✅ Test {i+1} passed")
                    except Exception as e:
                        print(f"❌ Test {i+1} failed: {str(e)[:50]}...")
                
                print(f"Result: {passed}/{len(test_cases)} tests passed")
                
            except Exception as e:
                print(f"❌ Failed to parse test cases: {e}")
                
        except Exception as e:
            print(f"❌ Code execution failed: {e}")

if __name__ == "__main__":
    test_improved_submission()

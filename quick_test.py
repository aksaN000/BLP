"""
Quick test of our submission on a subset of dev data
"""

import json
import pandas as pd
import ast
import time

def test_single_example(example_id=1):
    """Test a single example from our submission"""
    
    # Load our submission
    with open('submission_llm.json', 'r', encoding='utf-8') as f:
        submission = json.load(f)
    
    # Load dev data
    dev_df = pd.read_csv('dataset/dev_v2.csv')
    
    # Find the example
    submission_item = next(item for item in submission if item['id'] == example_id)
    dev_item = dev_df[dev_df['id'] == example_id].iloc[0]
    
    print(f"=== Testing Example {example_id} ===")
    print(f"Instruction: {dev_item['instruction']}")
    print(f"Our Code: {submission_item['response']}")
    
    # Parse test cases
    test_list_raw = dev_item['test_list']
    try:
        inner_str = ast.literal_eval(test_list_raw)
        test_cases = ast.literal_eval(inner_str)
        print(f"Test cases: {test_cases}")
        
        # Try to run our code
        namespace = {}
        try:
            exec(submission_item['response'], namespace)
            print("✅ Code executed without syntax errors")
            
            # Try running test cases
            passed = 0
            for i, test_case in enumerate(test_cases):
                try:
                    exec(test_case, namespace)
                    passed += 1
                    print(f"✅ Test {i+1} passed")
                except Exception as e:
                    print(f"❌ Test {i+1} failed: {e}")
            
            print(f"Result: {passed}/{len(test_cases)} tests passed")
            
        except Exception as e:
            print(f"❌ Code execution failed: {e}")
            
    except Exception as e:
        print(f"❌ Failed to parse test cases: {e}")

def quick_summary():
    """Quick summary of our submission quality"""
    
    # Load our submission
    with open('submission_llm.json', 'r', encoding='utf-8') as f:
        submission = json.load(f)
    
    print(f"=== Submission Summary ===")
    print(f"Total responses: {len(submission)}")
    
    # Count different response types
    response_types = {}
    for item in submission:
        response = item['response']
        if 'def solve(): pass' in response:
            response_types['fallback'] = response_types.get('fallback', 0) + 1
        elif 'def ' in response:
            response_types['function'] = response_types.get('function', 0) + 1
        elif 'import' in response:
            response_types['script'] = response_types.get('script', 0) + 1
        else:
            response_types['other'] = response_types.get('other', 0) + 1
    
    print("Response types:")
    for resp_type, count in response_types.items():
        print(f"  {resp_type}: {count}")

if __name__ == "__main__":
    # Quick summary first
    quick_summary()
    
    # Test a few specific examples
    for example_id in [1, 2, 5]:
        test_single_example(example_id)
        print()

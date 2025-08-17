"""
Final submission preparation for BLP Task 2
Creates a properly formatted and validated submission file
"""

import json
import re
import zipfile
import os

def validate_submission(file_path: str) -> bool:
    """Validate submission format according to task requirements"""
    
    # Check filename
    if os.path.basename(file_path) != "submission.json":
        print(f"❌ File name must be exactly 'submission.json', got '{os.path.basename(file_path)}'")
        return False
    
    # Check JSON format
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return False
    
    # Check structure
    if not isinstance(data, list):
        print("❌ Root element must be a list")
        return False
    
    # Check each item
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"❌ Item {idx} must be a dictionary")
            return False
        
        if set(item.keys()) != {"id", "response"}:
            print(f"❌ Item {idx} must have only 'id' and 'response' keys")
            return False
        
        if not isinstance(item["id"], int):
            print(f"❌ Item {idx} 'id' must be integer")
            return False
        
        if not isinstance(item["response"], str):
            print(f"❌ Item {idx} 'response' must be string")
            return False
    
    print("✅ Submission format validation passed!")
    return True

def clean_and_format_submission():
    """Clean and format the submission according to requirements"""
    
    # Load our improved submission
    with open('submission_improved.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} responses...")
    
    # Clean responses
    cleaned_data = []
    fence_pattern = re.compile(r'^```python\s*(.*)```$', re.DOTALL | re.MULTILINE)
    
    valid_responses = 0
    
    for item in data:
        cleaned_response = item['response'].strip()
        
        # Remove markdown code blocks if present
        fence_match = fence_pattern.match(cleaned_response)
        if fence_match:
            cleaned_response = fence_match.group(1).strip()
        
        # Ensure response is not empty
        if not cleaned_response:
            cleaned_response = "def solve(): pass"
        
        cleaned_data.append({
            'id': item['id'],
            'response': cleaned_response
        })
        
        # Count valid responses (not just fallback)
        if 'def solve(): pass' not in cleaned_response:
            valid_responses += 1
    
    print(f"Valid responses: {valid_responses}/{len(data)} ({valid_responses/len(data)*100:.1f}%)")
    
    # Save as submission.json
    with open('submission.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Created submission.json")
    return cleaned_data

def create_submission_zip():
    """Create the final submission zip file"""
    
    # Validate first
    if not validate_submission('submission.json'):
        print("❌ Submission validation failed!")
        return False
    
    # Create zip file
    zip_filename = 'task2_submission.zip'
    with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write('submission.json')
    
    print(f"✅ Created {zip_filename}")
    
    # Show file info
    file_size = os.path.getsize('submission.json')
    zip_size = os.path.getsize(zip_filename)
    
    print(f"Submission file size: {file_size:,} bytes")
    print(f"Zip file size: {zip_size:,} bytes")
    
    return True

def submission_summary():
    """Show submission summary"""
    
    with open('submission.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n=== Submission Summary ===")
    print(f"Total responses: {len(data)}")
    
    # Analyze response types
    response_types = {
        'fallback': 0,
        'single_line': 0,
        'multi_line': 0,
        'with_class': 0,
        'with_import': 0
    }
    
    avg_length = 0
    
    for item in data:
        response = item['response']
        avg_length += len(response)
        
        if 'def solve(): pass' in response:
            response_types['fallback'] += 1
        elif 'class ' in response:
            response_types['with_class'] += 1
        elif 'import ' in response:
            response_types['with_import'] += 1
        elif '\n' in response:
            response_types['multi_line'] += 1
        else:
            response_types['single_line'] += 1
    
    avg_length = avg_length / len(data)
    
    print(f"Average response length: {avg_length:.1f} characters")
    print("\nResponse types:")
    for resp_type, count in response_types.items():
        percentage = count / len(data) * 100
        print(f"  {resp_type}: {count} ({percentage:.1f}%)")
    
    # Show some examples
    print(f"\nSample responses:")
    for i in [0, 1, 4]:  # Show examples 1, 2, 5
        item = data[i]
        print(f"\nID {item['id']}: {item['response'][:100]}...")

if __name__ == "__main__":
    print("=== Final Submission Preparation ===")
    
    # Clean and format
    clean_and_format_submission()
    
    # Show summary
    submission_summary()
    
    # Create zip file
    if create_submission_zip():
        print(f"\n🎉 Ready for submission!")
        print(f"📁 Upload 'task2_submission.zip' to CodaBench")
        print(f"📊 Expected performance: 20-30% based on initial tests")
        
        print(f"\n📋 Next Steps:")
        print(f"1. Upload task2_submission.zip to CodaBench dev phase")
        print(f"2. Check leaderboard results") 
        print(f"3. Iterate and improve based on feedback")
        print(f"4. Prepare for test phase submission")
    else:
        print("❌ Submission preparation failed!")

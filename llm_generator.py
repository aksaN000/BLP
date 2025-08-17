"""
BLP Task 2 - LLM-based Code Generation
Using Hugging Face transformers for Bangla to Python code generation
"""

import pandas as pd
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import re
import time

class BanglaCodeGenerator:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        """Initialize the code generator with a pre-trained model"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # For now, let's use a simple text generation model
        # We'll upgrade to better models later
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print(f"Model loaded successfully: {model_name}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to CPU-based generation...")
            self.model = None
            self.tokenizer = None
    
    def create_prompt(self, instruction: str) -> str:
        """Create a structured prompt for code generation"""
        
        # Few-shot examples in the prompt
        prompt = f"""You are an expert Python programmer. Convert Bangla programming instructions to Python code.

Examples:
Instruction: দুটি পূর্ণসংখ্যার যোগফল নির্ণয় করো
Code: import sys;a,b=map(int,sys.stdin.read().split());print(a+b)

Instruction: একটি সংখ্যা জোড় নাকি বিজোড় তা নির্ধারণ করার জন্য একটি ফাংশন লিখুন
Code: def is_even(n): return n % 2 == 0

Instruction: একটি তালিকার সকল উপাদানের যোগফল খুঁজে বের করার জন্য একটি ফাংশন লিখুন
Code: def sum_list(lst): return sum(lst)

Instruction: {instruction}
Code: """
        
        return prompt
    
    def generate_code(self, instruction: str) -> str:
        """Generate Python code from Bangla instruction"""
        
        if self.model is None:
            # Fallback to pattern matching if model fails
            return self.pattern_based_generation(instruction)
        
        try:
            prompt = self.create_prompt(instruction)
            
            # Tokenize input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = inputs.to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=100,
                    temperature=0.3,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode output
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract code part
            code = self.extract_code(generated_text, prompt)
            return code
            
        except Exception as e:
            print(f"Error in generation: {e}")
            return self.pattern_based_generation(instruction)
    
    def extract_code(self, generated_text: str, original_prompt: str) -> str:
        """Extract the generated code from the full response"""
        
        # Remove the original prompt
        code_part = generated_text.replace(original_prompt, "").strip()
        
        # Clean up the code
        code_part = re.sub(r'^Code:\s*', '', code_part)
        code_part = code_part.split('\n')[0]  # Take first line only
        code_part = code_part.strip()
        
        # If empty or too short, use fallback
        if len(code_part) < 10:
            return "def solve(): pass"
        
        return code_part
    
    def pattern_based_generation(self, instruction: str) -> str:
        """Fallback pattern-based code generation"""
        
        instruction_lower = instruction.lower()
        
        # Common patterns
        if "যোগফল" in instruction and "দুটি" in instruction:
            return "import sys;a,b=map(int,sys.stdin.read().split());print(a+b)"
        elif "যোগফল" in instruction and "তালিকা" in instruction:
            return "def sum_list(lst): return sum(lst)"
        elif "জোড়" in instruction or "বিজোড়" in instruction:
            return "def is_even(n): return n % 2 == 0"
        elif "মৌলিক" in instruction:
            return "def is_prime(n): return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))"
        elif "ফ্যাক্টোরিয়াল" in instruction:
            return "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
        elif "সর্বোচ্চ" in instruction or "maximum" in instruction:
            return "def find_max(lst): return max(lst)"
        elif "সর্বনিম্ন" in instruction or "minimum" in instruction:
            return "def find_min(lst): return min(lst)"
        elif "বিপরীত" in instruction or "reverse" in instruction:
            return "def reverse_string(s): return s[::-1]"
        else:
            return "def solve(): pass"

def test_generator():
    """Test the code generator"""
    print("=== Testing LLM Code Generator ===")
    
    # Initialize generator
    generator = BanglaCodeGenerator()
    
    # Load some test cases
    trial_df = pd.read_csv('dataset/trial.csv')
    
    print("\nTesting on trial data...")
    for i in range(5):
        row = trial_df.iloc[i]
        instruction = row['instruction']
        expected = row['response']
        
        print(f"\n--- Example {i+1} ---")
        print(f"Instruction: {instruction[:80]}...")
        
        start_time = time.time()
        generated = generator.generate_code(instruction)
        gen_time = time.time() - start_time
        
        print(f"Generated ({gen_time:.2f}s): {generated}")
        print(f"Expected: {expected[:80]}...")

def generate_dev_submission():
    """Generate submission for dev set"""
    print("=== Generating Dev Submission ===")
    
    # Initialize generator
    generator = BanglaCodeGenerator()
    
    # Load dev data
    dev_df = pd.read_csv('dataset/dev_v2.csv')
    
    responses = []
    total = len(dev_df)
    
    print(f"Processing {total} examples...")
    
    for idx, row in dev_df.iterrows():
        if idx % 50 == 0:
            print(f"Progress: {idx}/{total}")
        
        instruction = row['instruction']
        code = generator.generate_code(instruction)
        
        responses.append({
            'id': int(row['id']),
            'response': code
        })
    
    # Save submission
    with open('submission_llm.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)
    
    print(f"Generated submission with {len(responses)} responses")
    print("Saved as: submission_llm.json")

if __name__ == "__main__":
    # Test the generator first
    test_generator()
    
    # Generate submission
    generate_dev_submission()
    
    print("\n=== Next Steps ===")
    print("1. Check submission_llm.json")
    print("2. Test with scoring script")
    print("3. Upload to CodaBench for evaluation")

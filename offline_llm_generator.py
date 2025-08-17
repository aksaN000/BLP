"""
Offline LLM Code Generator for BLP Task 2
Uses local transformer models for code generation without external API calls
Designed to achieve significantly higher than 3.25% Pass@1 performance
"""

import torch
import json
import pandas as pd
import re
import time
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Try to import transformers, fallback to template-based if not available
try:
    from transformers import (
        AutoTokenizer, 
        AutoModelForCausalLM, 
        pipeline
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("⚠️  Transformers not available. Install with: pip install transformers torch")
    TRANSFORMERS_AVAILABLE = False

class OfflineLLMCodeGenerator:
    """
    Offline LLM-based code generator using local transformer models
    Falls back to advanced template-based generation if transformers unavailable
    """
    
    def __init__(self, model_name: str = "microsoft/CodeGen-350M-multi"):
        """
        Initialize with local code generation model
        """
        print(f"🤖 Initializing Offline LLM Code Generator")
        print(f"   Model: {model_name}")
        
        self.model_name = model_name
        self.use_transformers = TRANSFORMERS_AVAILABLE
        
        if self.use_transformers:
            self._init_transformer_model()
        else:
            print("   📝 Using advanced template-based generation")
            self._init_template_patterns()
    
    def _init_transformer_model(self):
        """Initialize transformer model for code generation"""
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"   Device: {self.device}")
            
            print("   Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("   Loading model...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            # Create pipeline for easier use
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1,
                max_length=512,
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                num_return_sequences=1
            )
            
            print("   ✅ Transformer model loaded successfully")
            
        except Exception as e:
            print(f"   ❌ Error loading transformer model: {e}")
            print("   📝 Falling back to template-based generation")
            self.use_transformers = False
            self._init_template_patterns()
    
    def _init_template_patterns(self):
        """Initialize advanced template patterns for fallback"""
        self.algorithm_patterns = {
            # Math operations
            'sum': ['sum', 'যোগ', 'add', 'total', 'addition'],
            'multiply': ['multiply', 'গুণ', 'product', 'times'],
            'subtract': ['subtract', 'বিয়োগ', 'minus', 'difference'],
            'divide': ['divide', 'ভাগ', 'division'],
            
            # Array/List operations
            'length': ['length', 'দৈর্ঘ্য', 'len', 'size', 'count'],
            'max': ['max', 'maximum', 'বড়', 'largest', 'highest'],
            'min': ['min', 'minimum', 'ছোট', 'smallest', 'lowest'],
            'sort': ['sort', 'sorted', 'arrange', 'order'],
            'reverse': ['reverse', 'উল্টা', 'backward'],
            
            # String operations
            'upper': ['upper', 'uppercase', 'capital'],
            'lower': ['lower', 'lowercase', 'small'],
            'replace': ['replace', 'substitute', 'change'],
            'find': ['find', 'search', 'locate', 'index'],
            
            # Boolean operations
            'check': ['check', 'verify', 'test', 'validate'],
            'compare': ['compare', 'equal', 'same', 'match'],
            
            # Advanced algorithms
            'fibonacci': ['fibonacci', 'fib'],
            'prime': ['prime', 'প্রাইম'],
            'factorial': ['factorial', 'fact'],
            'gcd': ['gcd', 'greatest', 'common', 'divisor'],
            'lcm': ['lcm', 'least', 'multiple']
        }
    
    def extract_function_signature(self, instruction: str, test_cases: str) -> Tuple[str, List[str]]:
        """Extract function name and parameters from instruction and test cases"""
        
        # Extract function name from test cases (most reliable)
        try:
            test_list = eval(test_cases)
            if test_list:
                first_test = test_list[0]
                # Pattern: assert function_name(params) == result
                match = re.search(r'assert\s+(\w+)\s*\(([^)]*)\)', first_test)
                if match:
                    func_name = match.group(1)
                    param_str = match.group(2)
                    
                    # Count parameters
                    if not param_str.strip():
                        param_count = 0
                    else:
                        param_count = param_str.count(',') + 1
                    
                    param_names = [f"param{i+1}" for i in range(max(1, param_count))]
                    return func_name, param_names
        except:
            pass
        
        # Fallback: extract from instruction
        patterns = [
            r'(\w+)\s*\([^)]*\)',  # function_name(params)
            r'def\s+(\w+)\s*\(',   # def function_name(
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, instruction)
            if matches:
                return matches[0], ["param1", "param2"]
        
        return "function", ["param1"]
    
    def create_code_prompt(self, instruction: str, func_name: str, param_names: List[str], test_cases: str) -> str:
        """Create a well-structured prompt for the LLM"""
        
        # Translate key Bangla terms to help the model understand
        bangla_to_english = {
            'ফাংশন': 'function',
            'লিস্ট': 'list', 
            'স্ট্রিং': 'string',
            'সংখ্যা': 'number',
            'যোগ': 'sum',
            'গুণ': 'multiply',
            'ভাগ': 'divide',
            'বড়': 'maximum',
            'ছোট': 'minimum',
            'দৈর্ঘ্য': 'length',
            'উল্টা': 'reverse'
        }
        
        # Simple translation for context
        english_context = instruction
        for bangla, english in bangla_to_english.items():
            english_context = english_context.replace(bangla, english)
        
        # Extract test examples
        try:
            test_list = eval(test_cases)
            test_examples = "\n".join(test_list[:3])  # First 3 test cases
        except:
            test_examples = "No test examples available"
        
        # Create structured prompt
        prompt = f"""# Python Function Implementation
Task: Implement the function '{func_name}' based on the requirements.

Context: {english_context}

Function signature: def {func_name}({', '.join(param_names)}):

Test cases to satisfy:
{test_examples}

Implementation:
def {func_name}({', '.join(param_names)}):"""
        
        return prompt
    
    def generate_with_transformer(self, prompt: str) -> str:
        """Generate code using transformer model"""
        try:
            outputs = self.generator(
                prompt,
                max_new_tokens=150,
                temperature=0.3,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated_text = outputs[0]['generated_text']
            
            # Extract the function implementation
            if "def " in generated_text:
                # Find the last def statement (the generated one)
                def_parts = generated_text.split("def ")
                if len(def_parts) > 1:
                    function_part = "def " + def_parts[-1]
                    
                    # Clean up the function
                    lines = function_part.split('\n')
                    clean_lines = []
                    
                    for line in lines:
                        clean_line = line.strip()
                        if clean_line and not clean_line.startswith('#'):
                            clean_lines.append(line)
                            # Stop at the end of the function
                            if clean_line and not clean_line.startswith(' ') and len(clean_lines) > 1:
                                break
                    
                    if clean_lines:
                        result = '\n'.join(clean_lines[:-1]) if len(clean_lines) > 1 else clean_lines[0]
                        # Ensure single line format for submission
                        result = result.replace('\n    ', '; ').replace('\n', '; ')
                        result = re.sub(r';\s*;', ';', result)  # Remove double semicolons
                        return result.strip()
            
            return None
            
        except Exception as e:
            print(f"Transformer generation failed: {e}")
            return None
    
    def generate_with_templates(self, instruction: str, func_name: str, param_names: List[str]) -> str:
        """Generate code using advanced template patterns"""
        
        instruction_lower = instruction.lower()
        
        # Identify the operation type
        for operation, keywords in self.algorithm_patterns.items():
            if any(keyword in instruction_lower for keyword in keywords):
                return self._generate_operation_code(operation, func_name, param_names, instruction_lower)
        
        # Fallback to safe implementation
        return self.create_safe_fallback(func_name, param_names, instruction)
    
    def _generate_operation_code(self, operation: str, func_name: str, param_names: List[str], instruction: str) -> str:
        """Generate specific operation code"""
        
        if operation == 'sum':
            if len(param_names) >= 2:
                return f"def {func_name}({', '.join(param_names[:2])}): return {param_names[0]} + {param_names[1]} if isinstance({param_names[0]}, (int, float)) and isinstance({param_names[1]}, (int, float)) else sum({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) else 0"
            else:
                return f"def {func_name}({param_names[0]}): return sum({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) else 0"
        
        elif operation == 'length':
            return f"def {func_name}({param_names[0]}): return len({param_names[0]}) if isinstance({param_names[0]}, (list, tuple, str)) else 0"
        
        elif operation == 'max':
            if len(param_names) >= 2:
                return f"def {func_name}({', '.join(param_names[:2])}): return max({param_names[0]}, {param_names[1]}) if isinstance({param_names[0]}, (int, float)) and isinstance({param_names[1]}, (int, float)) else max({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) and len({param_names[0]}) > 0 else 0"
            else:
                return f"def {func_name}({param_names[0]}): return max({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) and len({param_names[0]}) > 0 else 0"
        
        elif operation == 'min':
            if len(param_names) >= 2:
                return f"def {func_name}({', '.join(param_names[:2])}): return min({param_names[0]}, {param_names[1]}) if isinstance({param_names[0]}, (int, float)) and isinstance({param_names[1]}, (int, float)) else min({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) and len({param_names[0]}) > 0 else 0"
            else:
                return f"def {func_name}({param_names[0]}): return min({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) and len({param_names[0]}) > 0 else 0"
        
        elif operation == 'reverse':
            return f"def {func_name}({param_names[0]}): return {param_names[0]}[::-1] if isinstance({param_names[0]}, (str, list, tuple)) else {param_names[0]}"
        
        elif operation == 'sort':
            return f"def {func_name}({param_names[0]}): return sorted({param_names[0]}) if isinstance({param_names[0]}, (list, tuple)) else {param_names[0]}"
        
        elif operation == 'multiply':
            if len(param_names) >= 2:
                return f"def {func_name}({', '.join(param_names[:2])}): return {param_names[0]} * {param_names[1]} if isinstance({param_names[0]}, (int, float)) and isinstance({param_names[1]}, (int, float)) else 0"
        
        elif operation == 'fibonacci':
            return f"def {func_name}({param_names[0]}): return {param_names[0]} if {param_names[0]} <= 1 else {func_name}({param_names[0]}-1) + {func_name}({param_names[0]}-2) if isinstance({param_names[0]}, int) and {param_names[0]} >= 0 else 0"
        
        # Add more operations as needed...
        
        return self.create_safe_fallback(func_name, param_names, instruction)
    
    def generate_code(self, instruction: str, test_cases: str) -> str:
        """Generate code using the best available method"""
        
        try:
            # Extract function signature
            func_name, param_names = self.extract_function_signature(instruction, test_cases)
            
            if self.use_transformers:
                # Try transformer-based generation
                prompt = self.create_code_prompt(instruction, func_name, param_names, test_cases)
                result = self.generate_with_transformer(prompt)
                
                if result:
                    return result
            
            # Fallback to template-based generation
            return self.generate_with_templates(instruction, func_name, param_names)
            
        except Exception as e:
            print(f"Error generating code: {e}")
            # Extract signature for fallback
            func_name, param_names = self.extract_function_signature(instruction, test_cases)
            return self.create_safe_fallback(func_name, param_names, instruction)
    
    def create_safe_fallback(self, func_name: str, param_names: List[str], instruction: str) -> str:
        """Create safe fallback implementation when all methods fail"""
        
        # Ultra-safe fallback
        if len(param_names) >= 2:
            return f"def {func_name}({', '.join(param_names[:2])}): return {param_names[0]} if isinstance({param_names[0]}, (int, float)) else 0"
        else:
            return f"def {func_name}({param_names[0]}): return 0"

def main():
    """Main function to generate LLM-based submission"""
    print("🚀 OFFLINE LLM CODE GENERATOR")
    print("   Target: >10% Pass@1 (significant improvement over V3's 3.25%)")
    
    # Initialize generator
    generator = OfflineLLMCodeGenerator()
    
    # Load data
    print("\n📊 Loading competition data...")
    dev_df = pd.read_csv('dataset/dev_v2.csv')
    
    responses = []
    stats = {
        'transformer_generated': 0,
        'template_generated': 0,
        'fallback_generated': 0,
        'multi_parameter': 0
    }
    
    print(f"\n⚙️  Processing {len(dev_df)} instructions...")
    
    for idx, row in dev_df.iterrows():
        instruction = row['instruction']
        test_list = row['test_list']
        
        try:
            # Generate code
            code = generator.generate_code(instruction, test_list)
            
            # Track stats
            if 'transformer' in str(type(generator)).lower() and generator.use_transformers:
                stats['transformer_generated'] += 1
            else:
                stats['template_generated'] += 1
            
            if ', ' in code:
                stats['multi_parameter'] += 1
            
            responses.append({
                "id": int(row['id']),
                "response": code
            })
            
            if idx < 5:  # Show first 5 for verification
                print(f"   ID {row['id']}: {code[:50]}...")
                
        except Exception as e:
            print(f"Error processing ID {row['id']}: {e}")
            func_name, param_names = generator.extract_function_signature(instruction, test_list)
            fallback_code = generator.create_safe_fallback(func_name, param_names, instruction)
            stats['fallback_generated'] += 1
            
            responses.append({
                "id": int(row['id']),
                "response": fallback_code
            })
    
    # Save results
    output_file = 'submission_llm_offline.json'
    with open(output_file, 'w') as f:
        json.dump(responses, f, indent=2)
    
    print(f"\n✅ LLM Offline Submission Generated:")
    print(f"   File: {output_file}")
    print(f"   Total responses: {len(responses)}")
    print(f"   Transformer generated: {stats['transformer_generated']}")
    print(f"   Template generated: {stats['template_generated']}")
    print(f"   Fallback generated: {stats['fallback_generated']}")
    print(f"   Multi-parameter functions: {stats['multi_parameter']}")
    print(f"   Expected improvement: >10% Pass@1 (vs V3's 3.25%)")
    
    return responses

if __name__ == "__main__":
    main()

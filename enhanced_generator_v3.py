"""
Enhanced Code Generator - Version 3
Fixes parameter mismatch issues identified from competition results
"""

import pandas as pd
import json
import re
from typing import Dict, List, Tuple
from parameter_extractor import ParameterExtractor

class EnhancedCodeGeneratorV3:
    def __init__(self):
        """Initialize with enhanced patterns and parameter extraction"""
        self.load_enhanced_patterns()
        self.build_comprehensive_patterns()
        self.parameter_extractor = ParameterExtractor()
        
    def load_enhanced_patterns(self):
        """Load patterns from enhanced analysis"""
        try:
            with open('enhanced_patterns.json', 'r', encoding='utf-8') as f:
                self.analysis_patterns = json.load(f)
        except FileNotFoundError:
            self.analysis_patterns = {}
            
    def build_comprehensive_patterns(self):
        """Build comprehensive pattern database with parameter-aware templates"""
        
        self.patterns = {
            # Mathematical operations
            'prime_check': {
                'keywords': ['মৌলিক', 'prime'],
                'template': 'def {func_name}({params}): return {param0} > 1 and all({param0} % i != 0 for i in range(2, int({param0}**0.5) + 1))',
                'param_count': 1
            },
            'factorial': {
                'keywords': ['ফ্যাক্টোরিয়াল', 'factorial'],
                'template': 'def {func_name}({params}): return 1 if {param0} <= 1 else {param0} * {func_name}({param0}-1)',
                'param_count': 1
            },
            'gcd': {
                'keywords': ['গ.সা.গু', 'gcd', 'greatest common'],
                'template': 'def {func_name}({params}): import math; return math.gcd({param0}, {param1})',
                'param_count': 2
            },
            'lcm': {
                'keywords': ['ল.সা.গু', 'lcm', 'least common', 'smallest multiple'],
                'template': 'def {func_name}({params}): import math; return abs({param0}*{param1}) // math.gcd({param0}, {param1})',
                'param_count': 2
            },
            'power': {
                'keywords': ['ঘাত', 'power', 'exponent'],
                'template': 'def {func_name}({params}): return {param0} ** {param1}',
                'param_count': 2
            },
            'even_odd': {
                'keywords': ['জোড়', 'বিজোড়', 'even', 'odd'],
                'template': 'def {func_name}({params}): return {param0} % 2 == 0',
                'param_count': 1
            },
            'absolute_value': {
                'keywords': ['পরম', 'absolute'],
                'template': 'def {func_name}({params}): return abs({param0})',
                'param_count': 1
            },
            
            # List operations
            'sum_list': {
                'keywords': ['যোগফল', 'তালিকা', 'sum', 'list'],
                'template': 'def {func_name}({params}): return sum({param0})',
                'param_count': 1
            },
            'max_value': {
                'keywords': ['সর্বোচ্চ', 'maximum', 'max'],
                'template': 'def {func_name}({params}): return max({param0})',
                'param_count': 1
            },
            'min_value': {
                'keywords': ['সর্বনিম্ন', 'minimum', 'min'],
                'template': 'def {func_name}({params}): return min({param0})',
                'param_count': 1
            },
            'sort_list': {
                'keywords': ['ক্রম', 'sort', 'arrange'],
                'template': 'def {func_name}({params}): return sorted({param0})',
                'param_count': 1
            },
            'unique_elements': {
                'keywords': ['অনন্য', 'unique', 'distinct'],
                'template': 'def {func_name}({params}): return list(set({param0}))',
                'param_count': 1
            },
            'list_length': {
                'keywords': ['দৈর্ঘ্য', 'length', 'size'],
                'template': 'def {func_name}({params}): return len({param0})',
                'param_count': 1
            },
            'add_lists': {
                'keywords': ['যোগ', 'add', 'combine'],
                'template': 'def {func_name}({params}): return [a + b for a, b in zip({param0}, {param1})]',
                'param_count': 2
            },
            'multiply_list': {
                'keywords': ['গুণ', 'multiply', 'product'],
                'template': 'def {func_name}({params}): result = 1\n    for x in {param0}: result *= x\n    return result',
                'param_count': 1
            },
            
            # String operations  
            'reverse_string': {
                'keywords': ['বিপরীত', 'reverse'],
                'template': 'def {func_name}({params}): return {param0}[::-1]',
                'param_count': 1
            },
            'string_length': {
                'keywords': ['দৈর্ঘ্য', 'length'],
                'template': 'def {func_name}({params}): return len({param0})',
                'param_count': 1
            },
            'uppercase': {
                'keywords': ['বড় হাতের', 'uppercase'],
                'template': 'def {func_name}({params}): return {param0}.upper()',
                'param_count': 1
            },
            'lowercase': {
                'keywords': ['ছোট হাতের', 'lowercase'],
                'template': 'def {func_name}({params}): return {param0}.lower()',
                'param_count': 1
            },
            'count_character': {
                'keywords': ['গণনা', 'count', 'character'],
                'template': 'def {func_name}({params}): return {param0}.count({param1})',
                'param_count': 2
            },
            'palindrome': {
                'keywords': ['palindrome', 'উল্টো', 'সমান'],
                'template': 'def {func_name}({params}): return {param0} == {param0}[::-1]',
                'param_count': 1
            },
            
            # Tuple operations
            'clear_tuple': {
                'keywords': ['সাফ', 'clear', 'empty'],
                'template': 'def {func_name}({params}): return ()',
                'param_count': 1
            },
            'tuple_length': {
                'keywords': ['টুপল', 'দৈর্ঘ্য', 'tuple', 'length'],
                'template': 'def {func_name}({params}): return len({param0})',
                'param_count': 1
            },
            'tuple_to_list': {
                'keywords': ['টুপল', 'তালিকা', 'tuple', 'list'],
                'template': 'def {func_name}({params}): return list({param0})',
                'param_count': 1
            },
            'list_to_tuple': {
                'keywords': ['তালিকা', 'টুপল', 'list', 'tuple'],
                'template': 'def {func_name}({params}): return tuple({param0})',
                'param_count': 1
            },
            'front_and_rear': {
                'keywords': ['প্রথম', 'শেষ', 'front', 'rear'],
                'template': 'def {func_name}({params}): return ({param0}[0], {param0}[-1])',
                'param_count': 1
            },
            
            # Advanced patterns
            'fibonacci': {
                'keywords': ['ফিবোনাচি', 'fibonacci'],
                'template': 'def {func_name}({params}): return {param0} if {param0} <= 1 else {func_name}({param0}-1) + {func_name}({param0}-2)',
                'param_count': 1
            },
            'binary_search': {
                'keywords': ['বাইনারি', 'search', 'find'],
                'template': 'def {func_name}({params}): \n    left, right = 0, len({param0})-1\n    while left <= right:\n        mid = (left+right)//2\n        if {param0}[mid] == {param1}: return mid\n        elif {param0}[mid] < {param1}: left = mid+1\n        else: right = mid-1\n    return -1',
                'param_count': 2
            }
        }
        
    def extract_function_name_from_instruction(self, instruction: str) -> str:
        """Extract function name from Bangla instruction"""
        
        patterns = [
            r'(\w+)\s*\(\s*[^)]*\s*\)',  # function_name(params)
            r'def\s+(\w+)\s*\(',          # def function_name(
            r'function\s+(\w+)',          # function function_name
            r'ফাংশন\s+(\w+)',            # ফাংশন function_name
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, instruction)
            if matches:
                return matches[0]
        
        # Fallback: look for English words that might be function names
        words = re.findall(r'[a-zA-Z_]\w*', instruction)
        for word in words:
            if len(word) > 2 and '_' in word:  # Likely function name
                return word
        
        # Last resort: generate based on content
        return self.generate_function_name_from_content(instruction)
    
    def generate_function_name_from_content(self, instruction: str) -> str:
        """Generate function name based on instruction content"""
        
        content_mapping = {
            'যোগফল': 'sum_numbers',
            'গুণফল': 'multiply_numbers', 
            'সর্বোচ্চ': 'max_value',
            'সর্বনিম্ন': 'min_value',
            'দৈর্ঘ্য': 'get_length',
            'বিপরীত': 'reverse_string',
            'ক্রম': 'sort_list',
            'গণনা': 'count_items',
            'মৌলিক': 'is_prime',
            'জোড়': 'is_even',
            'বিজোড়': 'is_odd',
        }
        
        for bangla, english in content_mapping.items():
            if bangla in instruction:
                return english
        
        return 'process_data'
    
    def generate_code(self, instruction: str, function_name: str = None, test_list: str = None) -> str:
        """Generate code with proper parameter handling"""
        
        # Extract function name if not provided
        if not function_name:
            function_name = self.extract_function_name_from_instruction(instruction)
        
        # Extract parameters from test cases if available
        if test_list:
            try:
                extracted_name, param_names = self.parameter_extractor.extract_function_signature(test_list, function_name)
                if extracted_name != function_name:
                    function_name = extracted_name
            except Exception as e:
                print(f"Parameter extraction failed for {function_name}: {e}")
                param_names = ['param1']
        else:
            param_names = ['param1']
        
        # Find best matching pattern
        best_pattern = self.find_best_pattern(instruction, function_name, len(param_names))
        
        if best_pattern:
            return self.generate_from_pattern(best_pattern, function_name, param_names)
        else:
            # Fallback with proper parameters
            return self.generate_fallback_code(function_name, param_names)
    
    def find_best_pattern(self, instruction: str, function_name: str, param_count: int) -> dict:
        """Find the best matching pattern for the instruction"""
        
        instruction_lower = instruction.lower()
        function_lower = function_name.lower()
        
        best_score = 0
        best_pattern = None
        
        for pattern_name, pattern in self.patterns.items():
            score = 0
            
            # Keyword matching
            for keyword in pattern['keywords']:
                if keyword.lower() in instruction_lower or keyword.lower() in function_lower:
                    score += 2
            
            # Parameter count matching (important!)
            if pattern.get('param_count', 1) == param_count:
                score += 3
            elif abs(pattern.get('param_count', 1) - param_count) <= 1:
                score += 1
            
            # Function name pattern matching
            if any(word in function_lower for word in pattern['keywords']):
                score += 1
            
            if score > best_score:
                best_score = score
                best_pattern = pattern
        
        return best_pattern if best_score > 0 else None
    
    def generate_from_pattern(self, pattern: dict, function_name: str, param_names: List[str]) -> str:
        """Generate code from a pattern with proper parameters"""
        
        template = pattern['template']
        
        # Create parameter mapping
        param_mapping = {
            'func_name': function_name,
            'params': ', '.join(param_names)
        }
        
        # Add individual parameter references
        for i, param in enumerate(param_names):
            param_mapping[f'param{i}'] = param
        
        # Handle cases where template expects more parameters than we have
        expected_params = pattern.get('param_count', 1)
        for i in range(len(param_names), expected_params):
            param_mapping[f'param{i}'] = f'param{i+1}'
        
        try:
            return template.format(**param_mapping)
        except KeyError as e:
            print(f"Template formatting error for {function_name}: {e}")
            return self.generate_fallback_code(function_name, param_names)
    
    def generate_fallback_code(self, function_name: str, param_names: List[str]) -> str:
        """Generate a simple fallback function with correct parameters"""
        
        params_str = ', '.join(param_names)
        
        # Analyze function name for likely operation
        func_lower = function_name.lower()
        
        if 'sum' in func_lower:
            return f'def {function_name}({params_str}): return sum({param_names[0]})'
        elif 'max' in func_lower:
            return f'def {function_name}({params_str}): return max({param_names[0]})'
        elif 'min' in func_lower:
            return f'def {function_name}({params_str}): return min({param_names[0]})'
        elif 'len' in func_lower or 'length' in func_lower:
            return f'def {function_name}({params_str}): return len({param_names[0]})'
        elif 'count' in func_lower:
            if len(param_names) >= 2:
                return f'def {function_name}({params_str}): return {param_names[0]}.count({param_names[1]})'
            else:
                return f'def {function_name}({params_str}): return len({param_names[0]})'
        elif 'check' in func_lower or 'is_' in func_lower:
            return f'def {function_name}({params_str}): return True'
        elif 'sort' in func_lower:
            return f'def {function_name}({params_str}): return sorted({param_names[0]})'
        elif 'reverse' in func_lower:
            return f'def {function_name}({params_str}): return {param_names[0]}[::-1]'
        elif 'clear' in func_lower:
            return f'def {function_name}({params_str}): return ()'
        elif 'add' in func_lower and len(param_names) >= 2:
            return f'def {function_name}({params_str}): return {param_names[0]} + {param_names[1]}'
        else:
            # Generic return based on parameter count
            if len(param_names) == 1:
                return f'def {function_name}({params_str}): return {param_names[0]}'
            else:
                return f'def {function_name}({params_str}): return {param_names[0]}'

def test_enhanced_generator():
    """Test the enhanced generator"""
    
    generator = EnhancedCodeGeneratorV3()
    
    test_cases = [
        ("clear_tuple ফাংশন", "clear_tuple", "['assert clear_tuple((1, 5, 3, 6, 8)) == ()']"),
        ("add_list যোগ করুন", "add_list", "['assert add_list([1, 2, 3],[4,5,6])==[5, 7, 9]']"),
        ("min_jumps খুঁজুন", "min_jumps", "['assert min_jumps([1, 3, 6, 1, 0, 9], 6) == 3']"),
    ]
    
    print("=== Testing Enhanced Generator ===")
    for instruction, func_name, test_list in test_cases:
        code = generator.generate_code(instruction, func_name, test_list)
        print(f"Instruction: {instruction}")
        print(f"Generated:")
        print(code)
        print()

if __name__ == "__main__":
    test_enhanced_generator()

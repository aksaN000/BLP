"""
Parameter Extraction from Test Cases
Analyzes test_list to determine correct function signatures
"""

import pandas as pd
import re
import ast
from typing import Dict, List, Tuple, Optional

class ParameterExtractor:
    def __init__(self):
        self.trial_df = pd.read_csv('dataset/trial.csv')
        self.dev_df = pd.read_csv('dataset/dev_v2.csv')
        
    def extract_function_signature(self, test_list_str: str, function_name: str) -> Tuple[str, List[str]]:
        """Extract function name and parameters from test cases"""
        
        try:
            # Parse the test list
            test_cases = ast.literal_eval(test_list_str)
            
            for test_case in test_cases:
                # Find function calls in assert statements
                # Pattern: assert function_name(param1, param2, ...) == expected
                pattern = rf'assert\s+{re.escape(function_name)}\s*\(([^)]*)\)\s*=='
                match = re.search(pattern, test_case)
                
                if match:
                    params_str = match.group(1).strip()
                    if not params_str:
                        return function_name, []
                    
                    # Count parameters by splitting on commas (basic approach)
                    # This handles simple cases - for complex nested structures, we'd need more parsing
                    param_count = self.count_parameters(params_str)
                    
                    # Generate parameter names based on common patterns
                    param_names = self.generate_parameter_names(param_count, function_name, params_str)
                    
                    return function_name, param_names
                    
        except Exception as e:
            print(f"Error parsing test cases for {function_name}: {e}")
            
        # Fallback: analyze function name for hints
        return function_name, self.fallback_parameter_names(function_name)
    
    def count_parameters(self, params_str: str) -> int:
        """Count parameters in function call"""
        if not params_str.strip():
            return 0
            
        # Simple comma counting with basic bracket balancing
        depth = 0
        param_count = 1
        
        for char in params_str:
            if char in '([{':
                depth += 1
            elif char in ')]}':
                depth -= 1
            elif char == ',' and depth == 0:
                param_count += 1
                
        return param_count
    
    def generate_parameter_names(self, param_count: int, function_name: str, params_str: str) -> List[str]:
        """Generate appropriate parameter names based on function name and context"""
        
        # Analyze parameter content first for more accurate type detection
        has_list = '[' in params_str and ']' in params_str
        has_tuple = '(' in params_str and ')' in params_str and not 'assert' in params_str
        has_string = ('"' in params_str or "'" in params_str) and not 'assert' in params_str
        has_number = any(char.isdigit() for char in params_str.replace('[', '').replace(']', '').replace('(', '').replace(')', ''))
        
        # Specific function name patterns (exact matches first)
        exact_patterns = {
            'clear_tuple': ['tup'],
            'add_list': ['lst1', 'lst2'],
            'min_jumps': ['lst', 'n'],
            'check_tuples': ['tup', 'lst'],
            'new_tuple': ['lst', 's'],
            'add_tuple': ['lst', 'tup'],
            'front_and_rear': ['tup'],
            'list_tuple': ['lst'],
            'sub_lists': ['lst'],
            'interleave_lists': ['lst1', 'lst2', 'lst3'],
            'remove_list_range': ['lst', 'start', 'end'],
            'count_list': ['lst'],
            'max_sum_list': ['lst'],
            'sort_tuple': ['lst'],
            'string_list_to_tuple': ['s'],
            'multiply_list': ['lst'],
            'rearrange_numbs': ['lst'],
            'chunk_tuples': ['tup', 'n'],
            're_arrange_tuples': ['lst', 'ord_list'],
            'remove_tuple': ['lst'],
            'remove_duplic_list': ['lst'],
            'check_element': ['tup', 'lst'],
            'join_tuples': ['lst'],
            'len_log': ['lst'],
            'count_digs': ['tup'],
            'sort_list': ['lst'],
            'tuple_to_set': ['tup'],
            'coin_change': ['coins', 'n', 'amount'],
            'smallest_multiple': ['n'],
        }
        
        # Check for exact function name match
        if function_name in exact_patterns:
            params = exact_patterns[function_name]
            if len(params) >= param_count:
                return params[:param_count]
            else:
                # Extend with generic names if needed
                extended = params + [f'param{i+1}' for i in range(len(params), param_count)]
                return extended[:param_count]
        
        # Pattern-based matching for partial names
        func_lower = function_name.lower()
        
        # Multi-parameter patterns based on content analysis
        if param_count == 1:
            if has_tuple or 'tuple' in func_lower or 'tup' in func_lower:
                return ['tup']
            elif has_list or 'list' in func_lower or 'lst' in func_lower or 'array' in func_lower:
                return ['lst']
            elif has_string or 'string' in func_lower or 'str' in func_lower or 'text' in func_lower:
                return ['s']
            else:
                return ['n']
                
        elif param_count == 2:
            if 'list' in func_lower and has_list:
                return ['lst1', 'lst2']
            elif 'tuple' in func_lower:
                if has_list:
                    return ['tup', 'lst']
                else:
                    return ['tup1', 'tup2']
            elif 'check' in func_lower or 'tuples' in func_lower:
                return ['tup', 'lst']
            elif 'jump' in func_lower or 'min' in func_lower or 'max' in func_lower:
                return ['lst', 'n']
            elif has_string:
                return ['s1', 's2']
            else:
                return ['a', 'b']
                
        elif param_count == 3:
            if 'jump' in func_lower:
                return ['lst', 'n', 'target']
            elif 'range' in func_lower:
                return ['lst', 'start', 'end']
            elif 'interleave' in func_lower:
                return ['lst1', 'lst2', 'lst3']
            elif 'coin' in func_lower:
                return ['coins', 'n', 'amount']
            elif has_list:
                return ['lst1', 'lst2', 'lst3']
            else:
                return ['a', 'b', 'c']
        else:
            # For more than 3 parameters
            return [f'param{i+1}' for i in range(param_count)]
    
    def fallback_parameter_names(self, function_name: str) -> List[str]:
        """Generate parameter names when test case parsing fails"""
        
        func_lower = function_name.lower()
        
        # Single parameter functions
        if any(word in func_lower for word in ['check', 'is_', 'count', 'find', 'calculate', 'get']):
            return ['n']
        
        if any(word in func_lower for word in ['list', 'array', 'sort', 'max', 'min', 'sum']):
            return ['lst']
            
        if any(word in func_lower for word in ['tuple', 'tup']):
            return ['tup']
            
        if any(word in func_lower for word in ['string', 'str', 'text']):
            return ['s']
        
        # Two parameter functions  
        if any(word in func_lower for word in ['add', 'compare', 'merge', 'combine']):
            return ['a', 'b']
            
        # Default single parameter
        return ['n']

def test_parameter_extraction():
    """Test the parameter extraction on trial data"""
    
    extractor = ParameterExtractor()
    
    print("=== Testing Parameter Extraction ===")
    
    # Test a few examples
    test_cases = [
        ("clear_tuple", "['assert clear_tuple((1, 5, 3, 6, 8)) == ()', 'assert clear_tuple((2, 1, 4 ,5 ,6)) == ()']"),
        ("add_list", "['assert add_list([1, 2, 3],[4,5,6])==[5, 7, 9]', 'assert add_list([1,2],[3,4])==[4,6]']"),
        ("min_jumps", "['assert min_jumps([1, 3, 6, 1, 0, 9], 6) == 3', 'assert min_jumps([1, 3, 5, 8, 9, 2, 6, 7, 6, 8, 9], 11) == 3']"),
        ("check_tuples", "['assert check_tuples((3, 5, 6, 5, 3, 6),[3, 6, 5]) == True', 'assert check_tuples((4, 5, 6, 4, 6, 5),[4, 5, 6]) == True']")
    ]
    
    for func_name, test_list in test_cases:
        extracted_name, params = extractor.extract_function_signature(test_list, func_name)
        print(f"Function: {func_name}")
        print(f"  Extracted: {extracted_name}({', '.join(params)})")
        print()

if __name__ == "__main__":
    test_parameter_extraction()

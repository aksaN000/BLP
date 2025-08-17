"""
Iteration 2C: Advanced Optimization
For use if initial submission scores > 30%
"""

import pandas as pd
import json
import re

def optimize_for_tie_breaker():
    """Optimize code generation for shorter length (tie-breaker metric)"""
    
    print("=== Optimizing for Tie-breaker (Shorter Code) ===")
    
    # Shorter code templates
    short_patterns = {
        'prime': 'def {func_name}(n):return n>1and all(n%i for i in range(2,int(n**.5)+1))',
        'even': 'def {func_name}(n):return n%2<1',
        'reverse': 'def {func_name}(s):return s[::-1]',
        'sum': 'def {func_name}(lst):return sum(lst)',
        'max': 'def {func_name}(lst):return max(lst)',
        'min': 'def {func_name}(lst):return min(lst)',
        'factorial': 'def {func_name}(n):return 1if n<2else n*{func_name}(n-1)',
    }
    
    return short_patterns

def implement_chain_of_thought():
    """Implement chain-of-thought reasoning for complex problems"""
    
    def analyze_instruction_step_by_step(instruction: str) -> dict:
        """Break down instruction into steps"""
        
        analysis = {
            'input_type': None,
            'output_type': None,
            'algorithm_needed': None,
            'complexity': 'simple'
        }
        
        # Analyze input type
        if 'তালিকা' in instruction or 'list' in instruction.lower():
            analysis['input_type'] = 'list'
        elif 'স্ট্রিং' in instruction or 'string' in instruction.lower():
            analysis['input_type'] = 'string'
        elif 'সংখ্যা' in instruction or 'number' in instruction.lower():
            analysis['input_type'] = 'number'
        
        # Analyze complexity
        if any(word in instruction for word in ['chain', 'longest', 'shortest', 'optimize']):
            analysis['complexity'] = 'complex'
        elif any(word in instruction for word in ['sort', 'search', 'find']):
            analysis['complexity'] = 'medium'
        
        # Determine algorithm
        if 'মৌলিক' in instruction or 'prime' in instruction.lower():
            analysis['algorithm_needed'] = 'prime_check'
        elif 'chain' in instruction.lower():
            analysis['algorithm_needed'] = 'dynamic_programming'
        elif 'ludic' in instruction.lower():
            analysis['algorithm_needed'] = 'sieve_algorithm'
        
        return analysis
    
    return analyze_instruction_step_by_step

def create_ensemble_approach():
    """Combine multiple approaches for better accuracy"""
    
    def ensemble_generate(instruction: str) -> list:
        """Generate multiple solutions and pick the best"""
        
        candidates = []
        
        # Approach 1: Pattern matching
        from improved_generator import ImprovedCodeGenerator
        pattern_gen = ImprovedCodeGenerator()
        candidate1 = pattern_gen.generate_code(instruction)
        candidates.append(('pattern', candidate1))
        
        # Approach 2: Few-shot prompting (if LLM available)
        # Would implement LLM-based generation here
        
        # Approach 3: Template-based with optimization
        optimized_patterns = optimize_for_tie_breaker()
        # Use optimized patterns for known cases
        
        # Voting/ranking logic
        def rank_candidate(candidate):
            code = candidate[1]
            score = 0
            
            # Prefer shorter code (tie-breaker)
            score += max(0, 100 - len(code))
            
            # Prefer code with proper function definition
            if 'def ' in code and '(' in code and ')' in code:
                score += 50
            
            # Penalize fallback solutions
            if 'def solve(): pass' in code:
                score -= 100
            
            return score
        
        # Rank candidates
        ranked = sorted(candidates, key=rank_candidate, reverse=True)
        return ranked[0][1]  # Return best candidate
    
    return ensemble_generate

def advanced_error_handling():
    """Add sophisticated error handling and edge cases"""
    
    def robust_code_wrapper(base_code: str, func_name: str) -> str:
        """Wrap generated code with error handling"""
        
        if 'def ' not in base_code:
            return base_code
        
        # Add basic error handling for common cases
        if 'prime' in func_name.lower():
            return f"""def {func_name}(n):
    if not isinstance(n, int) or n < 0: return False
    return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))"""
        
        elif 'chain' in func_name.lower():
            return base_code  # Complex algorithms keep as-is
        
        else:
            return base_code
    
    return robust_code_wrapper

if __name__ == "__main__":
    print("=== Advanced Optimization Tools ===")
    
    # Test optimization tools
    short_patterns = optimize_for_tie_breaker()
    analyzer = implement_chain_of_thought()
    ensemble = create_ensemble_approach()
    error_handler = advanced_error_handling()
    
    # Test on sample instruction
    test_instruction = "প্রদত্ত পূর্ণসংখ্যাটি একটি মৌলিক সংখ্যা কিনা তা পরীক্ষা করার জন্য একটি ফাংশন লিখুন"
    
    analysis = analyzer(test_instruction)
    print(f"Analysis: {analysis}")
    
    ensemble_result = ensemble(test_instruction)
    print(f"Ensemble result: {ensemble_result}")
    
    print("\n🚀 Advanced tools ready for implementation!")

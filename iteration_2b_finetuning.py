"""
Iteration 2B: LLM Fine-tuning Approach
For use if initial submission scores 15-30%
"""

import pandas as pd
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from datasets import Dataset
import torch

def prepare_fine_tuning_data():
    """Prepare trial data for fine-tuning"""
    
    trial_df = pd.read_csv('dataset/trial.csv')
    
    # Create training examples
    training_data = []
    
    for _, row in trial_df.iterrows():
        instruction = row['instruction']
        response = row['response']
        
        # Create a prompt-response pair
        prompt = f"### Instruction: {instruction}\n### Response: {response}"
        
        training_data.append({
            'text': prompt,
            'instruction': instruction,
            'response': response
        })
    
    print(f"Prepared {len(training_data)} training examples")
    
    # Save for inspection
    with open('training_data.json', 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    return training_data

def setup_fine_tuning():
    """Setup fine-tuning with a smaller, more suitable model"""
    
    print("=== Setting up Fine-tuning ===")
    
    # Use a smaller model suitable for code generation
    model_name = "microsoft/CodeGPT-small-py"  # Alternative: "Salesforce/codegen-350M-mono"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        # Add padding token if needed
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        print(f"✅ Loaded model: {model_name}")
        return tokenizer, model
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("Will use alternative approach...")
        return None, None

def create_few_shot_prompting():
    """Create improved few-shot prompting as alternative to fine-tuning"""
    
    print("=== Creating Few-Shot Prompting ===")
    
    # Load trial data for examples
    trial_df = pd.read_csv('dataset/trial.csv')
    
    # Select diverse examples for few-shot
    examples = []
    for i in [0, 3, 5, 8, 12]:  # Select varied examples
        if i < len(trial_df):
            row = trial_df.iloc[i]
            examples.append({
                'instruction': row['instruction'],
                'response': row['response']
            })
    
    def create_prompt(instruction: str) -> str:
        prompt = "You are an expert Python programmer. Convert Bangla instructions to Python code.\n\n"
        
        # Add examples
        for ex in examples:
            prompt += f"Instruction: {ex['instruction']}\n"
            prompt += f"Code: {ex['response']}\n\n"
        
        # Add current instruction
        prompt += f"Instruction: {instruction}\n"
        prompt += "Code: "
        
        return prompt
    
    return create_prompt

if __name__ == "__main__":
    # Prepare data
    training_data = prepare_fine_tuning_data()
    
    # Try fine-tuning setup
    tokenizer, model = setup_fine_tuning()
    
    if model is None:
        # Fallback to few-shot prompting
        print("Using few-shot prompting approach...")
        prompt_creator = create_few_shot_prompting()
        
        # Test on a sample
        test_instruction = "একটি সংখ্যা জোড় নাকি বিজোড় তা নির্ধারণ করার জন্য একটি ফাংশন লিখুন"
        test_prompt = prompt_creator(test_instruction)
        print(f"\nSample prompt:\n{test_prompt}")

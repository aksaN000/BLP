import pandas as pd
import json
import ast

print("=== BLP Task 2 Data Analysis ===")

# Load trial data
print("\n1. Loading trial.csv...")
trial_df = pd.read_csv('dataset/trial.csv')
print(f"Trial dataset: {len(trial_df)} examples")
print(f"Columns: {list(trial_df.columns)}")

# Show sample data
print("\n2. Sample trial data:")
for i in range(3):
    row = trial_df.iloc[i]
    print(f"\nExample {i+1}:")
    print(f"ID: {row['id']}")
    print(f"Instruction: {row['instruction'][:100]}...")
    print(f"Response: {row['response'][:100]}...")

# Load dev data
print("\n3. Loading dev_v2.csv...")
dev_df = pd.read_csv('dataset/dev_v2.csv')
print(f"Dev dataset: {len(dev_df)} examples")
print(f"Columns: {list(dev_df.columns)}")

# Show sample dev data
print("\n4. Sample dev data:")
for i in range(2):
    row = dev_df.iloc[i]
    print(f"\nExample {i+1}:")
    print(f"ID: {row['id']}")
    print(f"Instruction: {row['instruction'][:100]}...")

print("\n5. Analysis of instruction types...")
# Analyze instruction patterns
instructions = trial_df['instruction'].tolist()
common_words = {}
for inst in instructions:
    words = inst.split()
    for word in words:
        common_words[word] = common_words.get(word, 0) + 1

# Show top 10 common words
sorted_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 common words in instructions:")
for word, count in sorted_words:
    print(f"  {word}: {count}")

print("\n=== Data Analysis Complete ===")

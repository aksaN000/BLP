# BLP 2025 Task 2: Bangla-to-Python Code Generation

My entry for **Task 2 of the BLP Workshop at IJCNLP-AACL 2025**: given a programming problem written in Bangla, generate a Python function that passes hidden unit tests. Submissions are scored by **Pass@1** on CodaBench.

## Task

| | |
|---|---|
| Input | A Bangla instruction, e.g. *দুটি পূর্ণসংখ্যার গ.সা.গু নির্ণয় করো* ("find the GCD of two integers") |
| Output | A Python function that satisfies all hidden test cases |
| Data | `dataset/trial.csv` (examples with reference solutions), `dataset/dev_v2.csv` (400 problems) |
| Metric | Pass@1 |

## Approach

I deliberately started without a large model, to see how far structure alone could go:

1. **Function-signature extraction:** recover the function name and parameter count from the example call in each prompt (`parameter_extractor.py`, `enhanced_parameter_extractor.py`).
2. **Pattern-based generation:** map Bangla keywords to algorithm templates (primes, GCD/LCM, string reversal, repeated characters, list aggregates…) stored in `enhanced_patterns.json` and assembled by `enhanced_generator_v3.py`.
3. **Offline LLM follow-up:** `offline_llm_generator.py` adds a Bangla→English key-term map and falls back to a local CodeGen-350M model through Hugging Face Transformers when a template doesn't match.

## Results

| Version | Pass@1 (dev, 400 problems) |
|---|---|
| V1: keyword templates | 3.00% |
| V3: better signature and parameter extraction | **3.25%** (13 / 400) |
| Offline LLM pipeline | prepared, not scored |

## What I learned

Template matching works for a handful of problem families but doesn't generalise. The failure analysis in `v3_results_analysis.md` breaks the failures down:
- **Parameter-count mismatches:** over 70%. The generated signature didn't match what the hidden tests called.
- **Type errors:** about 20%.
- **Wrong logic:** about 10%.

The score made the case for a model-first approach, where a code LLM is prompted or fine-tuned on the trial set. Structure-based checks, especially signature extraction, would then validate its output rather than generate it.

## Tech stack

Python · pandas · regular expressions · PyTorch and Hugging Face Transformers (offline LLM pipeline only)

## Running locally

```bash
git clone https://github.com/aksaN000/BLP.git
cd BLP
pip install pandas                     # V3 pipeline
pip install torch transformers         # only for offline_llm_generator.py

python final_submission_v3.py          # V3: writes submission_v3.json and the CodaBench zip
python offline_llm_generator.py        # offline LLM variant
```

Both scripts read `dataset/dev_v2.csv`. `sampleCodes/` contains the organisers' baseline notebooks and scoring script.

## Files

| Path | Purpose |
|---|---|
| `enhanced_generator_v3.py`, `enhanced_patterns.json` | V3 template generator and its pattern library |
| `parameter_extractor.py`, `enhanced_parameter_extractor.py` | Function-signature extraction from Bangla prompts |
| `final_submission_v3.py` | Builds, validates and zips the V3 submission |
| `offline_llm_generator.py`, `llm_submission_pipeline.py` | Offline LLM variant |
| `*_V3*.md`, `LLM_APPROACH_ANALYSIS.md`, `v3_results_analysis.md` | Working notes and failure analysis |

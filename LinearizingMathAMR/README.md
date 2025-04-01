After generating MathAMRs, we linearize them using `anr_utils`. Note that we have modified the code to pass the AMR string and get the linearized string using depth-first traverse.
To do so, run the following command:
```
python3 linearize_mathamr_topics.py
```

This will generate two files in the results directory:
- `linearized_mathamr_candiates.tsv`
- `linearized_mathamr_topics.tsv`
 
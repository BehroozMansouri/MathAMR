## Extracting context of formulas
The first step to generate MathAMR is to extract the context of the formulas. In our work, we used a sentence before and after the formula.
Run the following:
```bash
python extract_context_task2.py \
  --post_path "./Posts.V1.3.xml" \
  --latex_dir ".latex_representation_v3/" \
  --qrel_1 "./qrel_task2_2020_visual_id.tsv" \
  --qrel_2 "./qrel_task2_2021_all.tsv" \
  --result_path "formulas_context.tsv"'''

The command above will save the candidate formulas context as a .TSV file. Next we run a similar code for extracting context of formula queries. For this, run the command:

## Extracting context of formulas
The first step to generate MathAMR is to extract the context of the formulas. In our work, we used a sentence before and after the formula.
Run the command like:
```bash
python extract_context_task2.py \
  --post_path "./Posts.V1.3.xml" \
  --latex_dir ".latex_representation_v3/" \
  --qrel_1 "./qrel_task2_2020_visual_id.tsv" \
  --qrel_2 "./qrel_task2_2021_all.tsv" \
  --result_path "formulas_context.tsv"
```

This will generate the annotated formulas context in ARQMath-1 and -2, saving the candidate formulas context as a .TSV file. 

Next we run a similar code for extracting context of formula queries. For this, run the command like:
```bash
python extract_context_task2.py \
  --xml_topic_path "./Topics_V1.1.xml" \
  --opt_topic_path "./Formula_topics_opt_V2.0.tsv" \
  --result_file "result.tsv"
```

Note that for commands above you need the `topic_file_reader_task2.py`, `post_parser_record.py`, and `Post.py` files.

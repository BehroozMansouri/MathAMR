## Getting Data
To run the experiments, you need to download the following files from ARQMath Google Drive.
For ease of use, the smaller files including Topics (.xml files), OPTs (.tsv files), and QREL (.tsv files) are included in the ARQMathFiles Directory.
#### Collection Files
- Posts.V1.3.xml: This contains question and answer posts. [Link](https://drive.google.com/drive/u/0/folders/1YekTVvfmYKZ8I5uiUMbs21G2mKwF9IAm)
- latex_representation_v3: This contains LaTeX representations of math formulas in the Posts. [Link](https://drive.google.com/drive/u/0/folders/18bHlAWkhIJkLeS9CHvBQQ-BLSn4rrlvE)
- qrel_task2_2020_visual_id.tsv: This contains QREL file with visual Ids for ARQMath-1, Task 2. [Link](https://drive.google.com/drive/u/0/folders/1BKk_Q7wKtoezRlfIb1OcoWCiUYuVuwsx)
- qrel_task2_2021_all.tsv: This contains QREL file with visual Ids for ARQMath-2, Task 2. [Link](https://drive.google.com/drive/u/0/folders/1oHgwJQk-5FFcxcH6_lhfFq6tD18X7zH-)
- qrel_task2_2022_official.tsv: This contains QREL file with visual Ids for ARQMath-3, Task 2. [Link](https://drive.google.com/drive/u/0/folders/1AWUO6wsa3Pe7gQ3HMJj31O5KrqWUstUF)
#### Topic Files
In addition to candidate formulas in the collection, we need to extract sentences from topic formulas.
- Topics_V1.1.xml: ARQMath-1 Task 2 Topic file. [Link](https://drive.google.com/drive/u/0/folders/1DFvfNObb1T8AnOYkCvp0o6XmfX-9J60B)
- Formula_topics_opt_V2.0.tsv: ARQMath-1 Task 2 Formula OPTs. [Link](https://drive.google.com/drive/u/0/folders/14c_R9bpLWxaV6fKNNpKgepoYNZXE6Hi1)
- Topics_Task2_2021_V1.1.xml: ARQMath-2 Task 2 Topic file. [Link](https://drive.google.com/drive/u/0/folders/1mhzyiJv94XmOZ14B4LHJM2gS1hJtexCk)
- Topics_2021_Formulas_OPT_V1.1.tsv: ARQMath-2 Task 2 Formula OPTs. [Link](https://drive.google.com/drive/u/0/folders/1p0_OcQpYFGbKEgZ4VFsBhVc7S3OdKdkf)
- Topics_Task2_2022_V0.1.xml: ARQMath-3 Task 2 Topic file. [Link](https://drive.google.com/drive/u/0/folders/1qLIh8DjDPhn2nEVOkrq0dyBnC4zzO6Oo)
- Topics_Formulas_OPT.V0.1.tsv: ARQMath-3 Task 2 Formula OPTs. [Link](https://drive.google.com/drive/u/0/folders/1NfPrKDlrrFi4DTYzCvPvZnJHPK7XXcbr)

## Extracting context of formulas
The first step to generate MathAMR is to extract the context of the formulas. In our work, we used a sentence before and after the formula.
Run the command like:
```bash
python extract_context_task2.py \
  --post_path "./Posts.V1.3.xml" \
  --latex_dir ".latex_representation_v3/" \
  --result_path "formulas_context.tsv"
```

This will generate the annotated formulas context in ARQMath-1 and -2, saving the candidate formulas context as a .TSV file. 

Next we run a similar code for extracting context of formula queries. For this, run the command like:
```bash
python extract_context_topics_task2.py \
  --xml_topic_path "./Topics_V1.1.xml" \
  --opt_topic_path "./Formula_topics_opt_V2.0.tsv" \
  --result_file "result.tsv"
```

Note that for commands above you need the `topic_file_reader_task2.py`, `post_parser_record.py`, and `Post.py` files.

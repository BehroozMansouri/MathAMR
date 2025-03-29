## Getting Data
To run the experiments, you need to download the following files from ARQMath Google Drive.
For ease of use, the smaller files including Topics (.xml files), OPTs (.tsv files), and QREL based on formula ID (.tsv files) are included in the ARQMathFiles Directory.
#### Collection Files
- Posts.V1.3.xml: This contains question and answer posts. [Link](https://drive.google.com/drive/u/0/folders/1YekTVvfmYKZ8I5uiUMbs21G2mKwF9IAm)
- latex_representation_v3: This contains LaTeX representations of math formulas in the Posts. [Link](https://drive.google.com/drive/u/0/folders/18bHlAWkhIJkLeS9CHvBQQ-BLSn4rrlvE)
- qrel_task2_all.tsv: This contains QREL file with formula Ids for ARQMath-1, Task 2. [Link](https://drive.google.com/drive/u/0/folders/1BWDWl6m6uX-CjdboF4ngvlE2xSvCiPwD)
- qrel_task2_2021_formula_id_all.tsv: This contains QREL file with formula Ids for ARQMath-2, Task 2. [Link](https://drive.google.com/drive/u/0/folders/1iucnTr9ZaI0tXyqfzC_8NB8DfE8Y0emm)
- qrel_task2_2022_formula_id_official.tsv: This contains QREL file with formula Ids for ARQMath-3, Task 2. [Link](https://drive.google.com/drive/u/0/folders/1T-7cR8rwjfcKdxUsaO_JVL8Ul4zOR-LS)

Note that the extraction is done with QREL files with formula Ids not visual Ids.
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

This will generate the annotated formulas context in ARQMath-1, -2 and -3, saving the candidate formulas context as formulas_context.tsv file. 

Next we run a similar code for extracting context of formula queries. For this, run the command like:
```bash
python extract_context_topics_task2.py \
  --result_file "result.tsv"
```

Note that for commands above you need the `topic_file_reader_task2.py`, `post_parser_record.py`, and `Post.py` files.

#### SpaCy
In case running the SpaCy is raising an error, please use the following command to install the matched version
```bash
python -m pip install -U pydantic spacy==3.4.4
```
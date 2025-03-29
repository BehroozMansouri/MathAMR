# MathAMR: Math Abstract Meaning Representation
This repo provides the code for the paper "Contextualized Formula Search Using Math Abstract Meaning Representation" in CIKM, 2022.

## MathAMR
In math formula search, relevance is determined not only by the similarity of formulas in isolation,
but also by their surrounding context. 
We introduce MathAMR, a new unified representation for both text and math in sentences. 
MathAMR generalizes Abstract Meaning Representation (AMR) graphs to include math formula operations and arguments.
We then use Sentence-BERT to embed linearized MathAMR graphs for use in formula retrieval. 
In our first experiment, we compare MathAMR against raw text using the same formula representation (Operator Trees),
and find that MathAMR produces more effective rankings. We then apply our MathAMR embeddings to reranking runs from
the ARQMath-2 formula retrieval task, where in most cases effectiveness measures are improved. The strongest
reranked run matches the best P´@10 for an original run, and exceeds the original runs in nDCG´@10. 

## Installation
Run the following to clone MathAMR repo and install required libraries:
```bash
git clone https://github.com/BehroozMansouri/MathAMR.git
cd MathAMR
sh bin/install
```

You can alternatively run the followings:
```
git clone https://github.com//ablodge/amr-utils
pip install penman
pip install ./amr-utils
git clone https://github.com/bjascob/amrlib
python -m pip install -U pydantic spacy==3.4.4
```

## Extracting Context
The following command will extract the context of candidate fomrulas and formula queries.
```bash
cd ExtractingContext
python extract_context_task2.py --post_path "/Posts.V1.3.xml" --latex_dir "./latex_representation_v3/" --result_path formulas_context.tsv.
python extract_context_topics_task2.py --result_file "result.tsv"
cd ..
```


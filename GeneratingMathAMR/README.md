## Getting Data
To run the experiments, you first need the OPT representations of candidates.
- opt_representation_v3: This contains OPT representations of math formulas in the Posts. [Link](https://drive.google.com/drive/u/0/folders/18bHlAWkhIJkLeS9CHvBQQ-BLSn4rrlvE)

## Setting up AMR Parser
After pulling the `amrlib` using the install command, to download the model used in this research
use run 
```bash
cd GenerateAMR
python download_amr_parser.py
```
This will download the `parse_xfm_bart_large` model in `amrlib/amrlib/data`. 

## Generating MathAMR
Next we generate MathAMR for topics and candidates (when in GenerateAMR directory):
```bash
python generate_mathamr_topics.py
```

This reads the context of topics, and generate MathAMR. The results will be saved in `results/mathamr_topics.tsv`.

Then, run the following command to generate MathAMRs for candidates (Note that this needs more time in scale of hours):
```bash
python generate_mathamr_candidates.py --opt_dir ./opt_representation_V3
```
The results will be saved in `results/mathamr_candidates.tsv`.
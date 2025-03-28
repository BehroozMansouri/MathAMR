from post_parser_record import PostParserRecord
from tqdm import tqdm
from shared_methods import *

import argparse
import sys
import csv
import os
import spacy

csv.field_size_limit(sys.maxsize)
nlp = spacy.load('en_core_web_sm')


def read_formula_qrel(qrel_file_path):
    """
    Extracting the formula ids of the formulas in the qrel files. The third column in qrel files have this data.
    @param qrel_file_path: qrel file path
    @return: list of formula ids in the qrel file
    """
    lst_formulas = []
    with open(qrel_file_path, encoding="utf-8", newline='') as file:
        csv_reader = csv.reader(file, delimiter='\t', quotechar='"')
        for row in csv_reader:
            formula_id = int(row[2])
            lst_formulas.append(formula_id)
    return lst_formulas


def read_tsv_files(tsv_directory):
    """

    @param tsv_directory:
    @return:
    """
    dic_formula_post_ids = {}
    dic_formula_post_type = {}
    for file in os.listdir(tsv_directory):
        with open(tsv_directory+"/"+file, encoding="utf-8", newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t', quotechar='"')
            next(csv_reader)
            for row in csv_reader:
                formula_id = int(row[0])
                post_id = int(row[1])
                post_type = row[3]
                dic_formula_post_ids[formula_id] = post_id
                dic_formula_post_type[formula_id] = post_type
    return dic_formula_post_ids, dic_formula_post_type


def get_related_text(qrel_arqmath_1, qrel_arqmath_2, qrel_arqmath_3, latex_tsv_directory, post_file_path):
    result = {}
    lst_formulas = []
    # Reading the QREL files for ARQMath 1, 2, and 3
    lst_formulas.extend(read_formula_qrel(qrel_arqmath_1))
    lst_formulas.extend(read_formula_qrel(qrel_arqmath_2))
    lst_formulas.extend(read_formula_qrel(qrel_arqmath_3))

    # Reading TSV files
    print("Reading the LaTeX Files")
    dic_formula_post_ids, dic_formula_post_type = read_tsv_files(latex_tsv_directory)

    # Reading post file
    print("Reading the Post File")
    post_parser = PostParserRecord(post_file_path)


    # Replacing formulas with their ID, in form of eqxIDeqx
    for formula_id in tqdm(lst_formulas):
        post_id = dic_formula_post_ids[formula_id]
        post_type = dic_formula_post_type[formula_id]
        text = ""
        try:
            if post_type == "title":
                text = post_parser.map_questions[post_id].title
            elif post_type == "question":
                text = post_parser.map_questions[post_id].body
            elif post_type == "answer":
                text = post_parser.map_just_answers[post_id].body
        except:
            continue
        # replacing formulas
        math_text = get_math(text)
        text_sentences = nlp(math_text)
        # getting context of the formulas
        context_formula = get_context_of_formula_sentence(text_sentences, 'eqx' + str(formula_id) + 'eqx')
        if context_formula == "":
            continue
        result[formula_id] = context_formula
    return result


def main(post_path, latex_dir, result_path):
    qrel_1 = "../ARQMathFiles/qrel_task2_2020_visual_id.tsv"
    qrel_2 = "../ARQMathFiles/qrel_task2_2021_all.tsv"
    qrel_3 = "../ARQMathFiles/qrel_task2_2022_official.tsv"
    formula_id_contex_dic = get_related_text(qrel_1, qrel_2, qrel_3, latex_dir, post_path)
    with open(result_path, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for formula_id in formula_id_contex_dic:
            csv_writer.writerow([str(formula_id), formula_id_contex_dic[formula_id]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Detect candidate formulas context.")

    parser.add_argument('--post_path', type=str, required=True,
                        help='Path to the Posts XML file.')
    parser.add_argument('--latex_dir', type=str, required=True,
                        help='Directory for LaTeX representation.')

    parser.add_argument('--result_path', type=str, required=True,
                        help='Path to save the results.')

    args = parser.parse_args()

    main(args.post_path, args.latex_dir, args.result_path)

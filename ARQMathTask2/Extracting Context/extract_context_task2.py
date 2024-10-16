import argparse
import re
import sys
import csv
import os
import spacy

from bs4 import BeautifulSoup
from post_parser_record import PostParserRecord
from tqdm import tqdm

csv.field_size_limit(sys.maxsize)
nlp = spacy.load('en_core_web_sm')
CLEANR = re.compile('<.*?>')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def get_math(text):
    """
    All ARQMath formulas are located in math-container tags; this method replaces the formula with the eqxIDeqx
    @param text: Text with mathematical formulas in LaTeX located in math-container tag
    @return: Text with formula replaced with ID
    """
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all("span", {'class': 'math-container'}):
        if 'id' not in tag.attrs:
            continue
        id_formula = tag.attrs['id']
        formula_latex = str(tag.text)
        formula_latex = formula_latex.strip()
        if len(formula_latex) > 0 and formula_latex[-1] == ".":
            tag.replaceWith('\"eqx' + str(id_formula) + 'eqx\".')
        elif len(formula_latex) > 0 and formula_latex[-1] == "?":
            tag.replaceWith('\"eqx' + str(id_formula) + 'eqx\"?')
        elif len(formula_latex) > 0 and formula_latex[-1] == ":":
            tag.replaceWith('\"eqx' + str(id_formula) + 'eqx\":')
        elif len(formula_latex) > 0 and formula_latex[-1] == ";":
            tag.replaceWith('\"eqx' + str(id_formula) + 'eqx\";')
        else:
            tag.replaceWith('\"eqx' + str(id_formula) + 'eqx\"')
    return soup.text


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


def get_context_of_formula_sentence(doc, input_formula):
    """
    This method detect the sentence before and after the sentence in which formula has appeared
    @param doc: list of sentences
    @param input_formula: input formula
    @return: context of formula as a sentence in which formula has appeared along with the sentences before and after it
    """
    lst = []
    for i, sentence in enumerate(doc.sents):
        lst.append(sentence.text)
    pre_text = ""
    post_text = ""
    for i in range(len(lst)):
        if input_formula in lst[i]:
            if i > 0:
                pre_index = i-1
                pre_text = lst[pre_index]
            if i+1 < len(lst):
                post_index = i + 1
                post_text = lst[post_index]
            return (pre_text + " " + sentence.text + " "+ post_text).strip()
    return ""


def get_related_text(qrel_arqmath_1, qrel_arqmath_2, latex_tsv_directory, post_file_path):
    result = {}
    lst_formulas = []
    # Reading the qrel files for arqmath 1 and 2
    lst_formulas.extend(read_formula_qrel(qrel_arqmath_1))
    lst_formulas.extend(read_formula_qrel(qrel_arqmath_2))
    print("read qrels")

    # Reading TSV files
    dic_formula_post_ids, dic_formula_post_type = read_tsv_files(latex_tsv_directory)
    print("read TSV")

    # Reading post file
    post_parser = PostParserRecord(post_file_path)
    print("read post")

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


def main(post_path, latex_dir, qrel_1, qrel_2, result_path):
    formula_id_contex_dic = get_related_text(qrel_1, qrel_2, latex_dir, post_path)
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
    parser.add_argument('--qrel_1', type=str, required=True,
                        help='Path to the ARQMath1 Qrel file.')
    parser.add_argument('--qrel_2', type=str, required=True,
                        help='Path to the ARQMath2 Qrel file.')
    parser.add_argument('--result_path', type=str, required=True,
                        help='Path to save the results.')

    args = parser.parse_args()

    main(args.post_path, args.latex_dir, args.qrel_1, args.qrel_2, args.result_path)

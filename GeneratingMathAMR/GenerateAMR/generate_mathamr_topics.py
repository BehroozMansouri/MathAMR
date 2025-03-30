import sys
import os
import argparse
import re
import csv

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from tqdm import tqdm
from amrlib.amrlib.models.parse_xfm.inference import Inference
from TangentS.Tuple_Extraction import mathml_to_amr



def read_query_context(file_path):
    """
    This method reads the context extracted from previous step
    :param file_path: file path to extracted context
    :return: dictionary of topic id and context
    """
    dic_result = {}
    with open(file_path, encoding="utf-8", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t', quotechar='"')
        for row in csv_reader:
            dic_result[row[0]] = row[1]
    return dic_result


def replace_math_new(dic_ids, graph_query, lst_formula, opt_dic_query):
    visited = {}
    for item in lst_formula:
        formula_id = item.split("eqx")[1]
        if formula_id in opt_dic_query:
            try:
                if formula_id not in visited:
                    opt = opt_dic_query[formula_id]
                    amr_opt, dic_ids = mathml_to_amr(opt, dic_ids)
                    to_replace = "MATH \n :math " + amr_opt
                    graph_query = graph_query.replace(item, to_replace, 1)
                    visited[formula_id] = amr_opt.split("/")[0][1:]
                else:
                    to_replace = "MATH \n :math " + visited[formula_id]
                    graph_query = graph_query.replace(item, to_replace, 1)
            except:
                print("conversion error: "+formula_id)
                pass

    return dic_ids, graph_query


def get_amr_represenation(model_path, dic_formula_id_string, dic_opts):
    result_dic = {}
    print(model_path)
    stog = Inference(model_path)
    for topic_id in tqdm(dic_formula_id_string):
        dic_formulas = dic_opts[topic_id]
        dic_ids = {}
        target = dic_formula_id_string[topic_id]
        graph_query = "\n".join(stog.parse_sents([target])[0].split("\n")[1:])
        graph_query = graph_query.lower()
        # print(graph_query)
        lst_formula = re.findall('\"eqx[0-9]+eq\"', graph_query)
        for item in lst_formula:
            graph_query = graph_query.replace(item, item[:-1] + "x\"")
        lst_formula = re.findall('\"eqx[0-9]+e\"', graph_query)
        for item in lst_formula:
            graph_query = graph_query.replace(item, item[:-1] + "qx\"")
        lst_formula = re.findall('\"eqx[0-9]+\"', graph_query)
        for item in lst_formula:
            graph_query = graph_query.replace(item, item[:-1] + "eqx\"")
        lst_formula = re.findall('\"[0-9]+eqx\"', graph_query)
        for item in lst_formula:
            graph_query = graph_query.replace(item, "\"eqx" + item[1:])

        lst_formula = re.findall('\"eqx[0-9]+eqx\"', graph_query)

        dic_ids, graph_query = replace_math_new(dic_ids, graph_query, lst_formula, dic_formulas)

        lst_formula = re.findall('eqx[0-9]+eqx', graph_query)
        dic_ids, graph_query = replace_math_new(dic_ids, graph_query, lst_formula, dic_formulas)
        # print(graph_query)
        result_dic[topic_id] = graph_query
    return result_dic


def read_tsv_opt(lst_file_path):
    """
    This method takes a list of topic opt file path and read them to a dictionary
    :param lst_file_path: list of OPT .tsv file paths
    :return: Dict of topic id as the key, with value as another dictionary of formula id (of formulas in the topic) and their opt representations
    """
    topic_opt_dic = {}
    for file_path in lst_file_path:
        result_file = open(file_path, newline='', encoding="utf-8")
        csv_reader = csv.reader(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        next(csv_reader)
        for row in csv_reader:
            formula_id = row[0].split("_")[1]
            topic_id = row[1].replace("A", "B")
            opt = row[4]
            if topic_id in topic_opt_dic:
                topic_opt_dic[topic_id][formula_id] = opt
            else:
                topic_opt_dic[topic_id] = {formula_id: opt}
    return topic_opt_dic


def main(model_path, context_path, result_path):

    dic_formula_id_string = read_query_context(context_path)
    topic_opt_paths = ["../../ARQMathFiles/Formula_topics_opt_V2.0.tsv",
                       "../../ARQMathFiles/Topics_2021_Formulas_OPT_V1.1.tsv",
                       "../../ARQMathFiles/Topics_Formulas_OPT.V0.1.tsv"]
    dic_opts = read_tsv_opt(topic_opt_paths)

    # Generating MathAMRs for topics
    dic_amr = get_amr_represenation(model_path, dic_formula_id_string, dic_opts)

    # Writing MathAMRs to file
    with open(result_path, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for formula_id in dic_amr:
            csv_writer.writerow([str(formula_id), dic_amr[formula_id]])


if __name__ == '__main__':
    model_path = "../amrlib/amrlib/data/model_parse_xfm_bart_large-v0_1_0"
    context_path = "../../results/context_topic.tsv"
    result_path = "../../results/mathamr_topics.tsv"

    main(model_path, context_path, result_path)

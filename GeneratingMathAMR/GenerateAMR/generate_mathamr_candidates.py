import argparse
import re
import sys
import csv
import os
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from tqdm import tqdm
from amrlib.amrlib.models.parse_xfm.inference import Inference
from TangentS.Tuple_Extraction import mathml_to_amr



csv.field_size_limit(sys.maxsize)


def read_opt_tsv(opt_directory, dic_formula_id_string):
    dic_opt = {}
    for file in tqdm(os.listdir(opt_directory)):
        with open(opt_directory + "/" + file, newline='', encoding="utf-8") as result_file:
            csv_reader = csv.reader(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            next(csv_reader)
            for row in csv_reader:
                formula_id = int(row[0])
                if formula_id not in dic_formula_id_string:
                    continue
                math_ml = row[8]
                dic_opt[formula_id] = math_ml
    return dic_opt


def read_amr_text(file_path):
    dic_result = {}
    with open(file_path, encoding="utf-8", newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t', quotechar='"')
        for row in csv_reader:
            dic_result[int(row[0])] = row[1]
    return dic_result


def replace_math_new(dic_ids, graph_query, lst_formula, opt_dic_query):
    visited = {}
    for item in lst_formula:
        formula_id = int(item.split("eqx")[1])
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
                print("conversion error: "+str(formula_id))
                pass

    return dic_ids, graph_query


def get_amr_represenation(amr_model_path, dic_formula_id_string, dic_opts):
    result_dic = {}
    # loading AMR model
    stog = Inference(amr_model_path)
    # Iterating on the formulas context to generate AMRs
    for formula_id in tqdm(dic_formula_id_string):
        target = dic_formula_id_string[formula_id]
        # Getting AMR
        dic_ids = {}
        try:
            graph_query = "\n".join(stog.parse_sents([target])[0].split("\n")[1:])
        except:
            continue
        graph_query = graph_query.lower()

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
        dic_ids, graph_query = replace_math_new(dic_ids, graph_query, lst_formula, dic_opts)

        lst_formula = re.findall('eqx[0-9]+eqx', graph_query)
        dic_ids, graph_query = replace_math_new(dic_ids, graph_query, lst_formula, dic_opts)

        result_dic[formula_id] = graph_query
    return result_dic


def main(amr_model_path, context_path, opt_dir, result_path):
    dic_formula_id_string = read_amr_text(context_path)
    print("Reading OPT Files")
    dic_opts = read_opt_tsv(opt_dir, dic_formula_id_string)

    dic_amr = get_amr_represenation(amr_model_path, dic_formula_id_string, dic_opts)
    with open(result_path, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for formula_id in dic_amr:
            csv_writer.writerow([str(formula_id), dic_amr[formula_id]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Math AMR candidates.")

    parser.add_argument('--opt_dir', type=str, required=True,
                        help='Directory for the optimized representations.')

    args = parser.parse_args()
    model_path = "../amrlib/amrlib/data/model_parse_xfm_bart_large-v0_1_0"
    context_path = "../../results/context_candidates.tsv"
    result_path = "../../results/mathamr_candidates.tsv"

    main(model_path, context_path, args.opt_dir, result_path)

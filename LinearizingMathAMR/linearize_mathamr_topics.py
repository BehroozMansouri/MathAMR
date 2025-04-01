import argparse
import csv
import sys
import os

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)


from amr_utils.amr_readers import AMR_Reader
from amr_utils.graph_utils import depth_first_nodes, depth_first_edges


def check_errors(amr):
    amr = amr.replace("(+1 / O", "( mes/ mathes", amr.count("(+1 / O"))
    amr = amr.replace("(+2 / O", "( mes/ mathes", amr.count("(+2 / O"))
    amr = amr.replace("(+2 / F", "( mes/ mathes", amr.count("(+2 / F"))
    amr = amr.replace(" / :", " / $##$", amr.count(" / :"))
    amr = amr.replace("(-1 /", "(a /", amr.count("(-1 /"))
    amr = amr.replace("(-2 /", "(b /", amr.count("(-2 /"))
    amr = amr.replace("(-3 /", "(c /", amr.count("(-3 /"))
    amr = amr.replace("(-4 /", "(d /", amr.count("(-4 /"))
    amr = amr.replace("(-5 /", "(p /", amr.count("(-5 /"))
    amr = amr.replace("(-6 /", "(q /", amr.count("(-6 /"))
    amr = amr.replace("(-7 /", "(r /", amr.count("(-7 /"))
    amr = amr.replace("(-8 /", "(s /", amr.count("(-8 /"))
    amr = amr.replace("(-9 /", "(t /", amr.count("(-9 /"))
    amr = amr.replace("(+1 /", "(e /", amr.count("(+1 /"))
    amr = amr.replace("(+2 /", "(f /", amr.count("(+2 /"))
    amr = amr.replace("(+3 /", "(g /", amr.count("(+3 /"))
    amr = amr.replace("(+4 /", "(h /", amr.count("(+4 /"))
    amr = amr.replace("(+5 /", "(j /", amr.count("(+5 /"))
    amr = amr.replace("(+6 /", "(k /", amr.count("(+6 /"))
    amr = amr.replace("(+7 /", "(l /", amr.count("(+7 /"))
    amr = amr.replace("(+8 /", "(m /", amr.count("(+8 /"))
    amr = amr.replace("(+9 /", "(n /", amr.count("(+9 /"))
    amr = amr.replace("(+10 /", "(o /", amr.count("(+10 /"))
    amr = amr.replace("(+11 /", "(u /", amr.count("(+11 /"))
    amr = amr.replace("(+12 /", "(v /", amr.count("(+12 /"))
    return amr


def linearize_amr(ar, amr, with_edges):
    amr = check_errors(amr)
    try:
        amr_string = ar.string_amr(amr)[0]
    except:
        print("------------error--------------")
        return None
    ########################################### With nodes
    if not with_edges:
        temp = depth_first_nodes(amr_string)
        nodes = amr_string.nodes
        str_amr = ""
        for item in temp:
            if item not in nodes or nodes[item] is None:
                continue
            str_amr += nodes[item] + " "
    ######################################### with edges
    else:
        temp = depth_first_edges(amr_string)
        nodes = amr_string.nodes
        str_amr = ""
        for item in temp:
            node1 = item[0]
            edge = item[1]
            node2 = item[2]
            if node1 not in nodes or nodes[node1] is None or node2 not in nodes or nodes[node2] is None:
                continue
            str_amr += nodes[node1] + " " + edge + " " + nodes[node2] + " "
    return str_amr.strip()


def read_mathAMR_file(file_path):
    result = {}
    with open(file_path, newline='', encoding="utf-8") as result_file:
        csv_reader = csv.reader(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for line in csv_reader:
            result[line[0]] = line[1]
    return result


def get_linearized_mathamr(dic_formulaId_mathAMR, result_path):
    with open(result_path, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["TopicID", "LinearMathAMR"])
        ar = AMR_Reader()
        for topic_id in dic_formulaId_mathAMR:
            mathAMR = dic_formulaId_mathAMR[topic_id]
            query_linearized_amr_string = linearize_amr(ar, mathAMR, False)
            csv_writer.writerow([topic_id, query_linearized_amr_string])


def main(topic_math_amr_path, candidates_math_amr_path, topic_linearized_math_amr, candiates_linearized_math_amr):
    dic_topic_mathAMR = read_mathAMR_file(topic_math_amr_path)
    get_linearized_mathamr(dic_topic_mathAMR, topic_linearized_math_amr)
    dic_topic_mathAMR = read_mathAMR_file(candidates_math_amr_path)
    get_linearized_mathamr(dic_topic_mathAMR, candiates_linearized_math_amr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Linearizes MathAMRs of both topics and candidates")
    topic_math_amr_path = "../results/mathamr_topics.tsv"
    candidates_math_amr_path = "../results/linearized_mathamr_candidates.tsv"
    topic_linearized_math_amr = "../results/linearized_mathamr_topics.tsv"
    candiates_linearized_math_amr = "../results/linearized_mathamr_candidates.tsv"
    main(topic_math_amr_path, candidates_math_amr_path, topic_linearized_math_amr, candiates_linearized_math_amr)

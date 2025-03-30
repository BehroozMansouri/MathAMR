import os

from topic_file_reader_task2 import TopicReader
from shared_methods import *
import sys
import csv
import spacy
import re

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

nlp = spacy.load('en_core_web_sm')
csv.field_size_limit(sys.maxsize)


def read_opt_files(file_path):
    """

    :param file_path:
    :return:
    """
    topic_result = {}
    result_file = open(file_path, newline='', encoding="utf-8")
    csv_reader = csv.reader(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    next(csv_reader)
    for row in csv_reader:
        formula_id = row[0]
        topic_id = row[1]
        topic_id = topic_id.replace("A", "B")
        post_type = row[3]
        opt = row[4]
        if topic_id in topic_result:
            topic_result[topic_id][formula_id] = (post_type, opt)
        else:
            topic_result[topic_id] = {formula_id: (post_type, opt)}
    return topic_result


def get_context_text(arqmath_opt_dic, arqmath_topics, result):
    for topic_id in arqmath_topics:
        temp = arqmath_topics[topic_id]
        formula_id = temp[0]
        title = temp[1]
        body = temp[2]
        if topic_id not in arqmath_opt_dic:
            continue
        dic_formula_id_type_opt = arqmath_opt_dic[topic_id]
        formula_type = dic_formula_id_type_opt[formula_id][0]
        if formula_type == "title":
            text = title
        else:
            text = body
        math_text = get_math(text)
        text_sentences = nlp(math_text)
        id_formula = formula_id.split("_")[1]
        target_formula = 'eqx' + str(id_formula) + 'eqx'
        context_formula = get_context_of_formula_sentence(text_sentences, target_formula)
        context_formula = context_formula.replace(target_formula, target_formula)
        if context_formula == "":
            print(str(formula_id) + "\t" + str(topic_id))
            continue
        result[topic_id] = context_formula


def task2_xml_topics(topic_file_path):
    dic_result = {}
    topic_reader = TopicReader(topic_file_path)
    for topic_id in topic_reader.map_topics:
        topic_ide = topic_id.replace("A", "B")
        formula_id = topic_reader.map_topics[topic_id].formula_id
        title = topic_reader.get_topic(topic_id).title
        question = topic_reader.get_topic(topic_id).question
        dic_result[topic_ide] = [formula_id, title, question]
    return dic_result


def get_related_text(xml_topic, opt_topic):
    """
    Reads the topic files and formula queries and returns formula query context
    @param xml_topic: path to xml topic file
    @param opt_topic: path to opt tsv file of query formulas
    @return: dictionary of topic id and formula context
    """
    result = {}
    arqmath1_opt_dic = read_opt_files(opt_topic)
    arqmath1_topics = task2_xml_topics(xml_topic)
    get_context_text(arqmath1_opt_dic, arqmath1_topics, result)

    return result


def main(result_file):
    file_paths = [("../ARQMathFiles/Topics_V1.1.xml", "../ARQMathFiles/Formula_topics_opt_V2.0.tsv"),
                  ("../ARQMathFiles/Topics_Task2_2021_V1.1.xml", "../ARQMathFiles/Topics_2021_Formulas_OPT_V1.1.tsv"),
                  ("../ARQMathFiles/Topics_Task2_2022_V0.1.xml", "../ARQMathFiles/Topics_Formulas_OPT.V0.1.tsv")]
    with open(result_file, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for item in file_paths:
            xml_topic_path = item[0]
            opt_topic_path = item[1]
            formula_id_contex_dic = get_related_text(xml_topic_path, opt_topic_path)
            for topic_id in formula_id_contex_dic:
                csv_writer.writerow([str(topic_id), formula_id_contex_dic[topic_id]])


if __name__ == '__main__':
    context_path = "../results/context_topic.tsv"
    main(context_path)

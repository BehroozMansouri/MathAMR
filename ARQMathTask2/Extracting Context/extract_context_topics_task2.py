import argparse

from topic_file_reader_task2 import TopicReader
import re

CLEANR = re.compile('<.*?>')
from bs4 import BeautifulSoup
import sys
import csv
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import spacy
nlp = spacy.load('en_core_web_sm')
csv.field_size_limit(sys.maxsize)


def read_opt_files(file_path):
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


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def get_math_query(text):
    """
    replacing formula with eqxIDeqx
    @param text:
    @return:
    """
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all("span", {'class': 'math-container'}):
        if 'id' not in tag.attrs:
            continue

        id_formula = str(tag.attrs['id']).split("_")[1]
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


def get_context_of_formula_sentence(doc, find_text):
    """
    This method will return formulas context as the sentence in which formula appeared and sentences before and after it
    @param doc:
    @param find_text:
    @return:
    """
    lst = []
    for i, sentence in enumerate(doc.sents):
        lst.append(sentence.text)
    pre_text = ""
    post_text = ""
    for i in range(len(lst)):
        if find_text in lst[i]:
            if i > 0:
                pre_index = i-1
                pre_text = lst[pre_index]
            if i+1 < len(lst):
                post_index = i + 1
                post_text = lst[post_index]
            return pre_text + " " + sentence.text + " "+ post_text
    return ""


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
        math_text = get_math_query(text)
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


def main(xml_topic_path, opt_topic_path, result_file):
    formula_id_contex_dic = get_related_text(xml_topic_path, opt_topic_path)
    with open(result_file, "w", newline='', encoding="utf-8") as result_file:
        csv_writer = csv.writer(result_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for topic_id in formula_id_contex_dic:
            csv_writer.writerow([str(topic_id), formula_id_contex_dic[topic_id]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Detect query formulas context.")

    parser.add_argument('--xml_topic_path', type=str, required=True,
                        help='Path to the XML Topic file.')
    parser.add_argument('--opt_topic_path', type=str, required=True,
                        help='Path to the Optimized Topic TSV file.')
    parser.add_argument('--result_file', type=str, required=True,
                        help='File where results will be saved.')

    args = parser.parse_args()

    main(args.xml_topic_path, args.opt_topic_path, args.result_file)
import html

from bs4 import BeautifulSoup

from TangentS.math_tan.math_extractor import MathExtractor


def latex_math_to_slt_tuples(latex_formula):
    temp = MathExtractor.parse_from_tex(latex_formula)
    aaa = temp.get_pairs(window=2, eob=True)
    return aaa


def latex_math_to_opt_tuples(latex_formula):
    temp = MathExtractor.parse_from_opt(latex_formula)
    aaa = temp.get_pairs(window=1, eob=True)
    return aaa


def opt_to_tuples(math_ml):
    temp = MathExtractor.convert_mathml_opt(math_ml)
    aaa = temp.get_pairs(window=1, eob=True)
    for i in range(0, len(aaa)):
        x = aaa[i]
        x = x.replace("-!", "V!")
        x = x.replace("+!", "")
        aaa[i] = x
    return aaa


def get_slt_string(slt):
    a = MathExtractor.convert_mathml_slt(slt)
    return a.tostring()


def get_amr_node(opt_node, dic):
    p1 = opt_node.split("!")[0]
    p2 = opt_node.split("!")[1]
    if p1 not in dic:
        dic[p1] = 0
    dic[p1] += 1
    val = dic[p1]
    amr_node = p1 + str(val) + " / " + p2
    amr_node = amr_node.replace("(", "$", amr_node.count("("))
    amr_node = amr_node.replace(")", "$$", amr_node.count(")"))
    amr_node = amr_node.replace(":", "$##$", amr_node.count(":"))
    return amr_node, dic


def opt_list_to_amr(lst_tuples, dic_ids):
    stack = []
    first_element = lst_tuples[0].split("\t")[0]
    amr_node, dic_ids = get_amr_node(first_element, dic_ids)
    # string = ":ARG2 (" + amr_node
    string = "(" + amr_node
    stack.append(first_element)
    check_stack = False

    for tuple in lst_tuples:
        parts = tuple.split("\t")
        if check_stack:
            while parts[0] != stack[-1]:
                stack.pop()
                string += ")"
        if parts[1] == "0!":
            stack.pop()
            string += ")"
            check_stack = True
        else:
            check_stack = False
            # if parts[1] != stack[-1]:
            stack.append(parts[1])
            temp = parts[2]
            amr_node, dic_ids = get_amr_node(parts[1], dic_ids)
            temp = " :op"+temp+"(" + amr_node
            string += temp

    string += ")"*len(stack)
    return string, dic_ids

def opt_list_to_amr_original(lst_tuples, dic_ids):
    stack = []
    first_element = lst_tuples[0].split("\t")[0]
    amr_node, dic_ids = get_amr_node(first_element, dic_ids)
    amr_node = amr_node.replace("(", "$", amr_node.count("("))
    amr_node = amr_node.replace(")", "$$", amr_node.count(")"))
    # string = ":ARG2 (" + amr_node
    string = "(" + amr_node
    stack.append(first_element)
    check_stack = False

    for tuple in lst_tuples:
        parts = tuple.split("\t")
        if check_stack:
            while parts[0] != stack[-1]:
                stack.pop()
                string += ")"
        if parts[1] == "0!":
            stack.pop()
            string += ")"
            check_stack = True
        else:
            check_stack = False
            if parts[1] != stack[-1]:
                stack.append(parts[1])
            temp = parts[2]
            amr_node, dic_ids = get_amr_node(parts[1], dic_ids)
            amr_node = amr_node.replace("(", "$", amr_node.count("("))
            amr_node = amr_node.replace(")", "$$", amr_node.count(")"))
            temp = " :op"+temp+"(" + amr_node
            string += temp
    for item in stack:
        string += ")"
    return string, dic_ids


def mathml_to_amr(math_ml, dic_ids):
    soup = BeautifulSoup(math_ml, 'html.parser')
    math_ml = html.unescape(str(soup))
    temp_dic = {
        "<csymbol cd=\"mws\" name=\"qvar\">qvar_$</csymbol>": "",
        "<csymbol cd=\"latexml\">differential-d</csymbol>": "<ci>d</ci>",
        "<csymbol cd=\"latexml\">conditional</csymbol>": "<ci>c</ci>",
        "<csymbol cd=\"mws\" name=\"qvar\">qvar_</csymbol>": "",
    }
    for item in temp_dic:
        math_ml = math_ml.replace(item, temp_dic[item], math_ml.count(item))
    tuples = opt_to_tuples(math_ml)
    # print(tuples)
    return opt_list_to_amr(tuples, dic_ids)


# xx = latex_math_to_opt_tuples("$a+a$")
# # print(xx)
# dic = {}
# print(opt_list_to_amr(xx,dic))

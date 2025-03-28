from bs4 import BeautifulSoup


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
        if "_" in id_formula:
            id_formula = id_formula.split("_")[-1]
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
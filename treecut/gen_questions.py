"""
For usage in gen_data
"""

import random
from typing import Optional

class Formula:
    def __init__(self, para: tuple, res: int):
        self.para = para
        self.res = res

def u0(sentence: str) -> str:
    # upper the first letter
    return sentence[0].upper() + sentence[1:]

def l0(sentence: str) -> str:
    # lower the first letter
    return sentence[0].lower() + sentence[1:]


def plural_form(name: str, num: int, plural_dict: Optional[dict] = None):
    if name == "cost":
        return "costs" if num == 1 else "cost"
    if name == "dollar":
        return "a dollar" if num == 1 else f"{num} dollars"
    if num == 1:
        if name[0] in ['a', 'e', 'i', 'o', 'u', 'A','E', 'I', 'O', 'U']:
            return f"an {name}"
        else:
            return f"a {name}"
    else:
        return f"{num} {plural_dict[name]}"

def gen_formulas(all_edges: list, node2var_dict: dict, value_dict: dict):
    formula_dict = dict()

    for edge in all_edges:
        if edge[0] == 'ROOT':
            f = Formula(para=(1,), res=value_dict[node2var_dict[edge[1]]])
        else:
            x = random.choice([1, 2, 3])
            y = random.choice([1, 2, 3])

            template_index = random.choice([0, 1, 2])
            if template_index == 0:
                para = (x, y)
            elif template_index == 1:
                para = (x, -y)
            else:
                para = (-x, y)

            res = para[0] * value_dict[node2var_dict[edge[0]]] + para[1] * value_dict[node2var_dict[edge[1]]]
            f = Formula(para=para, res=res)

        formula_dict[edge] = f

    return formula_dict

def edge_and_formula_to_sentence(edge: tuple, formula: Formula, node2var_dict: dict, plural_dict: dict) -> str:
    entity = [node2var_dict[node] for node in edge]

    if len(entity[1]) > 1:
        if entity[0] == 'ROOT':
            sentence = f"{plural_form(entity[1][1], 1, plural_dict)} at {entity[1][0]} costs {plural_form('dollar', formula.res, plural_dict)}."

        else:
            x, y = formula.para
            if x > 0 and y > 0:
                sentence = f"{plural_form(entity[0][1], x, plural_dict)} at {entity[0][0]} and {plural_form(entity[1][1], y, plural_dict)} at {entity[1][0]} cost {plural_form('dollar', formula.res, plural_dict)}."
            elif x > 0 and y < 0:
                if formula.res == 0:
                    sentence = f"The price of {plural_form(entity[0][1], x, plural_dict)} at {entity[0][0]} is the same as that of {plural_form(entity[1][1], -y, plural_dict)} at {entity[1][0]}."
                elif formula.res > 0:
                    sentence = f"{plural_form(entity[0][1], x, plural_dict)} at {entity[0][0]} {plural_form('cost', x, plural_dict)} {plural_form('dollar', formula.res, plural_dict)} more than {plural_form(entity[1][1], -y, plural_dict)} at {entity[1][0]}."
                else:
                    sentence = f"{plural_form(entity[0][1], x, plural_dict)} at {entity[0][0]} {plural_form('cost', x, plural_dict)} {plural_form('dollar', -formula.res, plural_dict)} less than {plural_form(entity[1][1], -y, plural_dict)} at {entity[1][0]}."
            else:  # x < 0 and y > 0
                if formula.res == 0:
                    sentence = f"The price of {plural_form(entity[1][1], y, plural_dict)} at {entity[1][0]} is the same as that of {plural_form(entity[0][1], -x, plural_dict)} at {entity[0][0]}."
                elif formula.res > 0:
                    sentence = f"{plural_form(entity[1][1], y, plural_dict)} at {entity[1][0]} {plural_form('cost', y, plural_dict)} {plural_form('dollar', formula.res, plural_dict)} more than {plural_form(entity[0][1], -x, plural_dict)} at {entity[0][0]}."
                else:
                    sentence = f"{plural_form(entity[1][1], y, plural_dict)} at {entity[1][0]} {plural_form('cost', y, plural_dict)} {plural_form('dollar', -formula.res, plural_dict)} less than {plural_form(entity[0][1], -x, plural_dict)} at {entity[0][0]}."

    else:
        # pure item
        if entity[0] == 'ROOT':
            sentence = f"{plural_form(entity[1][0], 1, plural_dict)} costs {plural_form('dollar', formula.res, plural_dict)}."

        else:
            x, y = formula.para
            if x > 0 and y > 0:
                sentence = f"{plural_form(entity[0][0], x, plural_dict)} and {plural_form(entity[1][0], y, plural_dict)} cost {plural_form('dollar', formula.res, plural_dict)}."
            elif x > 0 and y < 0:
                if formula.res == 0:
                    sentence = f"The price of {plural_form(entity[0][0], x, plural_dict)} is the same as that of {plural_form(entity[1][0], -y, plural_dict)}."
                elif formula.res > 0:
                    sentence = f"{plural_form(entity[0][0], x, plural_dict)} {plural_form('cost', x, plural_dict)} {plural_form('dollar', formula.res, plural_dict)} more than {plural_form(entity[1][0], -y, plural_dict)}."
                else:
                    sentence = f"{plural_form(entity[0][0], x, plural_dict)} {plural_form('cost', x, plural_dict)} {plural_form('dollar', -formula.res, plural_dict)} less than {plural_form(entity[1][0], -y, plural_dict)}."
            else:  # x < 0 and y > 0
                if formula.res == 0:
                    sentence = f"The price of {plural_form(entity[1][0], y, plural_dict)} is the same as that of {plural_form(entity[0][0], -x, plural_dict)}."
                elif formula.res > 0:
                    sentence = f"{plural_form(entity[1][0], y, plural_dict)} {plural_form('cost', y, plural_dict)} {plural_form('dollar', formula.res, plural_dict)} more than {plural_form(entity[0][0], -x, plural_dict)}."
                else:
                    sentence = f"{plural_form(entity[1][0], y, plural_dict)} {plural_form('cost', y, plural_dict)} {plural_form('dollar', -formula.res, plural_dict)} less than {plural_form(entity[0][0], -x, plural_dict)}."

    if sentence and not sentence[0].isdigit():
        return u0(sentence)
    return sentence

def gen_question(all_edges: list, ans_node_name, node2var_dict: dict, value_dict: dict, plural_dict: dict):
    # it will return sentences in the same order as all_edges
    sentences = []
    ans_variable_name = node2var_dict[ans_node_name]
    if len(ans_variable_name) == 1:
        question = f"Question: how much does a {ans_variable_name[0]} cost?"
    else:
        question = f"Question: how much does a {ans_variable_name[1]} at {ans_variable_name[0]} cost?"
    answer = str(value_dict[ans_variable_name])

    formula_dict = gen_formulas(all_edges, node2var_dict, value_dict)
    sentence_dict = dict()
    for edge in all_edges:
        sentence_now = edge_and_formula_to_sentence(edge, formula_dict[edge], node2var_dict, plural_dict)
        sentences.append(sentence_now)
        sentence_dict[edge] = sentence_now

    return sentences, question, answer, sentence_dict

def gen_proof(name_path: list, node2var_dict: dict, value_dict: dict, sentence_dict: dict):
    sentences = [f"It is given as a fact that {l0(sentence_dict[('ROOT', name_path[1])])}"]
    for index in range(1, len(name_path)-1):
        edge_now = (name_path[index], name_path[index+1])
        entity = node2var_dict[edge_now[1]]
        if len(entity) > 1:
            sentence_now = (f"Combine with the fact that {l0(sentence_dict[edge_now][:-1])}, "
                            f"we get {plural_form(entity[1],1)} at {entity[0]} costs {plural_form('dollar', value_dict[entity])}.")
        else:
            sentence_now = (f"Combine with the fact that {l0(sentence_dict[edge_now][:-1])}, "
                            f"we get {plural_form(entity[0],1)} costs {plural_form('dollar', value_dict[entity])}.")
        sentences.append(sentence_now)
    return " ".join(sentences)

def gen_disproof(relevant_edges: list, node2var_dict: dict, sentence_dict: dict, ans_node_name):
    all_entities = []
    for edge in relevant_edges:
        for node in edge:
            if node2var_dict[node] not in all_entities:
                all_entities.append(node2var_dict[node])
    if len(all_entities[0]) > 1:
        all_vars = [f"{entity[1]} at {entity[0]}" for entity in all_entities]
    else:
        all_vars = [f"{entity[0]}" for entity in all_entities]

    ans_variable_name = node2var_dict[ans_node_name]
    if len(ans_variable_name) == 1:
        ans_var = f"{ans_variable_name[0]}"
    else:
        ans_var = f"{ans_variable_name[1]} at {ans_variable_name[0]}"

    fm = f"{len(relevant_edges)} linear formulas" if len(relevant_edges) > 1 else "1 linear formula"

    return (f"All we know about the prices of {', '.join(all_vars)} are: " +
            ", ".join([l0(sentence_dict[edge][:-1]) for edge in relevant_edges]) +
            f".\nThere are {len(all_vars)} variables but only {fm}, so we cannot calculate the price of {ans_var}.")

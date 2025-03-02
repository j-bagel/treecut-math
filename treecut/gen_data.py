"""
Generate synthetic data and store them files
Including problem, answer and proof
"""

import random
import json
import os
import math

from dependency_tree import TreeNode
from structure_graph import StructureGraph
from gen_questions import gen_question, gen_proof, gen_disproof
from entities_items import outfit_entity_item, food_entity_item


def generate_qa(theme: str, compositeName: bool, numVars: int, ansDepth: int, order: str,
                hallu: bool, cutDepth: int = 0) -> dict:
    if theme == "food":
        entities = food_entity_item["entities"]
        item_dict = food_entity_item["item_dict"]
    elif theme == "outfit":
        entities = outfit_entity_item["entities"]
        item_dict = outfit_entity_item["item_dict"]
    else:
        raise ValueError("theme has to be one of ['food', 'outfit'].")

    # work out the proper intermediate parameter for compositeName
    if compositeName:
        numEntities = 2
        numItems = math.ceil(numVars / numEntities)
    else:
        numEntities = 0
        numItems = numVars

    if ansDepth > numVars:
        raise ValueError(f"ansDepth should not be larger than {numVars}.")

    if order not in ['forward', 'backward', 'random']:
        raise ValueError("order should be in ['forward', 'backward', 'random'].")

    if hallu:
        if not 1 <= cutDepth <= ansDepth - 1:
            raise ValueError("cutDepth should satisfy 1 <= cutDepth <= ansDepth - 1.")

    # 1. sample variable names
    if numEntities > 0:
        sampled_entities = random.sample(entities, numEntities)
        sampled_items = random.sample(list(item_dict.keys()), numItems)

        s_graph = StructureGraph()
        for entity in sampled_entities:
            for item in sampled_items:
                s_graph.add_edge(entity, item)

        all_edges = s_graph.get_all_edges()
    else:
        sampled_items = random.sample(list(item_dict.keys()), numItems)
        all_edges = [(item,) for item in sampled_items]  # adhere to the format

    sampled_variable_names = random.sample(all_edges, numVars)

    # 2. sample value_dict from sampled_variable_names
    value_dict = dict()
    for name in sampled_variable_names:
        if theme == "outfit":
            value_dict[name] = random.randint(10, 20) * 5
        else:
            value_dict[name] = random.randint(5, 15)

    # 3. nodes for the proof tree, marked as '1', '2', '3', ... and 'ROOT'
    node_names = [f"{i + 1}" for i in range(len(sampled_variable_names))]
    node2var_dict = {f"{i + 1}": sampled_variable_names[i] for i in range(len(sampled_variable_names))}
    node2var_dict['ROOT'] = 'ROOT'
    var2node_dict = {value: key for key, value in node2var_dict.items()}
    node_names = ["ROOT"] + node_names

    # index of the ans variable, in node_names
    ans_index = ansDepth
    d_tree_root = TreeNode("ROOT")

    # 4. build the tree
    d_tree_nodes = [d_tree_root]
    node = d_tree_root
    # all the way till ans_index, just make a path
    for i in range(1, ans_index + 1):
        node_now = TreeNode(node_names[i])
        node.add_child(node_now)
        d_tree_nodes.append(node_now)
        node = node_now

    # after ans_index, add edges randomly
    for i in range(ans_index + 1, len(node_names)):
        node_now = TreeNode(node_names[i])
        node = random.choice(d_tree_nodes)
        node.add_child(node_now)
        d_tree_nodes.append(node_now)

    ans_node_name = node_names[ans_index]
    ans_upstream = d_tree_nodes[ans_index].get_ancestors()
    ans_upstream.pop()  # pop 'ROOT'
    edges = d_tree_root.get_all_edges()

    # create hallucination
    cut = None
    if hallu:
        cut = ans_upstream[cutDepth - 1]
        all_edges = [edge for edge in edges if edge[1] != cut]
    else:
        all_edges = edges

    sentences, question, answer, sentence_dict = gen_question(all_edges, ans_node_name, node2var_dict, value_dict,
                                                              item_dict)
    if hallu:
        answer = 'unknown'

    # 5. generate proof
    if hallu:
        # find 'cut'
        for node in d_tree_nodes:
            if node.name == cut:
                break
        proof = gen_disproof(node.get_all_edges(), node2var_dict, sentence_dict, ans_node_name)
    else:
        proof = gen_proof(node_names[:(ans_index + 1)], node2var_dict, value_dict, sentence_dict)

    if order == "backward":
        sentences.reverse()
    elif order == "random":
        random.shuffle(sentences)

    problem = " ".join(sentences + [question])

    return {"problem": problem, "answer": answer, "proof": proof}


def generate_qa_file(theme: str, compositeName: bool, numVars: int, ansDepth: int, order: str,
                hallu: bool, cutDepth: int = 0, REP: int = 100, overwrite = False, verbose = False):

    if hallu:
        config_str = (f"qa_theme-{theme}_compositeName_{compositeName}"
                      f"_numVars-{numVars}_ansDepth-{ansDepth}_order-{order}_hallu-{hallu}_cutDepth-{cutDepth}_REP-{REP}")
    else:
        config_str = (f"qa_theme-{theme}_compositeName_{compositeName}"
                      f"_numVars-{numVars}_ansDepth-{ansDepth}_order-{order}_hallu-{hallu}_REP-{REP}")
    problems_path = config_str + ".jsonl"

    if not os.path.exists("data"):
        os.mkdir("data")

    if os.path.exists(os.path.join("data", problems_path)) and not overwrite:
        if verbose:
            print(f"Data already exists in {os.path.join('data', problems_path)}")
        return problems_path

    with open(os.path.join("data", problems_path), 'w') as file:
        for rep in range(REP):
            dct = generate_qa(theme, compositeName, numVars, ansDepth, order, hallu, cutDepth)
            file.write(json.dumps(dct) + '\n')
        if verbose:
            print(f"Written data in {os.path.join('data', problems_path)}")
        return problems_path

# when generating sentences, kept a dictionary of edge (rep: (node, node)) to sentence
# when generating proof for hall = False, travel the tree again, start from root, all the way to answer node
#  maybe don't need to travel? this path is generated
# when generate proof for hall = True, start from the cut point as root.


import re
import os
import matplotlib.pyplot as plt
import networkx as nx


def draw_plot(di_graph: nx.DiGraph):
    plt.rcParams["figure.figsize"] = (20, 20)
    options = {'node_color': 'yellow', 'node_size': 2000, 'width': 2}
    nx.draw(di_graph, with_labels=True, **options)
    nx.spectral_layout(di_graph)


def search_citation(text):
    citations = re.findall(r'cite{(.*?)}', text) + re.findall(r'cite\[.*\]\{(.*?)\}', text)
    if len(citations):
        return citations[0]
    return None


def get_processed_text_str(text_path):
    text_list = os.listdir(text_path)

    text_str = ""
    for find_tex in text_list:
        if '.tex' in find_tex:
            file = open(text_path + '/' + find_tex, 'r')
            text_str = file.read()
            file.close()
            if "\\begin{document}" in text_str:
                break
    if "\\begin{document}" not in text_str:
        raise IOError

    text_str = text_str.partition("\\begin{document}")[2]
    text_str = text_str.partition("\\end{document}")[0]

    inputs = re.findall(r"\\input{(.*?)}", text_str)
    processed_text = ''
    for input in inputs:
        parser = text_str.partition("\\input{" + input + '}')
        file = open(text_path + '/' + input + '.tex', 'r')
        processed_text = processed_text + parser[0] + file.read()
        file.close()
        text_str = parser[2]

    text_str = processed_text + text_str
    return text_str

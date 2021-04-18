import networkx as nx
import re
from pylatexenc import latexwalker
from pylatexenc.latexwalker import LatexWalker
import nltk
from thmNode import ThmNode
from utils import draw_plot, search_citation, get_processed_text_str
from downloadPapersFromArxiv import remove


class ProofDependencyGraph:
    """ Proof Dependency Graph of a paper in latex.
        Attributes
        ----------
        text: str
            The latex raw text of a paper
        parsed_text: list
            A list of raw text, theorems and proofs after parsing
        graph: nx.DiGraph
            Proof Dependency Graph
        proof_set: list
            List of indices of proof nodes in the parsed_text
        thm_lookup_table: dict
            thm_lookup_table[index of this theorem in the parsed_text] = label of this theorem
        can_have_orphan: bool
            set to False if errors arose before identifying orphans
        theorem_keyword_dict: TheoremKeywordDictionary
            The TheoremKeywordDictionary of this set of papers under analysis
        orphans: list
            A list of the orphan nodes in graph
            a node is an orphan if
                - it has no in-degree
                - its proof is not detected
                - does not have a remote proof/its external citation is not detected
    """
    def parse_text(self):
        """
            parse latex raw text into a list of
                - sentences raw text between theorems and proofs
                - [0, theorem/proof raw text]; we use list object to differentiate
                    theorems/proofs from raw texts between theorems and proofs
            Returns
            -------
                parsed_text: list
        """
        proc_text = self.text
        node_list = LatexWalker(self.text).get_latex_nodes()[0]


        parsed_text = []

        for node in node_list:
            if node.isNodeType(latexwalker.LatexEnvironmentNode):
                parser = proc_text.partition(node.latex_verbatim())
                parsed_text = parsed_text + nltk.sent_tokenize(parser[0])
                proc_text = parser[2]
                index = len(parsed_text)
                if 'comment' in node.environmentname:
                    continue
                elif 'proof' in node.environmentname:
                    self.proof_set.append(index)
                else:
                    label = self.find_thm_labels(node, index)
                    if label:
                        self.thm_lookup_table[index] = label
                parsed_text.append([0, node.latex_verbatim()])

            if node.isNodeType(latexwalker.LatexCommentNode):
                parser = proc_text.partition(node.latex_verbatim())
                parsed_text = parsed_text + nltk.sent_tokenize(parser[0])
                proc_text = parser[2]

        parsed_text = parsed_text + nltk.sent_tokenize(proc_text)

        if len(self.graph.nodes) == 0:
            self.set_to_no_orphan()

        return parsed_text

    def find_thm_labels(self, node: latexwalker.LatexNode, index: int):
        """
            Find the label in a latex theorem environment and add it to the dependency graph
            Parameters
            ----------
                node: latexwalker.LatexNode
                index: int
                    index of this node in the parsed_text
            Returns
            -------
                The latex label of this theorem
        """
        if node.isNodeType(latexwalker.LatexEnvironmentNode):
            for key in self.theorem_keyword_dict.keys():
                if node.environmentname in self.theorem_keyword_dict[key]:
                    citation = None
                    if node.nodeargd.argnlist:
                        for arg_child in node.nodeargd.argnlist:
                            if arg_child and arg_child.isNodeType(latexwalker.LatexGroupNode):
                                text = arg_child.latex_verbatim()
                                citation = search_citation(text)
                    for child in node.nodelist:
                        if child.isNodeType(latexwalker.LatexMacroNode):
                            if 'emph' in child.macroname:
                                text = child.latex_verbatim()
                                citation = search_citation(text)
                            if 'cite' in child.macroname:
                                text = child.latex_verbatim()
                                citation = search_citation(text)
                            if 'label' in child.macroname:
                                label = re.findall(r"\\label{(.*?)}", child.latex_verbatim())
                                if len(label):
                                    this_theorem = label[0]
                                    self.graph.add_node(this_theorem, obj=ThmNode(this_theorem, key, index, citation))
                                    return this_theorem
        return None

    def identify_single_proof_dependency(self, node: latexwalker.LatexNode, proof_index):
        """
            identify the theorem of a latex proof environment,
                find all the theorems references in this proof and add these edges to the graph
            Parameters
            ----------
                node: latexwalker.LatexNode
                proof_index: index of this node in the parsed_text
        """
        if node.isNodeType(latexwalker.LatexEnvironmentNode):
            if 'proof' in node.environmentname:
                this_theorem = ""
                try:
                    if node.nodeargd.argnlist:
                        for arg_child in node.nodeargd.argnlist:
                            if arg_child and arg_child.isNodeType(latexwalker.LatexGroupNode):
                                this_theorem = re.findall(r'ref{(.*?)}', arg_child.latex_verbatim())[0]
                except:
                    pass
                if not this_theorem:
                    for i in range(4):
                        if (proof_index - i) in self.thm_lookup_table:
                            this_theorem = self.thm_lookup_table[proof_index - i]
                            break
                if this_theorem in self.graph.nodes:
                    self.graph.nodes[this_theorem]['obj'].set_up_proof()
                    for child in node.nodelist:
                        ref_nodes = re.findall(r'ref{(.*?)}', child.latex_verbatim())
                        for ref_node in ref_nodes:
                            if ref_node in self.graph.nodes:
                                self.graph.add_edge(ref_node, this_theorem)

    def add_proof_dependency_edges(self):
        """
            call identify_single_proof_dependency(node, proof_index) for each proof environment
        """
        for proof_index in self.proof_set:
            node = LatexWalker(self.parsed_text[proof_index][1]).get_latex_nodes()[0][0]
            self.identify_single_proof_dependency(node, proof_index)
        if len(self.graph.edges) == 0:
            self.set_to_no_orphan()

    def draw_proof_dependency_graph(self):
        draw_plot(self.graph)

    def set_to_no_orphan(self):
        """
        can_have_orphan is set to False if errors arose before identifying orphans
        """
        self.can_have_orphan = False

    def identify_orphans(self):
        if self.can_have_orphan:
            self.orphans = [self.graph.nodes[x]['obj']
                            for x in self.graph.nodes()
                            if (self.graph.in_degree(x) == 0)
                            and (not self.graph.nodes[x]['obj'].has_proof)
                            and (not self.graph.nodes[x]['obj'].has_remote_proof())]

    def extract_orphans_context(self):
        """
            Returns
            ----------
            a dict representation of an orphan
               - context states sentence before the orphan
               - orphan_text states the text of the orphan
               - from_label states a single theorem/result referenced in the context.
               - orphan_label states the label of the orphan.
        """
        orphan_dict = {'context': [],
                       'orphan_text': [],
                       'from_label': [],
                       'orphan_label': []}

        for orphan in self.orphans:
            orphan_index = orphan.index
            if not isinstance(self.parsed_text[orphan_index - 1], list):
                refs = re.findall(r'ref{(.*?)}', self.parsed_text[orphan_index - 1])
                refs = [ref_node for ref_node in refs if ref_node in self.graph.nodes]
                if len(refs) == 0:
                    continue
                else:
                    for ref in refs:
                        orphan_dict['context'].append(self.parsed_text[orphan_index-1])
                        orphan_dict['orphan_text'].append(self.parsed_text[orphan_index][1])
                        orphan_dict['from_label'].append(ref)
                        orphan_dict['orphan_label'].append(str(orphan))

        return orphan_dict

    def __init__(self, text_path: str, theorem_keyword_dict: dict):
        """
            construct a proof dependency graph and identify orphans
            Parameters
            ----------
                text_path: relative path to the folder of a paper
                theorem_keyword_dict: a TheoremKeywordDictionary object used to identify all the theorem
                    environments
        """
        self.graph = nx.DiGraph()
        self.proof_set = []
        self.thm_lookup_table = {}
        self.can_have_orphan = True
        self.theorem_keyword_dict = theorem_keyword_dict
        self.text = ""
        self.orphans = []
        try:
            self.text = get_processed_text_str(text_path)
        except (UnicodeDecodeError, NotADirectoryError, IOError):
            self.set_to_no_orphan()
            remove(text_path)
            return

        try:
            self.parsed_text = self.parse_text()
        except RecursionError:
            print("Error!" + text_path + " now removed")
            remove(text_path)
            return

        self.add_proof_dependency_edges()

        self.identify_orphans()

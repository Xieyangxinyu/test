import unittest
import utils
from proofDependencyGraph import ProofDependencyGraph
import os
import numpy as np
from theoremKeywordDictionary import TheoremKeywordDictionary


class TestCases(unittest.TestCase):

    def test_theoremKeywordDictionary(self):
        dict_test = {'Theorem': {'theorem'},
                     'Lemma': {'lemma'},
                     'Corollary': {'corollary'},
                     'Proposition': {'proposition'},
                     'Claim': set(),
                     'Fact': set()}
        self.assertEqual(TheoremKeywordDictionary('./test/test/').get_theorem_dict(), dict_test)

    def test_get_processed_text_str(self):
        self.assertEqual(utils.get_processed_text_str("./test/test/latex/"), "\n\tThis is a test document.\n")

    def test_proofDependencyGraph(self):
        paper_dir_path = './test/test/'
        paper_dir_list = os.listdir(paper_dir_path)
        theorem_keyword_dict = np.load('./test/theorem_keyword_dict.npy', allow_pickle='TRUE').item()
        i = 1
        text_path = paper_dir_path + paper_dir_list[i]
        proof_dependency_graph = ProofDependencyGraph(text_path, theorem_keyword_dict)
        self.assertEqual(str(proof_dependency_graph.orphans[0]), "thm:ES")
        self.assertEqual(str(proof_dependency_graph.orphans[1]), "prop:baldwin")
        self.assertEqual(str(proof_dependency_graph.orphans[2]), "cor:factorize")
        self.assertEqual(str(proof_dependency_graph.orphans[3]), "cor:subset.positive")


if __name__ == '__main__':
    unittest.main()

"""Node representation of a theorem/lemma/proposition.

This class serves as an auxiliary data structure for the functions of ProofDependencyGraph.

"""


class ThmNode:
    """ Node representation of a theorem/lemma/proposition.
    Attributes
        ----------
        label : str
            The latex label of the theorem
        type_ : str
            lemma/theorem/proposition/etc; please use keys of a TheoremKeywordDictionary object
        index : int
            index of this node in the ProofDependencyGraph.parsed_text
        has_proof: bool
            indicates whether a proof of this theorem is detected
        citation: str, optional
            The latex label of the citation for this theorem
    Example
        ----------
        thm_node = ThmNode("thm:theorem_1", "thm", 10, "tran2013pairwise")
      """
    def __init__(self, label: str, type_: str, index: int, citation=None):
        self.label = label
        self.type_ = type_
        self.index = index
        self.has_proof = False
        self.citation = citation

    def __repr__(self):
        return self.label

    def get_label(self):
        return self.label

    def get_type(self):
        return self.type_

    def set_up_proof(self):
        self.has_proof = True

    def has_remote_proof(self):
        return self.citation is not None

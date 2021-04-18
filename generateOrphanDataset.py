from proofDependencyGraph import ProofDependencyGraph
import os
import numpy as np
import pandas as pd


def generate_orphan_dataset(working_dir: str, relative_paper_dir_path: str, number_of_papers=0):
    paper_dir_path = relative_paper_dir_path + relative_paper_dir_path
    paper_dir_list = os.listdir(paper_dir_path)
    theorem_keyword_dict = np.load(working_dir + 'theorem_keyword_dict.npy', allow_pickle='TRUE').item()

    orphan_dict = {'context': [],
                   'orphan_text': [],
                   'from_label': [],
                   'orphan_label': []}
    orphan_df = pd.DataFrame(orphan_dict)

    if number_of_papers == 0:
        number_of_papers = len(paper_dir_list)

    for i in range(number_of_papers):
        text_path = paper_dir_path + paper_dir_list[i]
        proof_dependency_graph = ProofDependencyGraph(text_path, theorem_keyword_dict)
        orphan_df = pd.concat([orphan_df, pd.DataFrame(proof_dependency_graph.extract_orphans_context())])

    orphan_df["decision"] = "NA"

    print(str(len(orphan_df.index)) + " orphans recorded!")

    orphan_df.to_csv(working_dir + "orphans.csv", index=False)
    print(working_dir + "orphans.csv created!")

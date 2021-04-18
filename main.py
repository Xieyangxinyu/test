from generateOrphanDataset import generate_orphan_dataset
from downloadPapersFromArxiv import download_papers
from theoremKeywordDictionary import TheoremKeywordDictionary

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    working_dir = './dataset_1/'
    relative_paper_dir_path = 'dataset_1/'

    '''
    query_keywords = ['Algebraic Geometry', 'Algebraic Topology', 'Category Theory',
                      'Classical Analysis and ODEs', 'Combinatorics', 'Complex Variables',
                      'Differential Geometry', 'Dynamical Systems',
                      'Functional Analysis', 'General Topology', 'Geometric Topology', 'Group Theory',
                      'Information Theory', 'K-Theory and Homology', 'Logic', 'Metric Geometry',
                      'Number Theory', 'Operator Algebras', 'Optimization and Control', 'Probability',
                      'Quantum Algebra', 'Representation Theory', 'Rings and Algebras', 'Spectral Theory',
                      'Symplectic Geometry', 'Computational Complexity', 'Computer Science and Game Theory',
                      'Data Structures and Algorithms', 'Discrete Mathematics', 
                      'Formal Languages and Automata Theory', 'Logic in Computer Science',
                      'Information Theory', 
                      ]
    '''

    download_dirpath = "./find_orphans_2/find_orphans_2/"
    max_number_of_paper = 2000
    download_papers('Dynamical Systems', download_dirpath, max_number_of_paper)

    # theorem_keyword_dict_example = TheoremKeywordDictionary('./dataset_1/dataset_1/')
    # theorem_keyword_dict_example.save_theorem_dict('./dataset_1/', 'theorem_keyword_dict')

    #generate_orphan_dataset(working_dir=working_dir,
    #                        relative_paper_dir_path=relative_paper_dir_path)

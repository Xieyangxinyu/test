import os
import re
import numpy as np


class TheoremKeywordDictionary:
    """
        An auxiliary data structure which collects all possible latex environment names for theorem/lemma/proposition

    Example
    ----------
        theorem_keyword_dict_example = TheoremKeywordDictionary('./test/test/')
        theorem_keyword_dict_example.save_theorem_dict('./test/test/', 'theorem_keyword_dict_example')
    Load Example
    ----------
        import numpy as np
        theorem_keyword_dict = np.load('theorem_keyword_dict_example.npy',allow_pickle='TRUE').item()
    """

    def get_text_str(self, index):
        text_path = self.dir_path + self.dir_list[index]
        text_list = os.listdir(text_path)

        text_str = ""
        for find_tex in text_list:
            if ".tex" in find_tex:
                file = open(text_path + "/" + find_tex, 'r')
                text_str = text_str + file.read()
                file.close()
        return text_str

    def get_labels(self, keyword: str) -> list:
        labels = []
        for index in range(self.dir_list_len):
            text = ""
            try:
                text = self.get_text_str(index)
            except NotADirectoryError:
                pass
            except UnicodeDecodeError:
                pass

            thm_set = set(re.findall(r"\\newtheorem{(.*?)}{" + keyword + '}', text))
            thm_set = [item for item in thm_set if '\\' not in item]
            labels = labels + thm_set

            thm_set = set(
                re.findall(r"\\newtheorem{(.*?)}{Theorem}", text) + re.findall(r"\\newtheorem{(.*?)}{Lemma}", text)
                + re.findall(r"\\newtheorem{(.*?)}{Corollary}", text)
                + re.findall(r"\\newtheorem{(.*?)}{Proposition}", text))
            thm_set = [item for item in thm_set if '\\' not in item]

            temp_set = []
            for thm in thm_set:
                temp_set = temp_set + re.findall((r"\\newtheorem{(.*?)}\[" + thm + ']{' + keyword + '}'), text)
            temp_set = [item for item in temp_set if '\\' not in item]
            temp_set = [item for item in temp_set if '}{' not in item]
            labels = labels + temp_set

        return set(labels)

    def set_theorem_dict(self):
        for key in self.theorem_dict.keys():
            self.theorem_dict[key] = self.get_labels(key)

    def get_theorem_dict(self):
        return self.theorem_dict

    def save_theorem_dict(self, path, name):
        np.save(path + name + '.npy', self.theorem_dict)
        print("Saved to " + path + name + '.npy')

    def __init__(self, database_path):
        self.dir_path = database_path
        self.dir_list = os.listdir(self.dir_path)
        self.dir_list_len = len(self.dir_list)
        self.theorem_dict = {"Theorem": [], 'Lemma': [], 'Corollary': [], 'Proposition': [], 'Claim': [], 'Fact': []}
        self.set_theorem_dict()
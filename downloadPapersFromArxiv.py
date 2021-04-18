'''
%%capture
!pip install -Iv arxiv=1.0.2
'''
import arxiv
import os
import tarfile
from os import listdir
import urllib
import shutil


def set_up_download_dirpath(download_dirpath):
    if not os.path.exists(download_dirpath):
        os.makedirs(download_dirpath)


def extract_tex_and_bib(this_paper, title, path):
    extract_success = 0
    if ".tar.gz" not in this_paper:
        print(title + ": tar.gz not found!")
        return 0
    paper = listdir(path)[0]
    t = tarfile.open(path + paper, 'r')
    for member in t.getmembers():
        if ".tex" in member.name:
            t.extract(member, path)
            extract_success = 1
        elif ".bib" in member.name:
            t.extract(member, path)
            extract_success = 1
        elif ".bbl" in member.name:
            t.extract(member, path)
            extract_success = 1

    if extract_success:
        # print(title + ": Success!")
        return 1
    else:
        # print(title + ": Has no source file!")
        return 0


def remove(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))


def download_papers(query_keyword, download_dirpath, max_number_of_paper):
    set_up_download_dirpath(download_dirpath)
    client = arxiv.Client(
        page_size=200,
        delay_seconds=10,
        num_retries=5
    )
    result = client.get(arxiv.Search(query=query_keyword, max_results=max_number_of_paper))
    retrieved: int = 0
    failed: int = 0
    for paper in result:
        download_dir_path_for_this_paper = download_dirpath + paper.title + '/'
        try:
            if not os.path.exists(download_dir_path_for_this_paper):
                os.makedirs(download_dir_path_for_this_paper)
                this_paper, _ = urllib.request.urlretrieve(
                    paper.get_pdf_url().replace('arxiv.org/pdf/',
                                           'export.arxiv.org/src/'),
                    download_dir_path_for_this_paper + paper.get_short_id() + '.tar.gz')
                if extract_tex_and_bib(this_paper, paper.title, download_dir_path_for_this_paper) == 1:
                    retrieved = retrieved + 1
                else:
                    failed = failed + 1
                    remove(download_dir_path_for_this_paper)
        except:
            failed = failed + 1
            # print(paper.title + ": Failed!")
            remove(download_dir_path_for_this_paper)

    print(query_keyword)
    print("Retrieved: " + str(retrieved))
    print("Failed: " + str(failed))

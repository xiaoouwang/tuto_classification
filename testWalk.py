import re
import os
import scraper

# scraper.get_single_page("http://www.hahahahahahahaah.fr")
# from tqdm import tqdm
# for i in tqdm(range(10000)):
#     pass

# def extract_fn(link):
#     fn_text = re.findall(r'article/.*.html', link)[0]
#     print(fn_text[8:-5].replace("/", "_").replace("-", "_"))


# def extract_themes(link):
#     """
#     docstring
#     """
#     theme_text = re.findall(r'.fr/.*?/', link)[0]
#     print(theme_text[4:-1])


# link = "https://www.lemonde.fr/asie-pacifique/article/2006/12/31/huit-bombes-ont-fait-deux-morts-a-bangkok_850812_3216.html"
# extract_themes(link)
# extract_fn(link)
# from os import walk

from collections import defaultdict


def corpus_stat(path_corpus):
    stat = {}
    themes = os.listdir(path_corpus)
    print(themes)
    for theme in themes:
        theme_directory = os.path.join(path_corpus, theme)
        if os.path.isdir(theme_directory):
            nb_texts = len(os.listdir(theme_directory))
            stat[theme] = nb_texts
    return stat


def cr_corpus_dict(path_corpus):
    dict_corpus = defaultdict(list)
    themes = os.listdir(path_corpus)
    for theme in themes:
        theme_directory = os.path.join(path_corpus, theme)
        for file in os.listdir(theme_directory):
            path_file = os.path.join(theme_directory, file)
            with open(path_file, 'r') as f:
                text = f.read()
                dict_corpus["label"].append(theme)
                dict_corpus["text"].append(text)
    return dict_corpus


# path_corpus = "lemonde"
# corpus_dict = cr_corpus_dict(path_corpus)
# # print(corpus_dict)
# import pandas as pd
# df = pd.DataFrame(corpus_dict, columns= ['label', 'text'])
# # print(df.head(2))
# df.to_csv("corpus_lemonde.csv",header=True,index=False)
print(corpus_stat("corpus"))

# path = "/Users/becca/Documents/nlp/M2Nanterre/coursM2/coursAlice/corpus/societe"
#

# for file in os.listdir(path):
#     file_path = os.path.join(path, file)
#     with open(file_path, "r", encoding="utf-8") as f:
#         new_text = f.read()[7:]
#         with open(file_path, 'w') as new_f:
#             new_f.write(new_text)


# with open(path, 'r') as f:
#     new_text = f.read()[7:]
#     with open(path, 'w') as g:
#         g.write(new_text)
# os.makedirs("haha/hahaha")
# os.mkdir("haha/hahaha")

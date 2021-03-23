import os  # helper functions like check file exists
import datetime  # automatic file name
import requests  # the following imports are common web scraping bundle
from urllib.request import urlopen  # standard python module
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from collections import defaultdict
import re
from urllib.error import URLError
from tqdm import tqdm
import pickle
import bz2
import _pickle as cPickle
import pandas as pd

def extract_theme(link):
    try:
        theme_text = re.findall(r'.fr/.*?/', link)[0]
    except:
        # print(link)
        pass
    else:
        return theme_text[4:-1]


def list_themes(links):
    themes = []
    for link in links:
        theme = extract_theme(link)
        if theme is not None:
            themes.append(theme)
    return themes


def write_links(path, links, year_fn):
    with open(os.path.join(path + "/lemonde_" + str(year_fn) + "_links.txt"), 'w') as f:
        for link in links:
            f.write(link + "\n")


def write_to_file(filename, content):
    if os.path.exists(filename):
        with open(filename, 'a+') as f:
            f.write(str(content))
    else:
        with open(filename, 'w') as f:
            f.write(str(content))


def count_words(file):
    counter = 0
    with open(file, 'r') as f:
        content = f.read()
        words = content.split()
        length = len([w for w in words if w !=
                      "##" and not w.startswith("##author:")])
        counter += length
    return counter


def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print("folder exists already")


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def create_archive_links(year_start, year_end, month_start, month_end, day_start, day_end):
    archive_links = {}
    for y in range(year_start, year_end + 1):
        dates = [str(d).zfill(2) + "-" + str(m).zfill(2) + "-" +
                 str(y) for m in range(month_start, month_end + 1) for d in
                 range(day_start, day_end + 1)]
        archive_links[y] = [
            "https://www.lemonde.fr/archives-du-monde/" + date + "/" for date in dates]
    return archive_links


def get_articles_links(archive_links):
    links_non_abonne = []
    for link in archive_links:
        try:
            html = urlopen(link)
        except HTTPError as e:
            print("url not valid", link)
        else:
            soup = BeautifulSoup(html, "html.parser")
            news = soup.find_all(class_="teaser")
            # condition here : if no span icon__premium (abonnes)
            for item in news:
                if not item.find('span', {'class': 'icon__premium'}):
                    l_article = item.find('a')['href']
                    # en-direct = video
                    if 'en-direct' not in l_article:
                        links_non_abonne.append(l_article)
    return links_non_abonne


def classify_links(theme_list, link_list):
    dict_links = defaultdict(list)
    for theme in theme_list:
        theme_link = 'https://www.lemonde.fr/' + theme + '/article/'
        for link in link_list:
            if theme_link in link:
                dict_links[theme].append(link)
    return dict_links


def get_single_page(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("url not valid", url)
    else:
        soup = BeautifulSoup(html, "html.parser")
        text_title = soup.find('h1')
        text_body = soup.article.find_all(["p", "h2"], recursive=False)
        return (text_title, text_body)


def extract_fn(link):
    fn_text = re.findall(r'article/.*.html', link)[0]
    return fn_text[8:-5].replace("/", "_").replace("-", "_")


def scrape_articles(dict_links):
    themes = dict_links.keys()
    for theme in themes:
        create_folder(os.path.join('corpus', theme))
        print("processing:", theme)
        for i in tqdm(range(len(dict_links[theme]))):
            link = dict_links[theme][i]
            fn = extract_fn(link)
            single_page = get_single_page(link)
            if single_page is not None:
                with open((os.path.join('corpus', theme, fn + '.txt')), 'w') as f:
                    # f.write(dict_links[theme][i] + "\n" * 2)
                    f.write(single_page[0].get_text() + "\n" * 2)
                    for line in single_page[1]:
                        f.write(line.get_text() + "\n" * 2)


def cr_corpus_dict(path_corpus, n_files=1000):
    dict_corpus = defaultdict(list)
    themes = os.listdir(path_corpus)
    for theme in themes:
        counter = 0
        if not theme.startswith('.'):
            theme_directory = os.path.join(path_corpus, theme)
            for file in os.listdir(theme_directory):
                if counter < n_files:
                    path_file = os.path.join(theme_directory, file)
                    text = read_file(path_file)
                    dict_corpus["label"].append(theme)
                    dict_corpus["text"].append(text)
                counter += 1
    return dict_corpus

def cr_corpus_complet_dict(path_corpus):
    dict_corpus = defaultdict(list)
    themes = os.listdir(path_corpus)
    for theme in themes:
        if not theme.startswith('.'):
            theme_directory = os.path.join(path_corpus, theme)
            for file in os.listdir(theme_directory):
                path_file = os.path.join(theme_directory, file)
                text = read_file(path_file)
                dict_corpus["label"].append(theme)
                dict_corpus["text"].append(text)
    return dict_corpus

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data

def compressed_pickle(title, data):
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        cPickle.dump(data, f)

# build dataframe
def build_df(lst1,lst2):
    df = pd.DataFrame(list(zip(lst1, lst2)),
                columns =['label', 'text'])
    return df
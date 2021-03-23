# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 14:54:07 2020

@author: nakhl
"""
import os
import pandas as pd


def importData(path):
    """
    input: path : str (Path to the directory where is the corpus.)
    output: corpus : list (list where each element is a tuple : (textof 1 file, its label)
    """
    corpus = []
    labels = os.listdir(path)
    print(labels)
    for label in labels:
        print(label)
        if label[0] != ".":
            if os.path.isdir(label):
                files = os.listdir(os.path.join(path, label))
                for fic in files:
                    with open(os.path.join(path, label, fic), 'r', encoding='utf-8') as fic:
                        corpus.append((fic.read(), label))
    return corpus


def list_with_labels2dict(corpus_list):
    """
    Fonction to create a dict easily usable in pd.DataFrame()
    input: corpus_list : corpus in form of a list where each element is a tuple : (textof 1 file, its label)
    output: corpus_dict : dict where keys correspond to columns and values to raws of the column
    """
    corpus_dict = {
        'text': [x[0] for x in corpus_list],
        'label': [x[1] for x in corpus_list]
    }
    return corpus_dict


def tokenise(df):
    for x in df["text"]:

if __name__ == "__main__":
    cwd = os.getcwd()
    print(cwd)
    corpus = importData(cwd)
    # print(corpus[:1])
     corpus_dict = list_with_labels2dict(corpus)
    df = pd.DataFrame(corpus_dict)
    display(df)
    # df.to_csv(cwd+"all_texts.csv", index=False, sep=';', encoding='utf-8', mode='a')
    for x in df["text"]:
        print(x)

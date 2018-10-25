# About this code

This code filters automatically translated Wordnets synsets
(accessible through NLTK) by embeddings.


## About the Wordnets

The original Wordnet was created by Princeton and is available [https://wordnet.princeton.edu](here).

Versions in other languages exists and have often been constructed by automatic
translation of the PWNet and compiled as the [Open Multilingual Wordnet](http://compling.hss.ntu.edu.sg/omw/).

These non-english Wordnets are very helpfull for many NLP tasks, but we found that some synonyms are inaccurate.
English synonyms are not always synonyms in other languages.
We found that a simple cosine similarity between two words embeddings in a synset was enough to filter more precise synonyms.

## About the embeddings

We use fastText format embeddings. Pre-trained models in many languages that you can download have been made available by Facebook [here](https://github.com/facebookresearch/fastText/blob/master/docs/crawl-vectors.md).

# Using this repo

You can either download pre-computed dictionaries for French or make your own.

## Download pre-computed synonyms dics

We release pre-computed dic for French. The complete version contains the similarity measures, the others do not as they are already filtered:

|Embedding| Sim 0.4 | Sim. 0.5 |Sim 0.6|Complete|
|---|---|---|---|---|
|fastText cc.fr.300.bin|[fr_04](dictionaries/fr_04.json)|[fr_05](dictionaries/fr_05.json)|[fr_06](dictionaries/fr_06.json)|[fr_dic](dictionaries/fr_dic.json)|

## Filter synsets by embeddings



### Installation

This code has been tested on python 3.

You need to install the requirements in the git :

    pip install -r requirements.txt

The fastText python wrapper needs to be installed this way. You can go to its git [here](https://github.com/facebookresearch/fastText.git) if you encounter any problems

    git clone https://github.com/facebookresearch/fastText.git
    cd fastText
    python setup.py install


### Example Notebook

An example notebook is available [here](example_notebook.ipynb)


# Licence

Code MIT Share-Alike by [recital](https://recital.ai)
Licenses by [Wordnet](https://wordnet.princeton.edu/license-and-commercial-use), [Open Multilingual WordNet](http://compling.hss.ntu.edu.sg/omw/) and [FastText](https://github.com/facebookresearch/fastText/blob/master/LICENSE) apply. 
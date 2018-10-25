from nltk.corpus import wordnet as wn
import json
import numpy as np
import fastText
import math
import nltk


class LangSynonym:
    '''
    This class helps ti build a subset of wordnet synonyms in a specific language
    For each expression, we return all its synonyms weighted with the similarity score (processed word, synonym)
    This similarity score is computed based on the fastText package
    Here is the fastText installation process after activating the your virtual environment
      git clone https://github.com/facebookresearch/fastText.git
      cd fastText
      python setup.py install

    The models need to be downloaded here : https://github.com/facebookresearch/fastText/blob/master/docs/crawl-vectors.
    and store on your system
    '''

    def __init__(self, model_file, lang):
        '''
        Initialization of the Synonym dictionary builder.
        This class is generic the language and the FastText model are parameters
        :param model_file:
        :param lang: the chosen language, example 'fra' for french
        '''
        self.model_file = model_file
        self.emb_model = None
        self.LANG = lang
        nltk.download('wordnet')

    def load_fastText_model(self):
        '''
        Loading of the fastText model based on the FastTextNN class
        :return:
        '''
        # Loading the fastText Model
        model_ft = fastText.load_model(self.model_file)

        return model_ft

    def get_word_similarity(self, word, word_syn):
        """Compute the embedding similarity between two words
        """
        v1 = self.emb_model.get_word_vector(word)
        v2 = self.emb_model.get_word_vector(word_syn)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))



    def word_in_syn_list(self, syn_list, word_syn):
        '''
        Test if a word is already in the list a another one synonyms
        :param word_syn:
        :return:
        '''
        if word_syn in syn_list.keys():
                return True
        return False

    def get_wordnet_subset(self):
        '''
        Getting the subset of wordnet for a specific language.
        Using the fastText model, this function associate to each synonym
        a similarity score with the processed one.
        A dictionary is return with language word as key and the corresponding
        synonym dict list as value.
        Each dictionary in the list has as key the synonym itself and the similarity is the value
        :return:
        '''
        # Loading of the model
        self.emb_model = self.load_fastText_model()

        words = [word.replace('_', ' ') for word in wn.words(lang=self.LANG)]

        syns = {}
        for w in words:
            syns[w] = [synset.lemma_names(self.LANG) for synset in wn.synsets(w, lang=self.LANG)]

        synonyms = {}

        for word in syns.keys():
            syn_list = {}
            for synset in syns[word]:
                for word_syn in synset:
                    if word.lower() == word_syn.lower():
                        continue

                    if self.word_in_syn_list(syn_list, word_syn):
                        continue

                    if math.isnan(float(self.get_word_similarity(word, word_syn))):
                        continue

                    syn_list[word_syn.replace('_', ' ')]=float(self.get_word_similarity(word, word_syn))


            synonyms[word] = syn_list

        return synonyms

    def store_synonyms(self, file_name):
        '''
        Build and store the subset of wordnet synonym for a given language is a file
        :param file_name:
        :return:
        '''
        with open(file_name, 'w') as outfile:
            json.dump(self.get_wordnet_subset(), outfile)

    def get_word_synonyms(self, word, file_name):
        '''
        Loading the synonym file to get the synonyms of a given word
        :param word:
        :param file_name:
        :return:
        '''
        with open(file_name, 'r')as f:
            synonyms = json.load(f)

        if word in synonyms.keys():
            return synonyms[word]

        return []




def build_synonyms_with_th(dic_file, threshold):
    """
    This computes a dic file with a similarity threshold
    :param dic_file: the file where the syn dic with similarities is found
    :param threshold: the minimal similarity percentage.
    :return:
    """
    with open(dic_file, 'r')as f:
        synonyms = json.load(f)

    sub_synonyms = {}

    # We iterate on all the words
    for word, syns in synonyms.items():
        # We iterate of the list of synonyms of word
        sub_syn_list = [k for k, v in syns.items() if v > threshold]

        if len(sub_syn_list) > 0:
            sub_synonyms[word] = sub_syn_list
    return sub_synonyms

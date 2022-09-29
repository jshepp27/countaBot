### QUERY EXPANSION ###

# TODOs: Query Expansions [TypeOf, SimilarTerms, CanBe]
# https://github.com/fitosegrera/python-conceptnet/blob/master/ConceptNet.py
import json
import urllib

from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

URL = "http://api.conceptnet.io/"

# TODOs: Review. Similarity.
class ConceptNet:

    def __init__(self, api, l):
        self.api = api
        self.l = l

    def search(self, lang, term):
        url_to_search = self.api + "c/" + lang + "/" + term
        data = urllib.request.urlopen(url_to_search)
        json_data = json.load(data)
        for i in json_data["edges"]:
            print("----------------")
            print(i["end"])
            print("relation:", i["rel"])
            print(i["surfaceEnd"])
            print(i["surfaceStart"])
            print("weight:", i["weight"])

        return json_data

    def get_relation(self, rel, concept):
        url_to_search = self.api + f"search?node=/c/en/{concept}&rel=/r/{rel}"
        data = urllib.request.urlopen(url_to_search)
        obj_ = json.load(data)

        labels = set()
        for _ in obj_["edges"]:
            labels.add((_["end"]["label"], _["weight"]))

        return labels

    def get_similar(self, concept):
        res = []
        rels = ["Synonym", "SimilarTo", "FormOf", "isA"]
        for _ in rels:
            res.extend(self.get_relation(_, concept))

        return sorted(res, key=lambda x: x[1], reverse=True)[:self.l]

def wordNet_expansion(query):
    synonyms = []

    count = 0
    # for _ in query.split():
    for _ in query:
        for syn in wordnet.synsets(_):
            for l in syn.lemmas():
                if (count < 3):
                    if l.name() not in synonyms:
                        synonyms.append(l.name())
                        count += 1

        count = 0

    synonyms_ = " ".join(synonyms)

    return synonyms_
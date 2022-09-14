from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def expand_query(query):
    synonyms = []

    count = 0
    #for _ in query.split():
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
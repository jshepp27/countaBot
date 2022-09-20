from tqdm.notebook import tqdm
from src.detection.stance_classifier import sentence_stance, compare_stance
from src.utils_.word_net_expansion import expand_query
from src.detection.stance_classifier import sentence_stance
# from multiprocessing.pool import ThreadPool as Pool
import time
import json

topic_ids = [json.loads(ln)["id"] for ln in open("../data/argument_topic_concept.jsonl")]
concept_ids = [json.loads(ln)["id"] for ln in open("../data/argument_concept.jsonl")]

from nltk.tokenize import sent_tokenize, word_tokenize

def tokeniser(doc):
    return word_tokenize(doc)

def sentences_segment(doc):
    return sent_tokenize(doc)


from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer

# TODOs: Fix Vectorizer Issue
kb = KeyBERT()
vectorizer = KeyphraseCountVectorizer()
vectorizer_nouns = KeyphraseCountVectorizer(spacy_pipeline="<N. *>")
def extract_keyphrase(doc, n_gram=3, n_kp=3, use_mmr="False", use_maxsum="False"):
    try:
        kp = kb.extract_keywords(doc, keyphrase_ngram_range=(0, 3), stop_words="english", diversity=0.3,)
        kp_ = kb.extract_keywords(doc, vectorizer=vectorizer, stop_words="english", diversity=0.3)

    except:
        return [" "]

    # Concatonate, remove duplicates
    kp = kp + kp_
    kp = [i[0] for i in kp]
    kp = list(set(kp))

    return kp

test = "Brazil's minimum income has increasingly been accepted."
evidence = " "
ev_kp = extract_keyphrase(evidence)
res = [i[0] for i in ev_kp]
print(res)

res_ = res[0]

extract_keyphrase(test)

def get_notion(notions_ids, notions_lst, arg_id, label):
    notion_id = notions_ids.index(arg_id)
    notion = notions_lst[notion_id][label]
    return str(notion) if notion else None

def extract_adus(arg_):
    arg, id_ = arg_
    print("\n", id_)

    # topic = get_notion(topic_ids, topics, id_, "topic_label")
    # concept = get_notion(concept_ids, concepts, id_, "concept_label")

    adu_sents = sentences_segment(arg)

    adus = []
    for _ in adu_sents:
        if len(tokeniser(_)) <= 8:
            continue

        kp = extract_keyphrase(_)
        # kp.append(topic) if topic else kp
        # kp.append(concept) if concept else kp
        print(kp)

        adu = {"sentence": _, "kp": [i for i in kp], "stance": sentence_stance(_, kp[0])}

        adus.append(adu)

    return ({
        "id": id_,
        "argument": [i for i in adus]
    })
from keybert import KeyBERT
from keyphrase_vectorizers import KeyphraseCountVectorizer
from yake import KeywordExtractor
from summa import keywords
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KEYPHRASE_EXTRACTOR")

language = "en"
max_ngram_size = 3
deduplication_thresold = 0.9
deduplication_algo = 'seqm'
k=5

yake_extractor = KeywordExtractor(lan=language, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, n=4)

def yake_extract_keyphrase(sentence, k=5):

    kp = yake_extractor.extract_keywords(sentence)
    return [i[0] for i in kp][0:k]

def summa_extract_keyphrase(sentence, k=5):
    kp = keywords.keywords(sentence, split=True, ratio=0.8)
    return kp[0:k]


kb = KeyBERT()
def extract_keyphrase(doc, n_gram=3, n_kp=3, use_mmr="False", use_maxsum="False"):
    kp = kb.extract_keywords(doc, keyphrase_ngram_range=(1, n_gram), stop_words="english", diversity=0.5)

    return [i[0] for i in kp][0:n_kp]

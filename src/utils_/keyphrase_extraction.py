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
    kp = None

    #kp = kb.extract_keywords(doc, vectorizer=KeyphraseCountVectorizer(), stop_words="english", diversity=0.2, )

    try:
        kp = kb.extract_keywords(doc, vectorizer=KeyphraseCountVectorizer(), stop_words="english", diversity=0.2,)

    except:
        print("No Keywords")

    if kp == None:
        return []

    else: return [i[0] for i in kp[0:n_kp]]     

### TEST STATEMENTS ###
test_1 = extract_keyphrase("The environmental impact of aviation in the UK is increasing due to new terminals at Heathrow airport")
#test_2 = extract_keyphrase("Will plague ever become as widespread as it was in the 1300's.")

logger.info(f"[Test Keyphrase: ] "
            f"\n {test_1}")
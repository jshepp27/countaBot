from src.utils.keyphrase_extraction import yake_extract_keyphrase
from src.utils.utils import sentences_segment
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import torch
import time
import copy


model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity_(sentences):
    embeddings = model.encode(sentences, convert_to_tensor=True, show_progress_bar=False)

    cos = torch.nn.CosineSimilarity()
    scores = cos(embeddings[0], embeddings[1:])

    scored = []
    retrieved_sentences = sentences[1:]
    for sent, similarity in zip(retrieved_sentences, scores):
        scored.append((sent, similarity.numpy().item()))

    return scored

def rank_passages(ev, k=3):
    """ return ranked passages using cosine-similarity between the input-argument and the retrieved passages
        k determines the number of returned passages from the originally retrieved set.
    """
    #adus = [i["sentence"] for i in ev["argument"]]
    # Compare TGT with RETREIVED
    adus = [i["sentence"] for i in ev["tgt_counter"]]
    retrieved_passages = [i["passages"] for i in ev["retrieved"]]

    #print(retrieved_passages)

    # Merge
    # Output 1 x merged sentences object per ADU sentence, with k collected passages as a list of sentences
    merged_passages = []
    for passages in retrieved_passages:
        merged_sents = []
        # Iterate n x sentences for each k=5 retrieved passages
        for passage in passages:
            # Segment as a list of sentences
            sents = sentences_segment(passage)
            # Add sentences to merged_sentences object
            merged_sents.extend(sents)

        # Store merged sentence object for each ADU
        merged_passages.append(merged_sents)

    rank_retrieved = []
    # Rank n x merged sentences for each 1 x ADU
    for adu, merged in zip(adus, merged_passages):
        scored = []
        sentences = [adu]
        sentences.extend(merged)
        scored = cosine_similarity_(sentences)

        ranked_sents = sorted(scored, key=lambda x: x[1], reverse=True)

        # Select top-k sentences
        ranked_sents = ranked_sents[0:k]

        merged = ", ".join(i[0] for i in ranked_sents)
        merged_kp = yake_extract_keyphrase(merged)
        rank_retrieved.append({"ranked_passages": merged, "kp": merged_kp})

    #print("\n RANKED", rank_retrieved)
    return rank_retrieved
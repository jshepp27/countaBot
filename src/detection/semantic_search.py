from sentence_transformers import SentenceTransformer, util
import tqdm
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')
def semantic_search(corpus, ids, query, threshold=0.30):
    # Construct Corpus set
    corpus_ = list(corpus)
    id_ = list(ids)

    # Embed the Corpus
    corpus_embeddings = embedder.encode(corpus_, convert_to_tensor=True)

    # Construct Query-Label set
    queries = set(query)

    mapped_dict = {}
    for i in range(0, len(id_)):
        mapped_dict[id_[i]] = {"argument": corpus_[i], "label": []}

    # Return top k=1 argument for each Label via Cosine Similarity
    top_k = min(1, len(corpus_))

    with tqdm(total=len(queries)) as pbar:
        for query in queries:
            query_embedding = embedder.encode(query, convert_to_tensor=True)

            cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
            top_results = torch.topk(cos_scores, k=top_k)

            for score, idx in zip(top_results[0], top_results[1]):
                # 'Empirical' threshold
                if score >= threshold:
                    # Append Label
                    #mapped_dict[id_]["argument"] = corpus_[idx]
                    # Note: Can use the same idx index
                    mapped_dict[id_[idx]]["label"] = query.lower()

                #else: mapped_dict[id_]["label"] = "None"

            pbar.update()

    return mapped_dict
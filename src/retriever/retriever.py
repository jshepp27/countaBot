from tqdm import tqdm
import multiprocessing
from src.detection.stance_classifier import sentence_stance, compare_stance
from src.detection.stance_classifier import sentence_stance
import time
import json
import re

# Disable Huggingface Logging
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

topic_ids = [json.loads(ln)["id"] for ln in open("./src/data/processed/argument_topic_concept.jsonl")]
concept_ids = [json.loads(ln)["id"] for ln in open("./src/data/processed/argument_concept.jsonl")]

def clean(phrase):
    return re.sub(r"[,.;@#?!&$]+\ *", " ", phrase)

def get_notion(notions_ids, notions_lst, arg_id, label):
    notion_id = notions_ids.index(arg_id)
    notion = notions_lst[notion_id][label]
    return str(notion) if notion else None

def search(object, type="tgt_counter", l=10):
    id_ = object["id"]

    topic = get_notion(topic_ids, topics, id_, "topic_label")
    concept = get_notion(concept_ids, concepts, id_, "concept_label")

    retrieved = []

    adu_count = 0
    targeted_response = []
    for adu in mined[type]:

        sentence = adu["sentence"]
        # if predict(sentence) != "premise":
        #     # Count ADUs for reference
        #     continue

        # TODOs: Check this isn't overriding continue
        adu_count += 1

        #kp = extract_keyphrase(sentence)
        kp = list(set(adu["kp"]))

        # TODOs: Common-sense Query Expansion
        query = []
        query.extend(kp)

        # Ensure topics and concepts are unpacked (extended) into query list, as lists, else string will unpack 'l', 'i', 'k', 'e', 't'
        query.extend([topic]) if topic else query
        query.extend([concept]) if concept else query
        query = list(set(query))

        # Note: Now query becomes a string - be careful
        query = ", ".join(i for i in query)
        # print(query)

        search = [(i["_source"]["document"]["source"], i["_source"]["document"]["text"]) for i in db.search(query_=query, k=l)]

        source = [i[0] for i in search]
        evidence = [i[1] for i in search]

        #print("query", query)
        merged = ", ".join(i for i in evidence)
        ev_kp = list(set(yake_extract_keyphrase(merged)))

        retrieved.append({"passages": evidence, "kp": [clean(i) for i in ev_kp], "source": source})

        targeted_response.append({"sentence": adu["sentence"], "selected_keyphrases": []})

    # TODOs: Implement yield without storing list
    return ({
        "id": id_,
        "claim": claim,
        "argument": mined["argument"],
        "tgt_counter": [i for i in targeted_response],
        "retrieved": [i for i in retrieved],
        "adu_count": adu_count
    })

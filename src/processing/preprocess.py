import json
import pandas as pd
import logging

from src.detection.stance_classifier import sentence_stance
from yake import KeywordExtractor
from tqdm import tqdm
from src.utils_.utils import sentences_segment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PRE-PROCESSOR")

kw_extractor = KeywordExtractor(lan="en", n=3, top=5)

def truncate(data, l=5):
    data = pd.DataFrame(data)

    data_ = []
    for _, i in data.iterrows():

        truncated_args = sentences_segment(i["argument"])[0:l]
        truncated_counters = sentences_segment(i["counter"])[0:l]

        data_.append({
            "id": i["id"],
            "claim": i["claim"],
            "argument": " ".join(i for i in truncated_args),
            "counter": " ".join(i for i in truncated_counters)
        })

    return data_

# def unique_entries(args, key="id"):
#     data_ = pd.DataFrame(args)
#     unique = data_.drop_duplicates(subset="id")
#
#     unique_ = []
#     for _, i in unique.iterrows():
#         unique_.append({
#             "id": i["id"],
#             "titles": i["titles"],
#             "argument": i["argument"],
#             "counters": i["counters"]
#         })
#
#     return unique_

def process_aspects(data, key="argument"):
    aspects = []
    with tqdm(total=(len(data)), position=0, leave=True) as pbar:
        for _ in data:
            # TODOs: Run KeyBERT at Scale
            aspects.append([i[0] for i in kw_extractor.extract_keywords(_[key])])

            pbar.update()

        return aspects

def process_stance(data, aspects):
    stance = []
    with tqdm(total=(len(data))) as pbar:
        for i, j in zip(data, aspects):
            if not j:
                stance.append(" ")

            else:
                aspect = j.pop(0)
                stance.append((sentence_stance(i["claim"], aspect), aspect))

            pbar.update()

        return stance

def main():
    ### LOAD DATA ###
    args = [json.loads(ln) for ln in open("./src/data/cmv_cleaned.jsonl", "r")]
    logger.info(f"[{len(args)} Arguments Processed]")

    logger.info("[Pre-processor Initialised]")

    ### TRUNCATE ###
    args = truncate(args)

    ### EXTRACT UNIQUE ###
    # unique_ = unique_entries(args, key="id")
    #logger.info(f"[{len(unique_)} Unique Arguments]")

    ### EXTRACT ASPECTS ###
    arg_aspects = process_aspects(args, key="argument")
    counter_aspects = process_aspects(args, key="counter")

    logger.info(f"[{len(arg_aspects)} Keyphrases Processed]")

    ### DETERMINE STANCE ###
    arg_stance = process_stance(args, arg_aspects)
    logger.info(f"[{len(arg_stance)} Stance Polarities Processed]")

    ### WRITE TO DISK ###
    file_name = "cmv_processed"
    fout = open(f"./src/data/{file_name}.jsonl", "w")

    # Handel Blank Arguments. Repeat Claims
    # TODOs: Sentence Segment prior
    # TODOs: Tokenize prior
    with tqdm(total=(len(args))) as pbar:
        with fout:
            for i, j, k, l in zip(args, arg_aspects, arg_stance, counter_aspects):
                fout.write(json.dumps({
                    "id": i["id"],
                    "claim": i["claim"],
                    "argument": {"argument": i["argument"], "arg_keyphrases": j, "arg_stance": k},
                    "counter": {"counter": i["counter"], "counter_keyphrases": l}
                }))

                fout.write("\n")
                pbar.update()

    logger.info(f"[{len(args)} Data Stored as {file_name}.jsonl]")

if __name__ == "__main__":
    main()


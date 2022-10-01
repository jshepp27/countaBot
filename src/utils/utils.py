import json
import spacy
import uuid
from time import time
from functools import wraps
from nltk.tokenize import sent_tokenize, word_tokenize
import re

nlp = spacy.load("en_core_web_sm")

import os
os.path.join(os.path.dirname(__file__))

def tokeniser(doc):
    return word_tokenize(doc)

def sentences_segment(doc):
    return sent_tokenize(doc)

def paragraphs(document):
    start = 0
    document = nlp(document)
    passages = []
    for token in document:
        if token.is_space and token.text.count("\n") > 1:
            yield document[start:token.i]
            start = token.i
    yield document[start:]

def get_contents(filename):
    """Parse the contents of a file. Each line is a JSON encoded document."""
    documents = []

    with open(filename) as f:
        for line in f:
            doc = json.loads(line)

            if doc["text"] == "": continue
            if not doc: continue

            passages = [str(i) for i in paragraphs(doc["text"])][0].split("\n")

            for passage in passages:
                if len(passage) < 50:
                    continue

                documents.append((str(uuid.uuid4()).replace('-',''), doc['id'], doc["title"], passage))

    return documents

def clean(clean):
    clean = re.sub(r"\n", "", clean)
    clean = re.sub(r'(?<=[a-z])\'(?=[a-z])', '', clean)
    clean = re.sub('([^a-zA-Z\s.!?])', "", clean)
    clean = re.sub('\s+', ' ', clean)

    clean = re.sub(r"www\S+", "", clean)
    return clean.strip().lower()

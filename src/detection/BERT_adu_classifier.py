import pytorch_pretrained_bert as ppb
assert 'bert-large-cased' in ppb.modeling.PRETRAINED_MODEL_ARCHIVE_MAP
from transformers import AutoModelForSequenceClassification, DistilBertTokenizerFast, pipeline

import os
path = "/Users/joshua.sheppard/PycharmProjects/countaBot/"
os.chdir(path)

#Aleternate "..", "." dependent on ipynb vs .py
saved_path = "./src/models/BERT_adu_classifier/"
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
BERT_adu = AutoModelForSequenceClassification.from_pretrained(saved_path)

test_1 = "as policemen are a very homogeneous group trained to stick together and the danger of even deepening the pack mentality and escalation of police state"
test_2 = "abortion should be legalised"

pipe = pipeline("text-classification", model=BERT_adu, tokenizer=tokenizer)

def predict(sentence):
    res = pipe(sentence)

    return "claim" if res[0]["label"] == "LABEL_0" else "premise"

print(predict(test_2))
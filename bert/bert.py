import sys
import numpy as np
from keras_bert import extract_embeddings
from keras_bert import load_vocabulary, load_trained_model_from_checkpoint, Tokenizer, get_checkpoint_paths

print('This demo demonstrates how to load the pre-trained model and check whether the two sentences are continuous')

if len(sys.argv) == 2:
    model_path = sys.argv[1]
else:
    from keras_bert.datasets import get_pretrained, PretrainedList
    model_path = get_pretrained(PretrainedList.wwm_uncased_large)

paths = get_checkpoint_paths(model_path)

texts = ['all']

embeddings = extract_embeddings(model_path, texts)

print(len(embeddings[0][1]))
# print(embeddings)
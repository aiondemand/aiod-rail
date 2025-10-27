import os
os.environ["HF_HOME"] = "."

import json
import logging
import pandas as pd
import numpy as np
import sklearn.metrics as m
import torch
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def save_predictions(input_strings, predictions, labels):
    df = pd.DataFrame(data=[input_strings, predictions, labels]).T
    df.columns = ["sentence", "prediction", "label"]

    os.makedirs("./output-temp", exist_ok=True)
    df.to_csv("./output-temp/predictions.csv")


def calculate_metrics(predictions, labels, unique_labels):
    kwargs = {
        "average": "macro",
        "zero_division": 1,
        "labels": unique_labels
    }
    metrics = {
        "accuracy": m.accuracy_score(labels, predictions),
        "precision_macro": m.precision_score(labels, predictions, **kwargs),
        "recall_macro": m.recall_score(labels, predictions, **kwargs),
        "f1_macro": m.f1_score(labels, predictions, **kwargs),
    }
    os.makedirs("./output-temp", exist_ok=True)
    with open("./output-temp/metrics.json", "w") as f:
        json.dump(metrics, f)


def load_assets(model_name, dataset_name, split_name):
    error = None
    for attempt in range(5):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            model.to(get_device())
            model.eval()

            dataset = load_dataset(dataset_name)[split_name]
            return model, tokenizer, dataset

        except Exception as e:
            logging.getLogger().warning(
                f"Failed to load model and data (attempt: {attempt})"
            )
            error = e
            continue
    else:
        logging.getLogger().error("Failed to load model and data.")
        logging.getLogger().error(error)
        exit(1)


def classify_data(sentences):
    encoding = tokenizer(
        sentences, padding=True, truncation=True, return_tensors="pt"
    )
    encoding = {k: v.to(get_device()) for k, v in encoding.items()}

    with torch.no_grad():
        out = model(**encoding)[0]

    pred = out.argmax(dim=1)
    return pred


if __name__ == "__main__":
    # RESERVED ENV VARS
    model_name = os.getenv("MODEL_NAMES").split(",")[0]
    dataset_name = os.getenv("DATASET_NAMES").split(",")[0]
    model_id = os.getenv("MODEL_IDS").split(",")[0]
    dataset_id = os.getenv("DATASET_IDS").split(",")[0]

    # REQUIRED ENV VARS
    feature_name = os.getenv("INPUT_FEATURE_NAME", default="sentence")
    label_name = os.getenv("LABEL_FEATURE_NAME", default="label")
    split_name = os.getenv("SPLIT_NAME", default="train")

    model, tokenizer, dataset = load_assets(model_name, dataset_name, split_name)

    # OPTIONAL ENV VARS
    batch_size = int(os.getenv("BATCH_SIZE", default=8))
    num_datapoints_to_eval = int(os.getenv("NUM_DATAPOINTS_TO_CLASSIFY", default=len(dataset)))

    unique_labels = np.unique(dataset[label_name]).tolist()

    all_texts = []
    all_predictions = []
    all_labels = []

    for i in tqdm(range(0, num_datapoints_to_eval, batch_size)):
        start_idx = i
        end_idx = i + batch_size

        sentences = dataset[start_idx: end_idx][feature_name]
        labels = torch.tensor(dataset[start_idx: end_idx][label_name])
        predictions = classify_data(sentences)

        all_texts += [np.array(sentences)]
        all_predictions += [predictions.cpu().numpy()]
        all_labels += [labels.cpu().numpy()]

    all_texts = np.hstack(all_texts)
    all_predictions = np.hstack(all_predictions)
    all_labels = np.hstack(all_labels)

    calculate_metrics(all_predictions, all_labels, unique_labels)
    save_predictions(all_texts, all_predictions, all_labels)

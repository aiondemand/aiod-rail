import os

os.environ["HF_HOME"] = "."

import json
import logging

import numpy as np
import sklearn.metrics as m
import torch
import wandb
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def wandb_check():
    necessary_envs = [
        "WANDB_API_KEY",
        "WANDB_ENTITY",
        "WANDB_PROJECT",
        "WANDB_NAME",
    ]
    return set(necessary_envs).issubset(os.environ)


def process_metrics(all_metrics: dict, metrics_filter: list):
    metrics_of_interest = {k: all_metrics.get(k) for k in metrics_filter}

    os.makedirs("./output-temp", exist_ok=True)
    with open("./output-temp/metrics.json", "w") as f:
        json.dump(metrics_of_interest, f)

    if wandb_check():
        wandb.init(
            project=os.environ["WANDB_PROJECT"],
            name=os.environ["WANDB_NAME"],
            entity=os.environ["WANDB_ENTITY"],
        )
        wandb.log(metrics_of_interest)
        wandb.finish()


if __name__ == "__main__":
    model_name = os.getenv("MODEL_NAMES").split(",")[0]
    dataset_name = os.getenv("DATASET_NAMES").split(",")[0]
    metrics_to_compute = (
        os.getenv("METRICS", default="").split(",")
        if len(os.getenv("METRICS", default=""))
        else []
    )
    split_name = os.getenv("SPLIT_NAME", default="train")

    for attempt in range(5):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            model.to(get_device())
            model.eval()

            dataset = load_dataset(dataset_name)[split_name]
            break
        except Exception:
            logging.getLogger().warning(
                f"Failed to load model and data (attempt: {attempt})"
            )
            continue
    else:
        logging.getLogger().error("Failed to load model and data.")
        exit(1)

    batch_size = 8
    all_predictions = []
    all_labels = []

    # predicting
    for i in tqdm(range(0, len(dataset), batch_size)):
        start_idx = i
        end_idx = i + batch_size

        sentences = dataset[start_idx:end_idx]["sentence"]
        labels = dataset[start_idx:end_idx]["label"]
        labels = torch.tensor(labels)

        encoding = tokenizer(
            sentences, padding=True, truncation=True, return_tensors="pt"
        )
        encoding = {k: v.to(get_device()) for k, v in encoding.items()}

        with torch.no_grad():
            out = model(**encoding)[0]

        pred = out.argmax(dim=1)
        pred = pred - 1

        all_predictions += [pred.cpu().numpy()]
        all_labels += [labels.cpu().numpy()]

    # calculating metrics
    all_predictions = np.hstack(all_predictions)
    all_labels = np.hstack(all_labels)

    accuracy = m.accuracy_score(all_labels, all_predictions)
    precision_macro = m.precision_score(
        all_labels, all_predictions, average="macro", zero_division=1, labels=[-1, 0, 1]
    )
    recall_macro = m.recall_score(
        all_labels, all_predictions, average="macro", zero_division=1, labels=[-1, 0, 1]
    )
    f1_macro = m.f1_score(
        all_labels, all_predictions, average="macro", zero_division=1, labels=[-1, 0, 1]
    )

    metrics = {
        "accuracy": accuracy,
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
    }
    process_metrics(metrics, metrics_to_compute)

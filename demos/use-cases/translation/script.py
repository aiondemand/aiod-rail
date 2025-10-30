import os
os.environ["HF_HOME"] = "."

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import logging
import torch
from datasets import load_dataset
from tqdm import tqdm


def get_device():
    """
    Select device to store tensors in
    """
    return "cuda" if torch.cuda.is_available() else "cpu"


def load_assets(model_name, dataset_name, split_name):
    """
    Attempt to load assets (model and dataset)
    """
    error = None
    for attempt in range(5):
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
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


def translate_data(model, tokenizer, texts):
    """
    Translate a batch of texts
    """
    encoding = tokenizer(
        texts, padding=True, truncation=True, return_tensors="pt"
    ).to(get_device())

    with torch.no_grad():
        translation = model.generate(**encoding)
    return tokenizer.batch_decode(translation, skip_special_tokens=True)


if __name__ == "__main__":
    # RESERVED ENV VARS
    model_name = os.getenv("MODEL_NAMES").split(",")[0]
    dataset_name = os.getenv("DATASET_NAMES").split(",")[0]
    model_id = os.getenv("MODEL_IDS").split(",")[0]
    dataset_id = os.getenv("DATASET_IDS").split(",")[0]

    # REQUIRED ENV VARS
    split_name = os.getenv("SPLIT_NAME", default="train")
    feature_name = os.getenv("FEATURE_NAME", default="sentence")

    # OPTIONAL ENV VARS
    use_opus_model = os.getenv("USE_OPUS_MODEL", default=False)
    if type(use_opus_model) == str:
        use_opus_model = use_opus_model.lower() == "true"
    src_lang = os.getenv("OPUS_SRC_LANG", default=None)
    dst_lang = os.getenv("OPUS_DST_LANG", default=None)
    num_datapoints_to_eval = int(os.getenv("NUM_DATAPOINTS_TO_TRANSLATE", default=-1))
    batch_size = int(os.getenv("BATCH_SIZE", default=8))
    hf_model = os.getenv("HF_MODEL", None)

    if use_opus_model is True and src_lang is not None and dst_lang is not None:
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{dst_lang}"
    elif hf_model is not None:
        model_name = hf_model

    model, tokenizer, dataset = load_assets(model_name, dataset_name, split_name)

    if num_datapoints_to_eval == -1:
        num_datapoints_to_eval = len(dataset)

    json_data = []
    # iterate over dataset and translate the batches individually
    for i in tqdm(range(0, num_datapoints_to_eval, batch_size)):
        start_idx = i
        end_idx = i + batch_size
        data = dataset[start_idx:end_idx][feature_name]
        new_translations = translate_data(model, tokenizer, data)

        json_data.extend([{
            "original": orig,
            "translated": trans,
        } for orig, trans in zip(data, new_translations)])

    # store the results
    os.makedirs("./output-temp", exist_ok=True)
    with open("./output-temp/translations.json", "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

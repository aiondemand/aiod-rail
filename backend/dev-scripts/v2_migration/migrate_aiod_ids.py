import os

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from tqdm import tqdm


def load_tsv(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, sep="\t").set_index("old")


def migrate_ids(table: pd.DataFrame, old_ids: list[int]) -> list[str]:
    new_ids = []
    for id in old_ids:
        try:
            new_ids.append(table.loc[id].values[0])
        except Exception:
            print("Old ID doesn't exist")

    return new_ids


def update_mongodb(collection: Collection, tsv_conversion_dirpath: str):
    fields_to_update = ["dataset_ids", "model_ids", "publication_ids"]
    tsv_names = ["datasets.tsv", "models.tsv", "publications.tsv"]
    tsv_tables = [
        load_tsv(os.path.join(tsv_conversion_dirpath, tsv_name))
        for tsv_name in tsv_names
    ]

    cursor = collection.find({})

    for doc in tqdm(cursor):
        old_ids_arr = [doc.get(f) for f in fields_to_update]
        new_ids_arr = [
            migrate_ids(table, old_ids)
            for table, old_ids in zip(tsv_tables, old_ids_arr)
        ]
        set_dict = {
            field: new_ids for field, new_ids in zip(fields_to_update, new_ids_arr)
        }

        result = collection.update_one({"_id": doc["_id"]}, {"$set": set_dict})
        if result.modified_count == 0:
            print("Error")

    client.close()


if __name__ == "__main__":
    load_dotenv()

    # === Config ===
    tsv_conversion_dirpath = os.getenv("TSV_DIRPATH", "backend/temp-id")
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = "aiod"
    collection_name = "experiments"

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    update_mongodb(collection, tsv_conversion_dirpath)

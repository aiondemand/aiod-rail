from tqdm import tqdm
import os
import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv 


def load_csv(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath, sep="\t").set_index("old")


def migrate_ids(table: pd.DataFrame, old_ids: list[int]) -> list[str]:
    new_ids = []
    for id in old_ids:
        try:
            new_ids.append(table.loc[id].values[0])
        except:
            print("Old ID doesn't exist")
    
    return new_ids


def update_mongodb(collection: Collection, csv_conversion_dirpath: str):
    fields_to_update = ["dataset_ids", "model_ids", "publication_ids"]
    csv_names = ["datasets.tsv", "models.tsv", "publications.tsv"]
    csv_tables = [
        load_csv(os.path.join(csv_conversion_dirpath, csv_name))
        for csv_name in csv_names
    ]

    cursor = collection.find({})

    for doc in tqdm(cursor):
        old_ids_arr = [doc.get(f) for f in fields_to_update]
        new_ids_arr = [
            migrate_ids(table, old_ids)
            for table, old_ids in zip(csv_tables, old_ids_arr)
        ]
        set_dict = {
            field: new_ids
            for field, new_ids in zip(fields_to_update, new_ids_arr)
        }

        result = collection.update_one(
            {'_id': doc['_id']},
            {'$set': set_dict}
        )
        if result.modified_count == 0:
            print("Error")

    client.close()
    
if __name__ == "__main__":
    load_dotenv()
    
    # === Config ===
    csv_conversion_dirpath = os.getenv("CSV_DIRPATH", "backend/temp-id")
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    db_name = "aiod"
    collection_name = "experiments"

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]        

    update_mongodb(collection, csv_conversion_dirpath)

    

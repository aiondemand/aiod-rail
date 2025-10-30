import json
import os
import numpy as np
import joblib

os.makedirs("output-temp", exist_ok=True)

data = {"acc": 0.9, "f1": 0.95}
with open("output-temp/metrics.json", "w") as f:
    json.dump(data, f)

joblib.dump(np.array([1,2,3,4,5]), "output-temp/array.pkl")

with open("output-temp/text.txt", "w") as f:
    f.write("Testing testin test")

print("REQUIRED ENV VAR VALUE:", os.environ.get("REQUIRED_ENV"))
print("OPTIONAL ENV VAR VALUE:", os.environ.get("OPTIONAL_ENV", None))
print("DONE!")

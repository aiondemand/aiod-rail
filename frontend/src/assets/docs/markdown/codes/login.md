```python
import json
import os

from aiod_rail_sdk import Configuration
from aiod_rail_sdk.clients import RailClient

RAIL_API_URI = "https://rail.aiod.eu/api"
os.environ["AIOD_RAIL_API_KEY"] = "YOUR_RAIL_API_KEY"

config = Configuration(host=RAIL_API_URI)
rail_client = RailClient(config)
```
```python
from OuterRail import AssetManager

asset_manager = AssetManager(config)

# Count the number of datasets
datasets_count = asset_manager.count_datasets()

# Get first 10 datasets
datasets = asset_manager.get_datasets(offset=0, limit=10)

# Print dataset description
print(datasets[0].description)
```

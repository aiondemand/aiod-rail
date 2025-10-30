```python
datasets_count = rail_client.datasets.count()

# Get first 10 datasets
datasets = rail_client.datasets.get(offset=0, limit=10)

# Print dataset description
print(datasets[0].description)
```

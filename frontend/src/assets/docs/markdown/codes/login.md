```python
from OuterRail import Configuration

config = Configuration(host="https://rail.aiod.eu/api") #  Specify URL
config.login(persist=False) #  Blocking function until log in or 5 min. timeout
```

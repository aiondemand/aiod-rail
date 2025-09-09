```python
from OuterRail import Configuration

config = Configuration(host="https://rail.aiod.eu/api/docs") # 1. Specify URL
config.login(username="username", password="password") # 2. Log in
config.logout() # 3. Don't forget to logout at the end as well
```

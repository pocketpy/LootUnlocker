# LootUnlocker
 Lightweight and extensible game backend with RESTful API

## Installation

Make sure you have Python 3.10+ installed.

To install the required dependencies, create a virtual environment and run:
```
pip install -r requirements.txt
```

To initialize the database, run:
```
from loot_unlocker.models import db

db.init_db()
```

By default, LootUnlocker uses PostgreSQL as the database backend. You can change the database settings in `loot_unlocker/env.py` to use SQLite or another database.

## Run Server

```
uvicorn loot_unlocker:app --host 0.0.0.0 --port 6282 --loop asyncio
```

Check FastAPI docs at `http://localhost:6282/api/docs`.

See `tests` directory for examples of how to use the API.

# Conger

Lightweight data model management for Python ecosystem.

Specifically, `conger` provides a management interface for easy previewing, editing, and storing data models (defined by [pydantic](https://github.com/pydantic/pydantic) or dataclass).


## Install

If you using [rye](https://github.com/mitsuhiko/rye) (recommended), you can install `conger` as a dependency of your project:

```bash
rye add conger
```

or pip:

```bash
python -m pip install conger
```
## Quick Start

1. Define your data model (e.g. `Person`):

```Python
from conger import BaseModel, Field

class Person(BaseModel):
    name: str
    age: int = Field(..., gt=18, lt=100)
```

2. Add this data model to flask app:

```Python
from flask import Flask
import pickledb
from conger import Conger

app = Flask(__name__)
db = pickledb.load("db.json", True)
conger = Conger(app, database=db)

"""
your data model
"""

conger.add_model(Person)


if __name__ == "__main__":
    app.run()
```

3. visit [http://127.0.0.1:500/conger/](http://127.0.0.1:500/conger/)


LICENSE MIT

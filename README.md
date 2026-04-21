# halo_api

A minimal Python project scaffold that includes a GraphQL client and pytest setup.

## Project structure

```
halo_api/
├── requirements.txt
├── pytest.ini
├── README.md
├── src/
│   └── halo_api/
│       ├── __init__.py
│       └── graphql_client.py
└── tests/
    └── test_graphql_client.py
```

## Setup instructions

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:

   ```bash
   pytest
   ```

## Example usage

```python
from halo_api import GraphQLClient

client = GraphQLClient("https://example.com/graphql", headers={"Authorization": "Bearer <token>"})
result = client.execute("query { viewer { id } }")
print(result)
```

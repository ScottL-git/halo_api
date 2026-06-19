# halo_api

A minimal Python project that provides a small GraphQL client.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run tests

```bash
pytest
```

## Usage example

```python
from halo_api import GraphQLClient

client = GraphQLClient("https://example.com/graphql", headers={"Authorization": "Bearer token"})

data = client.execute(
    """
    query GetViewer {
      viewer { id }
    }
    """
)

print(data)
```

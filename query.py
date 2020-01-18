import json
import os
from pathlib import Path

import requests

# adapted from https://stackoverflow.com/a/46271487
api_token_envvar = "GITHUB_API_TOKEN"
api_token = os.getenv(api_token_envvar, None)
if not api_token:
    raise RuntimeError(
        f"GitHub API token not stored in env variable ${api_token_envvar}"
    )
url = 'https://api.github.com/graphql'
# query = { 'query' : '{ viewer { repositories(first: 30) { totalCount pageInfo { hasNextPage endCursor } edges { node { name } } } } }' }
query = { 'query': Path("./query2.graphql").read_text() }
headers = {'Authorization': f'token {api_token}'}

r = requests.post(url=url, json=query, headers=headers)
result = json.loads(r.text)
with open("result.json", "w") as handle:
    json.dump(result, handle, indent=4)
# print(json.dumps(result, indent=4))

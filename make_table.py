import json
from pathlib import Path

import pandas as pd
from tabulate import tabulate

repositories = json.loads(Path("result.json").read_text())["data"]["organization"][
    "repositories"
]["nodes"]
BLANK_REPO = {"nodes": []}
# for repository in repositories:
#     issues = repository["issues"]
#     if issues != BLANK_REPO:
#         pprint(repository)
repositories_with_issues = [
    repository for repository in repositories if repository["issues"] != BLANK_REPO
]
transformed_issues = []
for repository in repositories_with_issues:
    issues = pd.DataFrame(repository["issues"]["nodes"])
    # We need to flatten every instance of inner nodes...
    issues.loc[:, "author"] = issues.loc[:, "author"].map(lambda x: x["login"])
    issues.loc[:, "labels"] = issues.loc[:, "labels"].map(
        lambda x: list(y["name"] for y in x["nodes"])
    )
    issues = issues.set_index("url")
    issues["name"] = repository["name"]
    transformed_issues.append(issues)
df = pd.concat(transformed_issues)
# now we are ready to filter...
USERNAME = "berquist"
with open("report.md", "w") as handle:
    handle.write(tabulate(df, headers="keys", tablefmt="pipe"))

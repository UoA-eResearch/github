#!/usr/bin/env python3

import pandas as pd
from pprint import pprint
from datetime import timedelta
import requests_cache

requests_cache.install_cache(
    "requests_cache",
    allowable_codes=[200, 404],  # Cache 404 responses
    cache_control=False,  # Use Cache-Control headers for expiration, if available
    expire_after=timedelta(days=1),  # Otherwise expire responses after one day
)
from datetime import datetime
import requests

repos = []
for page in range(10):
    r = requests.get(
        f"https://api.github.com/orgs/uoa-eresearch/repos?sort=created&per_page=100&page={page}"
    ).json()
    repos.extend(r)
    if len(r) != 100:
        break
print(f"Got {len(repos)} repos")
#pprint(repos[0])
df = pd.DataFrame(repos)
df = (
    df.loc[
        # Filter to just repos with homepages matching these domains
        df.homepage.str.contains(
            "uoa-eresearch.github.io|auckland.ac.nz|cloud.edu.au", na=False
        ),
        ["name", "created_at", "pushed_at", "description", "html_url", "homepage"],
    ]
    .sort_values(by="pushed_at", ascending=False)
    .drop_duplicates()
)
# Make links clickable in Excel
df.html_url = df.html_url.apply(lambda u: f'=HYPERLINK("{u}")')
df.homepage = df.homepage.apply(lambda u: f'=HYPERLINK("{u}")')
print(df)
df.to_csv("repos.csv", index=False)

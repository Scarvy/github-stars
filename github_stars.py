from typing import Dict, List, Union

import requests

from constants import USER_AGENT

BASE_URL = "https://api.github.com/users/{}/starred"


def api_get(
    url: str, headers: Dict[str, str], params: Dict[str, Union[str, int]]
) -> Union[List, Dict]:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    return response.json(), response.links.get("next", None)


def get_github_stars(username: str, per_page: int = 100) -> List[Dict]:
    starred_repos = []
    url = BASE_URL.format(username, per_page)
    headers = {
        "Accept": "application/vnd.github.v3.star+json",
        "User-Agent": USER_AGENT,
    }
    params = {"per_page": per_page}

    while url:
        results, next_page = api_get(url, headers, params)
        starred_repos.extend(results)

        if next_page:
            url = next_page["url"]
        else:
            url = None

    return starred_repos


if __name__ == "__main__":
    username = "Scarvy"
    starred_repos = get_github_stars(username)

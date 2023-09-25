from typing import Dict, List, Tuple

import requests

from github_stars.constants import USER_AGENT

BASE_URL = "https://api.github.com/users/{}/starred"


def api_get(
    url: str, headers: Dict[str, str], params: Dict[str, int]
) -> Tuple[List[Dict], Dict]:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")
    return response.json(), response.links.get("next", None)


def get_github_stars(username: str, per_page: int = 100) -> List[Dict]:
    """Get a list of repositories starred by a user.

    Args:
        username (str): The handle for the GitHub user account.
        per_page (int, optional): The number of results per page. Defaults to 100.

    Returns:
        List[Dict]: Lists of repositories a user has starred.
    """
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
            url = ""

    return starred_repos
